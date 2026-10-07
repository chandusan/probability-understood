/* Exact counting and stable probability calculations for Probability Part 2. */
(function(root,factory){const math=factory();if(typeof module==='object'&&module.exports)module.exports=math;else root.RulesMath=math;})(typeof window==='undefined'?globalThis:window,()=>{
  const factorial=n=>{let v=1n;for(let i=2;i<=n;i++)v*=BigInt(i);return v;};
  const chooseBig=(n,k)=>{if(k<0||k>n)return 0n;k=Math.min(k,n-k);let v=1n;for(let i=1;i<=k;i++)v=v*BigInt(n-k+i)/BigInt(i);return v;};
  const choose=(n,k)=>Number(chooseBig(n,k));
  function occupancy(m,n){if(n===1)return Array.from({length:m+1},(_,k)=>k===m?1:0);const p=1/n;return Array.from({length:m+1},(_,k)=>choose(m,k)*p**k*(1-p)**(m-k));}
  function birthday(n,days=365){if(n<=1)return 0;if(n>days)return 1;let log=0;for(let k=1;k<n;k++)log+=Math.log1p(-k/days);return -Math.expm1(log);}
  function coverageCount(m,s){let count=0n;for(let j=0;j<=s;j++)count+=(j%2?-1n:1n)*chooseBig(s,j)*BigInt(s-j)**BigInt(m);return count;}
  function derangement(n){let a=1n,b=0n;if(n===0)return a;for(let i=2;i<=n;i++){const c=BigInt(i-1)*(a+b);a=b;b=c;}return b;}
  function subsetAvoidCount(n,m){let total=0n;for(let k=0;k<=m;k++)total+=(k%2?-1n:1n)*chooseBig(m,k)*factorial(n-k);return total;}
  function multiset(counts){return factorial(counts.reduce((a,b)=>a+b,0))/counts.reduce((a,b)=>a*factorial(b),1n);}
  function bridge(k,atLeast=false){const denominator=choose(52,13);let a=0,both=0;const joint=[];for(let s=0;s<=13;s++){joint[s]=[];for(let h=0;h<=13;h++){const ways=choose(13,s)*choose(13,h)*choose(26,13-s-h);joint[s][h]=ways;if((atLeast?s>=k:s===k))a+=ways;if((atLeast?s>=k:s===k)&&(atLeast?h>=k:h===k))both+=ways;}}return{denominator,a,both,union:2*a-both,joint};}
  return{factorial,chooseBig,choose,occupancy,birthday,coverageCount,derangement,subsetAvoidCount,multiset,bridge};
});
