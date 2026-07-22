import json,re
from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
m=re.search(r'const EMBEDDED_DATA=(\{.*?\});\s*\n',s,re.S)
if not m:
    raise SystemExit('EMBEDDED_DATA not found')
data=json.loads(m.group(1))

new_daily=[
 {"business_date":"2026-07-16","total_sales":165380,"customers":121,"avg_spend":1367,"issued_count":None,"settlement_count":None,"settlement_amount":None,"net_count":None,"lunch_sales":None,"evening_sales":None,"late_sales":None,"notes":"集計日時7/17を営業日7/16として反映。内訳未確認は要確認。"},
 {"business_date":"2026-07-17","total_sales":152120,"customers":109,"avg_spend":1396,"issued_count":161,"settlement_count":-2,"settlement_amount":-1800,"net_count":159,"lunch_sales":19630,"evening_sales":87740,"late_sales":46550,"notes":"集計日時7/18を営業日7/17として反映。通帳入金一致。"},
 {"business_date":"2026-07-18","total_sales":138580,"customers":102,"avg_spend":1359,"issued_count":149,"settlement_count":-2,"settlement_amount":-1600,"net_count":147,"lunch_sales":25630,"evening_sales":85720,"late_sales":28830,"notes":"集計日時7/19を営業日7/18として反映。通帳入金一致。"},
 {"business_date":"2026-07-19","total_sales":278000,"customers":199,"avg_spend":1397,"issued_count":293,"settlement_count":0,"settlement_amount":0,"net_count":293,"lunch_sales":74620,"evening_sales":157520,"late_sales":45860,"notes":"集計日時7/20を営業日7/19として反映。通帳入金一致。"},
 {"business_date":"2026-07-20","total_sales":122250,"customers":85,"avg_spend":1438,"issued_count":125,"settlement_count":-2,"settlement_amount":-1600,"net_count":123,"lunch_sales":17360,"evening_sales":81730,"late_sales":24760,"notes":"集計日時7/22を営業日7/20として反映。7/21月曜は定休日。通帳未確認。"}
]

key='daily_2026-07'
arr=data.get(key,[])
by={x.get('business_date'):x for x in arr}
for x in new_daily: by[x['business_date']]=x
data[key]=sorted(by.values(),key=lambda x:x['business_date'])

july=data[key]
ms=sum(int(x.get('total_sales') or 0) for x in july)
mc=sum(int(x.get('customers') or 0) for x in july)
md=len([x for x in july if int(x.get('total_sales') or 0)>0])
bs=data.setdefault('bootstrap',{})
ov=bs.setdefault('overview',{})
ov.update({"month":"2026-07","month_sales":ms,"month_customers":mc,"month_days":md,"avg_daily":ms/md if md else 0,"avg_spend":ms/mc if mc else 0,"projection":ms/md*27 if md else 0})
bs['active_month']='2026-07'
if 'months' in bs and '2026-07' not in bs['months']: bs['months'].append('2026-07')

for k,v in list(data.items()):
    if isinstance(v,list) and ('monthly' in k.lower() or k=='monthly'):
        for row in v:
            if isinstance(row,dict) and (row.get('month')=='2026-07' or row.get('ym')=='2026-07'):
                for fld,val in [('total_sales',ms),('sales',ms),('month_sales',ms),('customers',mc),('total_customers',mc),('days',md),('month_days',md),('avg_daily',ms/md if md else 0),('avg_spend',ms/mc if mc else 0)]:
                    if fld in row: row[fld]=val

bank_rows=[
 {"business_date":"2026-07-17","deposit_date":"2026-07-21","sales":152120,"deposit":152120,"difference":0,"status":"一致"},
 {"business_date":"2026-07-18","deposit_date":"2026-07-21","sales":138580,"deposit":138580,"difference":0,"status":"一致"},
 {"business_date":"2026-07-19","deposit_date":"2026-07-21","sales":278000,"deposit":278000,"difference":0,"status":"一致"},
 {"business_date":"2026-07-20","deposit_date":None,"sales":122250,"deposit":None,"difference":None,"status":"通帳未確認"}
]
for k,v in list(data.items()):
    if isinstance(v,list) and 'bank' in k.lower() and ('2026-07' in k or k=='bank'):
        old={str(x.get('business_date') or x.get('sales_date')):x for x in v if isinstance(x,dict)}
        for r in bank_rows: old[r['business_date']]=r
        data[k]=list(old.values())

