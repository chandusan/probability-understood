(() => {
  const current=Number(document.body.dataset.slide), count=Number(document.body.dataset.slideCount)||31;
  const key=`probability-understood:${document.body.dataset.chapter||'data-summary'}:v1`;
  const getProgress=()=>{try{const p=JSON.parse(localStorage.getItem(key)||'{}');return {completed:Array.isArray(p.completed)?p.completed.filter(n=>Number.isInteger(n)&&n>=1&&n<=count):[],last:Number.isInteger(p.last)&&p.last>=1&&p.last<=count?p.last:1};}catch{return {completed:[],last:1};}};
  let progress=getProgress();
  const save=()=>{try{localStorage.setItem(key,JSON.stringify(progress));}catch{}};
  const drawProgress=()=>{
    const n=new Set(progress.completed).size;
    document.querySelectorAll('[data-completed-count]').forEach(el=>el.textContent=n);
    document.querySelector('[data-course-progress]').style.width=`${n/count*100}%`;
    document.querySelectorAll('.slide-link').forEach(a=>a.classList.toggle('done',progress.completed.includes(Number(a.dataset.slide))));
    const button=document.querySelector('[data-complete]'),done=progress.completed.includes(current);
    button.setAttribute('aria-pressed',String(done));button.textContent=done?'✓ Marked as understood':'Mark this slide as understood';
  };
  const resume=document.querySelector('[data-resume]');
  if(progress.last!==current){resume.href=document.body.dataset.slidePrefix+String(progress.last).padStart(2,'0')+'.html';resume.textContent=`Return to slide ${String(progress.last).padStart(2,'0')} →`;resume.hidden=false;}
  progress.last=current;save();drawProgress();
  document.querySelector('[data-complete]').addEventListener('click',()=>{progress.completed=progress.completed.includes(current)?progress.completed.filter(n=>n!==current):[...progress.completed,current];save();drawProgress();});
  const nav=document.querySelector('.slide-nav'),active=nav.querySelector('[aria-current=page]');
  if(active)nav.scrollTop=Math.max(0,active.offsetTop-nav.offsetTop-nav.clientHeight/2);
  const search=document.querySelector('.nav-search');
  search.addEventListener('input',()=>{const q=search.value.toLowerCase().trim();let visible=0;document.querySelectorAll('.nav-group').forEach(group=>{let count=0;group.querySelectorAll('.slide-link').forEach(a=>{a.hidden=!a.dataset.search.includes(q);if(!a.hidden)count++;});group.hidden=count===0;visible+=count;});document.querySelector('.no-results').hidden=visible>0;});
  const menuButton=document.querySelector('.menu-button'),sidebar=document.querySelector('.sidebar'),mobile=matchMedia('(max-width:740px)');
  function menu(open){document.body.classList.toggle('nav-open',open);menuButton.setAttribute('aria-expanded',String(open));sidebar.inert=mobile.matches&&!open;if(open)search.focus();else if(mobile.matches)menuButton.focus();}
  sidebar.inert=mobile.matches;
  mobile.addEventListener('change',()=>{sidebar.inert=mobile.matches&&!document.body.classList.contains('nav-open');});
  menuButton.addEventListener('click',()=>menu(!document.body.classList.contains('nav-open')));
  document.querySelectorAll('[data-close-nav]').forEach(b=>b.addEventListener('click',()=>menu(false)));
  document.addEventListener('keydown',e=>{if(e.key==='Escape'&&document.body.classList.contains('nav-open'))menu(false);if(e.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){e.preventDefault();if(mobile.matches)menu(true);else search.focus();}});
  const dialog=document.querySelector('.image-dialog');
  document.querySelectorAll('[data-zoom-slide]').forEach(b=>b.addEventListener('click',()=>dialog.showModal()));
  dialog.querySelector('[data-close-dialog]').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
  const savedDetails=new Map();
  window.addEventListener('beforeprint',()=>{document.querySelectorAll('details').forEach(d=>{savedDetails.set(d,d.open);d.open=true;});});
  window.addEventListener('afterprint',()=>{savedDetails.forEach((open,d)=>d.open=open);savedDetails.clear();});
  document.querySelector('[data-print]').addEventListener('click',()=>window.print());
  window.addEventListener('message',e=>{if(!e.data||e.data.type!=='lesson-lab-height')return;document.querySelectorAll('.experiment iframe').forEach(f=>{if(f.contentWindow===e.source){const h=Number(e.data.height);if(Number.isFinite(h))f.style.height=`${Math.max(180,Math.min(2400,h))}px`;}});});
  if(window.renderMathInElement){renderMathInElement(document.querySelector('.lesson'),{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false},{left:'\\(',right:'\\)',display:false},{left:'\\[',right:'\\]',display:true}],throwOnError:false,strict:'ignore',ignoredClasses:['no-math'],ignoredTags:['script','noscript','style','textarea','pre','code']});}
  const tocLinks=[...document.querySelectorAll('.page-toc a[href^="#"]')].filter(a=>a.hash!=='#lesson');
  function updateReading(){const max=document.documentElement.scrollHeight-innerHeight;document.querySelector('[data-reading-progress]').style.width=`${max>0?Math.min(100,scrollY/max*100):100}%`;let selected=null;for(const link of tocLinks){const el=document.getElementById(decodeURIComponent(link.hash.slice(1)));if(el&&el.getBoundingClientRect().top<160)selected=link;}tocLinks.forEach(a=>a.classList.toggle('active',a===selected));}
  addEventListener('scroll',updateReading,{passive:true});addEventListener('resize',updateReading);new ResizeObserver(updateReading).observe(document.querySelector('.lesson'));updateReading();
})();
