(() => {
  'use strict';
  const M=window.ConditionalMath,$=id=>document.getElementById(id);
  const pct=x=>x===null?'Undefined':x>0&&x<0.000001?'<0.0001%':x<1&&x>0.999999?'>99.9999%':(100*x).toLocaleString(undefined,{maximumFractionDigits:4})+'%';
  const ruinPct=(p,i,k)=>{const x=M.ruin(p,i,k);return i>0&&i<k&&x>=0.999999?'>99.9999%':pct(x);};
  const num=x=>x.toLocaleString(undefined,{maximumFractionDigits:3});
  const card=(label,value)=>`<div class="card"><span>${label}</span><strong>${value}</strong></div>`;
  const colors=['#1b7d6b','#5870a0','#b7753f','#acb7aa'];
  const id=document.body.dataset.lab;
  const saved=window.openai?.widgetState;
  function bind(ids,render){
    if(saved)for(const name of ids)if(saved[name]!==undefined){const el=$(name);if(name==='start-i')el.max=+$('total-k').value-1;if(name==='joint'){el.min=Math.max(0,+$('pa').value+ +$('pb').value-100);el.max=Math.min(+$('pa').value,+$('pb').value);}if(el.tagName==='SELECT'&&[...el.options].some(o=>o.value===saved[name]))el.value=saved[name];else if(el.tagName==='INPUT'&&Number.isFinite(+saved[name]))el.value=saved[name];}
    const run=()=>{render();const next={};for(const name of ids)next[name]=$(name).value;window.openai?.setWidgetState(next);};
    for(const name of ids)$(name).addEventListener('input',run);run();
  }
  if(id==='cond-events')bind(['pa','pb','joint','condition'],()=>{
    const a=+$('pa').value/100,b=+$('pb').value/100;
    $('joint').min=Math.round(100*Math.max(0,a+b-1));$('joint').max=Math.round(100*Math.min(a,b));
    const j=+$('joint').value/100,weights=M.regions(a,b,j),labels=['Both A and B','A only','B only','Neither'];
    ['pa','pb','joint'].forEach(n=>$(n+'-out').textContent=pct(+$(n).value/100));
    const type=$('condition').value,keep={all:[1,1,1,1],b:[1,0,1,0],notb:[0,1,0,1],atmost:[0,1,1,1]}[type];
    const den=weights.reduce((s,w,i)=>s+w*keep[i],0);
    $('event-rows').innerHTML=weights.map((w,i)=>`<tr><th>${labels[i]}</th><td>${pct(w)}</td><td>${!keep[i]?'Excluded':pct(M.ratio(w,den))}</td></tr>`).join('');
    $('event-bar').innerHTML=weights.map((w,i)=>`<span style="width:${w*100}%;background:${colors[i]};opacity:${keep[i]?1:.2}"></span>`).join('');
    $('event-legend').innerHTML=labels.map((s,i)=>`<span><i style="background:${colors[i]}"></i>${s}</span>`).join('');
    $('event-results').innerHTML=card('Probability of the condition',pct(den))+card('P(A | condition)',pct(M.ratio(weights[0]*keep[0]+weights[1]*keep[1],den)))+card('P(neither | condition)',pct(M.ratio(weights[3]*keep[3],den)));
    $('event-note').textContent=den===0?'This condition has probability zero, so the conditional probabilities are undefined.':`Keep the permitted regions, then divide each retained probability by ${num(den)}. “At most one” keeps A only, B only and neither. The overlap slider stays within the bounds needed for all four regions to be nonnegative.`;
  });
  if(id==='cond-coins')bind(['coin-condition'],()=>{
    const rows=M.coins(),type=$('coin-condition').value,passes=r=>type==='all'||(type==='ac'?r.a&&r.c:r[type]),kept=rows.filter(passes);
    $('coin-grid').innerHTML=rows.map(r=>`<div class="cond-coin ${passes(r)?'':'outside'}"><b>${r.s}</b><span>A: ${r.a?'yes':'no'} · B: ${r.b?'yes':'no'} · C: ${r.c?'yes':'no'}</span></div>`).join('');
    $('coin-results').innerHTML=card('Retained outcomes',`${kept.length} / 16`)+['a','b','c'].map(key=>card(`P(${key.toUpperCase()} | condition)`,`${kept.filter(r=>r[key]).length}/${kept.length} = ${pct(kept.filter(r=>r[key]).length/kept.length)}`)).join('');
    $('coin-note').textContent=type==='ac'?'A and C together force an even number of heads. All four retained strings fail B: P(B | A and C) = 0, even though P(B | A) = P(B | C) = 1/2.':'Each individual event contains 8 strings. Each pair intersection contains 4, so every pair is independent. Select “Both A and C” to see why all three are not mutually independent.';
  });
  if(id==='cond-bayes')bind(['prior','sensitivity','false-positive'],()=>{
    const p=+$('prior').value/100,s=+$('sensitivity').value/100,f=+$('false-positive').value/100,v=M.bayes(p,s,f),N=100000;
    ['prior','sensitivity','false-positive'].forEach(n=>$(n+'-out').textContent=pct(+$(n).value/100));
    $('test-rows').innerHTML=`<tr><th>Condition present</th><td>${num(N*v.yes)}</td><td>${num(N*p*(1-s))}</td><td>${num(N*p)}</td></tr><tr><th>Condition absent</th><td>${num(N*v.no)}</td><td>${num(N*(1-p)*(1-f))}</td><td>${num(N*(1-p))}</td></tr><tr><th>Total</th><td>${num(N*v.evidence)}</td><td>${num(N*(1-v.evidence))}</td><td>100,000</td></tr>`;
    $('test-results').innerHTML=card('Sensitivity (model input)',pct(s))+card('P(condition | positive)',pct(v.posterior));
    $('test-bar').innerHTML=v.posterior===null?'':`<span style="width:${100*v.posterior}%;background:${colors[0]}"></span><span style="width:${100*(1-v.posterior)}%;background:${colors[2]}"></span>`;
    $('test-note').textContent=v.posterior===null?'No positive tests are possible under these parameters; conditioning on a positive test is undefined.':`Among ${num(N*v.evidence)} positive tests, ${num(N*v.yes)} are true positives (green) and ${num(N*v.no)} are false positives (orange). The posterior is ${num(N*v.yes)} ÷ ${num(N*v.evidence)}. A false-positive rate is measured among people without the condition, not among all positive tests.`;
  });
  if(id==='cond-urns')bind(['red-a','red-b','observed'],()=>{
    const a=+$('red-a').value,b=+$('red-b').value,t=+$('observed').value,v=M.urns(a,b,20,t);
    ['red-a','red-b','observed'].forEach(n=>$(n+'-out').textContent=$(n).value);
    const row=(name,r,l,post)=>`<tr><th>${name}</th><td>${t===0?'1 (no evidence yet)':Array.from({length:Math.min(t,r+1)},(_,j)=>`${Math.max(0,r-j)}/${20-j}`).join(' × ')} = ${pct(l)}</td><td>${pct(post)}</td><td>${l===0?'Impossible evidence':`${r-t}/${20-t} = ${pct((r-t)/(20-t))}`}</td></tr>`;
    $('urn-rows').innerHTML=row('Urn A',a,v.la,v.posterior)+row('Urn B',b,v.lb,v.posterior===null?null:1-v.posterior);
    $('urn-results').innerHTML=card('P(A | observed reds)',pct(v.posterior))+card('P(next red | observed reds)',pct(v.next));
    $('urn-note').textContent=v.posterior===null?'Neither urn can produce that many red draws without replacement. The proposed evidence is impossible, so there is no posterior or next-draw conditional probability.':`Both urns still have ${20-t} balls after the observed draws. First update the urn probabilities using the evidence; then weight each remaining red fraction by its updated urn probability. With the slide’s values, this is (11/12)(10/18) + (1/12)(2/18) = 14/27.`;
  });
  if(id==='cond-ruin'){
    let params;
    bind(['win-p','total-k','start-i'],()=>{
      const p=+$('win-p').value/100,k=+$('total-k').value;$('start-i').max=k-1;
      const i=+$('start-i').value;params={p,k,i};
      $('win-p-out').textContent=pct(p);$('total-k-out').textContent=k;$('start-i-out').textContent=i;
      const value=M.ruin(p,i,k);
      const show=j=>ruinPct(p,j,k);
      $('ruin-results').innerHTML=card('Win one play',pct(p))+card('Eventually reach k before 0',show(i))+card('Fair-game comparison i/k',pct(i/k));
      const points=Array.from({length:k+1},(_,j)=>`${40+480*j/k},${220-180*M.ruin(p,j,k)}`).join(' ');
      $('ruin-chart').innerHTML=`<path d="M40 40 V220 H520" fill="none" stroke="#acb7aa"/><path d="M40 220 L520 40" stroke="#b7753f" stroke-dasharray="5 5" fill="none"/><polyline points="${points}" fill="none" stroke="#1b7d6b" stroke-width="3"/><circle cx="${40+480*i/k}" cy="${220-180*value}" r="5" fill="#233632"/><g fill="#697a6c" font-size="12"><text x="10" y="45">1</text><text x="10" y="225">0</text><text x="36" y="242">0</text><text x="510" y="242">${k}</text><text x="150" y="258">A's starting fortune (green = exact; dashed = fair)</text></g>`;
      $('ruin-equation').textContent=`Condition on the next play: P${i} = ${num(p)} × P${i+1} + ${num(1-p)} × P${i-1}. Displayed probabilities: P${i+1}: ${show(i+1)}; P${i-1}: ${show(i-1)}; P${i}: ${show(i)}. Values are rounded; every interior starting fortune has a probability strictly between 0 and 1.`;
      $('ruin-simulation').textContent='The curve is the exact probability, before any simulation.';
    });
    function play(){const {p,k,i}=params;let x=i,steps=0,path=[i];while(x>0&&x<k&&steps<20000){x+=Math.random()<p?1:-1;steps++;if(path.length<35)path.push(x);}return {x,steps,path,finished:x===0||x===k};}
    $('ruin-one').addEventListener('click',()=>{const r=play();$('ruin-simulation').textContent=`${r.path.join(' → ')}${r.steps>34?' → …':''}. ${r.finished?(r.x===params.k?'A reached k.':'A reached 0.'):'Still playing at the simulation limit.'} ${num(r.steps)} plays${r.steps>34?`; final simulated fortune ${r.x}`:''}.`;});
    $('ruin-many').addEventListener('click',()=>{let wins=0,losses=0,pending=0;for(let j=0;j<1000;j++){const r=play();if(!r.finished)pending++;else if(r.x===params.k)wins++;else losses++;}$('ruin-simulation').textContent=`1,000 games: ${wins} wins, ${losses} losses, ${pending} unfinished at 20,000 plays each. ${pending?`The win fraction is between ${pct(wins/1000)} and ${pct((wins+pending)/1000)}; unfinished games are not counted as losses.`:`Simulated win frequency: ${pct(wins/1000)}. Exact probability: ${ruinPct(params.p,params.i,params.k)}.`}`;});
  }
})();
