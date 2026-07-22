import json
import re
from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
m = re.search(r'const EMBEDDED_DATA=(\{.*?\});\s*\n', s, re.S)
if not m:
    raise SystemExit('EMBEDDED_DATA not found')
data = json.loads(m.group(1))

# 加来さんが確認した支出。主要出金合計7,697,331円は維持する。
categories = [
    {'name': '仕入・外注支払', 'amount': 3390475, 'status': '通帳・PDF集計額。確認済み取引先を含む'},
    {'name': '給与', 'amount': 2140844, 'status': '既存給与1,679,049円＋6/30アルバイト給与461,795円'},
    {'name': '要確認支出', 'amount': 0, 'status': '今回確認対象はすべて分類済み'},
    {'name': '税・社会保険等', 'amount': 628880, 'status': '5/29社会保険314,440円を含む確定分類'},
    {'name': '現金経費引出', 'amount': 427702, 'status': '6/23・3,942円は経費として確認済み'},
    {'name': '役員・関係者支払', 'amount': 123466, 'status': '既存分類'},
    {'name': '通信費', 'amount': 18142, 'status': '既存分類'},
    {'name': '銀行手数料', 'amount': 9680, 'status': '6/23・550円は小銭両替手数料'},
    {'name': '通信・システム費', 'amount': 3300, 'status': '既存分類'},
    {'name': '食材仕入（のうゆう）', 'amount': 436987, 'status': '6/1・チャーシュー等の肉類'},
    {'name': '社長立替経費精算', 'amount': 243049, 'status': '6/2・領収書精算、社長分'},
    {'name': '岡税理士事務所 顧問料', 'amount': 49896, 'status': '6/3・7月各24,948円。毎月定額、決算月は増額'},
    {'name': '北海道ガス ガス代', 'amount': 202910, 'status': '6/10・ガス代'},
    {'name': '社労士顧問料', 'amount': 22000, 'status': '6/22・毎月定額'},
]
transactions = [
    {'date': '2026-05-29', 'payee': '北海道振興株式会社', 'amount': 531187, 'category': '店舗固定費', 'status': '確認済み'},
    {'date': '2026-05-29', 'payee': '藤井表具', 'amount': 315700, 'category': 'カウンター改造・修理', 'status': '確認済み'},
    {'date': '2026-05-29', 'payee': 'ペイジー', 'amount': 314440, 'category': '社会保険', 'status': '確認済み'},
    {'date': '2026-06-01', 'payee': 'のうゆう', 'amount': 436987, 'category': '食材仕入・チャーシュー等肉類', 'status': '確認済み'},
    {'date': '2026-06-02', 'payee': '社長分', 'amount': 243049, 'category': '領収書精算・立替経費', 'status': '確認済み'},
    {'date': '2026-06-03', 'payee': '岡税理士事務所', 'amount': 24948, 'category': '税理士顧問料', 'status': '毎月定額・決算月は増額'},
    {'date': '2026-06-10', 'payee': '北海道ガス', 'amount': 202910, 'category': 'ガス代', 'status': '確認済み'},
    {'date': '2026-06-10', 'payee': '株式会社ジョブマーケティング北海道', 'amount': 184557, 'category': '求人広告費', 'status': '確認済み'},
    {'date': '2026-06-10', 'payee': 'マルカツ製麺', 'amount': 294284, 'category': '麺・餃子仕入', 'status': '確認済み'},
    {'date': '2026-06-22', 'payee': '社労士', 'amount': 22000, 'category': '社労士顧問料', 'status': '毎月定額・確認済み'},
    {'date': '2026-06-23', 'payee': '経費', 'amount': 3942, 'category': '現金経費', 'status': '経費として確認済み'},
    {'date': '2026-06-23', 'payee': '両替', 'amount': 550, 'category': '小銭両替手数料', 'status': '確認済み'},
    {'date': '2026-06-30', 'payee': 'アルバイト', 'amount': 461795, 'category': 'アルバイト給与', 'status': '確認済み'},
    {'date': '2026-06-30', 'payee': '北海道振興株式会社', 'amount': 541957, 'category': '店舗固定費', 'status': '確認済み'},
    {'date': '2026-07', 'payee': '岡税理士事務所', 'amount': 24948, 'category': '税理士顧問料', 'status': '毎月定額・日付は7月分として保持'},
    {'date': '2026-07-08', 'payee': 'マルカツ製麺', 'amount': 323469, 'category': '麺・餃子仕入', 'status': '確認済み'},
]
examples = [
    {'payee': 'のうゆう（6/1）', 'amount': 436987, 'status': 'チャーシュー等の肉類仕入'},
    {'payee': '社会保険（5/29）', 'amount': 314440, 'status': '金額・費目とも確認済み'},
    {'payee': '岡税理士事務所', 'amount': 24948, 'status': '毎月定額、決算月は増額'},
    {'payee': '社労士（6/22）', 'amount': 22000, 'status': '毎月定額の顧問料'},
    {'payee': '北海道ガス（6/10）', 'amount': 202910, 'status': 'ガス代'},
    {'payee': 'アルバイト（6/30）', 'amount': 461795, 'status': '給与'},
]

