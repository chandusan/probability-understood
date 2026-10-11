(function(root){
  'use strict';
  function ads(base=.05,after=.15){
    if([base,after].some(p=>!Number.isFinite(p)||p<0||p>1))throw new RangeError('Click probabilities must lie between zero and one');
    const pmf=[0,0,0,0],rows=[];
    for(let n=0;n<8;n++){
      const sequence=n.toString(2).padStart(3,'0').replaceAll('0','N').replaceAll('1','C');
      const factors=[...sequence].map((c,i)=>{const q=i&&sequence[i-1]==='C'?after:base;return c==='C'?q:1-q;});
      const x=[...sequence].filter(c=>c==='C').length,p=factors.reduce((a,b)=>a*b,1);pmf[x]+=p;rows.push({sequence,x,p,factors});
    }
    return {rows,pmf};
  }
  function stopTime(sequence){
    if(!/^[DIU]*$/.test(sequence))throw new RangeError('Use only D, I and U');
    for(let i=1;i<sequence.length;i++)if(sequence.slice(i-1,i+1)==='II'||(i>=2&&sequence.slice(i-2,i+1)==='UUU'))return i+1;
    return null;
  }
  function stopping(n){
    if(!Number.isInteger(n)||n<1||n>8)throw new RangeError('Choose a length from one to eight');
    const valid=[];let early=0,continuing=0;
    for(let j=0;j<3**n;j++){const s=j.toString(3).padStart(n,'0').replace(/[012]/g,c=>'DIU'[+c]),t=stopTime(s);if(t===n)valid.push(s);else if(t===null)continuing++;else early++;}
    return {valid,early,continuing,candidates:3**n};
  }
  function distribution(mode){
    if(mode==='table')return {values:[3,5,8,10],counts:[3,2,3,2],total:10,faces:null};
    const faces=mode==='nontraditional'?[[1,2,2,3,3,4],[1,3,4,5,6,8]]:[[1,2,3,4,5,6],[1,2,3,4,5,6]],map=new Map();
    for(const a of faces[0])for(const b of faces[1])map.set(a+b,(map.get(a+b)||0)+1);
    const values=[...map.keys()].sort((a,b)=>a-b);return {values,counts:values.map(x=>map.get(x)),total:36,faces};
  }
  function discreteAt(d,t){
    let below=0,at=0;d.values.forEach((x,i)=>{if(x<t)below+=d.counts[i];if(x===t)at+=d.counts[i];});
    return {below:below/d.total,at:at/d.total,cdf:(below+at)/d.total};
  }
  function distanceCDF(x){
    if(x<=0)return 0;if(x>=Math.SQRT2)return 1;
    if(x<=1)return Math.PI*x*x/4;
    const z=Math.sqrt(x*x-1);return z+x*x*(Math.PI/4-Math.atan(z));
  }
  function distancePDF(x){
    if(x<=0||x>=Math.SQRT2)return 0;
    return x<=1?Math.PI*x/2:Math.max(0,2*x*(Math.PI/4-Math.atan(Math.sqrt(x*x-1))));
  }
  function mixed(m,x){
    if(!Number.isFinite(m)||m<0||m>1)throw new RangeError('Point mass must lie between zero and one');
    const cdf=x<0?0:x>=2?1:m+(1-m)*x*x/4;
    const atom=x===0?m:0,left=cdf-atom;
    return {cdf,left,atom,atLeast:1-left,greater:1-cdf,density:x>0&&x<2?(1-m)*x/2:0};
  }
  const api={ads,stopTime,stopping,distribution,discreteAt,distanceCDF,distancePDF,mixed};
  root.RandomVariableMath=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window!=='undefined'?window:globalThis);
