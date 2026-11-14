import {createGroupSettings} from './group-settings.js?v=1';
import {accountState} from '../components/account-state.js';

export function createSettingsHub(ctx) {
  const {root, wizardRoot, state, json, tr, node, toast, navigate, askConfirm, $, refreshStatus} = ctx;
  const rank = {simple:0, standard:1, expert:2};
  const goals = [['copy','download:blue','Just download','Save chats and files once. Nothing keeps running in the background. The archive is signed, and verify.py checks every file in it.'],['watch','eye:teal','Follow chats','Keeps new messages and their changes with independent timestamps that the recipient checks. Saves photos and short videos. You can still write, join and accept chats from the panel. Needs requests outside Telegram.'],['evidence','fingerprint:violet','Evidence for a case','For a court or an authority: saves every file up to 1 GB and confirms each record as it is written, with independent timestamps that the recipient checks. Sending, joining and accepting chats from the panel are off. Needs requests outside Telegram.']];
  const goalLevels = {copy:'simple',watch:'standard',evidence:'standard'};
  const routes = [['auto','sparkle:violet','Automatic','Try WARP, then public proxies.'],['warp','shield:teal','Cloudflare WARP','Connect through a local tunnel.'],['proxy','link:orange','My proxy','Paste one proxy address.'],['direct','external:slate','Direct','Telegram will see this server’s address.']];
  const levels = [['simple','star:green','Simple','Only the essentials.'],['standard','settings:blue','Standard','Common settings and explanations.'],['expert','braces:slate','Expert','All fields, limits and technical details.']];
  const navLevels = {'system-map':'expert',topology:'expert',start:'simple',chats:'simple','secret-chats':'simple',observations:'simple',evidence:'simple',settings:'simple',
    board:'standard',accounts:'simple',access:'standard',sources:'standard',connection:'expert',witness:'expert',analysis:'expert',
    parameters:'expert','system-log':'expert',integrations:'expert',sealed:'expert'};
  let data=null, prefs=null, draft=null, section=null, generation=0, connectionBusy=false, checkTimer=null, statusTimer=null;
  let dialogs=null, moved=[], query='', reveal=new Set(), editing=false;
  let autoTried=false, routeDirty=false, checkFailure=null;
  let live=null, liveTimer=null, visited=0, recordedStep=null, shownSession=null, methodShown=false;
  let shownStep=null, shownStage=null, levelChosen=false, moreOpen=false, moreConnection=false;
  let groupScope=null, scopeDirty=false, history=null, historyLoading=null, undo=null, undoTimer=null;
  let sheet=null, sheetFor=null, pressed=false, focusHint=null, shownForm=null, historyFocus=false;
  const formSection=id=>id==='evidence-form'?'protection':'notifications';
  const tools=[['sources','sources:green','Recording rules'],['parameters','settings:slate','Parameters'],['access','users:blue','Access'],
    ['integrations','link:violet','Integrations / MCP'],['system-log','table:slate','System log'],['sealed','braces:indigo','GitHub Actions']];
  const hints={continuous:'Keep recording new messages and their changes after setup.',
    files:'Larger files are recorded without downloading their contents.',
    timestamps:'Independent services confirm when records existed.',
    drand:'Adds a public randomness beacon to records so their recording time can be checked.',
    notifications:'Sends a message when recording stops or needs attention.',
    replica:'Keeps a copy of the journal in storage you choose.',
    outside:'Timestamps, notifications and off-site copies contact services outside Telegram.'};
  const sections=['appearance','level','goal','connection','telegram','chats','collection','protection','notifications','group'];
  let preferencesQueue=Promise.resolve(), draftQueue=Promise.resolve(), preferencesSequence=0, draftSequence=0, checkSequence=0;
  const owner=()=>({generation,profile:state.profile,token:state.token,revision:state.workspaceRevision});
  const signedIn=()=>{const account=accountState(state.status||{});return account.hasSession&&!account.needsSignIn;};
  const current=who=>who.generation===generation&&who.profile===state.profile&&who.token===state.token&&who.revision===state.workspaceRevision;
  function requireOwner(who){
    if(!current(who))throw ctx.staleView();
  }
  async function request(who,path,body){
    requireOwner(who);
    const result=await json(path,body,{profile:who.profile,token:who.token});
    requireOwner(who);return result;
  }
  async function confirm(who,message){
    requireOwner(who);const accepted=await askConfirm(message);requireOwner(who);return accepted;
  }
  async function refresh(who){requireOwner(who);await refreshStatus();requireOwner(who);}
  const label=(value)=>tr({copy:'Just download',watch:'Follow chats',evidence:'Evidence',photos:'Photos up to 20 MB',
    short_media:'Photos and videos up to 60 seconds / 20 MB',all:'All files up to 1 GB',custom:'Custom file limits',
    auto:'Automatic',hide:'No, hide it',simple:'Simple',standard:'Standard',expert:'Expert',
    account:'All chats',selected:'Choose chats',folder:'Telegram folder',warp:'Cloudflare WARP',proxy:'My proxy',direct:'Direct',
    mtproxy_auto:'Automatic',mtproxy:'My proxy',socks5:'My proxy',http:'My proxy',vpn:'VPN'}[value]||String(value));
  const describe=value=>typeof value==='boolean'?tr(value?'On':'Off'):label(value);
  const sharedNames={goal:'Goal',monitoring:'What to record',recheck:'Recheck schedule',alert_rules:'Notification rules',
    reports:'Report settings',route:'Connection route'};
  const groupView=createGroupSettings({json,tr,trn:ctx.trn,node,toast,askConfirm,button,message,cards,label,describe,goals,run,root,
    fields:()=>data?.fields||[],openConnection:ctx.openConnection,back:async()=>{groupScope=null;data=await request(owner(),'settings');render();}});
  function button(text, fn, style='secondary') { const el=node('button',style,tr(text));el.type='button';el.onclick=()=>run(fn,el);return el; }
  const within=()=>section&&sheet?.firstChild?sheet:root;
  function focusMark(){
    const el=document.activeElement;if(!el?.closest?.('.hub-sheet,#view-settings'))return null;
    if(el.closest('.hub-undo'))return {find:section?'#hub-sheet-title':'.hub-heading h1',index:-1};
    const row=el.closest('[data-setting]');
    if(row){
      const pool=el.matches('.hub-choice')?'.hub-choice':el.matches('input,select')?'input,select':'button';
      return {find:'[data-setting="'+CSS.escape(row.dataset.setting)+'"]',pool,index:[...row.querySelectorAll(pool)].indexOf(el)};
    }
    const answer=el.closest('[data-answer]');
    if(answer)return {find:'[data-answer="'+CSS.escape(answer.dataset.answer)+'"]',index:-1};
    const entry=el.closest('.hub-summary[data-section]');
    return entry?{find:'.hub-summary[data-section="'+CSS.escape(entry.dataset.section)+'"]',index:-1}:null;
  }
  function refocus(mark){
    const row=mark&&within().querySelector(mark.find);
    (mark?.index>=0?row?.querySelectorAll(mark.pool)[mark.index]:row)?.focus({preventScroll:true});
  }
  async function run(fn, control) {
    const mark=focusMark();if(mark)focusHint=mark;if(control)control.disabled=true;
    try{return await fn();}catch(e){
      if(e.name==='StaleView')return;
      toast(e.message,true);
      const said=section&&sheet?.querySelector('.hub-sheet-said');
      if(said)said.textContent=e.message;
    }
    finally{if(control?.isConnected)control.disabled=false;if(focusHint===mark)focusHint=null;}
  }
  function message(text, cls='hint') { return node('p',cls,tr(text)); }
  function select(text, choices, value, fn) {
    const wrap=node('label','hub-label',tr(text)), el=node('select');
    for(const [key,name] of choices)el.append(new Option(tr(name),key));el.value=value;el.onchange=()=>run(()=>fn(el.value));wrap.append(el);return wrap;
  }
  function glyph(mark, cls) {
    const [name, tone] = String(mark).split(':'), el = node('span', cls + (tone ? ' tile' : ''));
    if (!tone) { el.textContent = mark; return el; }
    el.dataset.tone = tone; el.append(ctx.icon(name)); return el;
  }
  function cards(box, entries, value, fn) {
    const group=node('div','answer-cards');group.setAttribute('role','group');
    for(const [key,emoji,name,note] of entries){
      const b=button('',()=>fn(key),'answer-card');b.dataset.answer=key;b.setAttribute('aria-pressed',String(key===value));
      b.append(glyph(emoji,'answer-icon'),node('strong','',tr(name)),node('span','hint',tr(note)));group.append(b);
    }box.append(group);
  }
  function heading(){const box=node('div','hub-heading'),title=node('h1','',tr('Settings'));title.tabIndex=-1;box.append(title);return box;}
  function closed(text){
    const box=node('div','hub-closed'),mark=glyph('settings:slate','hub-closed-mark');
    box.append(mark,message(text));section=null;closeSheet();root.replaceChildren(heading(),box);
  }
  function restoreMoved(){for(const [el,marker] of moved){marker.replaceWith(el);}moved=[];}
  function move(el, host){if(!el)return;const marker=document.createComment('settings-form');el.before(marker);host.append(el);moved.push([el,marker]);}
  function lastLevel(){try{const value=localStorage.getItem('tgwitness-ui-level');return ['simple','standard','expert'].includes(value)?value:'simple';}catch{return 'simple';}}
  function applyPresentation() {
    if(!prefs)return;
    ctx.catalog();
    document.documentElement.dataset.uiLevel=prefs.level;
    try{localStorage.setItem('tgwitness-ui-level',prefs.level);}catch{}
    for(const b of document.querySelectorAll('.sidebar .nav[data-view]'))b.dataset.level=navLevels[b.dataset.view]||'expert';
    for(const [view,simple,full] of [['start','Home','Home'],['observations','Journal','Journal'],['evidence','Exports','Exports']]){
      const b=document.querySelector('.sidebar [data-view="'+view+'"]');
      const text=[...b.childNodes].find(n=>n.nodeType===3&&n.textContent.trim());if(text)text.textContent=' '+tr(prefs.level==='simple'?simple:full)+' ';
    }
    for(const control of document.querySelectorAll('[data-ui-level]'))control.value=prefs.level;
    ctx.applyPreferences(prefs);
  }
  function savePreferences(patch,who=owner()){
    requireOwner(who);
    prefs={...prefs,...patch};const body={...prefs}, sequence=++preferencesSequence;
    preferencesQueue=preferencesQueue.catch(()=>{}).then(async()=>{
      const result=await request(who,'preferences',body);
      if(sequence===preferencesSequence){prefs=result.saved;applyPresentation();}
    });return preferencesQueue;
  }
  async function bootstrap({openFirstRun=true}={}) {
    const who=owner(), initialRoute=location.href, draftVersion=draftSequence, preferenceVersion=preferencesSequence;
    const demo=state.status?.demo||window.TGW_ONLINE_DEMO;
    for(const control of document.querySelectorAll('[data-ui-level]'))control.hidden=!!demo;
    if(demo){$('hub-route-status').hidden=true;return;}
    const loaded=await request(who,'preferences');
    if(preferenceVersion===preferencesSequence)prefs=loaded.saved||{language:ctx.language,timezone:Intl.DateTimeFormat().resolvedOptions().timeZone||'UTC',theme:'system',level:lastLevel(),...(prefs||{})};
    const requestedLanguage=new URL(location.href).searchParams.get('lang');
    if(requestedLanguage===ctx.language&&prefs.language!==requestedLanguage)await savePreferences({language:requestedLanguage},who);
    else if(!loaded.saved)await savePreferences({},who);else applyPresentation();
    requireOwner(who);
    if(prefs.language!==ctx.language){await ctx.changeLanguage(prefs.language);return;}
    if(!state.me?.admin||state.status?.demo)return;
    const loadedSettings=await request(who,'settings');
    if(draftVersion!==draftSequence){scheduleStatus();return;}
    data=loadedSettings;draft={...data.wizard};
    if(openFirstRun&&location.href===initialRoute&&!draft.completed&&!draft.skipped)await navigate('first-run');
    requireOwner(who);
    scheduleStatus();
  }
  async function load(wanted=null,hub){
    const who=owner();
    if(hub!==undefined&&state.view==='settings'){
      const next=sections.includes(hub)?hub:null;
      if(section==='chats'&&scopeDirty&&next!=='chats'&&!await confirm(who,tr('Leave without saving the chat selection?'))){ctx.record?.();return;}
      if(next!==section)scopeDirty=false;
      section=next;query='';
    }
    if(state.status?.demo){closed('Demo workspace. Connect accounts in your live installation.');return;}
    if(!state.me?.admin){closed('Only the workspace administrator can change collection settings.');return;}
    if(!prefs){const result=await request(who,'preferences');prefs=result.saved||{language:ctx.language,timezone:Intl.DateTimeFormat().resolvedOptions().timeZone||'UTC',theme:'system',level:lastLevel(),...(prefs||{})};applyPresentation();}
    data=await request(who,'settings');draft={...data.wizard};
    visited=Math.max(visited,draft.step);
    if(state.view==='first-run'&&wanted&&wanted!==draft.step&&wanted<=visited&&!live){
      recordedStep=wanted;
      try{await saveDraft({step:wanted},who);}catch(error){if(error.name==='StaleView')throw error;toast(error.message,true);recordedStep=null;}
    }
    if(state.view==='first-run')await renderWizard(who);else render();
    requireOwner(who);
    updateIndicator(data.connection);
  }
  function saveDraft(patch={},who=owner()){
    requireOwner(who);
    draft={...draft,...patch};const body=draftBody(), sequence=++draftSequence;
    draftQueue=draftQueue.catch(()=>{}).then(async()=>{
      let result;
      try{result=await request(who,'first-run',body);}catch(error){
        if(current(who)&&sequence===draftSequence&&data?.wizard)draft={...data.wizard};
        throw error;
      }
      data=result;if(sequence===draftSequence)draft={...result.wizard};
    });return draftQueue;
  }
  async function applyGoal(goal,{first=false,keep=false,quiet=false}={},who=owner()){
    const plan=await request(who,'settings/goal/preview',{goal,keep_manual:keep});
    const text=plan.diff.map(row=>tr(data.fields.find(f=>f.key===row.key)?.label||row.key)+': '+describe(row.before)+' → '+describe(row.after)).join('\n');
    if(!first&&!quiet&&!await confirm(who,tr('Change goal?')+'\n\n'+(text||tr('The settings already match.'))))return false;
    const before={...data.values},goalBefore=data.goal;
    data=await request(who,'settings/goal',{goal,revision:plan.revision,keep_manual:keep});
    if(quiet)saved(before,goalBefore);
    await refresh(who);return true;
  }
  const fieldLabel=key=>key==='goal'?tr('Goal'):tr(data.fields.find(f=>f.key===key)?.label||key);
  function saved(before,goalBefore){
    history=null;
    const keys=Object.keys(data.values).filter(k=>JSON.stringify(data.values[k])!==JSON.stringify(before[k]));
    const parts=[...(goalBefore!==data.goal?[fieldLabel('goal')+': '+label(data.goal)]:[]),...keys.map(k=>fieldLabel(k)+': '+describe(data.values[k]))];
    if(!parts.length)return;
    showUndo(tr('Saved')+' · '+parts.slice(0,2).join(' · ')+(parts.length>2?' · +'+(parts.length-2):''),restoreLatest);
  }
  function showUndo(text,action){
    undo={text,action};paintUndo();clearTimeout(undoTimer);
    undoTimer=setTimeout(()=>{undo=null;paintUndo();},20000);
  }
  function paintUndo(){
    const shown=undo&&state.view==='settings',host=section&&sheet?.open?sheet.querySelector('.hub-sheet-body'):root;
    for(const old of [...root.querySelectorAll('.hub-undo'),...(sheet?.querySelectorAll('.hub-undo')||[])])if(!shown||old.parentElement!==host)old.remove();
    if(!shown||!host)return;
    let bar=host.querySelector(':scope>.hub-undo');
    if(!bar){bar=node('div','hub-undo');bar.setAttribute('role','status');host.append(bar);}
    const act=button('Undo',async()=>{const action=undo?.action;undo=null;paintUndo();if(action)await action();},'hub-undo-action');
    const close=button('',()=>{undo=null;paintUndo();},'hub-undo-close');close.append(ctx.icon('x'));close.setAttribute('aria-label',tr('Close'));
    bar.replaceChildren(node('span','hub-undo-text',undo.text),act,close);
  }
  async function loadHistory(who=owner()){
    if(history)return history;
    if(!historyLoading)historyLoading=request(who,'settings/history').then(result=>{history=result.changes;return history;}).finally(()=>{historyLoading=null;});
    return historyLoading;
  }
  async function restoreChange(seq,who=owner()){
    data=await request(who,'settings/restore',{seq,revision:data.revision});draft={...data.wizard};editing=false;history=null;
    await refresh(who);if(current(who)&&state.view==='settings')render();toast(tr('Change undone.'));
  }
  async function restoreLatest(){
    const who=owner(),rows=await loadHistory(who);
    if(rows?.length)await restoreChange(rows[0].seq,who);
  }
  function changeText(row){
    const parts=row.changes.map(c=>fieldLabel(c.key)+': '+describe(c.before)+' → '+describe(c.after));
    if('goal_after' in row)parts.unshift(fieldLabel('goal')+': '+(row.goal_before?label(row.goal_before):tr('Not chosen'))+' → '+(row.goal_after?label(row.goal_after):tr('Not chosen')));
    return parts.join(' · ');
  }
  function historyCard(box){
    const card=node('section','hub-history');card.hidden=true;box.append(card);
    loadHistory().then(rows=>{
      if(!card.isConnected||!rows?.length)return;
      card.hidden=false;card.replaceChildren(node('h2','',tr('Recent changes')));
      const list=node('ol','hub-history-list');
      for(const row of rows.slice(0,5)){
        const item=node('li','hub-history-row'),time=node('time','hint',new Date(row.at).toLocaleString(prefs.language,{timeZone:prefs.timezone,dateStyle:'medium',timeStyle:'short'}));
        time.dateTime=row.at;
        item.append(node('span','hub-history-text',(row.restored?tr('Undo of an earlier change')+' · ':'')+changeText(row)),time,
          button('Undo',()=>{historyFocus=true;return restoreChange(row.seq);},'text-link'));
        list.append(item);
      }
      card.append(list);
      if(historyFocus&&[document.body,null].includes(document.activeElement))list.querySelector('.text-link')?.focus({preventScroll:true});
      historyFocus=false;
    }).catch(()=>{});
  }
  async function edit(key,value,who=owner()){
    requireOwner(who);let values={...data.values},goalBefore=data.goal;
    try{
      let allow_outside=false,disable_dependents=false;
      if(['timestamps','drand','notifications','replica'].includes(key)&&value&&!values.outside){
        allow_outside=await confirm(who,tr('This feature needs external requests. Allow them?'));if(!allow_outside)return;
      }
      if(key==='outside'&&!value&&(values.timestamps||values.drand||values.notifications||values.replica)){
        disable_dependents=await confirm(who,tr('Turn off the dependent features too?'));if(!disable_dependents)return;
      }
      const send=()=>request(who,'settings/edit',{key,value,allow_outside,disable_dependents,revision:data.revision});
      let next;
      try{next=await send();}catch(error){
        if(error.status!==409)throw error;
        data=await request(who,'settings');values={...data.values};goalBefore=data.goal;next=await send();
      }
      data=next;saved(values,goalBefore);await refresh(who);
    }finally{if(current(who)&&state.view==='settings')render();}
  }
  function preferencesForm(box,{language=true}={}){
    if(language){const row=select('Language',Object.entries(ctx.languages),prefs.language,async value=>{const who=owner();await savePreferences({language:value},who);requireOwner(who);await ctx.changeLanguage(value);});
      row.dataset.setting='language';box.append(row);}
    const remember=(patch,text)=>{const before=Object.fromEntries(Object.keys(patch).map(k=>[k,prefs[k]]));
      return savePreferences(patch).then(()=>{if(state.view==='settings')showUndo(tr('Saved')+' · '+text,async()=>{await savePreferences(before);if(state.view==='settings')render();});});};
    const themes=[['system','System theme'],['light','Light theme'],['dark','Dark theme']];
    const theme=node('div','hub-choices');theme.setAttribute('role','group');theme.setAttribute('aria-label',tr('Theme'));
    for(const [value,name] of themes){const b=button(name,async()=>{await remember({theme:value},tr(name));render();},'hub-choice');b.setAttribute('aria-pressed',String(prefs.theme===value));theme.append(b);}
    const themeLabel=node('div','hub-label');themeLabel.dataset.setting='theme';themeLabel.append(node('span','',tr('Theme')),theme);box.append(themeLabel);
    const device=Intl.DateTimeFormat().resolvedOptions().timeZone||'UTC';
    const zones=[...new Set([prefs.timezone,device,'UTC',...(Intl.supportedValuesOf?.('timeZone')||[])])];
    const zone=select('Time zone',zones.map(x=>[x,x===device?x+' · '+tr('this device'):x]),prefs.timezone,value=>remember({timezone:value},value));
    zone.dataset.setting='timezone';box.append(zone);
  }
  function fieldRow(f){
    const row=node('div','hub-field');row.dataset.level=f.level;row.dataset.setting=f.key;
    const text=node('div','hub-field-text');text.append(node('strong','',tr(f.label)));
    if(hints[f.key])text.append(node('span','hint',tr(hints[f.key])));
    const mark=inheritMark(f.key);
    if(mark)text.append(mark);else if(f.modified)text.append(node('span','modified-tag',tr('Changed by you')));
    row.append(text);
    if(f.type==='bool'){
      const wrap=node('label','hub-switch'),control=node('input');control.type='checkbox';control.setAttribute('role','switch');control.checked=f.value;
      control.setAttribute('aria-label',tr(f.label));control.onchange=()=>run(()=>edit(f.key,control.checked),control);
      wrap.append(control,node('span','hub-switch-track'));row.append(wrap);
    }else if(f.key==='files'){
      row.classList.add('hub-field-wide');
      const group=node('div','hub-choices');group.setAttribute('role','group');group.setAttribute('aria-label',tr(f.label));
      for(const value of ['photos','short_media','all']){const b=button(label(value),()=>edit(f.key,value),'hub-choice');b.setAttribute('aria-pressed',String(f.value===value));group.append(b);}
      row.append(group);
      if(f.value==='custom')row.append(message('Custom file limits are set in Parameters. Pick an option to replace them.','hint hub-field-note'));
    }else{
      const field=select(f.label,['hide','auto'].map(v=>[v,label(v)]),f.value,v=>edit(f.key,v));row.append(field);
    }
    if(f.modified&&!mark)row.append(button('Restore goal value',async()=>{
      const who=owner(),plan=await request(who,'settings/goal/preview',{goal:data.goal});await edit(f.key,plan.values[f.key],who);
    },'text-link'));
    return row;
  }
  const inherited=key=>data?.inheritance?.keys?.[key];
  async function adoptGroup(keys,who=owner()){
    requireOwner(who);
    await json('profile-groups/'+encodeURIComponent(data.inheritance.group.id)+'/settings/adopt',{profiles:[who.profile],keys},{root:true,token:who.token});
    data=await request(who,'settings');render();await refresh(who);
  }
  function revertKey(key){
    const item=inherited(key);
    if(key==='route')return ctx.openConnection({scope:'account',mode:item.group_value.mode});
    if(data.fields.some(f=>f.key===key))return edit(key,item.group_value);
    return adoptGroup([key]);
  }
  function inheritMark(key){
    const item=inherited(key);if(!item)return null;
    const box=node('span','inherit-mark '+item.source);box.dataset.inherit=item.source;
    const source=node('span','inherit-source');source.append(ctx.icon(item.source==='group'?'link':'edit'),document.createTextNode(tr(item.source==='group'?'From the group':'Own value')));box.append(source);
    if(item.source==='own')box.append(button('Return to the group value',()=>revertKey(key),'text-link'));
    return box;
  }
  function sharedName(key){return key.startsWith('parameter:')?data.parameters.find(p=>p.key===key)?.label||key:sharedNames[key]||key;}
  async function openGroup(id){await groupView.load(id);groupScope=id;section=null;query='';render();}
  function openSection(name){section=name;query='';scopeDirty=false;shownForm=null;render();ctx.record?.();}
  async function closeSection(){
    if(!section)return;
    if(section==='chats'&&scopeDirty&&!await confirm(owner(),tr('Leave without saving the chat selection?')))return;
    if(shownForm&&$(shownForm)?.dataset.dirty==='true'&&!await confirm(owner(),tr('Leave without saving the changes in this form?')))return;
    const who=owner(),from=section;draft={...data.wizard};editing=false;scopeDirty=false;section=null;shownForm=null;render();ctx.record?.();
    (root.querySelector('.hub-summary[data-section="'+from+'"]')||root.querySelector('.hub-summary[data-section]'))?.focus({preventScroll:true});
    const before=JSON.stringify(data);data=await request(who,'settings');
    if(!section){draft={...data.wizard};if(state.view==='settings'&&JSON.stringify(data)!==before)render();}
  }
  function ensureSheet(){
    if(!sheet){
      sheet=node('dialog','hub-sheet');sheet.setAttribute('aria-labelledby','hub-sheet-title');
      sheet.addEventListener('cancel',event=>{if(event.target!==sheet)return;event.preventDefault();void run(closeSection);});
      sheet.addEventListener('close',event=>{
        if(event.target!==sheet||!section||sheet.open||state.view!=='settings')return;
        section=null;shownForm=null;editing=false;scopeDirty=false;if(data)draft={...data.wizard};
        window.TgWitnessDialogs?.closeAll();render();ctx.record?.();
      });
      sheet.addEventListener('pointerdown',event=>{pressed=event.target===sheet;});
      sheet.addEventListener('click',event=>{if(pressed&&event.target===sheet&&event.detail<2)void run(closeSection);pressed=false;});
    }
    if(!sheet.isConnected)(root.parentElement||document.body).append(sheet);
    return sheet;
  }
  function closeSheet(){
    restoreMoved();sheetFor=null;if(!sheet)return;
    if(sheet.open)sheet.close();
    sheet.replaceChildren();
  }
  function summaryRows(){
    const inheritance=data.inheritance,connected=fresh(data.connection);
    const rows=[['telegram','Telegram account',tr(accountState(state.status||{}).needsSignIn?'Sign in again':state.status?.collector?.connected?'Connected':signedIn()?'Session found':'Not connected'),state.status?.collector?.connected?'ok':'warn','account:blue'],
      ['chats','Which chats?',label(data.wizard.scope||'account')+(data.wizard.scope==='selected'?' · '+(data.wizard.chat_ids?.length||0):''),'ok','message:green'],
      ['connection','Connection',label(data.connection.mode)+(connected?' · '+tr('Working · {n} ms',{n:data.connection.check.latency_ms}):''),connected?'ok':'warn','shield:teal'],
      ['appearance','Language, time and appearance',ctx.languages[prefs.language]+' · '+prefs.timezone+' · '+label(prefs.level),'none','sun:orange'],
      ['goal','Goal',data.goal?label(data.goal):tr('Not chosen'),'none','star:pink'],
      ['collection','Collection and files',label(data.values.files),'none','archive:indigo'],
      ['protection','Record protection',tr(data.values.timestamps?'On':'Off'),data.values.timestamps?'ok':'off','lock:violet'],
      ['notifications','Notifications and off-site copy',tr(data.values.notifications?'On':'Off'),data.values.notifications?'ok':'off','bell:red'],
      ['level','Interface level',label(prefs.level),'none','settings:slate']];
    if(inheritance){
      const keys=Object.values(inheritance.keys),own=keys.filter(k=>k.source==='own').length;
      rows.push(['group','Shared with the group',inheritance.group.label+' · '+(own?ctx.trn('{n} own value','{n} own values',own):tr('follows the group')),'none','link:teal']);
    }
    return rows;
  }
  function arrow(){const el=node('span','hub-arrow');el.append(ctx.icon('chevron'));return el;}
  function listGroup(box,caption){
    const group=node('section','hub-group'),list=node('div','hub-list');
    group.append(node('h2','hub-caption',caption));
    group.append(list);box.append(group);return list;
  }
  function summaryRow(box,[id,name,summary,tone,icon]){
    const b=button('',()=>openSection(id),'hub-summary');b.dataset.section=id;b.dataset.tone=tone;
    const line=node('span','hub-summary-value');if(tone!=='none')line.append(node('span','hub-dot'));line.append(document.createTextNode(summary));
    b.append(glyph(icon,'hub-summary-icon'),node('strong','',tr(name)),line,arrow());box.append(b);
  }
  function toolRow(box,icon,text,fn,level){
    const b=button('',fn,'hub-summary hub-tool');if(level)b.dataset.level=level;
    b.append(glyph(icon,'hub-summary-icon'),node('strong','',tr(text)),arrow());box.append(b);
  }
  function profileCard(box,[id,,summary,tone]){
    const account=state.status?.collector?.account,name=ctx.profile()?.label||tr('Telegram account');
    const b=button('',()=>openSection(id),'hub-summary hub-profile');b.dataset.section=id;b.dataset.tone=tone;
    const who=node('span','hub-profile-who');
    who.append(node('strong','',name),node('span','hub-profile-id',account?(account.username?'@'+account.username+' · ':'')+'ID '+account.id:tr('No Telegram account yet')));
    const line=node('span','hub-summary-value');line.append(node('span','hub-dot'),document.createTextNode(summary));
    b.append(ctx.avatar(account?.id??null,account?.username||name,'xl'),who,line,arrow());box.append(b);
  }
  function autoCard(box){
    const modified=data.fields.filter(f=>f.modified);
    const card=node('section','hub-auto'+(modified.length?' changed':'')),head=node('div','hub-auto-head');
    head.append(glyph(modified.length?'edit:orange':'sparkle:violet','hub-auto-icon'),node('strong','',tr(modified.length?'Some settings differ from the recommended ones':'Recommended settings are on')));
    const chips=node('dl','hub-chips');
    for(const [key,value] of [['files',label(data.values.files)],['timestamps',tr(data.values.timestamps?'On':'Off')],
      ['notifications',tr(data.values.notifications?'On':'Off')],['outside',tr(data.values.outside?'On':'Off')]]){
      const chip=node('div','hub-chip');chip.append(node('dt','',fieldLabel(key)),node('dd','',value));chips.append(chip);
    }
    const actions=node('div','hub-actions');
    if(modified.length&&data.goal)actions.append(button('Return to recommended',()=>applyGoal(data.goal,{quiet:true}).then(()=>render()),'secondary'));
    actions.append(button('Undo last change',restoreLatest,'quiet hub-undo-last'));
    card.append(head,message(data.goal?tr('Chosen for “{goal}”. Change only what you need: every change can be undone.',{goal:label(data.goal)})
      :tr('Safe defaults are in use. Change only what you need: every change can be undone.')),chips,actions);box.append(card);
    loadHistory().then(rows=>{const last=card.querySelector('.hub-undo-last');if(last)last.hidden=!rows?.length;}).catch(()=>{});
    card.querySelector('.hub-undo-last').hidden=!history?.length;
  }
  function render(){
    restoreMoved();if(!data||!prefs)return;
    if(groupScope&&groupView.data){closeSheet();groupView.render(root);return;}
    const mark=focusMark()||([document.body,sheet,null].includes(document.activeElement)?focusHint:null);
    root.replaceChildren();
    root.append(heading());
    const inheritance=data.inheritance;
    if(section==='group'&&!inheritance)section=null;
    if(inheritance){
      const note=node('div','notice hub-group-note');
      note.append(node('span','',tr('This account is in the group {name}.',{name:inheritance.group.label})),
        button('Group settings',()=>openGroup(inheritance.group.id),'text-link'));
      root.append(note);
    }
    const summaries=summaryRows(),entry=id=>summaries.find(row=>row[0]===id);
    const overview=node('div','hub-overview'),lists=node('div','hub-lists'),side=node('div','hub-side');overview.append(lists,side);root.append(overview);
    profileCard(lists,entry('telegram'));
    const search=node('input','hub-search');search.type='search';search.placeholder=tr('Search all settings, including hidden ones');search.setAttribute('aria-label',search.placeholder);search.value=query;
    const results=node('div','hub-results hub-list'),groups=node('div','hub-groups');
    search.oninput=()=>{query=search.value;renderResults(results);};lists.append(search,results,groups);
    for(const [caption,ids] of [[tr('Account'),['chats','connection']],[tr('Recording'),['goal','collection','protection','notifications','group']],[tr('Panel'),['appearance']]]){
      const list=listGroup(groups,caption);
      for(const id of ids)if(entry(id))summaryRow(list,entry(id));
    }
    const more=listGroup(groups,tr('More tools'));
    for(const [view,icon,text] of tools)toolRow(more,icon,text,()=>openAdvanced(view),navLevels[view]);
    toolRow(more,'sparkle:orange','Open first setup',async()=>{await saveDraft({step:1});await navigate('first-run');});
    autoCard(side);historyCard(side);
    if(data.recommendations.length)side.append(message('Recommended: an off-site copy, a witness bot and a code check.','notice'));
    renderResults(results);
    if(section&&state.view==='settings')renderSheet(summaries,inheritance);else closeSheet();
    paintUndo();refocus(mark);
  }
  function renderSheet(summaries,inheritance){
    const box=ensureSheet(),same=box.open&&sheetFor===section,top=same?box.querySelector('.hub-sheet-body')?.scrollTop||0:0;
    sheetFor=section;box.replaceChildren();
    const bar=node('div','hub-detail-bar'),back=button('',closeSection,'icon-btn hub-back'),close=button('',closeSection,'icon-btn hub-close');
    back.append(ctx.icon('chevron'));back.setAttribute('aria-label',tr('Back to settings'));back.title=tr('Back to settings');
    close.append(ctx.icon('x'));close.setAttribute('aria-label',tr('Close'));close.title=tr('Close');
    const heading=node('h2','',tr(summaries.find(s=>s[0]===section)?.[1]||'Settings'));heading.id='hub-sheet-title';heading.tabIndex=-1;
    bar.append(back,heading,close);
    const body=node('div','hub-sheet-body'),detail=node('section','hub-detail'),said=node('p','visually-hidden hub-sheet-said');
    said.setAttribute('role','alert');body.append(detail);box.append(bar,body,said);
    if(section==='appearance')preferencesForm(detail);
    if(section==='appearance'||section==='level'){
      if(section==='appearance')detail.append(node('h3','hub-subtitle',tr('Interface level')));
      cards(detail,levels,prefs.level,async level=>{const before=prefs.level;await savePreferences({level});render();
        showUndo(tr('Saved')+' · '+label(level),async()=>{await savePreferences({level:before});render();});});
    }
    if(section==='group'&&inheritance){
      const keys=Object.keys(inheritance.keys).filter(k=>k!=='goal'&&!data.fields.some(f=>f.key===k));
      detail.append(message(keys.length?'Settings the group shares besides those in the other sections:':'The group shares only settings shown in the other sections.'));
      for(const key of keys){
        const row=node('div','hub-field');row.dataset.setting=key;const heading=node('div');
        heading.append(node('strong','',tr(sharedName(key))),inheritMark(key));row.append(heading);detail.append(row);
      }
      detail.append(button('Group settings',()=>openGroup(inheritance.group.id)));
    }
    if(section==='goal'){
      const goalMark=inheritMark('goal');if(goalMark)detail.append(goalMark);
      detail.append(message('A goal sets files, timestamps and notifications at once. You can undo it right after.'));
      cards(detail,goals,data.goal,async goal=>{if(goal===data.goal)return;await applyGoal(goal,{quiet:true});render();});
    }
    if(section==='connection')connectionForm(detail,false);
    if(section==='telegram'&&signedIn()&&window.TgWitnessDocumentation)detail.append(button('Profile',async()=>{await closeSection();await window.TgWitnessDocumentation.openAccount();}));
    if(section==='telegram')move(ctx.authCard(),detail);
    if(section==='chats'){detail.append(message('Choose all chats, individual chats or a Telegram folder.'));
      const box=node('div','hub-chats');detail.append(box);void chatsForm(box,owner(),true).catch(e=>{if(e.name!=='StaleView')box.append(message(e.message,'notice warning'));});detail.append(button('Pseudo-secret',async()=>{if(scopeDirty&&!await confirm(owner(),tr('Leave without saving the chat selection?')))return;scopeDirty=false;await navigate('secret-chats');}));}
    const fields=section==='connection'?[]:data.fields.filter(f=>f.section===section);
    const above=fields.filter(f=>rank[f.level]>rank[prefs.level]&&!reveal.has(section)),hidden=above.length<fields.length?above:[];
    for(const f of fields.filter(f=>!hidden.includes(f)))detail.append(fieldRow(f));
    if(hidden.length){const more=node('details','hub-more-options');more.append(node('summary','',trn('Show {n} more setting','Show {n} more settings',hidden.length)));
      for(const f of hidden)more.append(fieldRow(f));detail.append(more);}
    if(section==='notifications'){
      if(data.needs_notification_destination)detail.append(message('Notifications are enabled. Add a destination to receive them.','notice warning'));
      const actions=node('div','hub-actions');actions.append(button('Notification destinations',()=>openForm('alerts-form')),button('Off-site copy',()=>openForm('replica-form')));detail.append(actions);
    }
    if(section==='protection'){const actions=node('div','hub-actions');actions.append(button('Advanced protection settings',()=>openForm('evidence-form')));detail.append(actions);}
    if(data.collection_problem&&section==='collection')detail.append(message('Collection could not start. Check the connection and selected chats.','notice warning'));
    if(data.outside_problem&&['connection','protection','notifications'].includes(section))detail.append(message('External services need a working SOCKS5 or WARP route.','notice warning'));
    if(shownForm&&formSection(shownForm)===section)move($(shownForm),detail);
    if(!box.open)box.showModal();
    if(!same)heading.focus({preventScroll:true});
    body.scrollTop=top;
  }
  function renderResults(box){
    box.replaceChildren();root.querySelector('.hub-groups')?.toggleAttribute('hidden',!!query.trim());
    if(!query.trim())return;
    const q=query.trim().toLocaleLowerCase();
    const own=[['language','Language','[data-setting="language"]'],['theme','Theme','[data-setting="theme"]'],['timezone','Time zone','[data-setting="timezone"]'],
      ['level','Interface level','[data-answer]']].map(([key,label,find])=>({key,label,find,section:'appearance',level:'simple'}));
    const all=[...own,...data.fields,...data.parameters,...[...ctx.catalog()].map(f=>({...f,label:tr(f.label)}))];
    const matches=all.filter(f=>(tr(f.label)+' '+f.key).toLocaleLowerCase().includes(q));
    if(!matches.length)box.append(message('No settings found.','hint hub-empty'));
    for(const f of matches.slice(0,80)){
      const hidden=rank[f.level]>rank[prefs.level];
      const b=button('',async()=>{
        if(['alerts-form','replica-form','evidence-form'].includes(f.form))await openForm(f.form,f.id);
        else if(f.view)await openAdvanced(f.view,f.extra,f.id);
        else if(f.key.startsWith('parameter:'))await openAdvanced('parameters',null,'parameter-'+f.key.slice(10));
        else{reveal.add(f.section);openSection(f.section);
          const row=within().querySelector(f.find||'[data-setting="'+CSS.escape(f.key)+'"]');
          row?.scrollIntoView({block:'center'});(row?.matches('button,input,select,textarea')?row:row?.querySelector('input,select,textarea,button'))?.focus({preventScroll:true});}
      },'hub-summary hub-result');b.dataset.level=f.level;
      b.append(node('strong','',tr(f.label)),node('span','hub-summary-value',hidden?label(f.level):''),arrow());box.append(b);
    }
  }
  async function openForm(id, focus){
    const who=owner();
    section=formSection(id);shownForm=id;query='';render();ctx.record?.();
    const detail=sheet.querySelector('.hub-detail'),form=$(id);
    await ctx.loadSettingsForm(id);
    requireOwner(who);
    const control=focus?$(focus):form;
    for(let p=control.parentElement;p&&p!==detail;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;
    control.scrollIntoView({block:'center'});if(focus)control.focus();
  }
  async function openAdvanced(view, extra, id){
    const who=owner();
    restoreMoved();await navigate(view);
    requireOwner(who);
    const page=$('view-'+view);
    if(page&&!page.querySelector('.hub-back-link')){
      const link=button('Back to settings',()=>navigate('settings'),'text-link hub-back-link');page.prepend(link);
      const drop=event=>{if(event.detail?.view===view)return;link.remove();window.removeEventListener('tgwitness:route',drop);};
      window.addEventListener('tgwitness:route',drop);
    }
    if(extra)await ctx.openExtra(extra);
    requireOwner(who);
    if(id){const el=$(id);if(el){for(let p=el.parentElement;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;el.scrollIntoView({block:'center'});el.focus();}}
  }
  function connectionForm(box, first){
    const routeDraft=first?draft:(editing?draft:{...data.wizard,route:data.connection.strategy?.mode|| (data.connection.managed?'warp':data.connection.mode==='direct'?'direct':data.connection.mode==='mtproxy_auto'?'auto':'proxy'),allow_direct:data.connection.strategy?.allow_direct??data.connection.policy.exposure!=='hide'});
    if(!first){draft=routeDraft;editing=true;}
    const options=first?node('details','wizard-options'):null, routeBox=node('div'), extraBox=first?null:node('div');
    if(options){options.append(node('summary','',tr('Connection settings')),routeBox);options.open=prefs.level==='expert'||draft.route!=='auto'||!!draft.unchecked||!!checkFailure;}
    else box.append(routeBox);
    function updateRoutes(){routeBox.replaceChildren();cards(routeBox,routes,draft.route,async mode=>{
      const who=owner();
      if(connectionBusy)return;
      draft.route=mode;draft.unchecked=false;routeDirty=true;checkFailure=null;
      if(mode==='direct')draft.allow_direct=true;
      if(first)await saveDraft({step:4},who);requireOwner(who);updateRoutes();
      if(mode==='auto'||mode==='direct')await checkConnection(false,who);
    });
      const extra=first?routeBox:node('details','hub-more-options');
      if(!first){extra.append(node('summary','',tr('Advanced connection options')));extra.open=moreConnection;extra.ontoggle=()=>{moreConnection=extra.open;};}
      const protection=select('Can Telegram see this server’s address?',[['hide','No, hide it'],['allow','Only if nothing else works']],draft.allow_direct?'allow':'hide',async v=>{
        draft.allow_direct=v==='allow';draft.unchecked=false;routeDirty=true;if(!draft.allow_direct&&draft.route==='direct')draft.route='auto';
        if(first)await saveDraft({step:4});updateRoutes();updateNext();
      });extra.append(protection);
      if(!first&&data.fields.find(f=>f.key==='ip')?.modified){
        extra.append(message('Changed by you','modified-tag'),button('Restore goal value',async()=>{
          const who=owner(),plan=await request(who,'settings/goal/preview',{goal:data.goal});editing=false;await edit('ip',plan.values.ip,who);
        },'text-link'));
      }
      if(!first){for(const f of data.fields.filter(f=>f.section==='connection'&&f.key!=='ip'))extra.append(fieldRow(f));}
      if(draft.route==='proxy'){
        const input=node('input');input.type='password';input.id='hub-proxy';input.autocomplete='off';input.placeholder='tg://proxy, socks5://, http(s)://';input.setAttribute('aria-label',tr('Proxy address'));routeBox.append(input);
        input.oninput=()=>{routeDirty=true;updateNext();};
      }
      if(['auto','warp'].includes(draft.route))routeBox.append(message('Auto and WARP can download verified helpers and register this server with Cloudflare.'));
      routeBox.append(button(draft.route==='warp'?'Enable WARP':'Check connection',()=>checkConnection(draft.route==='warp')));
      if(!first)extraBox.replaceChildren(extra);
    }
    updateRoutes();
    const status=node('div','connection-result');status.id='hub-connection-result';status.setAttribute('role','status');box.append(status);
    if(extraBox)box.append(extraBox);
    if(options)box.append(options);
    if(connectionBusy){status.className='connection-result checking';status.textContent=tr('Checking connection…');}
    else if(checkFailure&&!fresh(data.connection))connectionFailed(checkFailure);
    else paintConnection(data.connection);
    if(first){const bypass=node('label','check-label');const check=node('input');check.type='checkbox';check.checked=!!draft.unchecked;
      check.onchange=()=>run(async()=>{const who=owner();draft.unchecked=check.checked;
        if(check.checked&&connectionBusy){checkSequence++;clearTimeout(checkTimer);await request(who,'connection/cancel',{});connectionBusy=false;}
        await saveDraft({step:4},who);updateNext();});
      bypass.append(check,document.createTextNode(tr('Continue without checking')));options.append(bypass);}
  }
  function openOptions(){const options=wizardRoot.querySelector('.wizard-options');if(options)options.open=true;}
  async function checkConnection(acceptSetup=false,who=owner()){
    requireOwner(who);
    if(connectionBusy)return;connectionBusy=true;checkFailure=null;updateNext();
    const profile=who.profile,attempt=++checkSequence;
    const currentAttempt=()=>current(who)&&checkSequence===attempt;
    const result=$('hub-connection-result');if(result){result.className='connection-result checking';result.textContent=tr('Checking connection…');}
    try{
      await request(who,'connection/prepare',{mode:draft.route,scope:'account',account:profile,
        allow_direct:draft.allow_direct,outside_enabled:data.values.outside,
        accept_setup:acceptSetup||draft.route==='auto',...(draft.route==='proxy'?{proxy_url:$('hub-proxy').value}:{})});
      const poll=async()=>{
        if(!currentAttempt())return;
        const current=await request(who,'connection');
        if(!currentAttempt())return;
        if(current.job.state==='ready'){await request(who,'connection/apply',{plan:current.job.plan});}
        else if(current.job.state==='applied'){
          if(current.job.rows.some(r=>!r.applied))throw new Error(current.job.rows.find(r=>!r.applied).error);
          connectionBusy=false;routeDirty=false;data.connection=current.current;draft.unchecked=false;
        if(state.view==='first-run')await saveDraft({unchecked:false},who);
        else{data=await request(who,'settings');}
          requireOwner(who);paintConnection(current.current);updateIndicator(current.current);updateNext();await refresh(who);return;
        }else if(['failed','expired'].includes(current.job.state))throw new Error(current.job.error||current.job.stage);
        if(currentAttempt())checkTimer=setTimeout(()=>poll().catch(e=>{if(currentAttempt())connectionFailed(e);}),800);
      };
      const safePoll=async()=>{try{await poll();}catch(e){if(currentAttempt())connectionFailed(e);}};
      if(currentAttempt())checkTimer=setTimeout(safePoll,600);
    }catch(e){if(currentAttempt())connectionFailed(e);}
  }
  function connectionFailed(error){connectionBusy=false;checkFailure=error;const box=$('hub-connection-result');if(box){openOptions();box.className='connection-result failed';box.replaceChildren(message('Connection failed. Try WARP or your own proxy.'));
    const details=node('details');details.append(node('summary','',tr('Technical details')),message(error.message));box.append(details);
    box.append(button('Try WARP',async()=>{draft.route='warp';if(state.view==='first-run')await renderWizard();else render();}),
      button('My proxy',async()=>{draft.route='proxy';if(state.view==='first-run')await renderWizard();else render();}),button('Check again',checkConnection));}updateNext();}
  function fresh(connection){return connection?.check?.telegram_connected&&connection.check.current!==false&&Date.now()/1000-connection.check.checked_at<300;}
  function draftChecked(){return !routeDirty&&fresh(data.connection)&&data.connection.strategy?.mode===draft.route&&!!data.connection.strategy?.allow_direct===draft.allow_direct;}
  function paintConnection(connection){const box=$('hub-connection-result');if(!box)return;box.replaceChildren();
    const ok=fresh(connection);box.className='connection-result '+(ok?'working':'unchecked');
    box.append(message(ok?tr('Working · {n} ms',{n:connection.check.latency_ms}):'Connection has not been verified.'));
    if(!ok){
      if(connection?.pool?.listed&&connection.pool.healthy===0&&connection.pool.probed_at){openOptions();box.className='connection-result failed';box.prepend(message('No public proxy answers. Try WARP or your own proxy.'));}
      if(state.view==='first-run')box.append(button('Try WARP',async()=>{draft.route='warp';await renderWizard();}),button('Check again',checkConnection));
    }
  }
  function updateIndicator(connection){
    const el=$('hub-route-status');if(!el)return;
    const ok=fresh(connection)&&(!state.status.collector.running||state.status.collector.connected!==false);
    el.classList.toggle('route-offline',!ok);el.textContent=ok?label(connection.mode)+' · '+connection.check.latency_ms+' '+tr('ms'):tr('No connection');
    el.onclick=()=>run(async()=>{await navigate('settings');if(state.view==='settings'&&data)openSection('connection');});
    const warning=$('hub-proxy-warning');
    warning.hidden=ok||!connection?.pool?.listed||connection.pool.healthy!==0||!connection.pool.probed_at;
    if(!warning.hidden){warning.replaceChildren(message('No public proxy answers. Try WARP or your own proxy.'));
      warning.append(button('Switch to WARP',async()=>{const who=owner();await navigate('settings');requireOwner(who);section='connection';draft.route='warp';editing=true;render();ctx.record?.();}),
        button('Check again',async()=>{const who=owner();await navigate('settings');requireOwner(who);openSection('connection');await checkConnection(false,who);}));}
  }
  function scheduleStatus(who=owner()){clearTimeout(statusTimer);statusTimer=setTimeout(async()=>{
    if(!current(who)||!state.token||!state.me?.admin||state.status?.demo)return;
    try{const result=await request(who,'connection');if(data)data.connection=result.current;updateIndicator(result.current);}catch{}
    if(current(who))scheduleStatus(who);
  },15000);}
  function wizardTop(page){
    const top=node('div','wizard-top'), brand=node('div','wizard-brand'), mark=node('img'), language=node('select','wizard-language');
    mark.src='/mark.svg';mark.alt='';mark.width=30;mark.height=30;
    brand.append(mark,node('span','',tr('First setup')));
    for(const [key,name] of Object.entries(ctx.languages))language.append(new Option(name,key));
    language.value=prefs.language;language.setAttribute('aria-label',tr('Language'));
    language.onchange=()=>run(async()=>{const who=owner();await savePreferences({language:language.value},who);requireOwner(who);await ctx.changeLanguage(language.value);},language);
    top.append(brand,language);
    if(draft?.completed){const close=button('✕',async()=>{await navigate('settings');},'icon-btn wizard-close');close.setAttribute('aria-label',tr('Close'));close.title=tr('Close');top.append(close);}
    page.append(top);
  }
  function wizardStages(page){
    const names=[tr('Goal'),tr('Connection'),tr('Telegram'),tr('Chats'),tr('Start')], targets=[1,4,5,6,7];
    const stage=live?names.length:Math.max(0,draft.step-3), last=names.length-1, list=node('ol','wizard-stepper');
    list.setAttribute('aria-label',tr('Setup progress'));
    list.style.setProperty('--from',String(Math.min(shownStage??stage,last)/last));list.style.setProperty('--to',String(Math.min(stage,last)/last));
    names.forEach((name,i)=>{
      const item=node('li','wizard-stage'+(i<stage?' done':i===stage?' current':'')), dot=node('span','wizard-dot',i<stage?'✓':String(i+1)), text=node('span','wizard-stage-name',name);
      dot.setAttribute('aria-hidden','true');item.style.setProperty('--i',String(i));
      if(i===stage)item.setAttribute('aria-current','step');
      if(i<stage&&!live){const jump=button('',async()=>{draft.step=targets[i];await saveDraft();await renderWizard();},'wizard-stage-link');jump.append(dot,text);item.append(jump);}
      else item.append(dot,text);
      list.append(item);
    });
    if(shownStage!==stage)list.classList.add('wizard-moved');
    shownStage=stage;page.append(list);
  }
  async function renderWizard(who=owner()){
    requireOwner(who);
    const focused=wizardRoot.contains(document.activeElement)?document.activeElement.closest('[data-answer]')?.dataset.answer:null;
    restoreMoved();wizardRoot.replaceChildren();if(!draft||!prefs)return;
    const page=node('div','first-run-shell'+(shownStep===null?' wizard-enter':''));wizardRoot.append(page);
    wizardTop(page);wizardStages(page);
    if(live){renderLive(page);return;}
    visited=Math.max(visited,draft.step);
    if(recordedStep!==draft.step){ctx.record?.({replace:recordedStep===null});recordedStep=draft.step;}
    const choosing=draft.step<4, screen=choosing?1:draft.step;
    const direction=shownStep===null?'enter':(shownStep<4?1:shownStep)===screen?'none':draft.step>shownStep?'forward':'back';
    shownStep=draft.step;
    const pane=node('div','wizard-pane');pane.dataset.direction=direction;page.append(pane);
    const names=['What do you want to do?','What do you want to do?','What do you want to do?','How should we connect?','Connect Telegram','Which chats?','Review your choices'];
    const heading=node('h1','',tr(names[draft.step-1]));heading.tabIndex=-1;pane.append(heading);
    if(choosing)pane.append(message('Save a copy of your Telegram account, or keep a record of conversations as they change.','wizard-lead'));
    const body=node('div','first-run-body');pane.append(body);
    if(choosing){
      cards(body,goals,draft.goal,async goal=>{
        draft.goal=goal;await saveDraft();
        if(!levelChosen&&!draft.completed&&prefs.level!==goalLevels[goal])await savePreferences({level:goalLevels[goal]});
        await renderWizard();
      });
      body.querySelector('[data-answer="copy"]')?.append(node('span','answer-badge',tr('Easiest')));
      const more=node('details','wizard-more'), moreBody=node('div','wizard-more-body');
      more.append(node('summary','',tr('More options')),moreBody);more.open=moreOpen;more.ontoggle=()=>{moreOpen=more.open;};
      moreBody.append(node('h2','',tr('Interface level')));
      cards(moreBody,levels,prefs.level,async level=>{levelChosen=true;await savePreferences({level});await renderWizard();});
      preferencesForm(moreBody,{language:false});
      body.append(more);
    }
    if(draft.step===4)connectionForm(body,true);
    if(draft.step===5){
      shownSession=signedIn();
      accountQuestion(body);
      if(shownSession)body.append(message('Telegram is connected.','notice success'));
      move(ctx.authCard(),body);
      if(!shownSession&&!methodShown){methodShown=true;ctx.authMethod(draft.account_kind==='main'?'qr':'files');}
    }
    if(draft.step===6)await chatsForm(body,who,false);
    if(draft.step===7){
      const summary=node('dl','setup-summary');for(const [key,value,go,more] of [['Goal',label(draft.goal),1,false],['Which chats?',label(draft.scope),6,false],['Telegram account',tr('Connected'),5,false],['Connection',label(draft.route),4,false],['Interface level',label(prefs.level),1,true],['Language',ctx.languages[prefs.language]||prefs.language,1,false],['Time zone',prefs.timezone,1,true]]){
        summary.append(node('dt','',tr(key)));const dd=node('dd','',value);dd.append(button('Edit',async()=>{draft.step=go;if(more)moreOpen=true;await saveDraft();await renderWizard();},'text-link'));summary.append(dd);
      }body.append(summary);
      if(draft.unchecked)body.append(message('Connection was not checked. Starting can fail.','notice warning'));
      if(data.needs_notification_destination)body.append(message('Add a notification destination later in Settings.'));
    }
    page.append(message('Everything can be changed later in Settings.','setup-reassurance'));
    const footer=node('div','wizard-actions');page.append(footer);
    const back=button('Back',async()=>{draft.step=draft.step===4?1:draft.step-1;await saveDraft();await renderWizard();});back.disabled=choosing;footer.append(back);
    const next=button(draft.step===7?(draft.goal==='copy'?'Start export':'Start'):'Next',async()=>{
      const action=owner();
      if(draft.step===7){
        const result=await request(action,'first-run/finish',draftBody());data=result;draft={...result.wizard};await refresh(action);
        if(result.action==='export'){await navigate('evidence');return;}
        if(state.view!=='first-run')return;
        live={started:Date.now(),done:false};await renderWizard(action);watchLive(action);return;
      }
      if(choosing){
        if(data.goal!==draft.goal&&!await applyGoal(draft.goal,{first:!data.goal},action))return;
        await saveDraft({step:4},action);await renderWizard(action);return;
      }
      await saveDraft({step:draft.step+1},action);await renderWizard(action);
    },'primary');next.id='first-run-next';footer.append(next);
    if(!draft.completed)page.append(button('Skip, I’ll set it up myself',async()=>{data=await request(owner(),'first-run/skip',{});await navigate('settings');},'text-link setup-skip'));
    updateNext();
    const restore=direction==='none'&&focused?page.querySelector('[data-answer="'+focused+'"]'):null;
    if(restore)restore.focus({preventScroll:true});else heading.focus({preventScroll:true});
    if(direction!=='none'&&page.getBoundingClientRect().top<0)page.scrollIntoView({block:'start'});
    if(draft.step===4&&draft.route==='auto'&&!autoTried&&!fresh(data.connection)){
      autoTried=true;void checkConnection(false,who);
    }
  }
  async function chatsForm(body,who,inSettings){
    const main=draft.goal!=='copy'&&draft.account_kind==='main';
    if(main&&draft.scope!=='selected')draft.scope='selected';
    const changed=async()=>{if(inSettings){scopeDirty=true;updateScopeSave();}else{await saveDraft();updateNext();}};
    const rerender=async()=>{if(inSettings)render();else await renderWizard();};
    cards(body,[['account','layers:blue','All chats','Includes new chats in continuous collection.'],['selected','check:green','Choose chats','Only the chats you select.'],['folder','inbox:orange','Telegram folder','Use a folder from Telegram.']],draft.scope,async scope=>{
      draft.scope=scope;await changed();await rerender();});
    if(main){
      for(const key of ['account','folder']){const card=body.querySelector('[data-answer="'+key+'"]');card.disabled=true;card.title=tr('Only on a separate account.');}
      body.append(message('Only chosen chats can be recorded on a main account.','notice warning'));
    }
    if(!dialogs&&!signedIn())body.append(message('Connect a Telegram account first.','notice warning'));
    else if(!dialogs){const loading=message('Loading chats…');body.append(loading);try{dialogs=await request(who,'dialogs');loading.remove();}catch(e){loading.remove();if(e.name==='StaleView')throw e;body.append(message(e.message,'notice warning'));}}
    requireOwner(who);
    if(!body.isConnected)return;
    if(dialogs){
      if(draft.scope==='folder')body.append(select('Telegram folder',[['','Choose a folder'],...dialogs.folders.map(f=>[String(f.id),f.title])],String(draft.folder_id??''),async id=>{draft.folder_id=id===''?null:Number(id);await changed();}));
      if(draft.scope==='selected'){
        const filter=node('input');filter.type='search';filter.placeholder=tr('Search chats');body.append(filter);
        const list=node('div','wizard-chats');body.append(list);
        for(const chat of dialogs.dialogs){const row=node('label','check-label'), check=node('input');check.type='checkbox';check.checked=draft.chat_ids.includes(chat.chat_id);
          check.onchange=()=>run(async()=>{draft.chat_ids=check.checked?[...new Set([...draft.chat_ids,chat.chat_id])]:draft.chat_ids.filter(id=>id!==chat.chat_id);await changed();});
          row.dataset.title=chat.title.toLocaleLowerCase();row.append(check,document.createTextNode(chat.title));list.append(row);}
        filter.oninput=()=>{for(const row of list.children)row.hidden=!row.dataset.title.includes(filter.value.toLocaleLowerCase());};
      }
      body.append(message(tr('{n} chats loaded. File size and duration are estimates.',{n:dialogs.dialogs.length})));
      if(dialogs.may_be_truncated)body.append(message('The chat list is limited. Increase the chat list limit in Settings.','notice warning'));
      const actions=node('div','hub-actions');body.append(actions);
      if(inSettings||draft.completed){
        const save=button('Save chat selection',async()=>{const action=owner();data=await request(action,'settings/scope',draftBody());draft={...data.wizard};scopeDirty=false;
          toast(tr('Settings saved.'));if(inSettings){render();return;}await navigate('settings');requireOwner(action);},'primary');
        save.dataset.scopeSave='';actions.append(save);
      }
      actions.append(button('Estimate size and time',async()=>{const estimate=await request(owner(),'first-run/estimate',draftBody());
        estimateBox.textContent=estimate.available?tr(estimate.size<1?'Less than 1 MB · {min}–{max} minutes. Based on a sample; actual results may differ.':'About {size} MB · {min}–{max} minutes. Based on a sample; actual results may differ.',estimate):tr('An estimate is not available yet.');}));
      const estimateBox=message('The estimate uses a small sample of the selected chats.');body.append(estimateBox);
      if(inSettings)updateScopeSave();
    }
  }
  function updateScopeSave(){
    const save=within().querySelector('[data-scope-save]');if(!save||!draft)return;
    save.disabled=!scopeDirty||draft.scope==='selected'&&!draft.chat_ids.length||draft.scope==='folder'&&draft.folder_id===null;
  }
  function accountQuestion(box){
    box.append(node('h2','',tr('Is this a separate account or your main one?')));
    cards(box,[['dedicated','shield:green','A separate account','Recommended. Made for recording: it joins only the chats you want to keep, and losing it costs nothing.'],
      ['main','account:slate','My main account','Not recommended: the account you use every day.']],draft.account_kind,async kind=>{
      draft.account_kind=kind;if(kind==='main'&&draft.scope!=='selected')draft.scope='selected';
      await saveDraft();await renderWizard();
    });
    const why=node('details','setting-help-block');why.append(node('summary','',tr('Why a separate account?')),
      message('Recording sees everything the account sees, including private chats of other people. A separate account keeps your own chats out of the journal and does not risk your main account.'));
    box.append(why);
    if(draft.account_kind==='main'){
      box.append(message('Telegram can restrict, freeze or ban an account that works through an unofficial API client, and a main account is hard to replace. Your own private chats can also end up in the journal and in exports. Only chosen chats can be recorded on a main account; the whole account and folders stay off. The protection scale counts a main account as a penalty.','notice warning'));
      box.append(message('For an account you cannot lose, use Official Web or Trusted Live under Independent capture: they record through the official Telegram client and make no API calls of their own.'));
    }
  }
  function liveParts(){const h=state.status?.health||{};return ['connection','intake','sources','media'].map(name=>({name,...(h[name]||{state:'unknown'})}));}
  function renderLive(page){
    const heading=node('h1','',tr(live.done?'Setup is applied.':live.timedOut?'Check connection':'Checking that recording works…'));heading.tabIndex=-1;page.append(heading);
    const list=node('div','first-run-live'+(live.shown?'':' wizard-appear'));list.setAttribute('aria-live','polite');
    liveParts().forEach((part,i)=>{
      const row=node('div','first-run-check');row.dataset.state=part.state;row.style.setProperty('--i',String(i));
      row.append(ctx.stateBadge(part.state),node('strong','',ctx.healthNames[part.name]),node('span','hint',ctx.healthLines(part.name,part)[0]||''));
      list.append(row);
    });
    live.shown=true;page.append(list);
    if(live.timedOut)page.append(button('Check again',async()=>{
      live.started=Date.now();live.timedOut=false;await renderWizard();watchLive();
    },'primary'));
    if(live.done){
      page.append(node('h2','wizard-done'+(live.celebrated?'':' wizard-appear'),tr('Done! What next:')));live.celebrated=true;
      const actions=node('div','first-run-next-actions');
      for(const [view,text,style] of [['chats','Open chats','primary'],['observations','Open the journal','secondary'],['evidence','How to export','secondary']])
        actions.append(button(text,async()=>{live=null;clearTimeout(liveTimer);await navigate(view);},style));
      page.append(actions);
    }
  }
  function watchLive(who=owner()){
    clearTimeout(liveTimer);
    const session=live;
    const active=()=>current(who)&&session&&live===session&&state.view==='first-run';
    const tick=async()=>{
      if(!active())return;
      let refreshed=false;
      try{await refresh(who);refreshed=true;}catch{}
      if(!active())return;
      const ready=refreshed&&liveParts().every(part=>['working','off'].includes(part.state));
      if(ready&&Date.now()-live.started>4000)live.done=true;
      else if(Date.now()-live.started>120000)live.timedOut=true;
      await renderWizard(who);
      if(active()&&!live.done&&!live.timedOut)liveTimer=setTimeout(tick,2000);
    };
    liveTimer=setTimeout(tick,1500);
  }
  function draftBody(){const {step,goal,route,allow_direct,unchecked,scope,chat_ids,folder_id,account_kind}=draft;return {step,goal,route,allow_direct,unchecked,scope,chat_ids,folder_id,account_kind:account_kind||null};}
  function updateNext(){const next=$('first-run-next');if(!next||!draft)return;
    next.disabled=connectionBusy||draft.step===4&&!draftChecked()&&!draft.unchecked||
      draft.step===5&&(!signedIn()||draft.goal!=='copy'&&!draft.account_kind)||
      draft.step===6&&(draft.scope==='selected'&&!draft.chat_ids.length||draft.scope==='folder'&&draft.folder_id===null);
  }
  for(const select of document.querySelectorAll('[data-ui-level]'))select.onchange=()=>run(async()=>{await savePreferences({level:select.value});if(state.view==='settings')render();});
  return {bootstrap,load,render,savePreferences,
    async openGroup(id){if(!data)data=await request(owner(),'settings');await openGroup(id);},
    get step(){return draft&&!live?draft.step:null;},
    get section(){return state.view==='settings'&&!groupScope?section:null;},
    leave(){section=null;shownForm=null;closeSheet();clearTimeout(liveTimer);live=null;recordedStep=null;groupScope=null;shownStep=shownStage=null;},
    status(){
      updateNext();if(data)updateIndicator(data.connection);
      const session=signedIn();
      if(state.view==='first-run'&&draft?.step===5&&!live&&shownSession!==null&&session!==shownSession)void renderWizard();
      shownSession=session;
    },
    reset(){generation++;checkSequence++;clearTimeout(checkTimer);clearTimeout(statusTimer);clearTimeout(liveTimer);section=null;shownForm=null;closeSheet();data=prefs=draft=dialogs=null;live=null;groupScope=null;groupView.reset();visited=0;recordedStep=shownSession=shownStep=shownStage=null;levelChosen=moreOpen=methodShown=false;connectionBusy=false;editing=false;autoTried=routeDirty=false;checkFailure=null;preferencesQueue=draftQueue=Promise.resolve();},
    async refreshPreferences(patch){if(prefs)await savePreferences(patch);},
  };
}
