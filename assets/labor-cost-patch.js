(() => {
  const SOCIAL_INSURANCE = {
    '2026-06': 314440
  };

  function insuranceFor(month) {
    return Number(SOCIAL_INSURANCE[month] || 0);
  }

  async function correctedPayroll() {
    let d = await api('/api/payroll');
    if (state.scope === 'month') d = d.filter(x => x.year_month === state.month);
    if (!d.length) {
      $('host').innerHTML = '<div class="notice"><b>この月の人件費は未確定です。</b> 現在公開できる確定値は2026年6月分だけです。</div>';
      return;
    }
    const r = d[0];
    const social = insuranceFor(r.year_month);
    const totalLabor = Number(r.salary_paid || 0) + social;
    const totalRate = Number(r.monthly_sales || 0) ? totalLabor / Number(r.monthly_sales) : 0;
    const salesMinusTotalLabor = Number(r.monthly_sales || 0) - totalLabor;

    $('host').innerHTML = `<div class="notice ok" style="margin-bottom:12px"><b>${ymLabel(r.year_month)}確定分・店舗全体の集計のみ公開</b>　個人名、個人別給与、給与明細画像は公開していません。</div>
    <div class="cards">
      <div class="card"><div class="label">社員 支給総額</div><div class="big">${yen(r.employee_gross)}</div><div class="sub">個人別内訳は非公開</div></div>
      <div class="card"><div class="label">アルバイト 支給総額</div><div class="big">${yen(r.parttime_gross)}</div><div class="sub">非課税交通費を含む</div></div>
      <div class="card"><div class="label">給与支給総額</div><div class="big">${yen(r.salary_paid)}</div><div class="sub">社員＋アルバイト</div></div>
      <div class="card"><div class="label">社会保険料</div><div class="big">${yen(social)}</div><div class="sub">資料記載の2026年5月分・6月支払対象</div></div>
      <div class="card"><div class="label">社会保険込み総人件費</div><div class="big">${yen(totalLabor)}</div><div class="sub">給与支給総額＋社会保険料</div></div>
      <div class="card"><div class="label">総人件費率</div><div class="big">${pct(totalRate)}</div><div class="sub">社会保険込み総人件費÷売上</div></div>
      <div class="card"><div class="label">売上－総人件費</div><div class="big">${yen(salesMinusTotalLabor)}</div><div class="sub">原価・家賃等の控除前</div></div>
    </div>
    <div class="panel" style="margin-top:12px"><h3>6月 総人件費分析</h3>${table(['年月','売上','社員','アルバイト','給与支給総額','社会保険料','総人件費','総人件費率','状態'],[[ymLabel(r.year_month),yen(r.monthly_sales),yen(r.employee_gross),yen(r.parttime_gross),yen(r.salary_paid),yen(social),yen(totalLabor),pct(totalRate),r.status]])}</div>
    <div class="notice" style="margin-top:12px"><b>重要：</b>人件費率は給与だけではなく、確認できた社会保険料を加えた総人件費で表示します。福利厚生費、採用費、外注人件費は別費目のため、この率には含めていません。</div>`;
  }

  function correctedConsulting() {
    renderConsultingBase();
    const pay = (EMBEDDED_DATA.payroll || [])[0];
    if (!pay) return;
    const social = insuranceFor(pay.year_month);
    const totalLabor = Number(pay.salary_paid || 0) + social;
    const totalRate = Number(pay.monthly_sales || 0) ? totalLabor / Number(pay.monthly_sales) : 0;
    const salaryOnlyRate = Number(pay.monthly_sales || 0) ? Number(pay.salary_paid || 0) / Number(pay.monthly_sales) : 0;
    const rateIncrease = totalRate - salaryOnlyRate;

    $('host').insertAdjacentHTML('beforeend', `<div class="panel" style="margin-top:12px"><h3>社会保険込み総人件費による経営判断</h3>
      <div class="cards">
        <div class="card"><div class="label">給与支給総額</div><div class="big">${yen(pay.salary_paid)}</div></div>
        <div class="card"><div class="label">社会保険料</div><div class="big">${yen(social)}</div></div>
        <div class="card"><div class="label">総人件費</div><div class="big">${yen(totalLabor)}</div></div>
        <div class="card"><div class="label">総人件費率</div><div class="big">${pct(totalRate)}</div><div class="sub">給与だけの率より ${(rateIncrease*100).toFixed(1)}ポイント上昇</div></div>
      </div>
      <div class="insight"><b>経営判断は給与だけの人件費率ではなく、社会保険を加えた総人件費率を基準にします。</b><br>給与のみの比率は${pct(salaryOnlyRate)}ですが、社会保険料${yen(social)}を加えると総人件費率は${pct(totalRate)}です。</div>
      <div class="insight"><b>採算を見る順番</b><br>売上から、社会保険込み総人件費、材料原価、家賃・共益費、水道光熱費、その他固定費を順に差し引いて営業利益を判断します。</div>
      <div class="notice"><b>区分上の注意：</b>「税・社会保険等」628,880円は税金等を含む集計区分なので、全額を人件費には入れません。今回、人件費へ加えたのは請求書で社会保険料と確認できた314,440円です。</div>
    </div>`);
  }

  window.renderPayroll = correctedPayroll;
  window.renderConsulting = correctedConsulting;
})();