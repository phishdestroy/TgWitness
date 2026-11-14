export function createReportGuidance({root, tr}) {
  const get=id=>root.querySelector('#report-guidance-'+id);
  let profiles=[], detailKey=null;
  const scopeField=document.createElement('label'), scope=document.createElement('select');
  scope.id='report-guidance-scope';scopeField.htmlFor=scope.id;
  scopeField.append(document.createTextNode(tr('Scope')),scope);
  get('procedure').parentElement.after(scopeField);
  const paragraph=text=>{const p=document.createElement('p');p.className='hint';p.textContent=text;return p;};
  function read(){
    return {jurisdiction:get('country').value,procedure:get('procedure').value,procedure_scope:scope.value||null,
      include_in_report:get('include').checked,local_note:get('local').checked,include_methods:get('methods').checked};
  }
  function sync(){
    const value=read(), profile=profiles.find(p=>p.code===value.jurisdiction), active=!!profile&&value.include_in_report;
    get('procedure').disabled=!profile;
    for(const option of get('procedure').options){
      option.disabled=!!profile?.examination_only&&!profile.examination_routes.some(p=>p.route===option.value);
    }
    const choices=(profile?.examination_routes||[]).filter(p=>p.route===value.procedure);
    get('procedure').setCustomValidity(active&&profile.examination_only&&!choices.length
      ?tr('This procedure is not covered by the selected profile.'):'');
    const scopeKey=value.jurisdiction+':'+value.procedure;
    if(scope.dataset.key!==scopeKey){
      scope.replaceChildren(new Option(tr('Not selected'),''),...choices.filter(p=>p.id).map(p=>new Option(p.scope||p.id,p.id)));
      scope.dataset.key=scopeKey;
    }
    scopeField.hidden=choices.length<2;
    scope.disabled=choices.length<2||!active;scope.required=choices.length>1&&active;
    scope.setCustomValidity(scope.required&&!scope.value?tr('Choose a scope for this procedure.'):'');
    const display=profile?.scope_profiles?.[scope.value]||profile;
    get('include').disabled=!profile;
    get('local').disabled=!active||display?.has_local_summary===false;
    get('methods').disabled=!active;
    const key=scopeKey+':'+scope.value;
    if(detailKey===key)return active;
    detailKey=key;
    const detail=get('detail');detail.replaceChildren();
    if(!profile)return;
    const criminal=value.procedure==='criminal';
    const status=criminal?display.criminal_status:'research_draft';
    detail.append(paragraph(display.scope),paragraph('Research date: '+display.reviewed_on+' · '+status.replaceAll('_',' ')),
      paragraph(criminal?display.criminal:display.basis));
    if(profile.examination_only&&!choices.length)detail.append(paragraph(tr('This procedure is not covered by the selected profile.')));
    const selected=choices.find(p=>p.id===scope.value);
    if(selected?.scope)detail.append(paragraph(selected.scope));
    const links=document.createElement('ul');
    for(const source of criminal?display.criminal_sources:display.sources){
      const item=document.createElement('li'),link=document.createElement('a');
      link.href=source.url;link.target='_blank';link.rel='noopener noreferrer';link.textContent=source.title;
      item.append(link);links.append(item);
    }
    detail.append(links);
    return active;
  }
  function reset(){
    profiles=[];detailKey=null;root.open=false;
    scope.dataset.key='';scope.replaceChildren();
    get('country').replaceChildren(new Option(tr('Not selected'),''));
    get('procedure').value='civil';get('include').checked=true;
    get('local').checked=get('methods').checked=false;sync();
  }
  function load(value={}, catalog){
    profiles=catalog.profiles;detailKey=null;
    get('country').replaceChildren(new Option(tr('Not selected'),''),...profiles.map(p=>new Option(p.name,p.code)));
    get('country').value=value.jurisdiction||'';get('procedure').value=value.procedure||'civil';
    get('include').checked=value.include_in_report!==false;get('local').checked=!!value.local_note;get('methods').checked=!!value.include_methods;
    root.open=!!value.jurisdiction;sync();scope.value=value.procedure_scope||'';sync();
  }
  scope.addEventListener('change',sync);
  reset();return {read,load,reset,sync};
}
