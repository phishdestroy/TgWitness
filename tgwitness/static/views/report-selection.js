import {createReportEditor} from './report-editor.js?v=3';

export function createReportSelection({root,tr,json,getOwner,ready,options,active,titles=()=>new Map()}) {
  const people=new Map();
  let peopleKey='';
  function loadPeople(){
    const chosen=ids(fields.chats),chats=(chosen.length?chosen:(catalog.chats||[]).map(row=>Number(row.id))).slice(0,5),key=getOwner()+':'+chats.join(',');
    if(!chats.length||key===peopleKey)return;
    peopleKey=key;
    Promise.allSettled(chats.map(chat=>json('chats/'+encodeURIComponent(chat)+'/authors'))).then(results=>{
      if(peopleKey!==key)return;
      for(const result of results)for(const author of result.value?.authors||[])if(author.name||author.username)people.set(Number(author.id),author.name||'@'+author.username);
      renderCatalog('senders');
    });
  }
  const find=id=>root.querySelector('#'+id), kinds=[...root.querySelectorAll('[data-report-kind]')];
  const make=(tag,text='',cls='')=>{const el=document.createElement(tag);el.textContent=String(text??'');if(cls)el.className=cls;return el;};
  const mask=text=>window.TgWitnessPrivacy?.preview(String(text??''))??tr('Message preview unavailable');
  let catalog={chats:[],senders:[]}, response=null, request=0, revision=0, pending=false, controller=null, stamp=null;
  let step=0,previewTimer=null,picked=[];
  const steps=['report-data','report-content','report-preview'];
  const pages=[find('report-data'),find('report-content-step'),find('report-preview')];
  const editor=createReportEditor({root,tr,onEdit:()=>{if(step!==1)selectStep(1);}});
  const count=value=>Number(value||0).toLocaleString();
  const fields={chats:find('report-selection-chats'),senders:find('report-selection-senders')};
  const secretField=make('input');secretField.type='hidden';secretField.id='report-selection-secret-chats';fields.chats.after(secretField);
  const messagesField=make('input');messagesField.type='hidden';messagesField.id='report-selection-messages';messagesField.value='[]';secretField.after(messagesField);
  messagesField.addEventListener('change',()=>{picked=JSON.parse(messagesField.value||'[]');renderPicked();renderCatalog('chats');});
  const containers={chats:find('report-chat-catalog'),senders:find('report-sender-catalog')};
  const searches={chats:root.querySelector('[data-report-search=chats]'),senders:root.querySelector('[data-report-search=senders]')};
  const allChats=make('input'),allLabel=make('label','','check-label');
  allChats.type='checkbox';allChats.id='report-selection-all-chats';allChats.checked=true;
  allLabel.append(allChats,document.createTextNode(' '+tr('All chats')));containers.chats.before(allLabel);
  allChats.addEventListener('change',()=>{
    if(allChats.checked){fields.chats.value=secretField.value='';picked=[];renderPicked();}
    fields.chats.dispatchEvent(new Event('input',{bubbles:true}));
  });
  function ids(field){
    const chunks=field.value.split(/[\s,;]+/).filter(Boolean);
    const valid=chunks.every(value=>/^-?[1-9]\d*$/.test(value)&&Number.isSafeInteger(Number(value)));
    field.setCustomValidity(valid?'':tr('Enter whole Telegram IDs separated by commas.'));
    return valid?[...new Set(chunks.map(Number))]:[];
  }
  function read(){
    const enabled=find('report-selection-chosen').checked,from=find('report-selection-from').value,to=find('report-selection-to').value;
    if(!enabled){
      for(const field of [fields.chats,fields.senders,allChats,find('report-selection-to'),kinds[0]])field.setCustomValidity('');
      return {enabled:false,chats:[],secret_chats:[],senders:[],messages:[],date_from:'',date_to:'',kinds:kinds.map(input=>input.dataset.reportKind),id_gaps:find('report-selection-gaps').checked};
    }
    find('report-selection-to').setCustomValidity(from&&to&&from>to?tr('The end date must not be earlier than the start date.'): '');
    const selected=kinds.filter(input=>input.checked).map(input=>input.dataset.reportKind);
    kinds[0].setCustomValidity(selected.length?'':tr('Choose at least one record type.'));
    const chats=ids(fields.chats);
    const secrets=ids(secretField);
    allChats.setCustomValidity(!allChats.checked&&!chats.length&&!secrets.length&&!picked.length?tr('Choose at least one chat.'):'');
    return {enabled,chats:allChats.checked?[]:chats,secret_chats:allChats.checked?[]:secrets,senders:ids(fields.senders),
      messages:allChats.checked?[]:picked.map(item=>({chat:item.chat,message:item.message})),
      date_from:from,date_to:to,kinds:selected,id_gaps:find('report-selection-gaps').checked};
  }
  function controls(){
    find('report-selection-options').disabled=!find('report-selection-chosen').checked;
    find('report-selection-options').hidden=!find('report-selection-chosen').checked;
    find('report-preview-run').disabled=pending;
    find('report-load-catalog').disabled=pending;
    const valid=response&&stamp===JSON.stringify(options())&&response.counts?.selected_records>0;
    root.querySelectorAll('[data-report-download]').forEach(button=>button.disabled=pending||!valid);
  }
  function selectStep(index,focus=true){
    step=Math.max(0,Math.min(index,pages.length-1));
    pages.forEach((page,i)=>page.hidden=i!==step);
    editor.step(step);
    root.querySelectorAll('[data-report-step]').forEach((button,i)=>{
      button.setAttribute('aria-current',i===step?'step':'false');
      button.setAttribute('aria-controls',pages[i].id);
    });
    find('report-step-back').hidden=step===0;
    find('report-step-next').hidden=step===2;
    find('report-draft-downloads').hidden=step!==2;
    find('report-step-position').textContent=(step+1)+' / '+pages.length;
    if(focus){root.scrollIntoView({block:'start',behavior:'instant'});pages[step].querySelector('[tabindex="-1"]')?.focus({preventScroll:true});}
    if(step===2&&ready())void preview(false);
  }
  function renderPicked(){
    messagesField.value=JSON.stringify(picked);
    const box=find('report-picked'),list=find('report-picked-list'),known=titles(),groups=new Map();
    box.hidden=!picked.length;
    find('report-picked-count').textContent=picked.length?tr('{n} selected',{n:count(picked.length)}):'';
    for(const item of picked){if(!groups.has(item.chat))groups.set(item.chat,[]);groups.get(item.chat).push(item);}
    const nodes=[];let left=60;
    for(const [chat,items] of groups){
      const group=make('div','','report-picked-group');
      group.append(make('span',known.get(chat)?mask(known.get(chat)):tr('Chat {id}',{id:chat}),'report-picked-chat'));
      for(const item of items.slice(0,left)){
        const chip=make('button','#'+item.message,'report-picked-chip');chip.type='button';chip.title=tr('Remove');
        chip.setAttribute('aria-label',tr('Remove')+': '+tr('Message {id}',{id:item.message}));
        chip.addEventListener('click',()=>dropPicked(picked.filter(other=>other!==item)));
        group.append(chip);
      }
      if(items.length>left)group.append(make('span',tr('+{n} more',{n:count(items.length-Math.max(0,left))}),'report-picked-more'));
      left=Math.max(0,left-items.length);nodes.push(group);
    }
    list.replaceChildren(...nodes);
  }
  function dropPicked(next){
    picked=next;renderPicked();fields.chats.dispatchEvent(new Event('input',{bubbles:true}));
  }
  find('report-picked-clear').addEventListener('click',()=>dropPicked([]));
  const numbers=find('report-selection-numbers'),numbersNote=find('report-selection-numbers-note');
  function typed(text){
    const found=[];
    for(const line of text.split('\n').map(value=>value.trim()).filter(Boolean)){
      const link=line.match(/^(?:https?:\/\/)?t\.me\/c\/(\d{1,13})\/(?:\d+\/)?(\d{1,10})(?:[?#]\S*)?$/i);
      const pair=link?null:line.match(/^(-?[1-9]\d{0,18})\s*:\s*(\d[\d\s,;]*)$/);
      const chat=link?-(1e12+Number(link[1])):pair?Number(pair[1]):NaN;
      const list=link?[Number(link[2])]:pair?pair[2].split(/[\s,;]+/).filter(Boolean).map(Number):[];
      if(!Number.isSafeInteger(chat)||!list.length||list.some(value=>value<1||value>=2**31))return {failed:line};
      for(const message of list)found.push({chat,message});
    }
    return {found};
  }
  numbers.addEventListener('input',event=>{event.stopPropagation();numbersNote.textContent='';});
  find('report-selection-numbers-add').addEventListener('click',()=>{
    const {found=[],failed}=typed(numbers.value),known=new Set(picked.map(item=>item.chat+':'+item.message));
    const fresh=found.filter(item=>!known.has(item.chat+':'+item.message)&&known.add(item.chat+':'+item.message));
    numbersNote.textContent=failed?tr('Could not read: {text}',{text:failed}):picked.length+fresh.length>1000?tr('Select no more than {n} messages.',{n:count(1000)}):'';
    if(numbersNote.textContent||!found.length)return;
    numbers.value='';allChats.checked=false;dropPicked([...picked,...fresh]);
  });
  function renderCatalog(key){
    const selected=new Set(ids(fields[key]).map(String)), query=searches[key].value.trim().toLowerCase();
    const rowsWithKeys=(catalog[key]||[]).map(row=>({...row,key:String(row.id)}));
    if(key==='chats'){
      for(const id of ids(secretField))selected.add('secret:'+id);
      for(const row of catalog.secret_chats||[])rowsWithKeys.push({...row,key:'secret:'+row.id,secret:true});
    }
    const all=new Map(rowsWithKeys.map(row=>[row.key,row]));
    for(const id of selected)if(!all.has(id))all.set(id,{id:id.replace('secret:',''),key:id,secret:id.startsWith('secret:'),count:null});
    const known=key==='chats'?titles():people;
    for(const row of all.values())if(!row.secret&&!row.title&&known.get(Number(row.id)))row.title=known.get(Number(row.id));
    const rows=[...all.values()].filter(row=>String(row.id).includes(query)||String(row.title||'').toLowerCase().includes(query));
    const nodes=rows.map(row=>{
      const label=make('label','','report-catalog-row'),input=make('input');input.type='checkbox';input.checked=selected.has(row.key);
      input.dataset.reportChoice=key;input.dataset.id=row.key;
      const title=row.secret?'Secret Chat '+row.id:row.title?mask(row.title):tr(key==='chats'?'Chat {id}':'Account {id}',{id:row.id});
      const info=make('span','','report-catalog-label');info.append(make('strong',title),make('small',row.secret?tr('Pseudo-secret'):String(row.id)));
      label.append(input,info,make('span',row.count===null?'—':count(row.count),'report-catalog-number'));
      input.addEventListener('change',()=>{
        if(key==='chats')allChats.checked=false;
        const field=row.secret?secretField:fields[key],current=new Set(ids(field));if(input.checked)current.add(Number(row.id));else current.delete(Number(row.id));
        field.value=[...current].join(', ');fields[key].dispatchEvent(new Event('input',{bubbles:true}));
      });return label;
    });
    const empty=catalog[key+'_status']==='too_many_groups'?tr('Too many choices to list. Enter the Telegram IDs below.')
      :response?tr('No matches.'):tr('Load the workspace to see available choices.');
    containers[key].replaceChildren(...(nodes.length?nodes:[make('p',empty,'hint')]));
    if(nodes.length&&catalog[key+'_status']==='too_many_groups')containers[key].prepend(make('p',empty,'hint'));
    find(key==='chats'?'report-chat-count':'report-sender-count').textContent=selected.size
      ?tr('{n} selected',{n:count(selected.size)}):key==='chats'&&picked.length&&!allChats.checked?''
      :tr(key==='chats'?(allChats.checked?'All chats included':'Choose at least one chat.'):'All authors included');
  }
  function changed(event){
    if(event?.target?.matches('[data-report-search]'))return;
    if(event?.target===fields.chats&&fields.chats.value.trim())allChats.checked=false;
    revision++;controls();read();
    if(event?.target===fields.chats||event?.target===fields.senders||event?.target?.name==='report-selection-mode'){
      renderCatalog('chats');renderCatalog('senders');
    }
    if(response||pending){find('report-preview-stale').hidden=false;find('report-preview-result').dataset.stale='true';}
    controls();clearTimeout(previewTimer);
    if(step!==1)previewTimer=setTimeout(()=>preview(false),500);
  }
  function table(headings,rows,cls=''){
    const scroll=make('div','','report-preview-scroll'),el=make('table','',cls),head=make('thead'),trHead=make('tr');
    for(const heading of headings){const cell=make('th',heading);cell.scope='col';trHead.append(cell);}head.append(trHead);
    const body=make('tbody');for(const row of rows){const line=make('tr');for(const item of row){const cell=make('td');if(item instanceof Node)cell.append(item);else cell.textContent=String(item??'—');line.append(cell);}body.append(line);}
    el.append(head,body);scroll.append(el);return scroll;
  }
  function chart(title,rows){
    const block=make('section','','report-preview-chart');block.append(make('h4',tr(title)));
    const maximum=Math.max(1,...rows.map(row=>Number(row.value||0)));
    for(const row of rows){
      const line=make('div','','report-preview-bar'),track=make('span','','report-preview-track'),fill=make('span');
      fill.style.width=(100*Number(row.value||0)/maximum)+'%';track.append(fill);track.setAttribute('aria-hidden','true');
      line.append(make('span',row.label),track,make('b',count(row.value)));block.append(line);
    }
    if(!rows.length)block.append(make('p',tr('No observations in this selection.'),'hint'));
    return block;
  }
  function rowLabel(row){return tr(row.label||'Unknown',row.label_values||{});}
  const kindLabel=kind=>({
    'message.new':tr('New message'),'message.snapshot':tr('History observation'),'message.recovered':tr('Recovered message'),
    'message.edited':tr('Edit'),'message.deleted':tr('Deletion notice'),'message.missing_on_recheck':tr('Missing on recheck'),
    'secret_chat.message':tr('Pseudo-secret message'),'secret_chat.action':tr('Pseudo-secret notice'),'secret_chat.file':tr('Pseudo-secret file preserved')
  }[kind]||String(kind||''));
  function message(row){
    if(!row)return make('span',tr('Not available'));
    const block=make('div','','report-preview-message');
    block.append(make('small','#'+row.seq+' · '+tr('Message {id}',{id:row.message_id??'—'})+' · '+String(row.observed_at||'')),make('p',mask(row.text)));
    return block;
  }
  function changeVersion(row,label){
    const block=make('div','','report-change-version');
    if(label)block.append(make('strong',label));
    block.append(make('small','#'+row.seq+' · '+kindLabel(row.kind)+' · '+String(row.observed_at||'')));
    if(row.context_only)block.append(make('span',tr('Context outside the selected filters'),'report-change-context'));
    block.append(make('p',row.withheld?tr('Message text was not retained.'):row.text?mask(row.text):tr('(no text)')));
    if(row.text_truncated)block.append(make('span',tr('Text shortened in this preview.'),'hint'));
    return block;
  }
  function renderChanges(changes){
    const section=make('section','','report-preview-changes');
    section.append(make('h4',tr('Changes and deleted messages')),
      make('p',tr('Selected changes with saved message history. Versions outside the filters are marked as context.'),'hint'));
    for(const row of changes.messages||[]){
      const card=make('article','','report-change-card'),versions=row.versions||[],latest=versions.at(-1),previous=versions.at(-2);
      card.append(make('h5',tr('Chat {id}',{id:row.chat_id})+' · '+tr('Message {id}',{id:row.message_id})));
      if(previous&&latest?.kind==='message.edited'){
        const pair=make('div','','report-change-pair');pair.append(changeVersion(previous,tr('Before')),changeVersion(latest,tr('After')));card.append(pair);
      }else if(latest)card.append(changeVersion(latest,tr('Saved version')));
      const earlier=versions.slice(0,previous&&latest?.kind==='message.edited'?-2:-1);
      if(earlier.length){const detail=make('details');detail.append(make('summary',tr('Earlier saved versions')));
        for(const version of earlier)detail.append(changeVersion(version));card.append(detail);}
      for(const gone of row.gone||[]){
        const notice=make('div','','report-change-gone');
        notice.append(make('strong',kindLabel(gone.kind)),make('small','#'+gone.seq+' · '+String(gone.observed_at||'')));
        if(gone.context_only)notice.append(make('span',tr('Context outside the selected filters'),'report-change-context'));
        const retained=versions.find(version=>version.seq===gone.previous_version_seq);
        if(retained)notice.append(changeVersion(retained,tr('Last saved content before this observation')));
        else notice.append(make('p',tr(gone.previous_version_seq==null?'No message content was saved before this observation.'
          :'The saved version is outside this preview. Open the report for the full context.')));
        card.append(notice);
      }
      if(row.versions_truncated||row.gone_truncated)card.append(make('p',tr('Preview shortened. Open the report for the full saved history.'),'hint'));
      section.append(card);
    }
    if(!changes.messages?.length)section.append(make('p',tr('No edits or deletion observations match these choices.'),'hint'));
    if(changes.truncated)section.append(make('p',tr('Showing {shown} of {total} changed messages.',{
      shown:count(changes.listed??changes.messages?.length),total:count(changes.total??changes.messages_changed)}),'hint'));
    return section;
  }
  function render(data){
    editor.summary(data);
    const target=find('report-preview-result'),source=data.source||{},counts=data.counts||{},stats=make('dl','','report-preview-counts');
    for(const [name,value] of [[tr('Selected records'),counts.selected_records],[tr('Message observations'),counts.message_observations],
      [tr('Observed message senders'),counts.participants],[tr('Chats'),counts.chats]]){const entry=make('div');entry.append(make('dt',name),make('dd',count(value)));stats.append(entry);}
    const provenance=make('p',tr('Calculated from {n} journal records, through record #{last}.',{n:count(source.records),last:source.last_seq??'—'}),'hint');
    target.replaceChildren(stats,provenance);
    const anchor=make('details'),summary=make('summary',tr('Journal head'));anchor.append(summary,make('code',source.journal_head||'—'));target.append(anchor);
    if(!counts.selected_records)target.append(make('p',tr('No records match these choices. Change the filters and build the preview again.'),'report-preview-empty'));
    const analytics=data.analytics||{},grid=make('div','','report-preview-charts');
    if(analytics.activity){
      const rows=analytics.activity.rows||[];
      grid.append(chart('Activity over time',rows.slice(-36).map(row=>({label:row.period,value:row.total}))));
      if(rows.length>36)grid.append(make('p',tr('Showing the latest {n} recorded periods. The report includes the complete selected period.',{n:36}),'hint'));
    }
    if(analytics.participants){const block=chart('Participant activity',(analytics.participants.rows||[]).map(row=>({label:rowLabel(row),value:row.total})));
      block.append(make('p',tr('Sender counts use new messages, history observations and recovered messages.'),'hint'));grid.append(block);}
    if(analytics.chats)grid.append(chart('Activity by chat',(analytics.chats.rows||[]).map(row=>({label:rowLabel(row),value:row.total}))));
    if(analytics.composition)grid.append(chart('Record composition',[
      ['new','New messages'],['snapshot','History observations'],['recovered','Recovered messages'],
      ['edited','Edits'],['deleted','Deletion notices'],['missing','Missing on recheck']
    ].map(([key,label])=>({label:tr(label),value:analytics.composition[key]||0}))));
    if(analytics.hourly){
      const block=make('section','','report-preview-chart report-preview-hours');block.append(make('h4',tr('Activity by weekday and hour')));
      const days=[tr('Monday'),tr('Tuesday'),tr('Wednesday'),tr('Thursday'),tr('Friday'),tr('Saturday'),tr('Sunday')],rows=analytics.hourly.rows||[];
      const maximum=Math.max(1,...rows.flat());
      block.append(table([tr('UTC'),...Array.from({length:24},(_,hour)=>String(hour).padStart(2,'0'))],rows.map((row,day)=>[
        days[day],...row.map(value=>{const cell=make('span',count(value),'report-heat-cell');cell.style.backgroundColor='rgb(36 126 140 / '+(.05+.45*Number(value)/maximum)+')';return cell;})
      ]),'report-heat-table'));grid.append(block);
    }
    if(grid.children.length){
      const charts=make('details','','report-advanced');charts.append(make('summary',tr('Charts')),
        make('p',tr('Activity uses observation times in UTC. Counts are recorded observations, not unique messages.'),'hint'),grid);target.append(charts);
    }
    for(const key of ['activity','participants','chats'])if(analytics[key]?.status&&analytics[key].status!=='available')
      target.append(make('p',tr('A chart could not be grouped within the report limits. No approximate counts are shown.'),'hint'));
    if(data.changes){const detail=make('details','','editor-details');detail.append(make('summary',tr('Changes and deleted messages')),renderChanges(data.changes));target.append(detail);}
    const samples=make('details','','editor-details');samples.append(make('summary',tr('Selected message samples')));target.append(samples);
    const messages=data.messages||{},rows=messages.rows||[];
    samples.append(table([tr('Record'),tr('Chat'),tr('Type'),tr('Observed at (UTC)'),tr('Message preview')],rows.map(row=>[
      '#'+row.seq,row.secret_chat_id!=null?'Secret Chat '+row.secret_chat_id:String(row.chat_id??'—'),kindLabel(row.kind),String(row.observed_at||'—'),message(row)
    ]),'report-message-table'));
    samples.append(make('p',tr('Showing {shown} of {total} selected records. Possible secrets are masked in this preview.',{shown:count(rows.length),total:count(messages.total)}),'hint'));
    const gaps=data.id_gaps||{};
    if(gaps.enabled){
      const detail=make('details','','editor-details');detail.append(make('summary',tr('Missing message IDs')));target.append(detail);
      if(gaps.chats_shared_numbering)detail.append(make('p',tr('Private chats, bots and ordinary groups share one account-wide numbering, so a number missing in one of them may belong to another chat. Chats not compared for this reason: {n}.',{n:count(gaps.chats_shared_numbering)}),'hint'));
      if(gaps.status==='not_compared')detail.append(make('p',tr('Message numbers were not compared: this selection has no whole channel or supergroup with saved messages in the chosen dates.'),'hint'));
      else{
        detail.append(make('p',tr('{ranges} ranges, {ids} message IDs not observed.',{ranges:count(gaps.ranges_total),ids:count(gaps.ids_total)}),'hint'));
        detail.append(table([tr('Chat'),tr('Missing IDs'),tr('Before the gap'),tr('After the gap')],(gaps.rows||[]).map(row=>[
          String(row.chat_id),String(row.start)+' – '+String(row.end)+' ('+count(row.count)+')',message(row.before),message(row.after)
        ]),'report-gap-table'));
        if(gaps.truncated)detail.append(make('p',tr('Preview shortened. The saved report lists the available gap details.'),'hint'));
        detail.append(make('p',tr('Missing numbers are gaps in the observed IDs; deletions are recorded as separate notices. Neighboring records are context and may be outside the chosen authors, event types or dates.'),'hint'));
      }
    }
  }
  async function preview(reveal=true){
    if(!ready()||pending)return;
    const body=options();if(!(reveal?root.reportValidity():root.checkValidity()))return;
    const mine=++request,owner=getOwner(),version=revision;
    controller?.abort();controller=new AbortController();pending=true;controls();
    find('report-preview-status').textContent=tr('Reading the selected journal records…');
    find('report-data-status').textContent=tr('Reading the selected journal records…');
    find('report-data-overview').setAttribute('aria-busy','true');
    find('report-preview-retry').hidden=true;
    const current=()=>mine===request&&owner===getOwner()&&active();
    try{
      const data=await json('report-preview',body,{signal:controller.signal});
      if(!current())return;
      if(version!==revision){find('report-preview-status').textContent=tr('Choices changed while the preview was running. Build it again.');find('report-preview-stale').hidden=false;return;}
      response=data;stamp=JSON.stringify(body);catalog=data.catalog||{chats:[],senders:[]};loadPeople();
      renderCatalog('chats');renderCatalog('senders');render(data);
      find('report-preview-stale').hidden=true;delete find('report-preview-result').dataset.stale;
      find('report-preview-status').textContent=tr('Selected records')+': '+count(data.counts?.selected_records);
      find('report-data-status').textContent='';
      if(reveal){find('report-preview').scrollIntoView({block:'start',behavior:'instant'});find('report-preview-title').focus({preventScroll:true});}
    }catch(error){
      if(!current()||['AbortError','StaleView'].includes(error.name))return;
      find('report-preview-status').textContent=tr('Could not build the preview.')+' '+error.message;find('report-preview-retry').hidden=false;
      find('report-data-status').textContent=find('report-preview-status').textContent;
    }finally{if(mine===request&&owner===getOwner()){
      pending=false;controls();
      find('report-data-overview').setAttribute('aria-busy','false');
      if(step!==1&&version!==revision){clearTimeout(previewTimer);previewTimer=setTimeout(()=>preview(false),500);}
    }}
  }
  for(const key of ['chats','senders'])searches[key].addEventListener('input',()=>renderCatalog(key));
  root.querySelectorAll('[data-report-step]').forEach(button=>button.addEventListener('click',()=>{
    selectStep(steps.indexOf(button.dataset.reportStep));
  }));
  find('report-step-back').addEventListener('click',()=>selectStep(step-1));
  find('report-step-next').addEventListener('click',()=>{read();if(root.reportValidity())selectStep(step+1);});
  root.addEventListener('invalid',event=>{
    const index=pages.findIndex(page=>page.contains(event.target));
    if(index>=0&&index!==step)selectStep(index,false);
    editor.reveal(event.target);
    let ancestor=event.target.parentElement;
    while(ancestor&&ancestor!==root){if(ancestor.tagName==='DETAILS')ancestor.open=true;ancestor=ancestor.parentElement;}
  },true);
  selectStep(0,false);
  find('report-preview-run').addEventListener('click',()=>preview());find('report-preview-retry').addEventListener('click',()=>preview());
  find('report-load-catalog').addEventListener('click',()=>preview(false));
  function leave(){request++;clearTimeout(previewTimer);controller?.abort();controller=null;pending=false;controls();}
  function reset(){
    leave();revision++;response=null;stamp=null;catalog={chats:[],senders:[]};people.clear();peopleKey='';picked=[];renderPicked();
    for(const field of Object.values(searches))field.value='';
    for(const field of [fields.chats,fields.senders,find('report-selection-to'),kinds[0]])field.setCustomValidity('');
    find('report-preview-result').replaceChildren();delete find('report-preview-result').dataset.stale;
    find('report-preview-status').textContent='';find('report-preview-stale').hidden=find('report-preview-retry').hidden=true;
    for(const box of Object.values(containers))box.replaceChildren();find('report-chat-count').textContent=find('report-sender-count').textContent='';
    editor.reset();selectStep(0,false);controls();
  }
  root.addEventListener('keydown',event=>{
    if(event.key!=='Enter'||event.isComposing||!event.target.matches('input:not([type=file]), select'))return;
    event.preventDefault();
    if(event.target.id==='report-profile-name')find('report-profile-save')?.click();
  });
  return {read,changed,preview,leave,reset,reveal(field){
    const index=pages.findIndex(page=>page.contains(field));if(index>=0)selectStep(index,false);
    editor.reveal(field);
    let parent=field.parentElement;while(parent&&parent!==root){if(parent.tagName==='DETAILS')parent.open=true;parent=parent.parentElement;}
    field.scrollIntoView({block:'center'});field.focus({preventScroll:true});
  },
    selectSecrets(chatIds=[]){
      this.load({enabled:true,secret_chats:chatIds,kinds:['secret_chat.message','secret_chat.action','secret_chat.file'],id_gaps:false});
      selectStep(0,false);secretField.dispatchEvent(new Event('input',{bubbles:true}));
    },
    selectMessages(chat,messageIds){
      const draft=read(),fresh=messageIds.map(message=>({chat,message}));
      const kept=draft.enabled?picked.filter(item=>item.chat!==chat).slice(0,Math.max(0,1000-fresh.length)):[];
      const whole=draft.enabled?ids(fields.chats).filter(id=>id!==chat):[];
      this.load(draft.enabled?{...draft,chats:whole,secret_chats:ids(secretField),messages:[...kept,...fresh],id_gaps:false}
        :{enabled:true,messages:fresh,id_gaps:false,kinds:kinds.filter(input=>input.dataset.reportKind.startsWith('message.')).map(input=>input.dataset.reportKind)});
      selectStep(0,false);fields.chats.dispatchEvent(new Event('input',{bubbles:true}));
    },
    selectChats(chatIds,senders=[]){
      this.load({enabled:true,chats:chatIds,senders,kinds:kinds.filter(input=>input.dataset.reportKind.startsWith('message.')).map(input=>input.dataset.reportKind)});
      selectStep(0,false);fields.chats.dispatchEvent(new Event('input',{bubbles:true}));
    },
    load(selection={}){
      selection=selection||{};find('report-selection-all').checked=!selection.enabled;find('report-selection-chosen').checked=!!selection.enabled;
      fields.chats.value=(selection.chats||[]).join(', ');fields.senders.value=(selection.senders||[]).join(', ');
      secretField.value=(selection.secret_chats||[]).join(', ');
      picked=(selection.messages||[]).map(item=>({chat:Number(item.chat),message:Number(item.message)}));renderPicked();
      allChats.checked=!(selection.chats||[]).length&&!(selection.secret_chats||[]).length&&!picked.length;
      for(const [id,key] of [['report-selection-from','date_from'],['report-selection-to','date_to']])find(id).value=selection[key]||'';
      const set=new Set(selection.kinds||kinds.map(input=>input.dataset.reportKind));for(const input of kinds)input.checked=set.has(input.dataset.reportKind);
      find('report-selection-gaps').checked=selection.id_gaps!==false;controls();renderCatalog('chats');renderCatalog('senders');
      if(stamp&&stamp!==JSON.stringify(options())){find('report-preview-stale').hidden=false;find('report-preview-result').dataset.stale='true';}
      clearTimeout(previewTimer);previewTimer=setTimeout(()=>preview(false),100);
    }
  };
}