data['expenses'] = {
    'categories': categories,
    'transactions': transactions,
    'examples': examples,
    'total': 7697331,
    'unknown_total': 0,
    'confirmed_at': '2026-07-22',
}
new_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
s = s[:m.start(1)] + new_json + s[m.end(1):]

consulting_base = r'''function renderConsultingBase(){
 const latest=state.monthly[state.monthly.length-1],prev=state.monthly[state.monthly.length-2],pay=EMBEDDED_DATA.payroll[0];
 const latestDaily=latest?latest.avg_daily:0,prevDaily=prev?prev.avg_daily:0,dailyChange=prevDaily?(latestDaily-prevDaily)/prevDaily:0;
 const latestCust=latest&&latest.days?latest.customers/latest.days:0,prevCust=prev&&prev.days?prev.customers/prev.days:0,custChange=prevCust?(latestCust-prevCust)/prevCust:0;
 const spendChange=prev&&prev.avg_spend?(latest.avg_spend-prev.avg_spend)/prev.avg_spend:0;
 const products=[...state.products].sort((a,b)=>b.sales-a.sales),top=products[0],productTotal=products.reduce((n,x)=>n+x.sales,0),beer=products.filter(x=>/ビール/.test(x.name)).reduce((n,x)=>n+x.sales,0);
 const periods=periodParts(),periodTotal=periods.reduce((n,x)=>n+x.value,0),night=(periods[1]?.value||0)+(periods[2]?.value||0);
 $('host').innerHTML=`<div class="notice ok" style="margin-bottom:12px"><b>経営コンサル要約</b>　売上・客数・客単価・商品・時間帯・給与・確認済み支出を統合した分析です。</div><div class="grid3"><div class="insight"><b>平均日商</b><br><span class="${dailyChange>=0?'up':'down'}">${dailyChange>=0?'改善':'低下'} ${Math.abs(dailyChange*100).toFixed(1)}％</span><div class="sub">7月進捗と6月の比較</div></div><div class="insight"><b>1日平均客数</b><br><span class="${custChange>=0?'up':'down'}">${custChange>=0?'改善':'低下'} ${Math.abs(custChange*100).toFixed(1)}％</span><div class="sub">売上変化の主因</div></div><div class="insight"><b>客単価</b><br><span class="${spendChange>=0?'up':'down'}">${spendChange>=0?'改善':'低下'} ${Math.abs(spendChange*100).toFixed(1)}％</span><div class="sub">価格・追加注文の効果</div></div></div><div class="panel" style="margin-top:12px"><h3>現状判断</h3><div class="insight"><b>売上の勢い</b><br>7月の平均日商は${yen(latestDaily)}で、6月${yen(prevDaily)}に対して${dailyChange>=0?'上回っています':'下回っています'}。月途中のため売上合計ではなく平均日商で判断します。</div><div class="insight"><b>人件費と社会保険</b><br>6月の給与支給率は${pct(pay.labor_cost_rate)}です。社会保険314,440円は確認済みで、税・社会保険等628,880円の分類に反映しています。金額不明ではありません。給与と社会保険を合わせて継続監視します。</div><div class="insight"><b>固定費</b><br>岡税理士事務所は月額24,948円（決算月増額）、社労士顧問料は月額22,000円です。北海道振興、北海道ガス、通信費とともに固定費として管理します。</div><div class="insight"><b>商品施策</b><br>売上上位は「${escapeHtml(top?.name||'集計対象なし')}」です。ビール売上は${yen(beer)}、商品売上内構成比は${pct(productTotal?beer/productTotal:0)}。ビール＋餃子セットは追加注文率と粗利額で効果を判定します。</div><div class="insight"><b>営業時間</b><br>夜＋深夜の売上構成は${pct(periodTotal?night/periodTotal:0)}です。時間帯売上と1時間当たり人件費を並べて配置を調整します。</div></div><div class="panel" style="margin-top:12px"><h3>実行優先順位</h3><ol><li>仕入・外注3,390,475円を取引先・請求書・対象商品へ分解する。</li><li>発生月と支払月を分け、月別営業利益と資金繰りを併記する。</li><li>のうゆう・マルカツ製麺の仕入を商品別売上へ接続し、商品粗利を算出する。</li><li>ビール・餃子セット導入前後の出数、売上、粗利を比較する。</li><li>時間帯別売上へシフト人数を重ね、低効率時間を調整する。</li></ol></div><div class="notice" style="margin-top:12px">7月売上は進捗値、6月給与は確定値です。期間の異なる数値を直接差し引いて利益とはしていません。</div>`;
}'''
s, n1 = re.subn(r'function renderConsultingBase\(\)\{.*?\n\}', consulting_base, s, count=1, flags=re.S)
if n1 != 1:
    raise SystemExit('renderConsultingBase replacement failed')

