(() => {
  const root=document.querySelector('.profile-report');
  if(!root)return;
  const labels=JSON.parse(root.dataset.profileLabels||'{}');
  const word=(key,values={})=>(labels[key]||key).replace(/\{(\w+)\}/g,(match,key)=>key in values?values[key]:match);
  const query=root.querySelector('.profile-query'),state=root.querySelector('.profile-filter-state');
  if(!query||!state)return;
  const sections=[...root.querySelectorAll('.profile-section')],links=[...root.querySelectorAll('.profile-index a')];
  const items=sections.map(section=>{
    const records=[...section.querySelectorAll('.rec,.msg-row,.svc-row,.message')];
    const rows=records.length?records:[...section.querySelectorAll('tbody tr')];
    return {section,rows,text:rows.map(row=>row.textContent.toLocaleLowerCase()),open:section.open,
      counted:['chapter-journal','chapter-directory','chapter-profiles','chapter-histories'].includes(section.id),
      badge:section.querySelector(':scope > summary .profile-count'),link:links.find(a=>a.hash==='#'+section.id)};
  });
  let chat='',chatTitle='',timer,printing=false;
  const total=items.reduce((sum,item)=>sum+item.rows.length,0);
  const format=new Intl.NumberFormat(document.documentElement.lang);
  function apply(){
    if(printing)return;
    const term=query.value.trim().toLocaleLowerCase();let shown=0;
    for(const item of items){
      let count=0;
      const scoped=chat&&item.section.id==='chapter-journal';
      item.rows.forEach((row,index)=>{
        row.hidden=!!((term&&!item.text[index].includes(term))||(scoped&&row.dataset.chat!==chat));
        if(!row.hidden)count++;
      });
      shown+=count;
      const filtered=!!term||!!scoped;
      item.section.hidden=!!(filtered&&item.rows.length&&!count);
      item.section.querySelectorAll('.day,.gap-row').forEach(row=>{row.hidden=filtered;});
      if(filtered&&count)item.section.open=true;
      if(!filtered)item.section.open=item.open;
      const badge=item.badge,navBadge=item.link?.querySelector('b');
      for(const node of [badge,navBadge])if(node){node.hidden=!item.rows.length||!item.counted;node.textContent=format.format(count);}
      if(item.link)item.link.hidden=item.section.hidden;
    }
    state.hidden=!term&&!chat;
    state.querySelector('.profile-scope').textContent=chat?word('Messages from {chat}',{chat:chatTitle}):word('All chats');
    state.querySelector('.profile-result').textContent=shown?word('Showing {shown} of {total} rows on this page',
      {shown:format.format(shown),total:format.format(total)}):word('No matching rows on this page.');
  }
  query.disabled=false;
  query.addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(apply,120);});
  query.addEventListener('keydown',event=>{if(event.key==='Escape'){query.value='';apply();}});
  root.querySelector('[data-profile-reset]').addEventListener('click',()=>{chat='';chatTitle='';query.value='';apply();query.focus();});
  root.addEventListener('click',event=>{
    const link=event.target.closest('[data-profile-chat]');if(!link)return;
    chat=link.dataset.profileChat;chatTitle=link.dataset.profileChatTitle;apply();
    const section=root.querySelector('#chapter-journal');if(section){section.hidden=false;section.open=true;}
  });
  root.querySelector('[data-profile-all]').addEventListener('click',()=>document.dispatchEvent(
    new CustomEvent('tgwitness-profile-records',{detail:{query:query.value,chat}})));
  document.addEventListener('tgwitness-viewer-ready',()=>{root.querySelector('[data-profile-all]').hidden=false;});
  function reveal(){
    let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}
    const target=document.getElementById(id);if(!target||!root.contains(target))return;
    let node=target;
    while(node&&node!==root){if(node.tagName==='DETAILS')node.open=true;node=node.parentElement;}
  }
  window.addEventListener('hashchange',reveal);
  const index=root.querySelector('.profile-index');let queued=false,active=null;
  function position(){
    queued=false;if(!root.getClientRects().length)return;
    const edge=index.getBoundingClientRect().bottom+8;
    let current=null;
    for(const section of sections)if(!section.hidden&&section.getBoundingClientRect().top<=edge)current=section.id;
    if(current===active)return;active=current;
    for(const link of links){
      const selected=link.hash==='#'+current;
      if(selected){link.setAttribute('aria-current','location');link.scrollIntoView({block:'nearest',inline:'nearest'});}
      else link.removeAttribute('aria-current');
    }
  }
  window.addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(position);}},{passive:true});
  window.addEventListener('resize',position);
  for(const item of items)item.section.addEventListener('toggle',()=>{
    if(!printing&&!query.value.trim()&&!chat)item.open=item.section.open;
  });
  const theme=root.querySelector('[data-profile-theme]');theme.disabled=false;
  theme.addEventListener('click',()=>{
    const html=document.documentElement,current=html.dataset.theme;
    const dark=current==='dark'||((!current||current==='auto')&&matchMedia('(prefers-color-scheme: dark)').matches);
    html.dataset.theme=dark?'light':'dark';
    document.querySelectorAll('[data-theme-pick]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.themePick===html.dataset.theme)));
  });
  const printer=root.querySelector('[data-profile-print]');printer.disabled=false;
  printer.addEventListener('click',()=>window.print());
  for(const table of root.querySelectorAll('table')){
    const button=document.createElement('button');button.type='button';button.className='profile-copy no-print';button.textContent=word('Copy table');
    table.before(button);
    button.addEventListener('click',async()=>{
      const text=[...table.rows].filter(row=>!row.hidden).map(row=>[...row.cells].map(cell=>cell.textContent.replace(/\s+/g,' ').trim()).join('\t')).join('\n');
      try{
        if(navigator.clipboard?.writeText)await navigator.clipboard.writeText(text);
        else throw new Error('clipboard');
        button.textContent=word('Copied');
      }catch{
        const selection=window.getSelection(),range=document.createRange();range.selectNodeContents(table);selection.removeAllRanges();selection.addRange(range);
        button.textContent=word('Copy unavailable. Select the table to copy it.');
      }
      setTimeout(()=>{button.textContent=word('Copy table');},2500);
    });
  }
  let restored=[];
  window.addEventListener('beforeprint',()=>{
    printing=true;
    restored=[...new Set([...sections,...items.flatMap(item=>item.rows),...root.querySelectorAll('.day,.gap-row')])]
      .map(node=>({node,hidden:node.hidden,open:node.open}));
    for(const {node} of restored){node.hidden=false;if(node.tagName==='DETAILS')node.open=true;}
    for(const item of items)if(item.badge)item.badge.textContent=format.format(item.rows.length);
  });
  window.addEventListener('afterprint',()=>{
    for(const {node,hidden,open} of restored){node.hidden=hidden;if(node.tagName==='DETAILS')node.open=open;}
    printing=false;apply();
  });
  document.addEventListener('keydown',event=>{
    if(event.key==='/'&&root.getClientRects().length&&!event.ctrlKey&&!event.metaKey&&!event.altKey&&!event.target.closest('input,textarea,select,[contenteditable]')){
      event.preventDefault();query.focus();
    }
  });
  apply();reveal();position();
})();
