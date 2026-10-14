const assert=require('node:assert/strict'),M=require('../src/multi-math.js');let checks=0;
const near=(a,b,t=1e-11)=>{assert.ok(Math.abs(a-b)<t,`${a} != ${b}`);checks++;};
const r=M.moments([15,35,25,15,10]);near(r.mean,1.7);near(r.second,4.3);near(r.variance,1.41);assert.equal(M.moments([0,0]),null);
// Enumerate all independent Bernoulli patterns and compare the grouped PMF.
for(const n of [1,3,7])for(const p of [.05,.3,.5,1]){const counts=Array(n+1).fill(0);for(let mask=0;mask<2**n;mask++){let successes=0,weight=1;for(let i=0;i<n;i++){const yes=!!(mask&(1<<i));successes+=yes;weight*=yes?p:1-p;}counts[successes]+=weight;}const d=M.distribution('binomial',{n,p});d.values.forEach(v=>near(v.p,counts[v.x]));near(d.cdf(n),1);near(d.mean,M.sum(counts.map((v,i)=>v*i)));}
// Enumerate unordered samples from a finite labeled population.
for(const [N,K,n]of [[8,3,4],[5,0,3],[5,5,3],[8,3,8]]){const counts=Array(n+1).fill(0);function sample(start,left,k){if(!left){counts[k]++;return;}for(let i=start;i<=N-left;i++)sample(i+1,left-1,k+(i<K));}sample(0,n,0);const total=M.sum(counts),d=M.distribution('hypergeometric',{N,K,n});d.values.forEach(v=>near(v.p,counts[v.x]/total));near(d.cdf(n),1);near(d.mean,M.sum(counts.map((v,i)=>v*i))/total);}
for(const lambda of [.1,4,13.1,30]){const d=M.distribution('poisson',{lambda});near(M.sum(d.values.map(v=>v.p)),1);near(M.sum(d.values.map(v=>v.x*v.p)),lambda);near(d.cdf(0),Math.exp(-lambda));}
for(const p of [.05,1/6,.3,1]){const d=M.distribution('geometric',{p});for(const k of [0,1,5,10,500]){near(d.tail(k),(1-p)**k);near(d.cdf(k)+d.tail(k),1);}near(d.values[0].p,p);}
// A slice's normalized density integrates to1; derivative of x² is2x.
for(const x of [.05,.2,.6,.95]){const r=M.slices(x),h=1e-6;near(r.conditionalHeight*x,1);near(((x+h)**2-(x-h)**2)/(2*h),r.marginal,1e-8);}
console.log(`${checks} independent probability and numerical checks passed.`);
