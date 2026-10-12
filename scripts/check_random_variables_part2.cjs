/* Independent enumeration and exact-count checks for the PDF 07 interactives. */
const assert=require('node:assert/strict');
const M=require('../src/joint-math.js');
let checks=0;
function equal(actual,expected){assert.deepEqual(actual,expected);checks++;}
function near(actual,expected,tolerance=1e-12){assert.ok(Math.abs(actual-expected)<=tolerance,`${actual} != ${expected}`);checks++;}

// Enumerate every unordered seven-image subset by its distinct image identities.
// Images 0–7 have minor errors, 8–12 are garbage, and 13–24 are perfect.
const auditReference=Array.from({length:8},()=>Array(6).fill(0));
let sampleCount=0;
function enumerateImages(start,remaining,x,y){
  if(remaining===0){auditReference[x][y]++;sampleCount++;return;}
  for(let id=start;id<=25-remaining;id++)enumerateImages(id+1,remaining-1,x+(id<8),y+(id>=8&&id<13));
}
enumerateImages(0,7,0,0);
const audit=M.audit();
equal(audit.counts,auditReference);equal(sampleCount,480700);equal(audit.total,sampleCount);
equal(audit.counts[2][1],69300);equal(audit.counts[7][0],8);
equal(audit.counts[7][1],0);equal(audit.counts[6][2],0);
near(audit.counts[7][0]/audit.total,8/480700);
equal(M.eventCount(audit,(_x,y)=>y>=1),sampleCount-audit.yTotals[0]);
equal(M.eventCount(audit,(_x,y)=>y===0),77520);
equal(M.eventCount(audit,(x,y)=>x+y<=2),auditReference.reduce((a,row,x)=>a+row.reduce((b,n,y)=>b+(x+y<=2?n:0),0),0));

// Enumerate all 6^5 ordered die-face sequences without using the count formula.
const diceReference=Array.from({length:6},()=>Array(6).fill(0));
let more=0,tied=0;
for(let code=0;code<7776;code++){
  let n=code,x=0,y=0;
  for(let roll=0;roll<5;roll++){const face=n%6+1;n=Math.floor(n/6);if(face===6)x++;if(face===5)y++;}
  diceReference[x][y]++;if(x>y)more++;if(x===y)tied++;
}
const dice=M.dice();equal(dice.counts,diceReference);equal(dice.total,7776);
equal(more,2676);equal(tied,2424);equal(M.eventCount(dice,(x,y)=>x>y),more);near(more/7776,(1-tied/7776)/2);
equal(dice.xTotals,[3125,3125,1250,250,25,1]);equal(dice.yTotals,dice.xTotals);
equal(dice.counts[1][1],1280);equal(dice.counts[5][0],1);

// Each conditional law sums to one and matches a fresh restriction of the enumeration.
for(const distribution of [audit,dice,M.churn(),M.tier()]){
  near(M.sum(distribution.pmf.flat()),1);
  equal(M.sum(distribution.xTotals),distribution.total);equal(M.sum(distribution.yTotals),distribution.total);
  for(const target of ['x','y']){
    const length=target==='x'?distribution.yTotals.length:distribution.xTotals.length;
    for(let given=0;given<length;given++){
      const c=M.conditional(distribution,target,given);near(M.sum(c.probabilities),1);
      equal(c.total,target==='x'?distribution.yTotals[given]:distribution.xTotals[given]);
      for(let value=0;value<c.counts.length;value++){
        const original=target==='x'?distribution.counts[value][given]:distribution.counts[given][value];
        equal(c.counts[value],original);near(c.probabilities[value],original/c.total);
      }
    }
  }
}
// Derive conditional dice counts by explicitly enumerating the five equally likely
// non-five labels in the remaining positions (success = six).
for(let y=0;y<=5;y++){
  const remaining=5-y,counts=Array(6).fill(0);
  for(let code=0;code<5**remaining;code++){let n=code,x=0;for(let r=0;r<remaining;r++){if(n%5===4)x++;n=Math.floor(n/5);}counts[x]++;}
  const c=M.conditional(dice,'x',y),reverse=M.conditional(dice,'y',y);
  counts.forEach((n,x)=>{near(c.probabilities[x],n/5**remaining);near(reverse.probabilities[x],n/5**remaining);});
}
equal(M.conditional(dice,'x',5).probabilities,[1,0,0,0,0,0]);
near(M.conditional(dice,'x',2).probabilities[1],48/125);

// Frequency interpretation and the distinction between overall baseline and
// an explicitly disjoint comparison group.
const churn=M.churn();equal(churn.xTotals,[70,30]);equal(churn.yTotals,[20,35,45]);
near(M.churnRisk(1).risk,3/4);near(M.churnRisk(1).ratio,5/2);
near(M.churnRisk(1,'others').comparisonRisk,3/16);near(M.churnRisk(1,'others').ratio,4);
near(M.churnRisk(2).risk,2/7);near(M.churnRisk(3).risk,1/9);
near(M.churnRisk(2).ratio,20/21);near(M.churnRisk(3).ratio,10/27);
for(let tier=1;tier<=3;tier++)for(const comparison of ['baseline','others']){const risk=M.churnRisk(tier,comparison);near(risk.ratio,risk.risk/risk.comparisonRisk);}

// Independently evaluate the source weight formula, including 0! = 1.
const weights=[1,2,3].map(x=>[0,1,2].map(y=>x**y/[1,1,2][y]*2**(-x)));
const weightTotal=weights.flat().reduce((a,b)=>a+b,0),tier=M.tier();near(weightTotal,57/16);near(tier.normalizer,1/weightTotal);
for(let x=0;x<3;x++)for(let y=0;y<3;y++)near(tier.pmf[x][y],weights[x][y]/weightTotal);
equal(tier.xTotals,[20,20,17]);equal(tier.yTotals,[14,22,21]);
equal(M.posterior(0).modes,[1]);equal(M.posterior(1).modes,[1,2]);equal(M.posterior(2).modes,[3]);
equal(M.posterior(2).counts,[4,8,9]);near(M.posterior(2).mean,47/21);near(M.posterior(2).probabilities[2],3/7);
for(const y of [0,1,2])near(M.sum(M.posterior(y).probabilities),1);
assert.throws(()=>M.conditional(dice,'x',6),RangeError);checks++;
assert.throws(()=>M.conditional(M.summarize([[1,0],[0,0]]),'x',1),RangeError);checks++;
console.log(`Random Variables Part 2: ${checks} checks passed; all 480,700 image samples and 7,776 die sequences independently enumerated.`);
