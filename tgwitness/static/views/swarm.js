import {createSwarmExport} from './swarm-export.js?v=1';

const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const STATES={busy:'Busy',idle:'Idle',waiting:'Telegram wait',blocked:'Blocked',offline:'Not connected',unavailable:'Unavailable'};
const ORDER={blocked:0,waiting:1,busy:2,idle:3,offline:4,unavailable:5};
const REASONS={sign_in:'Sign in again',route_down:'The route to Telegram is down',flood_wait:'Telegram asked this account to wait'};
const FILTERS=[['all','All'],['busy','Busy'],['idle','Idle'],['waiting','Telegram wait'],['blocked','Blocked'],['offline','Not connected']];
const PROBLEMS={'coverage.gap':'Coverage gap','collector.error':'Collector error','network.connection_failed':'Connection failed',
  'network.route_unavailable':'Route unavailable','network.slow_route':'Slow route','media.failed':'File not saved',
  'account.authorization_error':'Authorization error','storage.low':'Disk almost full','history.source.failed':'History source failed',
  'telegram.backoff':'Telegram asked to wait'};
const ROUTES={direct:'Direct',mtproxy_auto:'MTProxy · auto',mtproxy:'MTProxy',socks5:'SOCKS5',http:'HTTP proxy',warp:'WARP',vpn:'WireGuard'};
const POLL=1000;
const BULK=[['start','Start observation','play'],['stop','Pause observation','pause'],['route','Re-roll WARP','refresh'],
  ['verify','Check journals','shield'],['export','Export selected','download']];
const ITEM_STATES={queued:'Queued',working:'Working',done:'Done',skipped:'Skipped',failed:'Failed'};
const CODES={started:'Observation started',stopped:'Observation paused',already_running:'Already observing',
  not_running:'Not observing',no_session:'Sign in to Telegram first',no_warp:'Not on WARP',timeout:'Took too long',
  unavailable:'This workspace is unavailable.',cancelled:'Cancelled'};

