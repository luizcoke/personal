"""Extração auditável do layout conferido em outubro/2026; não é parser universal.

Executar com pdfplumber disponível. Respostas posteriores ficam em
dados/revisao_usuario.json, por ID, e prevalecem sobre a classificação inicial.
"""
from pathlib import Path
from decimal import Decimal as D
import json
import re
import sys
import unicodedata

import pdfplumber

PERIOD = Path(__file__).resolve().parents[1]
ROOT = PERIOD.parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import mensal


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def norm(text):
    return re.sub(r'[^A-Z0-9*]', '', unicodedata.normalize('NFKD', text.upper()))


def money(text):
    return text.replace(' ', '').replace('.', '').replace(',', '.')


def extract(source, pages):
    records, future, checks = [], [], []
    card, kind, section = None, 'nacional', 'atual'
    path = PERIOD / source['arquivo']
    password = None
    from pypdf import PdfReader
    if PdfReader(path).is_encrypted:
        password = str(read(ROOT / 'config.local.json')['pdf_password'])
    with pdfplumber.open(path, password=password) as pdf:
        for number in pages:
            page = pdf.pages[number - 1]
            # Coordenadas verificadas visualmente nas páginas renderizadas.
            for side, x0, x1 in [('esquerda', 145, 345), ('direita', 360, 560)]:
                lines = page.crop((x0, 0, x1, page.height)).extract_text(x_tolerance=1).splitlines()
                for index, line in enumerate(lines):
                    if line.startswith('Compras parceladas - próximas faturas'):
                        section = 'futuro'
                    if line.startswith('Limites de crédito'):
                        section = 'fora'
                    if line.startswith('Lançamentos internacionais'):
                        kind = 'internacional'
                    header = re.fullmatch(r'(LUIZ COKE NETO|PALOMA PAIXAO COKE) \(final (\d{4})\)', line)
                    if header:
                        card = header[2]
                    subtotal = re.fullmatch(r'Lançamentos no cartão \(final (\d{4})\) ([\d.,]+)', line)
                    if subtotal:
                        checks.append({'cartao': subtotal[1], 'tipo': 'nacional', 'valor': money(subtotal[2])})
                    subtotal = re.fullmatch(r'Total lançamentos inter\. em R\$ ([\d.,]+)', line)
                    if subtotal:
                        checks.append({'cartao': card, 'tipo': 'internacional', 'valor': money(subtotal[1])})
                    iof = re.fullmatch(r'Repasse de IOF em R\$ ([\d.,]+)', line)
                    if iof and section == 'atual':
                        records.append({'data': '', 'descricao': 'Repasse de IOF internacional', 'parcela': '',
                                        'valor_original': money(iof[1]), 'pagina': number, 'coluna': side,
                                        'linha_extraida': index + 1, 'cartao': card, 'tipo': 'iof', 'texto_fonte': line})
                    match = re.fullmatch(r'(\d{2}/\d{2}) (.+?)\s+(-?\s*[\d.]+,\d{2})', line)
                    if not match or section == 'fora':
                        continue
                    description = match[2].strip()
                    installment = re.search(r'(\d{2}/\d{2})$', description)
                    parcel = installment[1] if installment else ''
                    if installment:
                        description = description[:installment.start()].strip()
                    row = {'data': match[1], 'descricao': description, 'parcela': parcel,
                           'valor_original': money(match[3]), 'pagina': number, 'coluna': side,
                           'linha_extraida': index + 1, 'texto_fonte': line}
                    if section == 'futuro':
                        future.append(row)
                    else:
                        assert card, line
                        row.update(cartao=card, tipo=kind)
                        records.append(row)
    for index, row in enumerate(records, 1):
        row.update(id=f'{source["id"]}-{index:03}', fonte_id=source['id'])
    source['subtotais'] = checks
    assert sum((D(r['valor_original']) for r in records), D(0)) == D(source['total_integral'])
    return records, future


def classify(row):
    name = norm(row['descricao'])
    amount = D(row['valor_original'])
    row.update(valor_pessoal_exato=str(amount), status='regra_kb', observacao='')
    if row['cartao'] in mensal.read(ROOT / 'modelos/planilha.json').get('cartoes_paloma', ['3878']):
        row.update(linha='56', valor_pessoal_exato=str(amount / 2),
                   observacao='Única metade de todo gasto em cartão de Paloma, inclusive AABB; regra confirmada em 09/10/2026. Compras e estornos preservados, sem novo rateio.')
        return
    if row['tipo'] == 'iof':
        row.update(linha='45', observacao='IOF efetivo agregado deste cartão, contado uma vez. PDF não informa data individual.')
        return
    if name.startswith('JIMCOM*MAGALIDA'):
        row.update(linha='31', observacao='Gestão Bruna/Magali: continuação 02/04 e crédito da mesma compra; parte integral de Luiz conforme confirmação anterior. Fora do acerto de Paloma.')
        return
    if name == 'DESCANTECIPAPARCELAS':
        row.update(linha='66', status='provisoria', observacao='Crédito de antecipação preservado. Possível vínculo às parcelas Itaú Shop 14/15 e 15/15; confirmar antes de transferir para Compras / Presentes.')
        return
    rules = [
        ('51', ['ITAUSHOP', 'AMAZONMKTPLC*UPTEC']),
        ('27', ['MP*ASSTECNICAELE', 'SAMSUNGNOITAU']),
        ('54', ['IFD*', '99FOOD*', 'PANIFICADORA', 'PRACAPANAMERICANA', '30220687ADRIANA', 'DRTLANCHONETE']),
        ('37', ['AUTOPOSTOALBION']),
        ('41', ['RAIA', 'CAASPLAPA']),
        ('39', ['PAODEACUCAR']),
        ('62', ['APPLECOM/BILL'.replace('/', '')]),
        ('63', ['NETFLIX']),
        ('61', ['EBN*SPOTIFY']),
        ('64', ['ZOOSPECOMMERCEPARQ', 'ECOPARQUEECOMMERCE']),
        ('58', ['GITHUBINC']),
        ('novo-openai', ['OPENAI*CHATGPTSUBSCR']),
    ]
    if name.startswith('ASSOCIACAOATLETIC') and amount <= 250:
        row.update(linha='55', observacao='Regra vigente de refeições AABB até R$ 250. Parcela atual literal quando presente; sem inferir mensalidade.')
        return
    for line, patterns in rules:
        if any(name.startswith(pattern) for pattern in patterns):
            row['linha'] = line
            if row['parcela']:
                row['observacao'] = 'Parcela efetivamente cobrada nesta fatura; não somar parcelas futuras.'
            if name.startswith('ITAUSHOP') and row['parcela'] in ['14/15', '15/15']:
                row['observacao'] = 'Parcela adicional efetivamente cobrada; há desconto de antecipação na fatura, com vínculo ainda a confirmar.'
            return
    row.update(linha='66', status='provisoria', observacao='Descritor sem regra confirmada para este ciclo; mantido em Outros até identificar a finalidade.')
    if name == 'ESTRADAITAPECERICA':
        row.update(status='nao_identificado', observacao='Descritor já não reconhecido pelo usuário na base; manter em Outros, sem inferir atividade.')
    if name == 'AMAZONDIGITALBR':
        row['observacao'] = 'Hipótese de filme no ciclo anterior tinha escopo somente naquele período; confirmar a finalidade atual.'


