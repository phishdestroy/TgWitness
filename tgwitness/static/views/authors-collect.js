export function createAuthorsCollect({json,tr,duration,canCollect,accounts,groups,active,onComplete}){
  const node=(tag,text='',cls='')=>{const el=document.createElement(tag);el.textContent=String(text??'');if(cls)el.className=cls;return el;};
  const button=(text,work,cls='secondary small')=>{const el=node('button',tr(text),cls);el.type='button';el.addEventListener('click',work);return el;};
  const number=value=>Number(value||0).toLocaleString(document.documentElement.lang||undefined);
  const say=(text,values)=>Object.entries(values).reduce((out,[key,value])=>out.replaceAll('{'+key+'}',value),tr(text));
  const phases={running:'Collecting',paused:'Paused',complete:'Completed',partial:'Incomplete',cancelled:'Cancelled'};
  const states={starting:'Starting',running:'Collecting',waiting:'Telegram asked us to wait',idle:'Waiting for work',busy:'Another task is using this account.',
    no_account:'No Telegram account connected',unavailable:'Workspace unavailable',no_access:'No access to this chat',not_shared:'No access to this chat',finished:'Finished',stopped:'Stopped'};
  const reasons={telegram_wait:'Telegram asked us to wait. Collection resumes automatically.',retry_wait:'Waiting before another attempt.',
    waiting_for_account:'Another task is using this account.',helpers_working:'Other accounts are finishing their share.',operator:'Paused by you.',
    account_changed:'This collection belongs to another Telegram account.',authorization_required:'Connect a Telegram account first.',source_paused:'Resume the selected chats to continue.'};
  let host=null,chat=null,info=null,facts={authors:0,messages:0},last=null,timer=null,serial=0,working=false,pending=false,finished=null,error='';
  const live=()=>host?.isConnected&&active(chat);
  function mount(chatId,data,chatInfo){
    if(!host||chat!==chatId){clearTimeout(timer);serial++;chat=chatId;last=null;finished=null;error='';host=node('section','','authors-collect');}
    info=chatInfo;host.hidden=!canCollect();
    const people=data.authors.filter(person=>typeof person.id==='number'&&person.id>0);
    facts={authors:people.length,messages:people.reduce((sum,person)=>sum+(person.messages||0),0)};
    render();if(!timer&&!pending)void refresh();return host;
  }
  const ours=data=>!!data&&data.phase!=='idle'&&!data.options?.all_chats&&(data.options?.chat_ids||[]).length===1&&data.options.chat_ids[0]===chat;
  function render(){
    if(!host)return;host.replaceChildren();
    const data=last,mine=ours(data),occupied=!!data&&['running','paused'].includes(data.phase);
    const head=node('div','','authors-collect-head'),text=node('div');
    text.append(node('strong',tr('Collect all authors')),node('p',tr('Profiles, bios, profile photos, gifts and links of everyone who wrote in this chat. Several accounts can share the work.'),'hint'));
    const start=button('Collect all authors',()=>openDialog(),'primary small');start.id='authors-collect-start';start.disabled=working||occupied||!facts.authors;
    head.append(text,start);host.append(head);
    if(occupied&&!mine)host.append(node('p',tr('Another profile collection is running. Resume or cancel it in the People tab first.'),'hint'));
    if(mine)progress(data);
    if(error)host.append(node('p',error,'notice warning'));
  }
  function progress(data){
    const counts=data.counts||{},done=(counts.complete||0)+(counts.partial||0),total=counts.total||0,percent=total?Math.floor(done*100/total):0;
    const line=node('div','','authors-collect-progress');
    line.append(node('span',tr(phases[data.phase]||data.phase),'profile-phase '+data.phase),node('strong',percent+'%'),node('span',number(done)+' / '+number(total)));
    if(data.eta_seconds!=null)line.append(node('span',say('{time} left',{time:duration(data.eta_seconds)}),'hint'));
    const controls=data.phase==='running'?[['pause','Pause'],['cancel','Cancel']]:data.phase==='paused'?[['resume','Resume'],['cancel','Cancel']]:[];
    for(const [action,title] of controls){const control=button(title,()=>act(action));control.dataset.authorsAction=action;control.disabled=working;line.append(control);}
    host.append(line);
    const bar=node('progress');bar.max=100;bar.value=percent;bar.setAttribute('aria-label',tr('Collect all authors'));host.append(bar);
    if(data.reason&&reasons[data.reason])host.append(node('p',tr(reasons[data.reason]),'hint'));
    const list=node('ul','','authors-collect-workers'),lead=node('li');
    lead.append(node('b',tr('This account')),node('span',number(data.lead_done)));list.append(lead);
    for(const worker of data.workers||[]){
      const row=node('li','','worker-'+worker.state),state=tr(states[worker.state]||worker.state);
      const wait=worker.state==='waiting'&&worker.wait_until?' · '+say('{time} left',{time:duration(Math.max(0,Math.round(worker.wait_until-Date.now()/1000)))}):'';
      row.append(node('b',worker.label),node('span',state+wait,'hint'),node('span',number(worker.done)));list.append(row);
    }
    host.append(list);
  }
  async function act(action,body){
    if(working)return;working=true;error='';render();const ticket=serial;
    try{const data=await json('profiling/'+action,body||{});if(ticket===serial){last=data;}}
    catch(problem){if(ticket===serial)error=problem.message;}
    finally{if(ticket===serial){working=false;render();schedule();}}
  }
  function schedule(){clearTimeout(timer);timer=null;if(live())timer=setTimeout(refresh,2500);}
  async function refresh(){
    clearTimeout(timer);timer=null;
    if(!host||!canCollect()||pending)return;
    const ticket=serial;pending=true;
    try{const data=await json('profiling');if(ticket!==serial)return;last=data;error='';
      if(ours(data)&&['complete','partial'].includes(data.phase)){const key=data.id+':'+data.phase;if(finished!==null&&finished!==key)onComplete?.();finished=key;}
      else if(ours(data))finished=data.id+':'+data.phase;
      render();}
    catch(problem){if(ticket===serial){error=problem.message;render();}}
    finally{pending=false;if(ticket===serial)schedule();else if(live())void refresh();}
  }
  async function openDialog(){
    const shared=['channel','supergroup'].includes(info?.kind),others=accounts();let known=[];
    if(shared&&others.length){try{known=(await groups()).groups||[];}catch{known=[];}}
    const dialog=node('dialog','','export-dialog authors-collect-dialog'),form=node('form');form.method='dialog';
    form.append(node('h3',tr('Collect all authors')+(info?.title?' · '+info.title:'')),
      node('p',say('{authors} authors with saved messages · {messages} messages',{authors:number(facts.authors),messages:number(facts.messages)}),'hint'));
    const what=node('fieldset');what.append(node('legend',tr('What to collect')));
    for(const [name,title,locked] of [['profile','Profile and bio',true],['avatars','Profile photos'],['gifts','Gifts'],['links','Links']]){
      const label=node('label','','check-label'),input=node('input');input.type='checkbox';input.checked=true;input.disabled=!!locked;input.dataset.collect=name;
      label.append(input,document.createTextNode(' '+tr(title)));what.append(label);
    }
    const who=node('fieldset');who.append(node('legend',tr('Accounts')));
    const choice=(value,title,checked)=>{const label=node('label','','check-label'),input=node('input');input.type='radio';input.name='authors-accounts';input.value=value;input.checked=checked;label.append(input,document.createTextNode(' '+tr(title)));who.append(label);return input;};
    choice('solo','Only this account',true);const many=choice('many','This account and other accounts',false);
    const list=node('div','','authors-collect-accounts');list.hidden=true;
    if(!shared){many.disabled=true;who.append(node('p',tr('Other accounts can help only in channels and supergroups: in other chats each account numbers messages differently.'),'hint'));}
    else if(!others.length){many.disabled=true;who.append(node('p',tr('There are no other account workspaces.'),'hint'));}
    else{
      if(known.length){const pick=node('select');pick.setAttribute('aria-label',tr('Account group'));pick.append(new Option(tr('Choose a group'),''));
        for(const group of known)pick.append(new Option(group.label,group.id));
        pick.addEventListener('change',()=>{const members=new Set(known.find(group=>group.id===pick.value)?.members||[]);
          for(const box of list.querySelectorAll('input[type=checkbox]'))if(!box.disabled)box.checked=members.has(box.value);count();});list.append(pick);}
      for(const account of others){const label=node('label','','export-account'),box=node('input'),text=node('span','','export-account-who');box.type='checkbox';box.value=account.id;box.disabled=!account.free;
        box.addEventListener('change',()=>count());text.append(node('b',account.label),node('small',account.note));label.append(box,text);list.append(label);}
      list.append(node('p',tr('Accounts busy with another task are not touched. Each chosen account is reserved for this collection until it finishes or you pause it.'),'hint'));
    }
    who.append(list);
    const summary=node('p','','hint');
    const chosen=()=>many.checked?[...list.querySelectorAll('input[type=checkbox]:checked')].map(box=>box.value):[];
    const count=()=>{const n=chosen().length+1;summary.textContent=n>1?say('{n} accounts will share the work.',{n}):tr('Only this account will collect.');};
    for(const radio of who.querySelectorAll('input[type=radio]'))radio.addEventListener('change',()=>{list.hidden=!many.checked;count();});
    const buttons=node('div','','export-dialog-actions'),cancel=node('button',tr('Cancel'),'quiet'),go=node('button',tr('Start'),'primary');
    cancel.value='cancel';go.value='start';go.id='authors-collect-go';buttons.append(cancel,go);
    form.append(what,who,summary,buttons);dialog.append(form);document.body.append(dialog);count();
    dialog.addEventListener('keydown',event=>{if(event.key==='Escape')event.stopPropagation();});
    dialog.showModal();
    const result=await new Promise(resolve=>dialog.addEventListener('close',()=>resolve(dialog.returnValue),{once:true}));
    const options=Object.fromEntries([...what.querySelectorAll('input[data-collect]')].map(input=>[input.dataset.collect,input.checked]));
    const helpers=chosen();dialog.remove();
    if(result!=='start'||!live())return;
    await act('start',{all_chats:false,chat_ids:[chat],user_id:null,participants:false,avatars:options.avatars,gifts:options.gifts,links:options.links,accounts:helpers});
  }
  function reset(){clearTimeout(timer);timer=null;serial++;host=null;chat=null;last=null;working=false;pending=false;error='';}
  return {mount,refresh,reset};
}