expenses_fn = r'''function renderExpenses(){
 const e=expenseData(),cats=e.categories||[],external=cats.find(x=>x.name==='仕入・外注支払')?.amount||0,unknown=e.unknown_total||0;
 const rows=cats.map(x=>[x.name,yen(x.amount),x.status]);
 const ex=(e.examples||[]).map(x=>[x.payee,yen(x.amount),x.status]);
 const tx=(e.transactions||[]).map(x=>[x.date,x.payee,yen(x.amount),x.category,x.status]);
 $('host').innerHTML=`<div class="notice ok" style="margin-bottom:12px"><b>確認対象はすべて分類済み</b>　社会保険、税理士、社労士、仕入、ガス、求人広告、修理、給与、立替経費、両替手数料を確定情報として反映しています。</div><div class="cards"><div class="card"><div>仕入・外注支払</div><div class="big">${yen(external)}</div><div class="sub">取引先別分解を継続</div></div><div class="card"><div>主要出金合計</div><div class="big">${yen(e.total)}</div><div class="sub">確認済み分類の合計</div></div><div class="card"><div>要確認支出</div><div class="big">${yen(unknown)}</div><div class="sub">今回確認対象は残件なし</div></div></div><div class="panel" style="margin-top:12px"><h3>主要出金カテゴリ</h3>${table(['区分','金額','状態'],rows,true)}</div><div class="panel" style="margin-top:12px"><h3>日付別・確認済み支出一覧</h3>${table(['日付','相手先','金額','分類','状態'],tx,true)}</div><div class="panel" style="margin-top:12px"><h3>確認結果の要点</h3>${table(['相手先・日付','金額','状態'],ex,true)}</div><div class="notice ok" style="margin-top:12px"><b>管理方針：</b>確認済み金額を再び「不明」「要確認」へ戻しません。新しい通帳明細だけを追加確認対象とし、既存の確定分類は維持します。</div>`;
}'''
s, n2 = re.subn(r'function renderExpenses\(\)\{.*?\n\}', expenses_fn, s, count=1, flags=re.S)
if n2 != 1:
    raise SystemExit('renderExpenses replacement failed')

