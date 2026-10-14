/* Probability calculations shared by the lessons 08–10 explorers. */
(function(root){
'use strict';
const sum=a=>a.reduce((s,v)=>s+v,0);
function choose(n,k){if(k<0||k>n||!Number.isInteger(k))return 0;k=Math.min(k,n-k);let v=1;for(let i=1;i<=k;i++)v=v*(n-k+i)/i;return v;}
function moments(weights){const total=sum(weights);if(!(total>0))return null;const p=weights.map(v=>v/total),mean=sum(p.map((v,x)=>x*v)),variance=sum(p.map((v,x)=>v*(x-mean)**2));return{p,mean,variance,second:sum(p.map((v,x)=>v*x*x))};}
function distribution(kind,{n=20,p=.3,lambda=4,N=30,K=10}={}){
 let start=0,end=n,mean,variance,pmf,tail;
 if(kind==='binomial'){mean=n*p;variance=n*p*(1-p);pmf=x=>choose(n,x)*p**x*(1-p)**(n-x);}
 else if(kind==='poisson'){mean=variance=lambda;end=Math.ceil(lambda+10*Math.sqrt(lambda)+12);pmf=x=>{let v=Math.exp(-lambda);for(let i=1;i<=x;i++)v*=lambda/i;return v;};}
 else if(kind==='geometric'){start=1;mean=1/p;variance=(1-p)/p**2;end=Math.ceil(Math.log(1e-10)/Math.log(1-p));if(p===1)end=1;pmf=x=>p*(1-p)**(x-1);tail=k=>(1-p)**Math.max(0,Math.floor(k));}
 else if(kind==='hypergeometric'){start=Math.max(0,n-(N-K));end=Math.min(n,K);mean=n*K/N;variance=n*(K/N)*(1-K/N)*(N-n)/(N-1);pmf=x=>choose(K,x)*choose(N-K,n-x)/choose(N,n);}
 else throw Error('Unknown distribution');
 const values=Array.from({length:end-start+1},(_,i)=>({x:i+start,p:pmf(i+start)}));
 const cdf=k=>kind==='geometric'?(k<1?0:1-tail(k)):sum(values.filter(v=>v.x<=k).map(v=>v.p));
 return{values,mean,variance,cdf,tail:k=>kind==='geometric'?tail(k):Math.max(0,1-cdf(k))};
}
const api={sum,choose,moments,distribution,slices:x=>({marginal:2*x,cdf:x*x,conditionalHeight:1/x})};
if(typeof module==='object'&&module.exports)module.exports=api;else root.MultiMath=api;
})(typeof globalThis!=='undefined'?globalThis:this);
