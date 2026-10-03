(() => {
  const key='probability-understood:experiment:'+location.pathname;
  let state=null;try{state=JSON.parse(localStorage.getItem(key)||'null');}catch{}
  window.openai={widgetState:state,setWidgetState:async next=>{window.openai.widgetState=next;try{localStorage.setItem(key,JSON.stringify(next));}catch{}}};
  addEventListener('DOMContentLoaded',()=>{
    const root=document.querySelector('.lab-root');let last=0;
    const resize=()=>{const height=Math.ceil(root.getBoundingClientRect().height+parseFloat(getComputedStyle(document.body).paddingTop)+parseFloat(getComputedStyle(document.body).paddingBottom)+4);if(height!==last){last=height;parent.postMessage({type:'lesson-lab-height',height},'*');}};
    new ResizeObserver(resize).observe(root);addEventListener('load',resize);resize();
  });
})();
