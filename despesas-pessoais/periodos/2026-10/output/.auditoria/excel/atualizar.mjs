import fs from 'node:fs/promises';
import {FileBlob, SpreadsheetFile} from '@oai/artifact-tool';
const base='C:/github/personal/despesas-pessoais';
const out=base+'/periodos/2026-10/output/.auditoria/excel';
const source=process.argv.includes('--verificar')?out+'/final-validado.xlsx':base+'/planilhas/Despesas dia a dia - 2026.xlsx';
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(source));
if(process.argv.includes('--verificar')){wb.recalculate();for(const [sn,c,e] of [['Gastos','P81',13858.11],['Gastos','P19',19311.19],['Gastos','P83',5453.08],['Gastos Apartamento','F27',2245.46],['Gastos Apartamento','J24',2039.55]]){const v=wb.worksheets.getItem(sn).getRange(c).values[0][0];if(Math.abs(v-e)>0.001)throw Error(sn+c+' '+v);console.log(sn+'!'+c+' = '+v);}process.exit(0);}
console.log((await wb.inspect({kind:'sheet',include:'id,name',maxChars:2000})).ndjson);
const gastos=wb.worksheets.getItem('Gastos'), pal=wb.worksheets.getItem('Gastos Apartamento');
console.log(JSON.stringify({totais:gastos.getRange('O80:Q83').values,formulas:gastos.getRange('P80:P83').formulas,receita:gastos.getRange('P11:P19').values}));
for(const [sheetName,range,name] of [['Gastos','C49:P71','antes-gastos'],['Gastos Apartamento','B2:J27','antes-paloma']]){
 const img=await wb.render({sheetName,range,scale:1.5,format:'png'});await fs.writeFile(out+'/'+name+'.png',new Uint8Array(await img.arrayBuffer()));
}
if(!process.argv.includes('--editar'))process.exit(0);
const backup=base+'/planilhas/.backups/Despesas dia a dia - 2026.antes-fechamento-outubro-20261116.xlsx';
await fs.mkdir(base+'/planilhas/.backups',{recursive:true});
try{await fs.copyFile(source,backup,1);}catch(e){if(e.code!=='EEXIST')throw e;if(!(await fs.readFile(source)).equals(await fs.readFile(backup)))throw Error('Fonte mudou desde backup; revisar antes de editar.');}
const conf=JSON.parse(await fs.readFile(base+'/periodos/2026-10/output/.auditoria/dados/conferencia_mensal.json','utf8'));
const edits=[];
function val(sheet,cell,value,styleFrom){sheet.getRange(cell).values=[[value]];edits.push({sheet:sheet===gastos?'Gastos':'Gastos Apartamento',cell,value,styleFrom});}
function formula(sheet,cell,text,styleFrom){sheet.getRange(cell).formulas=[[text]];edits.push({sheet:sheet===gastos?'Gastos':'Gastos Apartamento',cell,formula:text,styleFrom});}
for(const row of conf.linhas){
 let excel=row.linha_excel;
 if(row.linha==='novo-projetos-empresa')excel='59';
 if(row.linha==='70')excel='72';
 if(excel)val(gastos,'P'+excel,Number(row.total));
 else if(Number(row.total)!==0)throw Error('Linha sem destino: '+row.linha);
}
val(gastos,'C59','Projetos/Empresa');val(gastos,'D59','Projetos/Empresa');
const income={3:13268.31,4:1620,5:1010.82,6:0,7:10708.86,8:0,9:0,10:0,12:988.07,13:1565.41,14:4684.42,15:0,16:58.90,17:0};
for(const [row,value] of Object.entries(income))val(gastos,'P'+row,value);
for(const [cell,text] of Object.entries({P11:'=SUM(P3:P10)',P18:'=SUM(P12:P17)',P19:'=P11-P18',P47:'=SUM(P21:P46)',P48:'=IF($P$19=0,"-",P47/$P$19)',P70:'=SUM(P49:P69)',P71:'=IF($P$19=0,"-",P70/$P$19)',P77:'=SUM(P72:P76)',P78:'=IF($P$19=0,"-",P77/$P$19)',P80:'=P19',P81:'=SUM(P47,P70,P77)',P82:'=P48+P71+P78',P83:'=P80-P81'}))formula(gastos,cell,text);
val(pal,'B2','Gastos totais — outubro/2026');
val(pal,'E10',880);val(pal,'E11',2974.38);val(pal,'D12','04/08');val(pal,'D13','04/14');
pal.getRange('B14:F14').copyFrom(pal.getRange('B10:F10'),'all');
val(pal,'B14','Faxina SOS Diaristas','B10');val(pal,'C14','PIX','C10');val(pal,'D14','À vista','D10');val(pal,'E14',199,'E10');formula(pal,'F14','=E14/2','F10');
for(const [cell,text] of Object.entries({F10:'=E10/2',F11:'=ROUND(E11/2,2)',F12:'=E12/2',F13:'=E13/2',E26:'=SUM(E9:E25)',F26:'=SUM(F9:F25)',F27:'=F8+F26'}))formula(pal,cell,text);
pal.getRange('I24:J24').copyFrom(pal.getRange('I23:J23'),'all');
val(pal,'I24','out/2026','I23');formula(pal,'J24','=SUM(Gastos!P53:P55)','J23');
formula(pal,'J27','=SUM(J3:J26)');
wb.recalculate();
for(const [sheet,cell,expected] of [[gastos,'P81',13858.11],[gastos,'P19',19311.19],[gastos,'P83',5453.08],[pal,'F27',2245.46],[pal,'J24',2039.55]]){
 const actual=sheet.getRange(cell).values[0][0];if(typeof actual!=='number'||Math.abs(actual-expected)>0.001)throw Error(cell+' expected '+expected+' actual '+actual);
}
const checks={Gastos:{receitas:gastos.getRange('P19').values[0][0],despesas:gastos.getRange('P81').values[0][0],saldo:gastos.getRange('P83').values[0][0]},Paloma:{total:pal.getRange('F27').values[0][0],alimentacao:pal.getRange('J24').values[0][0]}};
await fs.writeFile(out+'/edicoes.json',JSON.stringify({source,backup,edits,checks},null,2));
for(const [sheetName,range,name] of [['Gastos','C49:P71','depois-gastos'],['Gastos','M1:R19','depois-receitas'],['Gastos','M77:R83','depois-totais'],['Gastos Apartamento','B1:J27','depois-paloma']]){
 const img=await wb.render({sheetName,range,scale:1.5,format:'png'});await fs.writeFile(out+'/'+name+'.png',new Uint8Array(await img.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(wb)).save(out+'/edicao-artifact.xlsx');
console.log(JSON.stringify(checks));
