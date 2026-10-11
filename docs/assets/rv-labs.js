(() => {
  'use strict';
  const M=window.RandomVariableMath,$=id=>document.getElementById(id),green='#1b7d6b',orange='#b7753f',gray='#b6c0b6',ink='#30423a';
  const num=x=>x.toLocaleString(undefined,{maximumFractionDigits:6});
  const pct=x=>x>0&&x<.000001?'<0.0001%':x<1&&x>.999999?'>99.9999%':(100*x).toLocaleString(undefined,{maximumFractionDigits:4})+'%';
  const card=(label,value)=>`<div class="card"><span>${label}</span><strong>${value}</strong></div>`;
  function bind(ids,render){
    const saved=window.openai?.widgetState;
    for(const name of ids){const el=$(name);if(!saved||saved[name]===undefined)continue;
      if(el.tagName==='SELECT'){if([...el.options].some(o=>o.value===saved[name]))el.value=saved[name];}
      else if(el.type==='text')el.value=String(saved[name]).slice(0,el.maxLength);
      else if(Number.isFinite(+saved[name]))el.value=saved[name];
    }
    const run=()=>{render();const next={};for(const name of ids)next[name]=$(name).value;window.openai?.setWidgetState(next);};
    for(const name of ids)$(name).addEventListener('input',run);run();
  }
  function coords(xmin,xmax,ymax=1){return {x:t=>48+468*(t-xmin)/(xmax-xmin),y:p=>242-206*p/ymax};}
  function axes(xmin,xmax,ymax=1,ticks=[]){
    const {x,y}=coords(xmin,xmax,ymax);
    return `<path d="M48 30 V242 H516" fill="none" stroke="${gray}"/>`+[0,ymax/2,ymax].map(v=>`<path d="M48 ${y(v)} H516" stroke="${gray}" opacity=".3"/><text x="41" y="${y(v)+4}" text-anchor="end" font-size="11" fill="${ink}">${num(v)}</text>`).join('')+ticks.map(v=>`<text x="${x(v)}" y="261" text-anchor="middle" font-size="11" fill="${ink}">${num(v)}</text>`).join('');
  }
  function curve(fn,xmin,xmax,ymax,ticks,t){
    const {x,y}=coords(xmin,xmax,ymax),points=Array.from({length:241},(_,i)=>{const v=xmin+(xmax-xmin)*i/240;return `${x(v)},${y(fn(v))}`;}).join(' ');
    return axes(xmin,xmax,ymax,ticks)+`<polyline points="${points}" fill="none" stroke="${green}" stroke-width="2.5"/><path d="M${x(t)} 30 V242" stroke="${orange}" stroke-dasharray="4 4"/><circle cx="${x(t)}" cy="${y(fn(t))}" r="4" fill="${orange}"/>`;
  }
  if(document.body.dataset.lab==='rv-ads')bind(['ad-base','ad-after','ad-count'],()=>{
    const base=+$('ad-base').value/100,after=+$('ad-after').value/100,v=M.ads(base,after),selected=$('ad-count').value;
    $('ad-base-out').textContent=pct(base);$('ad-after-out').textContent=pct(after);
    $('ad-paths').innerHTML=v.rows.map(r=>`<tr class="${selected!=='all'&&r.x===+selected?'rv-highlight':''}"><th>${r.sequence}</th><td>${r.x}</td><td>${r.factors.map(num).join(' × ')}</td><td>${pct(r.p)}</td></tr>`).join('');
    $('ad-results').innerHTML=v.pmf.map((p,x)=>card(`P(X = ${x})`,pct(p))).join('');
    $('ad-note').textContent=`The four masses add to ${num(v.pmf.reduce((a,b)=>a+b,0))}. ${base===0?'No first click can occur. After every nonclick the rate is also zero, so X = 0 with certainty. The after-click rate is never used; this is the degenerate Binomial(3, 0) distribution.':base===after?'Both click rates are equal, so the conditional probabilities no longer depend on the previous result. This becomes a binomial model with three trials.':'The next click probability depends on the previous result. Equal click counts need not have equal path probabilities, and a binomial formula with a single fixed click rate does not apply.'}`;
  });
  if(document.body.dataset.lab==='rv-stopping')bind(['stop-length','stop-sequence'],()=>{
    const n=+$('stop-length').value,v=M.stopping(n),s=$('stop-sequence').value.toUpperCase().replace(/\s/g,'');
    $('stop-length-out').textContent=n;
    $('stop-results').innerHTML=card(`First stop at N = ${n}`,`${v.valid.length} ${v.valid.length===1?'string':'strings'}`)+card('Would have stopped earlier',`${v.early} candidates`)+card('No trigger yet',`${v.continuing} candidates`);
    $('stop-strings').innerHTML=v.valid.map(s=>`<code>${s}</code>`).join('');
    if(!s||!/^[DIU]+$/.test(s)){$('stop-preview').textContent='';$('stop-check').textContent='Enter a sequence using D, I and U to check when the rule first fires.';return;}
    const t=M.stopTime(s),width=t===null?0:(s.slice(t-2,t)==='II'?2:3);
    $('stop-preview').innerHTML=[...s].map((c,i)=>`<span class="${t!==null&&i>=t?'after-stop':t!==null&&i>=t-width?'trigger':''}">${c}</span>`).join('');
    $('stop-check').textContent=t===null?`${s} has no stopping trigger. It is a continuing history, not a completed outcome.`:t<s.length?`The first trigger occurs at epoch ${t}. The completed outcome is ${s.slice(0,t)}. Later letters would never be evaluated under this stopping rule.`:`${s} is a valid completed outcome: the first trigger is at epoch ${t}, so N = ${t}.`;
  });
  if(document.body.dataset.lab==='rv-dice')bind(['dice-model','dice-threshold'],()=>{
    const mode=$('dice-model').value,t=+$('dice-threshold').value,d=M.distribution(mode),v=M.discreteAt(d,t),probs=d.counts.map(n=>n/d.total);
    $('dice-threshold-out').textContent=num(t);
    $('dice-description').textContent=d.faces?'Each die has six equally likely physical faces, and the dice are independent. The 36 face pairs are equally likely. Repeated labels still belong to distinct faces.':'The PMF is P(X = 3) = 0.3, P(X = 5) = 0.2, P(X = 8) = 0.3, P(X = 10) = 0.2.';
    $('dice-results').innerHTML=card('P(X < t) = F(t−)',pct(v.below))+card('P(X = t): jump size',pct(v.at))+card('P(X ≤ t) = F(t)',pct(v.cdf));
    let cumulative=0;
    $('dice-rows').innerHTML=d.values.map((x,i)=>{const before=cumulative;cumulative+=d.counts[i];return `<tr class="${x<=t?'rv-highlight':''}"><th>${x}</th><td>${d.counts[i]}/${d.total} = ${pct(probs[i])}</td><td>${before}/${d.total}</td><td>${cumulative}/${d.total}</td></tr>`;}).join('');
    const ymax=Math.max(.2,Math.max(...probs)*1.15),pm=coords(0,13,ymax),cf=coords(0,13);
    $('dice-pmf').innerHTML=axes(0,13,ymax,d.values)+d.values.map((x,i)=>`<rect x="${pm.x(x)-9}" y="${pm.y(probs[i])}" width="18" height="${242-pm.y(probs[i])}" fill="${x<=t?green:gray}"/>`).join('')+`<path d="M${pm.x(t)} 30 V242" stroke="${orange}" stroke-dasharray="4 4"/>`;
    let lastX=0,lastP=0,steps='';
    d.values.forEach((value,i)=>{const nextP=lastP+probs[i];steps+=`<path d="M${cf.x(lastX)} ${cf.y(lastP)} H${cf.x(value)}" stroke="${green}" stroke-width="2.5" fill="none"/><circle cx="${cf.x(value)}" cy="${cf.y(lastP)}" r="3.5" stroke="${green}" stroke-width="1.5" fill="white"/><circle cx="${cf.x(value)}" cy="${cf.y(nextP)}" r="3.5" fill="${green}"/>`;lastX=value;lastP=nextP;});
    steps+=`<path d="M${cf.x(lastX)} ${cf.y(1)} H${cf.x(13)}" stroke="${green}" stroke-width="2.5"/><path d="M${cf.x(t)} 30 V242" stroke="${orange}" stroke-dasharray="4 4"/><circle cx="${cf.x(t)}" cy="${cf.y(v.cdf)}" r="5" fill="${orange}"/>`;
    $('dice-cdf').innerHTML=axes(0,13,1,d.values)+steps;
    $('dice-grid').innerHTML=d.faces?`<table><caption>Physical face pairs: green cells satisfy X ≤ t.</caption><thead><tr><th>Die 1 / Die 2</th>${d.faces[1].map((b,j)=>`<th>Face ${j+1}: ${b}</th>`).join('')}</tr></thead><tbody>${d.faces[0].map((a,i)=>`<tr><th>Face ${i+1}: ${a}</th>${d.faces[1].map(b=>`<td class="${a+b<=t?'rv-highlight':''}">${a+b}</td>`).join('')}</tr>`).join('')}</tbody></table>`:'';
    $('dice-note').textContent=`The CDF includes the mass at the threshold: F(t) = F(t−) + P(X = t) = ${num(v.below)} + ${num(v.at)} = ${num(v.cdf)}. ${v.at>0?'Changing ≤ to < removes the highlighted threshold’s point mass.':'There is no mass exactly at this threshold, so < and ≤ give the same result here.'}`;
  });
  if(document.body.dataset.lab==='rv-distance')bind(['distance-r'],()=>{
    const r=+$('distance-r').value,F=M.distanceCDF(r),f=M.distancePDF(r);
    $('distance-r-out').textContent=num(r);
    $('distance-results').innerHTML=card('F(r) = P(X ≤ r)',pct(F))+card('Density f(r)',`${num(f)} per unit`)+card('P(X = r)', '0');
    const end=r<=Math.SQRT2?`<path d="M40 340 L${40+250*r/Math.SQRT2} ${340-250*r/Math.SQRT2}" stroke="${orange}" stroke-width="2"/>`:'';
    $('distance-square').innerHTML=`<defs><clipPath id="square-clip"><rect x="40" y="90" width="250" height="250"/></clipPath></defs><rect x="40" y="90" width="250" height="250" fill="#edf0e9"/><g clip-path="url(#square-clip)"><circle cx="40" cy="340" r="${250*r}" fill="#b5d8c5" stroke="${green}" stroke-width="2"/></g><rect x="40" y="90" width="250" height="250" fill="none" stroke="${ink}" stroke-width="2"/>${end}<circle cx="40" cy="340" r="4" fill="${ink}"/><g fill="${ink}" font-size="13"><text x="35" y="365">(0, 0)</text><text x="272" y="365">(1, 0)</text><text x="272" y="80">(1, 1)</text><text x="15" y="80">(0, 1)</text><text x="100" y="35">Area inside = ${num(F)}</text></g>`;
    $('distance-cdf').innerHTML=curve(M.distanceCDF,0,1.6,1,[0,.5,1,1.5],r);
    $('distance-pdf').innerHTML=curve(M.distancePDF,0,1.6,1.8,[0,.5,1,1.5],r);
    $('distance-note').textContent=r<=1?'For 0 ≤ r ≤ 1, a full quarter-circle fits in the square: F(r) = πr²/4. The density f(r) = πr/2 measures the rate at which area grows. The circle boundary itself has area zero.':r<Math.SQRT2?'For 1 < r < √2, parts of the quarter-circle lie outside the square. The CDF counts only the intersection. F(r) = √(r² − 1) + r²[π/4 − arctan(√(r² − 1))]. The remaining arc gets shorter as the circle approaches the far corner.':'For r ≥ √2, every point of the square is included. F(r) = 1 and the density is zero beyond this maximum distance. Including one exact boundary distance still adds no probability.';
  });
  if(document.body.dataset.lab==='rv-mixed')bind(['mixed-mass','mixed-threshold'],()=>{
    const m=+$('mixed-mass').value/100,t=+$('mixed-threshold').value,v=M.mixed(m,t),c=coords(-.25,2.5);
    $('mixed-mass-out').textContent=pct(m);$('mixed-threshold-out').textContent=`${num(t)} ($${num(100*t)})`;
    $('mixed-results').innerHTML=card('P(X = t)',pct(v.atom))+card('P(X ≥ t) = 1 − F(t−)',pct(v.atLeast))+card('P(X > t) = 1 − F(t)',pct(v.greater));
    const points=Array.from({length:201},(_,i)=>{const x=i/100;return `${c.x(x)},${c.y(M.mixed(m,x).cdf)}`;}).join(' ');
    $('mixed-cdf').innerHTML=axes(-.25,2.5,1,[0,.5,1,1.5,2,2.5])+`<path d="M${c.x(-.25)} ${c.y(0)} H${c.x(0)}" stroke="${green}" stroke-width="2.5"/><polyline points="${points}" fill="none" stroke="${green}" stroke-width="2.5"/><path d="M${c.x(2)} ${c.y(1)} H${c.x(2.5)}" stroke="${green}" stroke-width="2.5"/><circle cx="${c.x(0)}" cy="${c.y(0)}" r="4" fill="white" stroke="${green}" stroke-width="2"/><circle cx="${c.x(0)}" cy="${c.y(m)}" r="4" fill="${green}"/><path d="M${c.x(t)} 30 V242" stroke="${orange}" stroke-dasharray="4 4"/><circle cx="${c.x(t)}" cy="${c.y(v.cdf)}" r="4" fill="${orange}"/>`;
    const y2=c.y(1-m);
    $('mixed-pdf').innerHTML=axes(-.25,2.5,1,[0,.5,1,1.5,2,2.5])+`<path d="M${c.x(0)} 242 L${c.x(2)} ${y2} V242 Z" fill="#b5d8c5"/><path d="M${c.x(0)} 242 L${c.x(2)} ${y2}" fill="none" stroke="${green}" stroke-width="2.5"/><text x="90" y="45" font-size="13" fill="${ink}">Continuous area = ${num(1-m)}</text>`;
    $('mixed-note').textContent=`Separate point mass: P(X = 0) = ${pct(m)}. Continuous area: ${pct(1-m)}. ${t===0?'At zero, ≥ includes the atom while > excludes it.':`There is no atom at ${num(t)}, so ≥ and > give the same probability.`} ${m===1?'All users spend zero under this setting; conditioning on being a paying user is undefined.':'The density for paying users integrates to one after conditioning; the density contribution for all users integrates to 1 − m.'}`;
  });
})();
