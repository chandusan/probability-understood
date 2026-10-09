// Verify the learning examples with finite counts and an independent linear solver.
const assert=require('node:assert/strict');
const M=require('../src/cond-math.js');
let checks=0;
function close(actual,expected,label){assert.ok(Math.abs(actual-expected)<1e-10,`${label}: ${actual} versus ${expected}`);checks++;}
const region=M.regions(.45,.60,.25);
close(region[3]/(1-region[0]),4/15,'subscription conditional');
for(let a=0;a<=10;a++)for(let b=0;b<=10;b++){
  const lo=Math.max(0,a+b-10),hi=Math.min(a,b);
  for(let j=lo;j<=hi;j++){const r=M.regions(a/10,b/10,j/10);close(r.reduce((s,x)=>s+x,0),1,'region total');assert.ok(r.every(x=>x>=-1e-12));}
}
assert.equal(M.ratio(0,0),null);
assert.throws(()=>M.regions(.2,.3,.5),RangeError);
const coin=M.coins();assert.equal(new Set(coin.map(r=>r.s)).size,16);
for(const key of ['a','b','c'])assert.equal(coin.filter(r=>r[key]).length,8);
for(const [a,b] of [['a','b'],['a','c'],['b','c']])assert.equal(coin.filter(r=>r[a]&&r[b]).length,4);
assert.equal(coin.filter(r=>r.a&&r.b&&r.c).length,0);
const test=M.bayes(.001,.96,.02);
close(test.yes*100000,96,'true positive count');close(test.no*100000,1998,'false positive count');close(test.posterior,16/349,'positive test posterior');
assert.equal(M.bayes(0,1,0).posterior,null);
function orderedRedCounts(red,total){let two=0,three=0;for(let a=0;a<total;a++)for(let b=0;b<total;b++)if(a!==b){if(a<red&&b<red)two++;for(let c=0;c<total;c++)if(c!==a&&c!==b&&a<red&&b<red&&c<red)three++;}return {two,three};}
const a=orderedRedCounts(12,20),b=orderedRedCounts(4,20),urn=M.urns(12,4,20,2);
assert.equal(a.two,132);assert.equal(b.two,12);
close(urn.posterior,a.two/(a.two+b.two),'urn posterior from counted pairs');
close(urn.next,(a.three+b.three)/(18*(a.two+b.two)),'prediction from counted triples');
close(urn.next,14/27,'predictive fraction');
assert.equal(M.urns(1,2,20,3).posterior,null);
assert.equal(M.urns(5,1,20,2).posterior,1);
close(M.urns(12,4,20,0).next,.4,'no evidence prediction');
function solveAbsorbingSystem(p,k){
  const n=k-1,A=Array.from({length:n},()=>Array(n+1).fill(0));
  for(let row=0;row<n;row++){A[row][row]=1;if(row>0)A[row][row-1]=-(1-p);if(row<n-1)A[row][row+1]=-p;else A[row][n]=p;}
  for(let c=0;c<n;c++){
    let pivot=c;for(let r=c+1;r<n;r++)if(Math.abs(A[r][c])>Math.abs(A[pivot][c]))pivot=r;
    [A[c],A[pivot]]=[A[pivot],A[c]];const d=A[c][c];for(let j=c;j<=n;j++)A[c][j]/=d;
    for(let r=0;r<n;r++)if(r!==c){const m=A[r][c];for(let j=c;j<=n;j++)A[r][j]-=m*A[c][j];}
  }
  return [0,...A.map(row=>row[n]),1];
}
for(const p of [.01,.2,.49,.5,.51,.75,.99])for(const k of [2,5,20,40]){
  const expected=solveAbsorbingSystem(p,k);for(let i=0;i<=k;i++)close(M.ruin(p,i,k),expected[i],'ruin vs independent system');
}
assert.equal(M.ruin(0,3,10),0);assert.equal(M.ruin(1,3,10),1);
close(.86*.9+.14*.2,.802,'soccer total');close(.86*.9/.802,387/401,'soccer posterior');
close(.95*.08/(.95*.08+.05*.85),152/237,'legitimate given flag');
close(.05*.85*.95/(.05*.85*.95+.95*.08*.1),1615/1919,'fraud given both signals');
console.log(`Probability Part 3: ${checks} numerical checks plus exhaustive outcome and endpoint checks passed.`);
