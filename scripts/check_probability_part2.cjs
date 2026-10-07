/* Mathematical invariants and independently enumerated small sample spaces. */
const assert=require('node:assert/strict');
const M=require('../src/rules-math.js');
const close=(actual,expected,tol=1e-12)=>assert.ok(Math.abs(actual-expected)<tol,`${actual} != ${expected}`);
for(let n=1;n<=12;n++)for(let m=1;m<=30;m++){
  const p=M.occupancy(m,n);close(p.reduce((a,b)=>a+b,0),1);
  close(p.reduce((a,b,k)=>a+k*b,0),m/n);
  assert.ok(p.every(x=>x>=0&&x<=1));
}
assert.equal(M.chooseBig(49,6),13983816n);
assert.equal(M.chooseBig(52,13),635013559600n);
close(M.birthday(23),0.5072972343239854);
assert.ok(M.birthday(22)<.5&&M.birthday(23)>.5);
assert.equal(M.birthday(366),1);assert.equal(M.birthday(1),0);
assert.equal(M.multiset([3,2,1]),60n);
// Enumerate all small dice sequences, independently of inclusion–exclusion.
for(let s=2;s<=4;s++)for(let m=1;m<=6;m++){
  let count=0n;
  for(let code=0;code<s**m;code++){
    let x=code,mask=0;for(let i=0;i<m;i++){mask|=1<<(x%s);x=Math.floor(x/s);}
    if(mask===(1<<s)-1)count++;
  }
  assert.equal(M.coverageCount(m,s),count);
}
assert.equal(M.coverageCount(10,6),16435440n);
// Enumerate permutations and compare both full and partial avoidance.
function permutations(a){if(!a.length)return[[]];return a.flatMap((x,i)=>permutations(a.filter((_,j)=>j!==i)).map(p=>[x,...p]));}
for(let n=1;n<=7;n++){
  const ps=permutations(Array.from({length:n},(_,i)=>i));
  for(let m=0;m<=n;m++){
    const actual=BigInt(ps.filter(p=>p.slice(0,m).every((x,i)=>x!==i)).length);
    assert.equal(M.subsetAvoidCount(n,m),actual);
  }
  assert.equal(M.subsetAvoidCount(n,n),M.derangement(n));
}
const b=M.bridge(5);
assert.equal(b.a,79181063676);assert.equal(b.both,4306559400);
assert.equal(b.union,154055567952);
assert.equal(b.union,2*M.choose(13,5)*M.choose(39,8)-M.choose(13,5)**2*M.choose(26,3));
const atLeast=M.bridge(5,true);assert.ok(atLeast.union>b.union);
close(atLeast.union/atLeast.denominator,0.3433140909424518);
assert.equal(M.bridge(7).both,0);
assert.equal(M.bridge(1,true).union,M.choose(52,13)-M.choose(26,13));
for(let k=1;k<=10;k++)for(const minimum of [false,true]){
  const r=M.bridge(k,minimum);assert.ok(r.both<=r.a&&r.union>=r.a&&r.union<=r.denominator);
  assert.equal(r.joint.flat().reduce((a,b)=>a+b,0),r.denominator);
}
console.log('Passed: normalized distributions, birthday threshold, multiset counts, exhaustive small dice/permutation spaces, and bridge identities.');
