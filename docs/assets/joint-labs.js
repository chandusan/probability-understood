(() => {
  'use strict';
  const M=window.JointMath,$=id=>document.getElementById(id);
  const number=n=>n.toLocaleString(undefined,{maximumFractionDigits:6});
  const percent=p=>(100*p).toLocaleString(undefined,{maximumFractionDigits:4})+'%';
  const fraction=(a,b)=>`${number(a)}/${number(b)}`;
  const card=(label,value)=>`<div class="card"><span>${label}</span><strong>${value}</strong></div>`;
  const bars=(labels,counts,total)=>labels.map((label,i)=>`<div class="joint-bar-row"><span>${label}</span><div class="joint-bar-track" aria-hidden="true"><div class="joint-bar-fill" style="width:${100*counts[i]/total}%"></div></div><span class="joint-bar-value">${percent(counts[i]/total)}<small>${fraction(counts[i],total)}</small></span></div>`).join('');
  function bind(ids,render){
    const saved=window.openai?.widgetState;
    for(const id of ids){const el=$(id);if(saved&&[...el.options].some(option=>option.value===saved[id]))el.value=saved[id];}
    const run=()=>{render();window.openai?.setWidgetState(Object.fromEntries(ids.map(id=>[id,$(id).value])));};
    for(const id of ids)$(id).addEventListener('input',run);run();return run;
  }
  function tableCell(count,total,selected,maximum){
    const shade=count?` style="background-color:rgba(27,125,107,${.035+.22*count/maximum})"`:'';
    return `<td class="${count===0?'joint-zero ':''}${selected?'joint-selected':''}"${shade}>${fraction(count,total)}<small>${count===0?'impossible':percent(count/total)}</small></td>`;
  }
  if(document.body.dataset.lab==='joint-audit'){
    const d=M.audit(),max=Math.max(...d.counts.flat());
    const run=bind(['audit-event','audit-x','audit-y'],()=>{
      const x=+$('audit-x').value,y=+$('audit-y').value,event=$('audit-event').value;
      const selected=event==='cell'?(a,b)=>a===x&&b===y:event==='garbage'?(_a,b)=>b>=1:event==='clean'?(_a,b)=>b===0:(a,b)=>a+b<=2;
      const count=M.eventCount(d,selected),good=7-x-y;
      $('audit-x').disabled=event!=='cell';$('audit-y').disabled=event!=='cell';
      $('audit-results').innerHTML=card('Favorable samples',number(count))+card('All equally likely samples',number(d.total))+card('Event probability',percent(count/d.total));
      if(event==='cell'){
        $('audit-formula').textContent=good<0?`X = ${x} and Y = ${y} would require ${x+y} flawed images in a sample of only 7. The probability is exactly 0.`:`P(X = ${x}, Y = ${y}) = C(8, ${x}) × C(5, ${y}) × C(12, ${good}) / C(25, 7) = ${number(M.choose(8,x))} × ${number(M.choose(5,y))} × ${number(M.choose(12,good))} / ${number(d.total)} = ${fraction(count,d.total)}.`;
        $('audit-note').textContent=good<0?'The striped cell is structurally impossible. It is not a small positive probability that has been rounded to zero.':`Choose ${x} of the 8 minor-error images, ${y} of the 5 garbage images, and the remaining ${good} of the 12 perfect images. Each combination gives a different sample, so multiply those counts. Then divide by the number of all possible 7-image samples.`;
      }else{
        const name=event==='garbage'?'Y ≥ 1':event==='clean'?'Y = 0':'X + Y ≤ 2';
        $('audit-formula').textContent=`P(${name}) = (sum of favorable sample counts in the outlined cells) / C(25, 7) = ${fraction(count,d.total)} = ${percent(count/d.total)}.`;
        $('audit-note').textContent='Every sample has exactly one pair (X, Y). The cells describe disjoint events, so adding their counts does not double-count any sample. The denominator stays the same: all 7-image samples are still possible before seeing the result.';
      }
      $('audit-table').innerHTML=`<table><caption>Columns: minor errors X. Rows: garbage images Y. Each cell shows its exact favorable sample count and probability; the common denominator is ${number(d.total)}.</caption><thead><tr><th scope="col">Y ∖ X</th>${d.counts.map((_,i)=>`<th scope="col">X = ${i}</th>`).join('')}</tr></thead><tbody>${d.yTotals.map((_,b)=>`<tr><th scope="row">Y = ${b}</th>${d.counts.map((row,a)=>{const n=row[b],chosen=selected(a,b);return `<td class="${n===0?'joint-zero ':''}${chosen?'joint-selected':''}"${n?` style="background-color:rgba(27,125,107,${.035+.22*n/max})"`:''}><button class="joint-cell-button" data-x="${a}" data-y="${b}" aria-pressed="${chosen}" aria-label="Inspect X equals ${a}, Y equals ${b}: ${n} favorable samples${n?'':', impossible'}">${number(n)}<small>${n?percent(n/d.total):'impossible'}</small></button></td>`;}).join('')}</tr>`).join('')}</tbody></table>`;
    });
    $('audit-table').addEventListener('click',event=>{const button=event.target.closest('button[data-x]');if(!button)return;$('audit-event').value='cell';$('audit-x').value=button.dataset.x;$('audit-y').value=button.dataset.y;run();$('audit-x').focus();});
  }
  if(document.body.dataset.lab==='joint-dice'){
    const d=M.dice(),max=Math.max(...d.counts.flat()),values=Array.from({length:6},(_,i)=>i);
    bind(['joint-dice-view','joint-dice-fixed'],()=>{
      const mode=$('joint-dice-view').value,fixed=+$('joint-dice-fixed').value,isConditional=mode==='cx'||mode==='cy',target=mode==='my'||mode==='cy'?'y':'x';
      const isMarginal=mode==='mx'||mode==='my',unused=mode==='joint'||mode==='more';
      $('joint-dice-fixed-label').hidden=unused;$('joint-dice-fixed').disabled=unused;
      $('joint-dice-fixed-title').textContent=isConditional?`Known ${target==='x'?'five count Y':'six count X'}`:`Inspect ${target==='x'?'six count X':'five count Y'}`;
      let highlight=()=>false,chartCounts=d.xTotals,chartTotal=d.total,chartLabels=values.map(i=>`X = ${i}`),chartTitle='Marginal distribution of X: ignore how many fives occurred';
      let chartNote='Bar lengths use the same 0–100% scale. The six marginal probabilities add to 100%.';
      if(mode==='joint'){
        $('joint-dice-results').innerHTML=card('Equally likely sequences',number(d.total))+card('Possible count pairs','21')+card('Sum of all cell probabilities','100%');
        $('joint-dice-formula').innerHTML='p(x, y) = C(5, x) C(5 − x, y) 4<sup>5 − x − y</sup> / 6<sup>5</sup>, for nonnegative integers x, y with x + y ≤ 5.';
        $('joint-dice-note').textContent='Choose the six positions, then the five positions from those remaining. Each other position has four possible faces (1, 2, 3, or 4). The table counts individual face sequences; different count pairs are not equally likely.';
      }else if(mode==='more'){
        highlight=(x,y)=>x>y;const win=M.eventCount(d,highlight),tie=M.eventCount(d,(x,y)=>x===y),loss=d.total-win-tie;
        $('joint-dice-results').innerHTML=card('Sequences with X > Y',number(win))+card('P(X > Y)',percent(win/d.total))+card('P(X = Y)',percent(tie/d.total));
        $('joint-dice-formula').textContent=`P(X > Y) = ${fraction(win,d.total)}. Swapping the labels 5 and 6 pairs each X > Y sequence with one X < Y sequence, so this also equals (1 − ${fraction(tie,d.total)}) / 2.`;
        $('joint-dice-note').textContent='Add all outlined cells below the diagonal: their row value X exceeds their column value Y. The diagonal is the tie event and must be excluded before dividing the remaining probability equally between the two directions.';
        chartCounts=[win,tie,loss];chartLabels=['X > Y','X = Y','X < Y'];chartTitle='Three disjoint events exhaust all possible rolls';
      }else if(isConditional){
        const c=M.conditional(d,target,fixed),known=target==='x'?'Y':'X',name=target.toUpperCase(),remaining=5-fixed;
        highlight=target==='x'?(_x,y)=>y===fixed:(x,_y)=>x===fixed;
        chartCounts=c.counts;chartTotal=c.total;chartLabels=values.map(i=>`${name} = ${i}`);chartTitle=`Conditional distribution of ${name} given ${known} = ${fixed}`;
        $('joint-dice-results').innerHTML=card(`Sequences with ${known} = ${fixed}`,number(c.total))+card(`P(${known} = ${fixed})`,percent(c.total/d.total))+card('Conditional probabilities sum to','100%');
        $('joint-dice-formula').textContent=`P(${name} = ${name.toLowerCase()} | ${known} = ${fixed}) = p(x, y) / P(${known} = ${fixed}) = (cell count / 7,776) / (${number(c.total)} / 7,776) = cell count / ${number(c.total)}.`;
        $('joint-dice-note').textContent=remaining===0?`Knowing ${known} = 5 uses all five rolls. No roll can show the other face, so ${name} = 0 with conditional probability 1.`:`Keep only the outlined ${target==='x'?'column':'row'}; its ${number(c.total)} face sequences become the new sample space. After fixing the ${fixed} ${known==='Y'?'fives':'sixes'}, there are ${remaining} other rolls. Each has five equally likely remaining faces, and only one is a ${name==='X'?'six':'five'}, giving probability 1/5 per remaining roll. Thus ${name} | ${known} = ${fixed} follows Binomial(${remaining}, 1/5).`;
        chartNote='The table retains its original joint probabilities. The bars below divide the selected slice’s cell counts by its own total; these are the conditional probabilities.';
      }else if(isMarginal){
        const totals=target==='x'?d.xTotals:d.yTotals,name=target.toUpperCase();
        highlight=target==='x'?(x,_y)=>x===fixed:(_x,y)=>y===fixed;
        chartCounts=totals;chartLabels=values.map(i=>`${name} = ${i}`);chartTitle=`Marginal distribution of ${name}`;
        $('joint-dice-results').innerHTML=card(`Sequences with ${name} = ${fixed}`,number(totals[fixed]))+card(`P(${name} = ${fixed})`,percent(totals[fixed]/d.total))+card('Denominator stays',number(d.total));
        $('joint-dice-formula').textContent=`P(${name} = ${fixed}) = (sum of counts in the outlined ${target==='x'?'row':'column'}) / 7,776 = ${fraction(totals[fixed],d.total)}.`;
        $('joint-dice-note').textContent=`Ignore the other count and add every way it can occur alongside ${name} = ${fixed}. We have not learned a new fact restricting the sample space, so the denominator remains all 7,776 sequences. Over five independent rolls, the marginal count follows Binomial(5, 1/6).`;
      }
      $('joint-dice-table').innerHTML=`<table><caption>Joint probabilities p(x, y): each cell is an exact count divided by 7,776. Outlines identify the event or slice being inspected. Striped cells require more than 5 rolls and are impossible.</caption><thead><tr><th scope="col">X ∖ Y</th>${values.map(i=>`<th scope="col">Y = ${i}</th>`).join('')}<th scope="col">P(X = x)</th></tr></thead><tbody>${values.map(x=>`<tr><th scope="row">X = ${x}</th>${values.map(y=>tableCell(d.counts[x][y],d.total,highlight(x,y),max)).join('')}<td class="joint-total">${fraction(d.xTotals[x],d.total)}<small>${percent(d.xTotals[x]/d.total)}</small></td></tr>`).join('')}</tbody><tfoot><tr><th scope="row">P(Y = y)</th>${d.yTotals.map(n=>`<td class="joint-total">${fraction(n,d.total)}<small>${percent(n/d.total)}</small></td>`).join('')}<td class="joint-total">1</td></tr></tfoot></table>`;
      $('joint-dice-bars-title').textContent=chartTitle;$('joint-dice-bars').innerHTML=bars(chartLabels,chartCounts,chartTotal);$('joint-dice-bars-note').textContent=chartNote;
    });
  }
  if(document.body.dataset.lab==='joint-churn'){
    const d=M.churn(),names=['Low','Medium','High'];
    bind(['churn-tier','churn-comparison'],()=>{
      const tier=+$('churn-tier').value,index=tier-1,comparison=$('churn-comparison').value,r=M.churnRisk(tier,comparison),retained=r.group-r.events,name=names[index].toLowerCase();
      $('churn-results').innerHTML=card(`Joint: churned AND ${name}`,percent(r.events/d.total))+card(`Marginal: ${name} engagement`,percent(r.group/d.total))+card(`Conditional: churned GIVEN ${name}`,percent(r.risk));
      $('churn-formula').textContent=`P(X = 1 | Y = ${tier}) = P(X = 1, Y = ${tier}) / P(Y = ${tier}) = (${r.events}/100) / (${r.group}/100) = ${r.events}/${r.group} = ${percent(r.risk)}.`;
      $('churn-table').innerHTML=`<table class="joint-churn-table"><caption>Joint probabilities use all 100 customers as their denominator. The outlined column selects the group used for conditioning.</caption><thead><tr><th scope="col">Churn status X</th>${names.map((n,i)=>`<th scope="col">${n}, Y = ${i+1}</th>`).join('')}<th scope="col">Marginal</th></tr></thead><tbody>${d.counts.map((row,x)=>`<tr><th scope="row">${x?'Churned, X = 1':'Retained, X = 0'}</th>${row.map((n,y)=>`<td class="${y===index?'joint-highlight joint-selected':''}">${n}/100<small>${percent(n/100)}</small></td>`).join('')}<td class="joint-total">${d.xTotals[x]}/100</td></tr>`).join('')}</tbody><tfoot><tr><th scope="row">Marginal P(Y = y)</th>${d.yTotals.map((n,y)=>`<td class="joint-total ${y===index?'joint-selected':''}">${n}/100</td>`).join('')}<td class="joint-total">1</td></tr></tfoot></table>`;
      $('churn-bars-title').textContent=`Within ${name} engagement: the conditional distribution of X`;
      $('churn-bars').innerHTML=bars(['Retained','Churned'],[retained,r.events],r.group);
      $('churn-people').innerHTML=d.yTotals.map((total,y)=>Array.from({length:total},(_,i)=>`<span class="joint-person ${y===index?(i<d.counts[0][y]?'joint-member':'joint-event'):'joint-outside'}"></span>`).join('')).join('');
      $('churn-frequency-note').textContent=`Each square is one of the illustrative 100 customers. The ${r.group} colored squares are the ${name}-engagement group: ${retained} light green retained customers and ${r.events} dark green churned customers. Only these ${r.group} belong in the conditional denominator.`;
      const comparator=comparison==='baseline'?'all customers':'customers in the other two tiers';
      $('churn-risk').textContent=`Risk ratio relative to ${comparator}: (${r.events}/${r.group}) / (${r.comparisonEvents}/${r.comparisonGroup}) = ${number(r.ratio)}. The selected group's churn probability is ${number(r.ratio)} times the ${percent(r.comparisonRisk)} comparison risk. ${comparison==='baseline'?'The baseline includes this engagement group; this reproduces the comparison requested in the slide.':'This comparison excludes the selected tier, so the groups are disjoint and the denominator is a different risk.'}`;
    });
  }
  if(document.body.dataset.lab==='joint-tier'){
    const d=M.tier(),names=['Basic','Pro','Enterprise'];
    bind(['tier-breaches'],()=>{
      const y=+$('tier-breaches').value,p=M.posterior(y),modeNames=p.modes.map(x=>`${names[x-1]} (${x})`),meanNumerator=M.sum(p.counts.map((n,i)=>(i+1)*n));
      $('tier-results').innerHTML=card(`P(Y = ${y} breaches)`,`${p.total}/57`)+card('Most likely tier (MAP)',modeNames.join(' or '))+card('Posterior mean of tier number',number(p.mean));
      $('tier-formula').textContent=`P(X = x | Y = ${y}) = (cell numerator / 57) / (${p.total} / 57) = cell numerator / ${p.total}. The selected column's numerators are ${p.counts.join(', ')} and add to ${p.total}.`;
      $('tier-table').innerHTML=`<table class="joint-tier-table"><caption>Every joint entry is an integer divided by 57. Outlines select the observed breach count; its column total is the conditioning denominator before cancellation.</caption><thead><tr><th scope="col">Tier X ∖ Breaches Y</th>${[0,1,2].map(i=>`<th scope="col">Y = ${i}</th>`).join('')}<th scope="col">P(X = x)</th></tr></thead><tbody>${d.counts.map((row,i)=>`<tr><th scope="row">${names[i]}, X = ${i+1}</th>${row.map((n,j)=>`<td class="${j===y?'joint-highlight joint-selected':''}">${n}/57</td>`).join('')}<td class="joint-total">${d.xTotals[i]}/57</td></tr>`).join('')}</tbody><tfoot><tr><th scope="row">P(Y = y)</th>${d.yTotals.map((n,j)=>`<td class="joint-total ${j===y?'joint-selected':''}">${n}/57</td>`).join('')}<td class="joint-total">57/57 = 1</td></tr></tfoot></table>`;
      $('tier-bars-title').textContent=`Posterior tier probabilities after observing Y = ${y}`;
      $('tier-bars').innerHTML=bars(names.map((name,i)=>`${name} (${i+1})`),p.counts,p.total);
      $('tier-note').textContent=p.modes.length===1?`If every wrong tier prediction has the same cost, choose the tier with the largest posterior probability: ${modeNames[0]}, with probability ${Math.max(...p.counts)}/${p.total} = ${percent(Math.max(...p.probabilities))}. This is the maximum a posteriori (MAP) choice. It is the best-supported category, not a certainty.`:`With the same cost for every wrong tier prediction, Basic and Pro tie for the best categorical guess: each has posterior probability 8/22 = ${percent(8/22)}. There is no unique MAP choice for this observation.`;
      $('tier-mean-note').textContent=`The posterior mean is the weighted average of the numerical labels: (1 × ${p.counts[0]} + 2 × ${p.counts[1]} + 3 × ${p.counts[2]}) / ${p.total} = ${meanNumerator}/${p.total} ≈ ${number(p.mean)}. This is a numerical average, not another subscription tier. The MAP rule answers which category is most likely; a mean answers a different question about the numbered scale.`;
    });
  }
})();
