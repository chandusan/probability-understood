/* Independent checks of the chapter's finite counts and geometric probabilities. */
const assert=require('node:assert/strict');
const M=require('../src/rv-math.js');
let checks=0;
function near(actual,expected,tolerance=1e-11){assert.ok(Math.abs(actual-expected)<=tolerance,`${actual} != ${expected}`);checks++;}
function equal(actual,expected){assert.deepEqual(actual,expected);checks++;}

// Exact millionths from the eight products in the original ad exercise.
equal(M.ads().pmf.map(p=>Math.round(p*1e6)),[857375,125875,15625,1125]);
const expectedPaths={NNN:857375,NNC:45125,NCN:40375,NCC:7125,CNN:40375,CNC:2125,CCN:6375,CCC:1125};
for(const row of M.ads().rows)equal(Math.round(row.p*1e6),expectedPaths[row.sequence]);
for(const p of [0,.05,.25,.5,.8,1]){
 const a=M.ads(p,p).pmf;[1,3,3,1].forEach((c,k)=>near(a[k],c*p**k*(1-p)**(3-k)));
 for(const q of [0,.15,.7,1])near(M.ads(p,q).pmf.reduce((a,b)=>a+b),1);
}

// Find trigger positions by substring search independently of the production scan.
const referenceStop=s=>{const positions=[s.indexOf('II'),s.indexOf('UUU')];return Math.min(positions[0]<0?Infinity:positions[0]+2,positions[1]<0?Infinity:positions[1]+3);};
equal(M.stopping(2).valid,['II']);
equal(M.stopping(3).valid,['DII','UII','UUU']);
equal(M.stopping(4).valid,['DDII','DUII','DUUU','IDII','IUII','IUUU','UDII','UUII']);
for(let n=2;n<=6;n++){
 let strings=[''];for(let i=0;i<n;i++)strings=strings.flatMap(s=>['D','I','U'].map(c=>s+c));
 const exact=strings.filter(s=>referenceStop(s)===n),v=M.stopping(n);
 equal(v.valid,exact);equal(v.valid.length+v.early+v.continuing,3**n);
 for(const s of strings)equal(M.stopTime(s),Number.isFinite(referenceStop(s))?referenceStop(s):null);
}

// Both physical dice models produce the same eleven masses, despite different faces.
for(const mode of ['standard','nontraditional']){
 const d=M.distribution(mode);equal(d.values,[2,3,4,5,6,7,8,9,10,11,12]);equal(d.counts,[1,2,3,4,5,6,5,4,3,2,1]);
 for(let t=0;t<=13;t+=.5){const v=M.discreteAt(d,t);near(v.cdf-v.below,v.at);near(v.cdf,d.values.reduce((p,x,i)=>p+(x<=t?d.counts[i]/36:0),0));}
}
const four=M.distribution('table');near(M.discreteAt(four,5).below,.3);near(M.discreteAt(four,5).at,.2);near(M.discreteAt(four,5).cdf,.5);

// Numerically integrate vertical slices of the circle-square intersection.
function squareArea(r){if(r<=0)return 0;const end=Math.min(1,r),n=100000,h=end/n;let sum=0;for(let j=0;j<n;j++){const u=(j+.5)*h;sum+=Math.min(1,Math.sqrt(Math.max(0,r*r-u*u)));}return sum*h;}
for(const r of [.1,.5,.99,1,1.001,1.1,1.25,1.4,Math.SQRT2,1.6])near(M.distanceCDF(r),squareArea(r),2e-8);
near(M.distanceCDF(-1),0);near(M.distanceCDF(1),Math.PI/4);near(M.distanceCDF(Math.SQRT2),1);
for(const r of [.1,.5,.9,1.01,1.1,1.3,1.4]){const h=1e-6;near((M.distanceCDF(r+h)-M.distanceCDF(r-h))/(2*h),M.distancePDF(r),2e-8);}
let integral=0;const h=Math.SQRT2/100000;for(let j=0;j<100000;j++)integral+=M.distancePDF((j+.5)*h)*h;near(integral,1,2e-7);
for(let i=0;i<1600;i++){const r=i/1000;assert.ok(M.distanceCDF(r)<=M.distanceCDF(r+.001)+1e-12);checks++;}

// CDF jumps and tail endpoint choices for a mixture of an atom and a density.
for(const m of [0,.1,.4,.75,1]){
 near(M.mixed(m,0).cdf,m);near(M.mixed(m,0).left,0);near(M.mixed(m,0).atLeast,1);near(M.mixed(m,0).greater,1-m);
 near(M.mixed(m,-.5).cdf,0);near(M.mixed(m,2).cdf,1);near(M.mixed(m,3).atLeast,0);
 for(const x of [.2,.5,1,1.8]){const a=M.mixed(m,x);near(a.cdf-a.left,0);near(a.atLeast,a.greater);const h=1e-6;near((M.mixed(m,x+h).cdf-M.mixed(m,x-h).cdf)/(2*h),a.density,1e-9);}
}
near(M.mixed(.4,1).atLeast,.45);near(M.mixed(.4,0).atom,.4);

// Remaining exercise answers: polynomial CDF, infinite PMF, lottery net gains.
near((2**2+2**3)/12,1);near((2**2+2**3)/12-(0**2+0**3)/12,1);
let mass=0;for(let x=1;x<=100;x++)mass+=(4/3)*x*(1/3)**x;near(mass,1);near(1-(4/3)*(1/3+2/9),7/27);
near((4987+10+2+1)/5000,1);equal([0,100,500,1000].map(prize=>prize-1),[-1,99,499,999]);
console.log(`Random Variables: ${checks} numerical, exhaustive-count and endpoint checks passed.`);
