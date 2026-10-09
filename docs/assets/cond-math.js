(function(root){
  'use strict';
  const ratio=(a,b)=>b>0?a/b:null;
  function regions(a,b,j){
    if([a,b,j].some(x=>!Number.isFinite(x))||a<0||a>1||b<0||b>1||j<Math.max(0,a+b-1)-1e-12||j>Math.min(a,b)+1e-12)throw new RangeError('Inconsistent event probabilities');
    return [j,a-j,b-j,Math.max(0,1-a-b+j)];
  }
  function bayes(prior,sensitivity,falsePositive){
    const yes=prior*sensitivity,no=(1-prior)*falsePositive;
    return {yes,no,evidence:yes+no,posterior:ratio(yes,yes+no)};
  }
  function allRed(red,total,draws){
    if(!Number.isInteger(draws)||draws<0||draws>total)throw new RangeError('Invalid draw count');
    if(draws>red)return 0;
    let p=1;for(let j=0;j<draws;j++)p*=(red-j)/(total-j);return p;
  }
  function urns(a,b,total,t,prior=.5){
    const la=allRed(a,total,t),lb=allRed(b,total,t),evidence=prior*la+(1-prior)*lb;
    const posterior=ratio(prior*la,evidence);
    const next=posterior===null||t===total?null:posterior*Math.max(0,a-t)/(total-t)+(1-posterior)*Math.max(0,b-t)/(total-t);
    return {la,lb,evidence,posterior,next};
  }
  function ruin(p,i,k){
    if(!Number.isInteger(k)||k<1||!Number.isInteger(i)||i<0||i>k||p<0||p>1)throw new RangeError('Invalid game parameters');
    if(i===0)return 0;if(i===k)return 1;
    if(p===0)return 0;if(p===1)return 1;if(p===.5)return i/k;
    const logR=Math.log1p(-p)-Math.log(p),shift=Math.max(0,(k-1)*logR);
    let numerator=0,denominator=0;
    for(let j=0;j<k;j++){const w=Math.exp(j*logR-shift);denominator+=w;if(j<i)numerator+=w;}
    return numerator/denominator;
  }
  function coins(){return Array.from({length:16},(_,n)=>{const s=n.toString(2).padStart(4,'0').replaceAll('0','H').replaceAll('1','T');return {s,a:s[0]===s[1],b:[...s].filter(x=>x==='H').length%2===1,c:s[2]===s[3]};});}
  const api={ratio,regions,bayes,allRed,urns,ruin,coins};
  root.ConditionalMath=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