# PDF由来の出金分類を埋込データとして保持
expenses={
 "source":"経営改善提案書PDF・通帳分類",
 "period":"資料掲載期間（発生月・支払月の完全一致は要確認）",
 "categories":[
  {"name":"仕入・外注支払","amount":3390475,"status":"PDF掲載額"},
  {"name":"給与","amount":1679049,"status":"PDF掲載額"},
  {"name":"要確認支出","amount":1416637,"status":"費目未確定"},
  {"name":"税・社会保険等","amount":628880,"status":"PDF掲載額"},
  {"name":"現金経費引出","amount":427702,"status":"領収書照合要"},
  {"name":"役員・関係者支払","amount":123466,"status":"PDF掲載額"},
  {"name":"通信費","amount":18142,"status":"PDF掲載額"},
  {"name":"銀行手数料","amount":9680,"status":"PDF掲載額"},
  {"name":"通信・システム費","amount":3300,"status":"PDF掲載額"}
 ],
 "examples":[
  {"payee":"カ）エイシン","amount":50112,"status":"確認済"},
  {"payee":"ホッカイドウ…","amount":531187,"status":"相手先要確認"},
  {"payee":"カ）サッポロタイセイ","amount":108000,"status":"確認済"},
  {"payee":"ユ）フジイ…","amount":315700,"status":"相手先要確認"}
 ]
}
expenses['total']=sum(x['amount'] for x in expenses['categories'])
data['expenses']=expenses

new_json=json.dumps(data,ensure_ascii=False,separators=(',',':'))
s=s[:m.start(1)]+new_json+s[m.end(1):]
s=s.replace('売上は7月15日分まで','売上は7月20日分まで')
s=s.replace('7月15日分まで','7月20日分まで')

# 外注費・経費を同一ダッシュボードのタブへ統合
if "t_expenses" not in s:
    anchor='<button id="t_quality" onclick="showTab(\'quality\')">品質検証</button>'
    button='<button id="t_expenses" onclick="showTab(\'expenses\')">仕入・外注・経費</button>'
    if anchor not in s: raise SystemExit('quality tab anchor missing')
    s=s.replace(anchor,button+anchor,1)

if "tab==='expenses'" not in s:
    anchor="if(tab==='bank')return renderBank();"
    if anchor not in s: raise SystemExit('showTab bank anchor missing')
    s=s.replace(anchor,anchor+"if(tab==='expenses')return renderExpenses();",1)

# 既存コンサルを基礎関数へ変更し、PDF出金分析を同じコンサル画面へ追加
if 'function renderConsultingBase(){' not in s:
    s=s.replace('function renderConsulting(){','function renderConsultingBase(){',1)

