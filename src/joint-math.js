(function(root){
  'use strict';
  function choose(n,k){
    if(!Number.isInteger(n)||!Number.isInteger(k)||n<0||k<0||k>n)return 0;
    k=Math.min(k,n-k);let value=1;for(let i=1;i<=k;i++)value=value*(n-i+1)/i;return Math.round(value);
  }
  const sum=values=>values.reduce((a,b)=>a+b,0);
  function summarize(counts){
    const xTotals=counts.map(sum),yTotals=counts[0].map((_,y)=>sum(counts.map(row=>row[y]))),total=sum(xTotals);
    return {counts,xTotals,yTotals,total,pmf:counts.map(row=>row.map(c=>c/total))};
  }
  function audit(){return summarize(Array.from({length:8},(_,x)=>Array.from({length:6},(_,y)=>choose(8,x)*choose(5,y)*choose(12,7-x-y))));}
  function dice(){return summarize(Array.from({length:6},(_,x)=>Array.from({length:6},(_,y)=>x+y<=5?choose(5,x)*choose(5-x,y)*4**(5-x-y):0)));}
  function conditional(distribution,target,given){
    if(!['x','y'].includes(target)||!Number.isInteger(given))throw new RangeError('Choose the target variable and an integer conditioning value.');
    const counts=target==='x'?distribution.counts.map(row=>row[given]):distribution.counts[given];
    if(!counts||counts.some(c=>c===undefined))throw new RangeError('The conditioning value is outside the support.');
    const total=sum(counts);if(total===0)throw new RangeError('The conditioning event must have positive probability.');
    return {counts:[...counts],total,probabilities:counts.map(c=>c/total)};
  }
  function eventCount(distribution,predicate){let count=0;distribution.counts.forEach((row,x)=>row.forEach((n,y)=>{if(predicate(x,y))count+=n;}));return count;}
  function churn(){return summarize([[5,25,40],[15,10,5]]);}
  function churnRisk(tier,comparison='baseline'){
    if(!Number.isInteger(tier)||tier<1||tier>3)throw new RangeError('Choose engagement tier 1, 2 or 3.');
    if(!['baseline','others'].includes(comparison))throw new RangeError('Choose the baseline or the other engagement tiers.');
    const d=churn(),index=tier-1,events=d.counts[1][index],group=d.yTotals[index],risk=events/group;
    const comparisonEvents=comparison==='baseline'?d.xTotals[1]:d.xTotals[1]-events;
    const comparisonGroup=comparison==='baseline'?d.total:d.total-group;
    const comparisonRisk=comparisonEvents/comparisonGroup;
    return {events,group,risk,comparisonEvents,comparisonGroup,comparisonRisk,ratio:risk/comparisonRisk};
  }
  function tier(){return {...summarize([[8,8,4],[4,8,8],[2,6,9]]),normalizer:16/57,unscaledTotal:57/16};}
  function posterior(breaches){
    const d=tier(),c=conditional(d,'x',breaches),max=Math.max(...c.counts),modes=c.counts.flatMap((n,i)=>n===max?[i+1]:[]);
    return {...c,modes,mean:sum(c.probabilities.map((p,i)=>(i+1)*p))};
  }
  const api={choose,sum,summarize,audit,dice,conditional,eventCount,churn,churnRisk,tier,posterior};
  root.JointMath=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
