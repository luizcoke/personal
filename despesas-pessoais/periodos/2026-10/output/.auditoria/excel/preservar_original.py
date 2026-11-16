"""Transplanta somente células autorizadas da edição Artifact para o pacote original.
Preserva literalmente pivôs, vínculos, estilos, demais abas e meses.
"""
from pathlib import Path
from zipfile import ZipFile
import json,re,hashlib,xml.etree.ElementTree as E
from xml.sax.saxutils import escape
HERE=Path(__file__).resolve().parent
plan=json.loads((HERE/'edicoes.json').read_text(encoding='utf-8'))
source=Path(plan['source']);backup=Path(plan['backup']);stage=HERE/'final-validado.xlsx'
assert source.read_bytes()==backup.read_bytes(),'Original mudou após backup'
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
paths={'Gastos':'xl/worksheets/sheet2.xml','Gastos Apartamento':'xl/worksheets/sheet3.xml'}
def sheetpaths(z):
 rels={x.attrib['Id']:x.attrib['Target'] for x in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
 result={}
 for s in E.fromstring(z.read('xl/workbook.xml')).find('m:sheets',ns):
  target=rels[s.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
  result[s.attrib['name']]=target.lstrip('/') if target.startswith('/') else 'xl/'+target
 return result
def cells(z,path):return {c.attrib['r']:c for c in E.fromstring(z.read(path)).findall('m:sheetData/m:row/m:c',ns)}
changes={}
with ZipFile(source) as src,ZipFile(HERE/'edicao-artifact.xlsx') as edited:
 ep=sheetpaths(edited)
 for name,path in paths.items():
  old=cells(src,path);new=cells(edited,ep[name]);xml=src.read(path).decode('utf-8')
  for edit in [x for x in plan['edits'] if x['sheet']==name]:
   a=edit['cell'];c=new[a];orig=old[a];style=old[edit.get('styleFrom') or a].attrib.get('s','0')
   if 'formula' in edit:
    f=c.find('m:f',ns);v=c.find('m:v',ns)
    assert f is not None and f.text==edit['formula'][1:],(name,a)
    assert v is not None and c.attrib.get('t')!='e',(name,a,'no cache')
    body='<f>'+escape(f.text)+'</f><v>'+escape(v.text or '')+'</v>';typ=''
   elif isinstance(edit['value'],str):
    body='<is><t>'+escape(edit['value'])+'</t></is>';typ=' t="inlineStr"'
   else:
    v=c.find('m:v',ns);assert v is not None and abs(float(v.text)-edit['value'])<1e-6,(name,a)
    body='<v>'+v.text+'</v>';typ=''
   replacement=f'<c r="{a}" s="{style}"{typ}>{body}</c>'
   pattern=rf'<c\b(?=[^>]*\br="{a}")[^>]*?(?:/>|>.*?</c>)'
   xml,count=re.subn(pattern,lambda m:replacement,xml,flags=re.S)
   assert count==1,(name,a,count)
  changes[path]=xml.encode('utf-8')
 # All untouched ZIP members are retained, including all pivot caches/links/styles.
 with ZipFile(stage,'w') as dst:
  for item in src.infolist():dst.writestr(item,changes.get(item.filename,src.read(item.filename)))
with ZipFile(source) as before,ZipFile(stage) as after:
 assert set(before.namelist())==set(after.namelist())
 changed=[n for n in before.namelist() if before.read(n)!=after.read(n)]
 assert set(changed)==set(paths.values()),changed
 for name,path in paths.items():
  b=cells(before,path);a=cells(after,path);allowed={x['cell'] for x in plan['edits'] if x['sheet']==name}
  assert set(a)==set(b)
  for addr in a:
   if addr not in allowed:assert E.tostring(a[addr])==E.tostring(b[addr]),(name,addr)
 for path,cell,value in [('xl/worksheets/sheet2.xml','P81',13858.11),('xl/worksheets/sheet2.xml','P19',19311.19),('xl/worksheets/sheet2.xml','P83',5453.08),('xl/worksheets/sheet3.xml','F27',2245.46),('xl/worksheets/sheet3.xml','J24',2039.55)]:
  actual=float(cells(after,path)[cell].find('m:v',ns).text);assert abs(actual-value)<1e-6,(cell,actual)
 print('Preservação verificada:',len(before.namelist()),'partes; somente duas abas alteradas;',len(plan['edits']),'edições de célula.')
manifest={'arquivo':str(source),'backup':str(backup),'sha256_antes':hashlib.sha256(source.read_bytes()).hexdigest(),'sha256_depois':hashlib.sha256(stage.read_bytes()).hexdigest(),'partes_alteradas':changed,'verificacao':'Somente células autorizadas em duas abas; outros meses, demais abas, tabelas dinâmicas, vínculos, estilos e objetos preservados. Recálculo Artifact e valores-chave conferidos; Excel nativo não executado.','edicoes':plan['edits'],'totais':plan['checks']}
(HERE.parent/'dados/atualizacao_excel.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