export function createSwarm({root,json,tr,trn,getState,options,toast,openAccount,taskLabel,download}){
  const t=value=>esc(tr(value));
  const icon=(name,cls='icon')=>`<svg class="${cls}" aria-hidden="true"><use href="#i-${name}"/></svg>`;
  const listeners=new AbortController();
  const tiles=new Map();
  let data=null,visible=false,timer=null,clock=null,request=null,generation=0,received=0,failed=false;
  let filter='all',query='',sort='state',order='';
  const selected=new Set();let job=null,jobTimer=null,jobBusy=false;
  root.innerHTML=`<div class="sw">
    <header class="sw-head">
      <div class="sw-title"><h1>${t('Swarm')}</h1><span class="sw-live" data-sw="live"></span></div>
      <p class="sw-sub">${t('Every account at work on this server, updated every second.')}</p>
    </header>
    <div class="sw-kpis" data-sw="kpis"></div>
    <section class="sw-export-slot" data-sw="export" aria-label="${t('Swarm export')}"></section>
    <div class="sw-bar">
      <div class="sw-filters" role="group" aria-label="${t('Show')}">${FILTERS.map(([id,label])=>`<button type="button" class="sw-chip" data-sw-filter="${id}" aria-pressed="${id==='all'}"><span>${t(label)}</span><b data-sw-count="${id}"></b></button>`).join('')}</div>
      <div class="sw-tools">
        <button type="button" class="sw-select-all" data-sw="select-all">${icon('check')}<span>${t('Select all shown')}</span></button>
        <label class="sw-search">${icon('search')}<input type="search" data-sw="query" placeholder="${t('Find an account')}" aria-label="${t('Find an account')}"></label>
        <select data-sw="sort" aria-label="${t('Sort')}">
          <option value="state">${t('Problems first')}</option><option value="name">${t('By name')}</option>
          <option value="speed">${t('Fastest first')}</option><option value="queue">${t('Longest file queue first')}</option>
        </select>
      </div>
    </div>
    <div class="sw-error" data-sw="error" role="status" hidden></div>
    <div class="sw-bulk" data-sw="bulk" role="toolbar" aria-label="${t('Selected')}" hidden>
      <b data-sw="bulk-count"></b>
      <div class="sw-bulk-actions">${BULK.map(([id,label,glyph])=>`<button type="button" class="secondary small" data-sw-bulk="${id}">${icon(glyph)}<span>${t(label)}</span></button>`).join('')}</div>
      <button type="button" class="quiet small" data-sw="bulk-clear">${t('Clear selection')}</button>
    </div>
    <section class="sw-job" data-sw="job" aria-live="polite" hidden>
      <header><b data-sw="job-title"></b><span data-sw="job-summary"></span><button type="button" class="quiet small" data-sw="job-hide">${t('Hide')}</button></header>
      <ul data-sw="job-items"></ul>
    </section>
    <div class="sw-grid" data-sw="grid" role="list" aria-label="${t('Accounts')}"></div>
    <p class="sw-empty" data-sw="empty" hidden>${t('No account matches this filter.')}</p>
    <footer class="sw-foot" data-sw="foot"></footer>
  </div>`;
  const find=name=>root.querySelector(`[data-sw="${name}"]`);
  const grid=find('grid');
  const exporter=createSwarmExport({root:find('export'),json,tr,trn,toast,download});
  const put=(element,value,attr)=>{if(!element)return;const v=String(value??''),key=attr?'_a_'+attr:'_v';if(element[key]===v)return;element[key]=v;if(attr)element.setAttribute(attr,v);else element.textContent=v;};
  const number=value=>Number(value||0).toLocaleString(document.documentElement.lang||undefined,{maximumFractionDigits:1});
  const ago=seconds=>seconds<60?tr('{n} s ago',{n:Math.max(0,Math.round(seconds))}):seconds<3600?tr('{n} min ago',{n:Math.round(seconds/60)}):tr('{n} h ago',{n:Math.round(seconds/3600)});
  const left=seconds=>seconds<120?tr('{n} s',{n:Math.max(0,Math.round(seconds))}):tr('{n} min',{n:Math.ceil(seconds/60)});

  function kpis(){
    const s=data.totals||{},gates=data.gates?.handshakes||{};
    const items=[
      ['users','Accounts',s.accounts,tr('{busy} busy · {idle} idle',{busy:number(s.busy),idle:number(s.idle)}),''],
      ['alert','Need attention',(s.blocked||0)+(s.waiting||0),tr('{blocked} blocked · {waiting} waiting',{blocked:number(s.blocked),waiting:number(s.waiting)}),(s.blocked?'bad':s.waiting?'warn':'ok')],
      ['activity','Records per second',s.records_per_second,tr('journal records written',{}),'tx'],
      ['download','Files downloading',s.downloads,tr('{n} queued',{n:number(s.queued_files)}),''],
      ['link','File connections',s.connections,tr('to Telegram data centers'),''],
      ['refresh','Connecting now',gates.active||0,tr('{waiting} waiting · limit {limit}',{waiting:number(gates.waiting),limit:number(gates.at_once)}),gates.timeouts?'warn':''],
    ];
    const html=items.map(([g,label,value,small,tone])=>`<div class="sw-kpi ${tone?'sw-t-'+tone:''}">${icon(g)}<b>${number(value)}</b><span>${t(label)}</span><small>${esc(small)}</small></div>`).join('');
    const box=find('kpis');if(box._html!==html){box.innerHTML=html;box._html=html;}
    for(const [id] of FILTERS)put(root.querySelector(`[data-sw-count="${id}"]`),id==='all'?number(s.accounts):number(s[id]));
  }

  function tile(id){
    let item=tiles.get(id);
    if(item)return item;
    const el=document.createElement('article');
    el.className='sw-tile';el.setAttribute('role','listitem');el.tabIndex=0;el.dataset.id=id;
    el.innerHTML=`<header class="sw-tile-head"><input type="checkbox" class="sw-pick" data-k="pick"><i class="sw-dot" aria-hidden="true"></i><b class="sw-name" data-k="name"></b><span class="sw-state" data-k="state"></span></header>
      <div class="sw-user" data-k="user"></div>
      <div class="sw-task"><span data-k="task"></span><span class="sw-bar-track" data-k="track" hidden><i data-k="fill"></i></span></div>
      <dl class="sw-metrics">
        <div><dt>${t('Records/s')}</dt><dd data-k="rate"></dd></div>
        <div><dt>${t('Files queued')}</dt><dd data-k="queue"></dd></div>
        <div><dt>${t('File connections')}</dt><dd data-k="conn"></dd></div>
      </dl>
      <div class="sw-badges"><span class="sw-badge sw-badge-wait" data-k="flood" hidden></span><span class="sw-badge" data-k="route" hidden></span></div>
      <p class="sw-problem" data-k="problem" hidden></p>`;
    const parts={};for(const node of el.querySelectorAll('[data-k]'))parts[node.dataset.k]=node;
    item={el,parts};tiles.set(id,item);return item;
  }

  function taskText(row){
    if(row.state==='unavailable')return tr('This workspace could not start.');
    if(row.task==='history'&&row.history){
      return tr('Loading full history · {done} of {total} sources',{done:number(row.history.finished),total:number(row.history.sources)});
    }
    if(row.task==='chat_export'&&row.detail){
      const percent=row.detail.total?Math.min(100,Math.round(100*(row.detail.captured||0)/row.detail.total)):null;
      return tr('Exporting {chat}',{chat:row.detail.title||('#'+row.detail.chat_id)})+(percent!==null?' · '+percent+'%':'');
    }
    const info=row.task?taskLabel?.({task:row.task}):null;
    if(info)return tr(info.label);
    if(row.downloads?.active)return tr('Downloading files');
    if(row.state==='waiting')return tr('Waiting until Telegram allows more requests');
    return row.state==='offline'?tr('Not connected to Telegram'):tr('Idle, ready for a task');
  }

  function progress(row){
    if(row.task==='history'&&row.history?.sources)return row.history.finished/row.history.sources;
    if(row.task==='chat_export'&&row.detail?.total)return Math.min(1,(row.detail.captured||0)/row.detail.total);
    return null;
  }

  function update(row,now){
    const {el,parts}=tile(row.id);
    put(el,row.state,'data-state');
    put(parts.name,row.label);
    put(parts.state,tr(STATES[row.state]||row.state));
    const account=row.account;
    put(parts.user,account?(account.username?'@'+account.username:'ID '+account.id):(row.state==='unavailable'?row.reason:tr('No Telegram account yet')));
    const task=taskText(row);put(parts.task,task);put(parts.task,task,'title');
    const share=progress(row);
    parts.track.hidden=share===null;
    if(share!==null){const width=Math.round(share*100)+'%';if(parts.fill.style.width!==width)parts.fill.style.width=width;}
    put(parts.rate,row.rates?number(row.rates.records):'—');
    put(parts.queue,row.queue?number(row.queue.queued+row.queue.running):'—');
    const d=row.downloads;
    put(parts.conn,d?(d.connections?number(d.connections)+(d.busy?' · '+tr('{n} busy',{n:number(d.busy)}):''):'0'):'—');
    const flood=row.flood;
    parts.flood.hidden=!flood;
    if(flood)put(parts.flood,tr('Wait {time}',{time:left(flood.remaining)})+' · '+flood.method+(flood.methods>1?' +'+(flood.methods-1):''));
    const route=row.route;
    parts.route.hidden=!route?.kind;
    if(route?.kind){
      const name=route.managed==='warp'?'WARP':tr(ROUTES[route.kind]||route.kind);
      put(parts.route,name+(route.ema_ms?' · '+tr('{n} ms',{n:number(route.ema_ms)}):'')+(route.fallback?' · '+tr('direct fallback'):''));
      put(parts.route,route.status||'unknown','data-status');
    }
    const picked=selected.has(row.id);
    if(parts.pick.checked!==picked)parts.pick.checked=picked;
    put(parts.pick,tr('Select')+': '+row.label,'aria-label');
    el.classList.toggle('sw-picked',picked);
    let problem='';
    if(row.reason&&REASONS[row.reason])problem=tr(REASONS[row.reason]);
    else if(row.problem&&now-row.problem.at<3600)problem=tr(PROBLEMS[row.problem.kind]||row.problem.kind)+(row.problem.reason?' · '+row.problem.reason:'')+' · '+ago(now-row.problem.at);
    else if(row.last_error)problem=tr('Last error: {error}',{error:row.last_error});
    parts.problem.hidden=!problem;put(parts.problem,problem);
    el.title=row.label;
    return el;
  }

  function visibleRows(){
    const needle=query.trim().toLowerCase();
    const rows=(data?.accounts||[]).filter(row=>(filter==='all'||row.state===filter)&&(!needle||[row.label,row.account?.username,String(row.account?.id||''),row.id].some(v=>String(v||'').toLowerCase().includes(needle))));
    const name=(a,b)=>String(a.label).localeCompare(String(b.label));
    const by={state:(a,b)=>(ORDER[a.state]??9)-(ORDER[b.state]??9)||name(a,b),name,
      speed:(a,b)=>(b.rates?.records||0)-(a.rates?.records||0)||name(a,b),
      queue:(a,b)=>((b.queue?.queued||0)+(b.queue?.running||0))-((a.queue?.queued||0)+(a.queue?.running||0))||name(a,b)}[sort]||name;
    return rows.sort(by);
  }

  function render(){
    if(!data)return;
    kpis();
    const now=Date.now()/1000,rows=visibleRows(),ids=rows.map(row=>row.id).join(',');
    const elements=rows.map(row=>update(row,now));
    if(ids!==order){grid.replaceChildren(...elements);order=ids;}
    for(const id of [...tiles.keys()])if(!data.accounts.some(row=>row.id===id))tiles.delete(id);
    find('empty').hidden=rows.length>0;
    const files=data.files||{},gates=data.gates?.handshakes||{};
    const foot=[tr('Same file requested at once, downloaded once: {n}',{n:number(files.joined)}),
      tr('Connections set up since start: {n}, timed out: {timeouts}',{n:number(gates.started),timeouts:number(gates.timeouts)})].join(' · ');
    put(find('foot'),foot);
    for(const id of [...selected])if(!data.accounts.some(row=>row.id===id))selected.delete(id);
    bulkBar();
    live();
  }

  function bulkBar(){
    const bar=find('bulk');bar.hidden=!selected.size;
    put(find('bulk-count'),tr('{n} selected',{n:number(selected.size)}));
    for(const b of root.querySelectorAll('[data-sw-bulk]'))b.disabled=jobBusy||!selected.size;
  }

  function pick(id,value){
    if(value)selected.add(id);else selected.delete(id);
    const item=tiles.get(id);
    if(item){item.parts.pick.checked=value;item.el.classList.toggle('sw-picked',value);}
    bulkBar();
  }

  function itemText(item){
    if(item.code==='verified')return trn('{n} record checked','{n} records checked',item.values?.n||0)+(item.values?.head?' · '+item.values.head+'…':'');
    if(item.code==='rerolled'){
      const values={before:item.values?.before??'—',after:item.values?.after??'—'};
      return tr(item.values?.identity?'New WARP identity: {before} → {after} ms':'Re-rolled: {before} → {after} ms',values);
    }
    if(item.code==='error')return tr(item.message||'Failed');
    return tr(CODES[item.code]||ITEM_STATES[item.state]||item.state);
  }

  function showJob(){
    const box=find('job');box.hidden=!job;
    if(!job)return;
    const label=(BULK.find(([id])=>id===job.action)||[])[1]||job.action;
    put(find('job-title'),tr(label)+' · '+trn('{n} account','{n} accounts',job.items.length));
    const c=job.counts||{};
    put(find('job-summary'),job.finished_at?tr('{done} done · {skipped} skipped · {failed} failed',
      {done:number(c.done),skipped:number(c.skipped),failed:number(c.failed)}):tr('Working')+'… '+number((c.done||0)+(c.skipped||0)+(c.failed||0))+' / '+number(job.items.length));
    const html=job.items.map(item=>`<li data-state="${esc(item.state)}"><b>${esc(item.profile==='default'&&item.label==='Main workspace'?tr('Main workspace'):item.label)}</b><span>${esc(tr(ITEM_STATES[item.state]||item.state))}</span><small>${esc(item.state==='queued'||item.state==='working'?'':itemText(item))}</small></li>`).join('');
    const list=find('job-items');if(list._html!==html){list.innerHTML=html;list._html=html;}
  }

  async function followJob(id){
    clearTimeout(jobTimer);
    if(!visible)return;
    try{
      const value=await json('swarm/bulk/'+encodeURIComponent(id),undefined,{root:true});
      if(!job||job.id!==id)return;
      job=value;showJob();
      if(value.finished_at){
        jobBusy=false;bulkBar();
        const c=value.counts||{};
        toast(tr((BULK.find(([a])=>a===value.action)||[])[1]||value.action)+': '+tr('{done} done · {skipped} skipped · {failed} failed',
          {done:number(c.done),skipped:number(c.skipped),failed:number(c.failed)}),!!c.failed);
        void load();return;
      }
    }catch(error){if(!job||job.id!==id)return;}
    jobTimer=setTimeout(()=>followJob(id),1000);
  }

  async function runBulk(action){
    const profiles=[...selected];
    if(!profiles.length||jobBusy)return;
    if(action==='export'){
      jobBusy=true;bulkBar();
      try{
        const result=await download('swarm/bulk-export?profiles='+encodeURIComponent(profiles.join(',')),'tgwitness-selected-accounts.zip',true,true);
        if(result!==false)toast(tr('Group export saved: each account’s signed export and a signed list of them.'));
      }catch(error){toast(error.message,true);}
      finally{jobBusy=false;bulkBar();}
      return;
    }
    jobBusy=true;bulkBar();
    try{
      job=await json('swarm/bulk',{action,profiles},{root:true});showJob();
      void followJob(job.id);
    }catch(error){jobBusy=false;bulkBar();toast(error.message,true);}
  }

  function live(){
    const el=find('live');if(!el)return;
    const age=received?Math.round((Date.now()-received)/1000):null;
    const stale=failed||age!==null&&age>5;
    root.classList.toggle('sw-stale',stale);
    put(el,age===null?tr('Loading…'):age<2?tr('Live'):tr('Updated {time}',{time:ago(age)}));
  }

  async function load(){
    if(!visible||document.hidden)return;
    clearTimeout(timer);request?.abort();
    const serial=++generation,controller=new AbortController();request=controller;
    const parent=options()?.signal,abort=()=>controller.abort();parent?.addEventListener('abort',abort,{once:true});
    const deadline=setTimeout(()=>controller.abort('timeout'),10000);if(parent?.aborted)controller.abort();
    try{
      const result=await json('swarm',undefined,{root:true,signal:controller.signal});
      if(serial!==generation||!visible||controller.signal.aborted)return;
      if(result.schema!=='tgwitness-swarm-v1'||!Array.isArray(result.accounts))throw new Error(tr('Swarm data is unavailable.'));
      for(const row of result.accounts)if(row.id==='default'&&row.label==='Main workspace')row.label=tr('Main workspace');
      data=result;received=Date.now();failed=false;find('error').hidden=true;render();
    }catch(error){
      if(serial!==generation||!visible||controller.signal.aborted&&controller.signal.reason!=='timeout')return;
      failed=true;const e=find('error');e.hidden=false;e.textContent=tr('Refresh failed. Showing the last snapshot.');live();
    }finally{
      clearTimeout(deadline);parent?.removeEventListener('abort',abort);
      if(serial===generation){request=null;if(visible&&!document.hidden)timer=setTimeout(load,POLL);}
    }
  }

  root.addEventListener('click',event=>{
    const chip=event.target.closest('[data-sw-filter]');
    if(chip){filter=chip.dataset.swFilter;for(const b of root.querySelectorAll('[data-sw-filter]'))b.setAttribute('aria-pressed',String(b===chip));order='';render();return;}
    const box=event.target.closest('.sw-pick');
    if(box){pick(box.closest('.sw-tile').dataset.id,box.checked);return;}
    const action=event.target.closest('[data-sw-bulk]');
    if(action){void runBulk(action.dataset.swBulk);return;}
    if(event.target.closest('[data-sw="select-all"]')){
      const rows=visibleRows(),all=rows.length&&rows.every(row=>selected.has(row.id));
      for(const row of rows)pick(row.id,!all);return;
    }
    if(event.target.closest('[data-sw="bulk-clear"]')){for(const id of [...selected])pick(id,false);return;}
    if(event.target.closest('[data-sw="job-hide"]')){if(!jobBusy){job=null;showJob();}return;}
    const card=event.target.closest('.sw-tile');
    if(card&&!event.target.closest('button,a,input,select'))Promise.resolve(openAccount?.(card.dataset.id)).catch(error=>toast(error.message,true));
  },{signal:listeners.signal});
  root.addEventListener('keydown',event=>{
    if(event.target.closest?.('.sw-pick'))return;
    const card=event.target.closest?.('.sw-tile');
    if(card&&event.target===card&&(event.key==='Enter'||event.key===' ')){event.preventDefault();card.click();}
  },{signal:listeners.signal});
  find('query').addEventListener('input',event=>{query=event.target.value;order='';render();},{signal:listeners.signal});
  find('sort').addEventListener('change',event=>{sort=event.target.value;order='';render();},{signal:listeners.signal});
  document.addEventListener('visibilitychange',()=>{if(!visible)return;if(document.hidden){clearTimeout(timer);request?.abort();generation++;}else void load();},{signal:listeners.signal});

  function leave(){visible=false;generation++;request?.abort();request=null;clearTimeout(timer);clearTimeout(jobTimer);clearInterval(clock);exporter.leave();}
  return {
    async enter(){leave();if(getState().view!=='swarm'||!getState().me?.admin)return;visible=true;clock=setInterval(live,1000);if(data)render();else live();
      if(job&&!job.finished_at)void followJob(job.id);
      await Promise.all([load(),exporter.enter()]);},
    leave,
    resetSession(){leave();exporter.reset();data=null;received=0;failed=false;order='';tiles.clear();grid.replaceChildren();find('kpis').innerHTML='';find('kpis')._html='';find('error').hidden=true;
      selected.clear();job=null;jobBusy=false;showJob();bulkBar();live();},
    destroy(){leave();exporter.destroy();listeners.abort();},
  };
}