integration_js=r'''
function expenseData(){return EMBEDDED_DATA.expenses||{categories:[],examples:[],total:0}}
function renderExpenses(){
 const e=expenseData(),cats=e.categories||[],external=cats.find(x=>x.name==='仕入・外注支払')?.amount||0,unknown=cats.find(x=>x.name==='要確認支出')?.amount||0;
 const rows=cats.map(x=>[x.name,yen(x.amount),x.status]);
 const ex=(e.examples||[]).map(x=>[x.payee,yen(x.amount),x.status]);
 $('host').innerHTML=`<div class="notice ok" style="margin-bottom:12px"><b>月別経営分析へ完全統合済み</b>　PDF由来の仕入・外注費、給与、税・社会保険、現金経費等を同じダッシュボード内で確認できます。発生月と支払月が一致しない可能性があるため、未確認分は利益に断定計上しません。</div><div class="cards"><div class="card"><div>仕入・外注支払</div><div class="big">${yen(external)}</div><div class="sub">PDF掲載額</div></div><div class="card"><div>主要出金合計</div><div class="big">${yen(e.total)}</div><div class="sub">9分類の単純合計</div></div><div class="card"><div>要確認支出</div><div class="big">${yen(unknown)}</div><div class="sub">相手先・費目未確定</div></div></div><div class="panel" style="margin-top:12px"><h3>PDF掲載の主要出金カテゴリ</h3>${table(['区分','金額','状態'],rows,true)}</div><div class="panel" style="margin-top:12px"><h3>仕入・外注支払の通帳確認例</h3>${table(['通帳摘要・相手先','金額','状態'],ex,true)}<div class="sub">例示行であり、3,390,475円の全内訳ではありません。</div></div><div class="notice" style="margin-top:12px"><b>管理方針：</b>仕入・外注支払は一括費用で終わらせず、取引先・請求書・対象商品・支払日へ分解します。未確定明細を推測で埋めず、要確認として残します。</div>`;
}
function renderConsulting(){
 renderConsultingBase();
 const e=expenseData(),cats=e.categories||[],external=cats.find(x=>x.name==='仕入・外注支払')?.amount||0,payroll=cats.find(x=>x.name==='給与')?.amount||0,unknown=cats.find(x=>x.name==='要確認支出')?.amount||0,tax=cats.find(x=>x.name==='税・社会保険等')?.amount||0;
 const knownBurden=external+payroll+tax;
 $('host').insertAdjacentHTML('beforeend',`<div class="panel" style="margin-top:12px"><h3>PDF出金を取り込んだ経営分析コンサル</h3><div class="insight"><b>最優先課題は売上増だけではなく、3,390,475円の仕入・外注支払の分解です。</b><br>この金額を一括のままでは、材料原価、業務委託、設備・修繕、その他支払のどれが利益を圧迫しているか判断できません。取引先別・請求書別に分け、売上に直接対応する原価と固定的な外注費を分離する必要があります。</div><div class="insight"><b>確認済み主要負担</b><br>仕入・外注支払${yen(external)}＋給与${yen(payroll)}＋税・社会保険等${yen(tax)}＝${yen(knownBurden)}です。ただし、PDFの集計期間と月別売上の対象期間が完全一致すると確認できていないため、この差額をそのまま赤字・利益とは判定しません。</div><div class="insight"><b>要確認支出${yen(unknown)}が利益判定を止めています。</b><br>この支出を費目確定せずに経営判断すると、原価率・人件費率・固定費率のすべてが歪みます。金額の大きい順に摘要、請求書、領収書を照合するのが最短です。</div><div class="insight"><b>改善の順番</b><br>①仕入・外注3,390,475円を取引先別に分解、②要確認支出1,416,637円を確定、③発生月と支払月を分離、④商品別売上と材料原価を接続、⑤月別営業利益と資金繰りを同時表示、の順で進めます。</div></div><div class="notice" style="margin-top:12px"><b>結論：</b>売上分析だけでは経営改善になりません。今回の統合により、売上・人件費・外注費・税社保・未確定支出を同じ画面で確認し、何が利益を圧迫しているかを追える構造にしました。</div>`);
}
'''
if 'function expenseData()' not in s:
    anchor='function extractSalesDate(note,txdate)'
    if anchor not in s: raise SystemExit('consulting integration anchor missing')
    s=s.replace(anchor,integration_js+'\n'+anchor,1)

required=['月別経営分析','経営コンサル','商品別・全商品','ABC分析','ビール・セット','時間帯','売上入金照合','仕入・外注・経費','品質検証','3390475','1416637','function renderExpenses','PDF出金を取り込んだ経営分析コンサル']
missing=[x for x in required if x not in s]
if missing: raise SystemExit('required features missing: '+','.join(missing))
for d in ['2026-07-16','2026-07-17','2026-07-18','2026-07-19','2026-07-20']:
    if d not in s: raise SystemExit('daily row missing: '+d)
if sum(x['total_sales'] for x in new_daily)!=856330 or sum(x['customers'] for x in new_daily)!=616:
    raise SystemExit('new daily control total mismatch')
if expenses['total']!=7697331:
    raise SystemExit('expense control total mismatch')
if s.count('function renderConsulting(){')!=1 or s.count('function renderConsultingBase(){')!=1:
    raise SystemExit('consulting function integration mismatch')

p.write_text(s,encoding='utf-8')
print(f'Integrated dashboard verified: July sales={ms:,}, expenses={expenses["total"]:,}')