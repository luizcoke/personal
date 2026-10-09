from pathlib import Path
from decimal import Decimal as D
import copy,json,sys,tempfile,unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import mensal
P=ROOT/'periodos/2026-08'

@unittest.skipUnless((P/'auditoria/dados/lancamentos.json').exists(),'Regressão requer dados locais de agosto/2026.')
class MonthlyValidation(unittest.TestCase):
    def setUp(self):self.data=mensal.read(P/'auditoria/dados/lancamentos.json')
    def row(self,ident):return next(r for r in self.data['lancamentos'] if r['id']==ident)
    def validate(self):
        # A cópia Git contém os dados; PDFs originais são restaurados separadamente.
        have_originals=all((P/source['arquivo']).is_file() for source in self.data['fontes'])
        return mensal.validate(P,ledger=self.data,check_files=have_originals)
    def test_real_month_preserves_every_sheet_row_and_original_total(self):
        result=self.validate();old=mensal.read(P/'auditoria/dados/consolidado_planilha.json')
        self.assertEqual(len(self.data['lancamentos']),178)
        self.assertEqual(result['total'],D('17608.97'))
        actual={r['linha']:(r['total'],r['valores']) for r in result['linhas']}
        expected={r['linha']:(r['total'],r['valores']) for r in old['linhas']}
        self.assertEqual(actual,expected)
    def test_duplicate_transaction_rejected(self):
        self.data['lancamentos'].append(copy.deepcopy(self.data['lancamentos'][0]))
        with self.assertRaisesRegex(mensal.ValidationError,'ID de lançamento duplicado'):self.validate()
    def test_bank_outside_month_rejected(self):
        self.row('EXT-056')['data']='2026-09-01'
        with self.assertRaisesRegex(mensal.ValidationError,'fora do mês'):self.validate()
    def test_second_split_of_personal_provision_rejected(self):
        self.row('EXT-056')['valor_pessoal_exato']='124.225'
        with self.assertRaisesRegex(mensal.ValidationError,'rateada novamente'):self.validate()
    def test_family_card_cannot_be_counted_as_another_category(self):
        row=next(r for r in self.data['lancamentos'] if r.get('cartao')=='3878')
        row['linha']='51'
        with self.assertRaisesRegex(mensal.ValidationError,'uma única metade'):self.validate()
    def test_second_paloma_card_preserves_single_half(self):
        # A titularidade, e não a categoria/estabelecimento, determina a metade.
        for row in self.data['lancamentos']:
            if row.get('cartao')=='3878':row['cartao']='6553'
        for source in self.data['fontes']:
            for subtotal in source.get('subtotais',[]):
                if subtotal['cartao']=='3878':subtotal['cartao']='6553'
        self.assertEqual(self.validate()['total'],D('17608.97'))
        row=next(r for r in self.data['lancamentos'] if r.get('cartao')=='6553')
        row['valor_pessoal_exato']=str(D(row['valor_original'])/4)
        with self.assertRaisesRegex(mensal.ValidationError,'uma única metade'):self.validate()
    def test_luiz_card_cannot_use_paloma_line(self):
        self.row('MASTERCARD-001')['linha']='56'
        with self.assertRaisesRegex(mensal.ValidationError,'não identificado como de Paloma'):self.validate()
    def test_same_credit_cannot_be_spent_twice(self):
        row=self.row('EXT-058');row['credito_vinculado']='EXT-019';row['valor_pessoal_exato']='415.25'
        with self.assertRaisesRegex(mensal.ValidationError,'crédito utilizado mais de uma vez'):self.validate()
    def test_confirmed_grouped_credit_can_be_allocated_once(self):
        first=self.row('EXT-043');second=self.row('EXT-037')
        first['creditos_aplicados']=[{'id':'EXT-016','valor':'30.00'}];first['valor_pessoal_exato']='33.60'
        second['creditos_aplicados']=[{'id':'EXT-016','valor':'70.00'}];second['valor_pessoal_exato']='117.50'
        result=self.validate()
        self.assertEqual(result['creditos_utilizados']['EXT-016']['valor_utilizado'],'100.00')
        self.assertEqual(result['total'],D('17508.97'))
    def test_returned_pix_is_not_available_for_reimbursement(self):
        row=self.row('EXT-029');row['creditos_aplicados']=[{'id':'EXT-026','valor':'875.00'}];row['valor_pessoal_exato']='875.00'
        with self.assertRaisesRegex(mensal.ValidationError,'PIX devolvido'):self.validate()
    def test_missing_bank_movement_breaks_balance(self):
        self.data['lancamentos']=[r for r in self.data['lancamentos'] if r['id']!='EXT-016']
        with self.assertRaisesRegex(mensal.ValidationError,'Saldo bancário não fecha'):self.validate()
    def test_renderer_has_same_total_and_all_45_model_lines(self):
        result=self.validate()
        with tempfile.TemporaryDirectory(prefix='.verificacao-',dir=ROOT) as temp:
            folder=Path(temp).resolve();self.assertTrue(folder.is_relative_to(ROOT))
            output=mensal.render(folder,result,output=folder)
            text=output.read_text(encoding='utf-8')
            self.assertIn('17.608,97',text)
            for row in result['linhas']:
                self.assertTrue(any(line.startswith('| '+mensal.sheet_line(row)+' | ') for line in text.splitlines()))
            self.assertTrue((folder/'PENDENCIAS.md').exists())

class Preparation(unittest.TestCase):
    def test_import_is_idempotent_and_does_not_overwrite_different_document(self):
        with tempfile.TemporaryDirectory(prefix='.verificacao-',dir=ROOT) as temp:
            folder=Path(temp).resolve();self.assertTrue(folder.is_relative_to(ROOT))
            incoming=folder/'in';incoming.mkdir()
            one=incoming/'extrato.pdf';one.write_bytes(b'%PDF-test-original')
            period,count=mensal.prepare(folder,'2026-09','2026-10',[one]);self.assertEqual(count,1)
            second=incoming/'copia.pdf';second.write_bytes(one.read_bytes())
            _,count=mensal.prepare(folder,'2026-09','2026-10',[one,second]);self.assertEqual(count,0)
            one.write_bytes(b'%PDF-another')
            with self.assertRaisesRegex(mensal.ValidationError,'Outro arquivo'):mensal.prepare(folder,'2026-09','2026-10',[one])
            self.assertEqual((period/'entradas/extrato.pdf').read_bytes(),b'%PDF-test-original')
    def test_period_path_rejects_escape(self):
        with self.assertRaises(mensal.ValidationError):mensal.period_path('../../elsewhere')

if __name__=='__main__':unittest.main(verbosity=2)