consulting_fn = r'''function renderConsulting(){
 renderConsultingBase();
 const e=expenseData(),cats=e.categories||[],external=cats.find(x=>x.name==='仕入・外注支払')?.amount||0,payroll=cats.find(x=>x.name==='給与')?.amount||0,tax=cats.find(x=>x.name==='税・社会保険等')?.amount||0,unknown=e.unknown_total||0;
 const knownBurden=external+payroll+tax;
 $('host').insertAdjacentHTML('beforeend',`<div class="panel" style="margin-top:12px"><h3>確認済み支出を反映した経営分析</h3><div class="insight"><b>要確認支出は${yen(unknown)}です。</b><br>今回照会した支出はすべて分類済みです。社会保険314,440円、社労士顧問料22,000円、税理士顧問料24,948円などを確定情報として扱います。</div><div class="insight"><b>確認済み主要負担</b><br>仕入・外注支払${yen(external)}＋給与${yen(payroll)}＋税・社会保険等${yen(tax)}＝${yen(knownBurden)}です。集計期間が異なるため売上との差額をそのまま利益とはしませんが、費目不明を理由に分析を止める状態は解消しました。</div><div class="insight"><b>固定費と変動費の分離</b><br>税理士、社労士、北海道振興、北海道ガス、通信費は固定費側で管理します。のうゆう、マルカツ製麺は食材原価側、藤井表具はカウンター改造・修理、ジョブマーケティング北海道は求人広告費として分離します。</div><div class="insight"><b>次の分析段階</b><br>①仕入先別月次推移、②商品別材料原価、③固定費月額、④人件費＋社会保険、⑤営業利益と資金繰り、の順で精度を上げます。</div></div><div class="notice ok" style="margin-top:12px"><b>結論：</b>社会保険の金額が分からない、支出先が分からない、という旧判断は撤回済みです。確定情報を基準に経営判断します。</div>`);
}'''
s, n3 = re.subn(r'function renderConsulting\(\)\{.*?\n\}', consulting_fn, s, count=1, flags=re.S)
if n3 != 1:
    raise SystemExit('renderConsulting replacement failed')

# 残存し得る古い表現と、過去更新で生じた重複定義を除去。
s = s.replace("const tx=(e.transactions||[]).map(x=>[x.date,x.payee,yen(x.amount),x.category,x.status]);const tx=(e.transactions||[]).map(x=>[x.date,x.payee,yen(x.amount),x.category,x.status]);", "const tx=(e.transactions||[]).map(x=>[x.date,x.payee,yen(x.amount),x.category,x.status]);")

for forbidden in [
    '会社負担社会保険等を含まないため',
    '社会保険の金額が不明',
    '社会保険金額が不明',
    '要確認支出が利益判定を止めています',
    '唯一の未確認支出',
    'NSS.ジロウ？',
]:
    if forbidden in s:
        raise SystemExit('stale wording remains: ' + forbidden)

if sum(x['amount'] for x in categories) != 7697331:
    raise SystemExit('expense total mismatch')
if data['expenses']['unknown_total'] != 0:
    raise SystemExit('unknown total mismatch')
if s.count("const tx=(e.transactions||[]).map") != 1:
    raise SystemExit('transaction renderer duplicate or missing')
for token in ['社会保険314,440円', '社労士顧問料', '岡税理士事務所', 'のうゆう', 'マルカツ製麺', 'ジョブマーケティング北海道', '藤井表具']:
    if token not in s:
        raise SystemExit('missing confirmation: ' + token)

p.write_text(s, encoding='utf-8')
print('Expense analysis finalized; unknown=0; stale wording removed; JS duplicate fixed')