def main():
    manifest = read(PERIOD / 'periodo.json')
    sources, records, futures = [], [], {}
    for brand, total, due, pages in [('MASTERCARD', '8102.16', '2026-10-15', [2, 3, 4]), ('VISA', '653.42', '2026-10-01', [2])]:
        entry = next(f for f in manifest['arquivos'] if brand in f['arquivo'])
        source = dict(entry, id=brand, nome=brand.title(), tipo='cartao', total_integral=total, vencimento=due)
        current, future = extract(source, pages)
        sources.append(source)
        records.extend(current)
        futures[brand] = future
    mensal.write(PERIOD / 'auditoria/dados/lancamentos_extraidos.json', {'fontes': sources, 'lancamentos': records})
    mensal.write(PERIOD / 'auditoria/dados/parcelas_futuras.json', {'ciclo_previsto': '2026-11', 'incluido_no_resumo_atual': False, 'fontes': futures})
    for row in records:
        classify(row)
    overrides = PERIOD / 'auditoria/dados/revisao_usuario.json'
    if overrides.exists():
        for row in records:
            row.update(read(overrides).get('lancamentos', {}).get(row['id'], {}))
    ledger = {'versao': 1, 'mes_referencia': manifest['mes_referencia'], 'ciclo_faturas': manifest['ciclo_faturas'],
              'fontes': sources, 'lancamentos': records, 'observacoes': [
                  'Processamento parcial: somente Mastercard e Visa recebidos. Extrato Itaú de 01 a 30/09/2026 ausente; não há conciliação bancária nem total mensal completo.',
                  'Referência setembro/2026 pelo prefixo 2026-09 da pasta; ciclo outubro/2026 confirmado pelos cabeçalhos. O sufixo ref_ago da pasta não reabre agosto, que permanece fechado.',
                  'Faturas completas: compras de agosto e outubro e parcelas antigas entram conforme cobrança efetiva, sem filtro pela data da compra.',
                  'Todos os cartões de Paloma são divididos 50%, inclusive AABB, conforme confirmação de 09/10/2026. Cartões 3878 (R$ 4.200,57) e 6553 (R$ 50,00): metade conjunta exata R$ 2.125,285; linha 56 arredondada uma vez para R$ 2.125,29.',
                  'Magali 02/04 de R$ 129,46 e crédito de R$ 0,06: participação integral de Luiz, conforme decisão específica da mesma compra. Sem nova cobrança a Paloma.',
                  'Pagamentos das faturas anteriores, simulações, limites e compras futuras não compõem os lançamentos atuais.',
                  'Ausência do extrato impede conferir WALTER 02/02, provisão de Bruna, eSocial, contas e PIX/reembolsos. Nenhum valor anterior foi repetido como gasto deste mês.',
              ]}
    bank_path = PERIOD / 'auditoria/dados/extrato_normalizado.json'
    if bank_path.exists():
        bank_data = mensal.read(bank_path)
        ledger['fontes'].append(bank_data['fonte'])
        ledger['lancamentos'].extend(bank_data['lancamentos'])
        previous = mensal.read(PERIOD / 'auditoria/dados/lancamentos.json')
        ledger['observacoes'] = [n for n in ledger['observacoes'] if not n.startswith(('Processamento parcial:', 'Ausência do extrato'))]
        ledger['observacoes'] += [n for n in previous['observacoes'] if n.startswith(('Extrato de setembro:', 'Banco e cartões:', 'Condomínio, eSocial', 'AABB:'))]
    mensal.write(PERIOD / 'auditoria/dados/lancamentos.json', ledger)
    result = mensal.validate(PERIOD)
    print(f'{len(records)} lançamentos; total pessoal parcial R$ {mensal.br(result["total"])}')
    for source in sources:
        if source['tipo'] == 'cartao':
            print(source['id'], source['total_integral'], source['subtotais'])
    for row in records:
        if row['status'] in ['provisoria', 'nao_identificado']:
            print(row['id'], row['descricao'], row['valor_original'], row['linha'])


if __name__ == '__main__':
    main()
