(function(){
  var root=document.documentElement,tb=document.getElementById('theme');
  function cur(){var t=root.getAttribute('data-theme');if(t)return t;return window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light'}
  function label(){if(tb){var d=cur()==='dark';tb.setAttribute('aria-pressed',d?'true':'false');tb.setAttribute('aria-label',d?'Switch to light mode':'Switch to dark mode')}}
  if(tb){label();tb.addEventListener('click',function(){var n=cur()==='dark'?'light':'dark';root.setAttribute('data-theme',n);try{localStorage.setItem('theme',n)}catch(e){}label()})}
  // state search (homepage)
  var q=document.getElementById('q');if(!q)return;var em=document.getElementById('empty');
  q.addEventListener('input',function(){var v=q.value.toLowerCase(),n=0;[].forEach.call(document.querySelectorAll('#s li'),function(l){l.hidden=!l.dataset.n.includes(v);if(!l.hidden)n++});if(em)em.hidden=n>0});
})();
