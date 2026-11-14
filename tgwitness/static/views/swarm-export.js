const esc=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const FILES=[['','As set in each workspace'],['skip','Skip attachments (fastest)'],['hashes','Server hashes only'],['download','Download attachments']];
const PRIORITY=[[0,'Urgent'],[1,'High'],[2,'Normal'],[3,'Low']];
const TASKS={queued:'Waiting',running:'Exporting',done:'Ready',failed:'Failed',cancelled:'Cancelled'};
const ACCOUNTS={free:'Free',busy:'Busy',waiting:'Telegram wait',unavailable:'Unavailable'};
const WAITING={telegram_wait:'Telegram asked the account to wait',account_busy:'The account became busy',moved_by_operator:'Moved by the operator'};
const ACTIVE=new Set(['queued','running']);

export function createSwarmExport({root,json,tr,trn,toast,download}){
  const t=value=>esc(tr(value));
  const icon=(name,cls='icon')=>`<svg class="${cls}" aria-hidden="true"><use href="#i-${name}"/></svg>`;
  const number=value=>Number(value||0).toLocaleString(document.documentElement.lang||undefined,{maximumFractionDigits:1});
  const size=bytes=>bytes>=1048576?tr('{n} MB',{n:number(bytes/1048576)}):tr('{n} KB',{n:number(Math.max(1,bytes/1024))});
  const listeners=new AbortController();
  let data=null,timer=null,visible=false,request=0,session=0,chosen=new Set(),mode='all';
  root.innerHTML=`<details class="se" data-se="card">
    <summary class="se-summary">${icon('download')}<b>${t('Swarm export')}</b><span class="se-sub" data-se="summary">${t('Paste chats; free accounts export them in parallel.')}</span></summary>
    <form class="se-form" data-se="form">
      <label class="se-field se-peers"><span>${t('Chats: @username, t.me link or chat ID, one per line')}</span>
        <textarea data-se="peers" rows="5" spellcheck="false" placeholder="@channel&#10;https://t.me/example&#10;-1001234567890"></textarea></label>
      <div class="se-side">
        <label class="se-field"><span>${t('Attachments')}</span><select data-se="files">${FILES.map(([v,l])=>`<option value="${v}">${t(l)}</option>`).join('')}</select></label>
        <label class="se-field"><span>${t('Priority')}</span><select data-se="priority">${PRIORITY.map(([v,l])=>`<option value="${v}"${v===2?' selected':''}>${t(l)}</option>`).join('')}</select></label>
        <div class="se-field" role="radiogroup" aria-label="${t('Accounts')}"><span>${t('Accounts')}</span>
          <label class="se-radio"><input type="radio" name="se-accounts" value="all" checked> ${t('All free accounts')}</label>
          <label class="se-radio"><input type="radio" name="se-accounts" value="chosen"> ${t('Only the chosen ones')}</label></div>
      </div>
      <div class="se-picks" data-se="picks" hidden></div>
      <div class="se-actions"><button type="submit" class="primary" data-se="start">${icon('play')}${t('Start export')}</button>
        <span class="se-note" data-se="note"></span></div>
    </form>
    <div class="se-jobs" data-se="jobs"></div>
  </details>`;
  const find=name=>root.querySelector(`[data-se="${name}"]`);
  const card=find('card'),jobsBox=find('jobs');

  function accountName(id){const row=data?.accounts?.find(a=>a.id===id);return row?(row.id==='default'&&row.label==='Main workspace'?tr('Main workspace'):row.label):id||'—';}

  function renderPicks(){
    const box=find('picks');box.hidden=mode!=='chosen';
    if(!data||mode!=='chosen')return;
    box.innerHTML=data.accounts.map(a=>`<button type="button" class="se-pick" data-se-pick="${esc(a.id)}" data-state="${esc(a.state)}" aria-pressed="${chosen.has(a.id)}">
      <i aria-hidden="true"></i><span>${esc(accountName(a.id))}</span><small>${esc(a.username?'@'+a.username:tr(ACCOUNTS[a.state]||a.state))}</small></button>`).join('');
  }

  function progressCell(task){
    const p=task.progress||{};
    if(task.state==='running'){
      const share=p.total?Math.min(1,(p.captured||0)/p.total):null;
      const text=p.total?tr('{done} of {total} messages',{done:number(p.captured),total:number(p.total)}):trn('{n} message','{n} messages',p.captured||0);
      const eta=p.eta_seconds?' · '+tr('about {time} left',{time:p.eta_seconds<120?tr('{n} s',{n:Math.round(p.eta_seconds)}):tr('{n} min',{n:Math.ceil(p.eta_seconds/60)})}):'';
      return `<div class="se-progress">${share!==null?`<span class="se-track"><i data-se-share="${Math.round(share*100)}"></i></span>`:''}<small>${esc(text+eta)}</small></div>`;
    }
    if(task.result)return `<small>${esc(trn('{n} message','{n} messages',task.result.captured||0)+' · '+size(task.result.bytes))}</small>`;
    if(task.state==='queued'){
      const why=task.waiting?tr(WAITING[task.waiting]||task.waiting):tr('In the queue');
      return `<small>${esc(why+(task.retry_in?' · '+tr('next try in {n} s',{n:Math.ceil(task.retry_in)}):''))}</small>`;
    }
    return '';
  }

  function accountOptions(task){
    const options=task.state==='running'?[`<option value="" selected disabled>${t('Move to…')}</option>`,`<option value="*">${t('Any free account')}</option>`]
      :[`<option value="">${t('Any free account')}</option>`];
    for(const a of data.accounts){
      if(task.affinity&&!task.affinity.includes(a.id))continue;
      if(task.state==='running'&&a.id===task.account)continue;
      options.push(`<option value="${esc(a.id)}"${task.state!=='running'&&task.pinned===a.id?' selected':''}>${esc(accountName(a.id))} · ${t(ACCOUNTS[a.state]||a.state)}</option>`);
    }
    return options.join('');
  }

  function row(job,task){
    const peer=task.payload?.peer||{},p=task.progress||{};
    const title=p.title||peer.input||peer.value;
    const actions=[];
    if(task.state==='queued')actions.push(`<select class="se-mini" data-se-priority="${task.id}" aria-label="${t('Priority')}">${PRIORITY.map(([v,l])=>`<option value="${v}"${task.priority===v?' selected':''}>${t(l)}</option>`).join('')}</select>`);
    if(ACTIVE.has(task.state))actions.push(`<select class="se-mini" data-se-move="${task.id}" aria-label="${t('Move to another account')}">${accountOptions(task)}</select>`,
      `<button type="button" class="se-icon" data-se-act="cancel" data-task="${task.id}" title="${t('Cancel')}" aria-label="${t('Cancel')}">${icon('x')}</button>`);
    if(task.state==='failed'||task.state==='cancelled')actions.push(`<button type="button" class="se-text" data-se-act="retry" data-task="${task.id}">${icon('refresh')}${t('Try again')}</button>`);
    if(task.result)actions.push(`<button type="button" class="se-text" data-se-act="download" data-job="${job.id}" data-task="${task.id}" data-name="${esc(task.result.filename||'')}">${icon('download')}${t(task.result.partial?'Download partial':'Download')}</button>`);
    const excluded=Object.entries(task.excluded||{}).map(([id,why])=>accountName(id)+': '+tr(why));
    const notes=[task.error?tr(task.error):'',...excluded].filter(Boolean);
    const wait=p.wait_seconds?`<span class="se-wait">${esc(tr('Wait {time}',{time:tr('{n} s',{n:Math.round(p.wait_seconds)})}))}</span>`:'';
    return `<tr data-state="${task.state}">
      <td class="se-chat"><div><b>${esc(title)}</b>${peer.input&&peer.input!==title?`<small>${esc(peer.input)}</small>`:''}${notes.length?`<small class="se-notes">${esc(notes.join(' · '))}</small>`:''}</div></td>
      <td>${esc(task.account?accountName(task.account):task.pinned?accountName(task.pinned):'—')}</td>
      <td>${progressCell(task)}${wait}</td>
      <td><span class="se-state" data-state="${task.state}">${t(TASKS[task.state]||task.state)}</span></td>
      <td class="se-row-actions"><div>${actions.join('')}</div></td></tr>`;
  }

  function renderJobs(){
    if(jobsBox.contains(document.activeElement)&&document.activeElement.tagName==='SELECT')return;
    const jobs=data?.jobs||[];
    if(!jobs.length){jobsBox.innerHTML='';return;}
    jobsBox.innerHTML=jobs.map(job=>{
      const c=job.counts||{},active=(c.queued||0)+(c.running||0);
      const when=job.created_at?new Date(job.created_at).toLocaleString(document.documentElement.lang||undefined,{dateStyle:'short',timeStyle:'short'}):'';
      const problems=(job.problems||[]).map(x=>tr('Line {n}',{n:x.line})+': '+x.input).join(' · ');
      return `<section class="se-job">
        <header><b>${esc(when)}</b><span>${esc(tr('Chats: {n}',{n:number(job.peers)}))} · ${esc(tr('ready {done} · exporting {running} · waiting {queued} · failed {failed}',{done:number(c.done),running:number(c.running),queued:number(c.queued),failed:number(c.failed)}))}</span>
          ${active?'':`<button type="button" class="se-text" data-se-act="forget" data-job="${job.id}">${icon('trash')}${t('Remove from the list')}</button>`}</header>
        ${problems?`<p class="se-problems">${esc(tr('Skipped lines')+': '+problems)}</p>`:''}
        <div class="se-table-wrap"><table class="se-table"><thead><tr><th>${t('Chat')}</th><th>${t('Account')}</th><th>${t('Progress')}</th><th>${t('State')}</th><th><span class="visually-hidden">${t('Actions')}</span></th></tr></thead>
        <tbody>${(job.tasks||[]).map(task=>row(job,task)).join('')}</tbody></table></div></section>`;
    }).join('');
    for(const bar of jobsBox.querySelectorAll('[data-se-share]'))bar.style.width=bar.dataset.seShare+'%';
  }

  function render(){
    if(!data)return;
    const tasks=(data.jobs||[]).flatMap(job=>job.tasks||[]);
    const running=tasks.filter(x=>x.state==='running').length,queued=tasks.filter(x=>x.state==='queued').length;
    const free=data.accounts.filter(a=>a.state==='free').length;
    find('summary').textContent=running||queued?tr('exporting {running} · waiting {queued}',{running:number(running),queued:number(queued)})
      :tr('Paste chats; free accounts export them in parallel.');
    find('note').textContent=tr('Free accounts now: {free} of {total}. Observing or busy accounts take no task until they are free.',{free:number(free),total:number(data.accounts.length)});
    if(running||queued)card.open=true;
    renderPicks();renderJobs();
  }

  async function refresh(){
    const serial=++request;
    try{const result=await json('swarm/exports',undefined,{root:true});if(serial===request){data=result;render();}}
    catch(error){if(serial===request&&visible)find('note').textContent=error.message;}
  }

  function schedule(){
    clearTimeout(timer);if(!visible||document.hidden)return;
    const active=(data?.jobs||[]).some(job=>(job.tasks||[]).some(task=>ACTIVE.has(task.state)));
    timer=setTimeout(async()=>{await refresh();schedule();},active?2000:10000);
  }

  async function act(body,taskId){
    await json('swarm/tasks/'+encodeURIComponent(taskId),body,{root:true});await refresh();
  }

  find('form').addEventListener('submit',async event=>{
    event.preventDefault();
    const button=find('start');if(button.disabled)return;button.disabled=true;
    const peers=find('peers'),sent=peers.value,owner=session;
    try{
      const accounts=mode==='chosen'?[...chosen]:null;
      if(mode==='chosen'&&!accounts.length)throw new Error(tr('Choose at least one account workspace.'));
      const job=await json('swarm/exports',{peers:sent,accounts,files:find('files').value||null,
        priority:Number(find('priority').value)},{root:true});
      if(owner!==session)return;
      if(peers.value===sent)peers.value='';
      toast(tr('Export started. Chats: {n}.',{n:number(job.peers)})+(job.problems?.length?' '+tr('Skipped lines: {n}',{n:job.problems.length}):''));
      if(visible){await refresh();if(owner===session)schedule();}
    }catch(error){if(owner===session)toast(error.message,true);}finally{if(owner===session)button.disabled=false;}
  },{signal:listeners.signal});
  root.addEventListener('change',event=>{
    const target=event.target;
    if(target.name==='se-accounts'){mode=target.value;renderPicks();return;}
    if(target.dataset.sePriority)void act({action:'priority',priority:Number(target.value)},target.dataset.sePriority).catch(e=>toast(e.message,true));
    if(target.dataset.seMove)void act({action:'reassign',account:target.value&&target.value!=='*'?target.value:null},target.dataset.seMove).then(()=>target.blur()).catch(e=>toast(e.message,true));
  },{signal:listeners.signal});
  root.addEventListener('click',event=>{
    const pick=event.target.closest('[data-se-pick]');
    if(pick){const id=pick.dataset.sePick;chosen.has(id)?chosen.delete(id):chosen.add(id);pick.setAttribute('aria-pressed',String(chosen.has(id)));return;}
    const button=event.target.closest('[data-se-act]');if(!button)return;
    const action=button.dataset.seAct;
    if(action==='download'){
      Promise.resolve(download('swarm/exports/'+encodeURIComponent(button.dataset.job)+'/tasks/'+encodeURIComponent(button.dataset.task)+'/download',
        button.dataset.name||'tgwitness-chat-export.zip',true,true)).catch(error=>toast(error.message,true));return;
    }
    if(action==='forget'){json('swarm/exports/'+encodeURIComponent(button.dataset.job)+'/forget',{},{root:true}).then(result=>{data=result;render();}).catch(error=>toast(error.message,true));return;}
    void act({action},button.dataset.task).catch(error=>toast(error.message,true));
  },{signal:listeners.signal});
  document.addEventListener('visibilitychange',()=>{if(visible&&!document.hidden)void refresh().then(schedule);},{signal:listeners.signal});

  return {
    async enter(){visible=true;await refresh();schedule();},
    leave(){visible=false;clearTimeout(timer);request++;},
    reset(){visible=false;clearTimeout(timer);request++;session++;data=null;chosen=new Set();mode='all';jobsBox.innerHTML='';find('peers').value='';find('start').disabled=false;card.open=false;},
    destroy(){visible=false;clearTimeout(timer);request++;session++;listeners.abort();},
  };
}
