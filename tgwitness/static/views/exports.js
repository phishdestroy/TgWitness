export function createExports({root, tr, json, getSession, fmtTime, toast,downloadAgain,onTab}) {
  const find = id => root.querySelector('#'+id), tabs = [...root.querySelectorAll('[data-export-tab]')];
  let session = getSession(), request = 0, transfer = 0, selected = 'downloads', entries = [];
  const bytes = size => size < 1024 ? tr('{n} B',{n:size}) : size < 1048576
    ? tr('{n} KiB',{n:(size/1024).toFixed(1)}) : tr('{n} MiB',{n:(size/1048576).toFixed(1)});
  const make = (tag, text='', cls='') => {
    const el = document.createElement(tag);el.textContent=text;if(cls)el.className=cls;return el;
  };
  const encryptionLabel=make('label',tr('Password encryption')),encryption=make('select'),encryptionHint=make('p','','hint');
  encryption.id='export-encryption';encryptionLabel.htmlFor=encryption.id;
  encryption.append(new Option(tr('ZIP (7-Zip / WinRAR)'),'zip'),
    new Option(tr('Stronger encryption (scrypt + AES-GCM, requires verify.py to open)'),'tgwpw'));
  encryptionHint.id='export-encryption-hint';encryption.setAttribute('aria-describedby',encryptionHint.id);
  const encryptionText=()=>{encryptionHint.textContent=tr(encryption.value==='tgwpw'
    ? 'Open with an independently obtained verify.py: python verify.py unseal-password export.tgwpw --out output-file. Then verify the decrypted evidence.'
    : 'ZIP password protection uses WinZip AES (weak key stretching). Use a long random passphrase of 20+ characters, or choose the stronger encryption for sensitive exports.');};
  encryption.addEventListener('change',encryptionText);encryptionText();
  find('export-password-field').append(encryptionLabel,encryption,encryptionHint);
  const heroButton=root.querySelector('.evidence-hero .evidence-body [data-export="zip"]'),encryptOn=root.querySelector('#export-encrypt-on');
  if(heroButton){
    const containerLabel=make('label',tr('Container')),container=make('select'),containerHint=make('p','','hint');
    container.id='export-container';containerLabel.htmlFor=container.id;containerHint.id='export-container-hint';
    container.setAttribute('aria-describedby',containerHint.id);
    container.append(new Option('ZIP','zip'),new Option(tr('ASiC-E (adds a CAdES signature for ETSI validators)'),'asice'));
    const heroText=[...heroButton.childNodes].find(node=>node.nodeType===3&&node.nodeValue.trim());
    const containerText=()=>{
      const locked=!!encryptOn?.checked;container.options[1].disabled=locked;if(locked)container.value='zip';
      heroButton.dataset.export=container.value;
      if(heroText)heroText.nodeValue=' '+tr(container.value==='asice'?'Download signed ASiC-E container':'Download signed ZIP');
      containerHint.textContent=tr(locked?'Password-protected exports cannot be ASiC-E containers. Turn off the password to choose ASiC-E.'
        : container.value==='asice'?'The same signed archive plus a mimetype entry and META-INF/ASiCManifest.xml with a CAdES signature made with this workspace’s own certificate. CAdES validators such as EU DSS can check its format and integrity; the certificate is self-issued, not qualified and not on any trusted list.'
        : 'Plain ZIP sealed with the Ed25519 journal key.');
    };
    container.addEventListener('change',containerText);encryptOn?.addEventListener('change',containerText);
    heroButton.before(containerLabel,container,containerHint);containerText();
  }
  const STATES={requested:'Waiting for a signature',attached_not_checked:'Attached, not checked',
    verified:'Verified: the signature covers this export and its certificate chains to a root certificate you supplied',
    algorithm_not_supported:'Algorithm not supported',
    signature_invalid:'Signature invalid',bytes_mismatch:'Signed bytes do not match this export',
    trust_not_established:'The signature covers this export; its certificate does not chain to a root certificate you supplied'};
  const told=reason=>typeof reason==='string'?tr(reason):tr(reason.text,Object.fromEntries(Object.entries(reason.values||{})
    .map(([key,value])=>[key,key==='reason'&&typeof value==='string'?tr(value):value])));
  const includable=item=>item.attached_at&&!['signature_invalid','bytes_mismatch','requested'].includes(item.state);
  const toBase64=async file=>{
    const data=new Uint8Array(await file.arrayBuffer());let text='';
    for(let i=0;i<data.length;i+=32768)text+=String.fromCharCode(...data.subarray(i,i+32768));
    return btoa(text);
  };
  const saveBytes=(encoded,filename)=>{
    const url=URL.createObjectURL(new Blob([Uint8Array.from(atob(encoded),c=>c.charCodeAt(0))],{type:'application/octet-stream'}));
    const link=make('a');link.href=url;link.download=filename;document.body.append(link);link.click();link.remove();
    setTimeout(()=>URL.revokeObjectURL(url),30000);
  };
  const fileField=(text,accept)=>{
    const label=make('label',text),input=make('input');input.type='file';input.accept=accept;label.append(input);return [label,input];
  };
  function signatureFacts(item){
    const facts=make('dl'),add=(label,text)=>{if(text)facts.append(make('dt',label),make('dd',String(text)));};
    if(item.signed_name)add(tr('Signed bytes'),item.signed_name+' · '+bytes(item.content_bytes||0));
    add(tr('SHA-256 of the signed bytes'),item.content_sha256);
    if(item.embedded!==undefined)add(tr('Content'),tr(item.embedded?'Embedded in the signature':'Detached'));
    for(const signer of item.signers||[]){
      add(tr('Signer'),signer.certificate?.subject);add(tr('Issuer'),signer.certificate?.issuer);
      add(tr('Serial number'),signer.certificate?.serial);
      add(tr('Signing time claimed by the signer'),signer.claimed_signing_time||tr('Not stated'));
      add(tr('Timestamped time'),signer.timestamp?(signer.timestamp.verified?signer.timestamp.time
        :tr('{time}, timestamp not verified',{time:signer.timestamp.time||'?'})):tr('No timestamp'));
      add(tr('Digest algorithm'),signer.digest_algorithm);add(tr('Signature algorithm'),signer.signature_algorithm);
      add(tr('Content binding'),tr(signer.binding?'Verified':'Not verified'));
      add(tr('Signature value'),tr(signer.signature?'Verified':'Not verified'));
      add(tr('Certificate chain'),signer.chain?.join(' → '));
    }
    if(item.signers)add(tr('Revocation and trusted lists'),tr('Not checked'));
    return facts;
  }
  function signatureView(title,item,note=''){
    const box=make('div','','external-signature-item');
    box.append(make('strong',title),make('p',tr(STATES[item.state]||item.state)));
    if(note)box.append(make('p',note,'hint'));
    box.append(signatureFacts(item));
    for(const reason of [...(item.reasons||[]),...(item.signers||[]).flatMap(signer=>signer.reasons||[])])box.append(make('p',told(reason),'hint'));
    return box;
  }
  async function signatures(entry,body){
    const owner=getSession(),base='exports/'+entry.id+'/external-signatures';
    body.replaceChildren(make('p',tr('Checking…'),'hint'));
    let found;
    try{found=await json(base);}catch(error){if(owner===getSession())body.replaceChildren(make('p',error.message,'hint'));return;}
    if(owner!==getSession())return;
    const parts=[],refresh=()=>signatures(entry,body);
    const run=async(button,work)=>{button.disabled=true;try{await work();await refresh();}catch(error){toast(error.message,true);}finally{button.disabled=false;}};
    if(found.program_signature)parts.push(signatureView(tr('Program CAdES signature (this workspace’s certificate)'),found.program_signature,tr(found.program_signature.note||'')));
    for(const item of found.signatures){
      const box=signatureView(tr('External signature {n}',{n:item.number}),item);
      if(item.state==='requested'){
        box.insertBefore(make('p',tr(item.instruction)),box.children[2]);
        const again=make('button',tr('Save bytes to sign'),'quiet');again.type='button';
        again.addEventListener('click',()=>saveBytes(item.content_base64,item.filename));
        const [fileLabel,file]=fileField(tr('Signature file (.p7s)'),'.p7s,.p7m,.p7,.pem,.sig,application/pkcs7-signature');
        const [rootLabel,roots]=fileField(tr('Trusted root certificates (PEM, optional)'),'.pem,.crt,.cer');
        const [extraLabel,extra]=fileField(tr('Other certificates of the chain (PEM, optional)'),'.pem,.crt,.cer');
        const attach=make('button',tr('Attach signature'),'secondary');attach.type='button';
        attach.addEventListener('click',()=>run(attach,async()=>{
          if(!file.files[0])throw new Error(tr('Choose the signature file.'));
          await json(base+'/'+item.number,{signature:await toBase64(file.files[0]),
            roots:roots.files[0]?await toBase64(roots.files[0]):'',certificates:extra.files[0]?await toBase64(extra.files[0]):''});
        }));
        if(item.content_base64)box.append(again);
        box.append(fileLabel,rootLabel,extraLabel,attach);
      }else if(item.attached_at){
        const [rootLabel,roots]=fileField(tr('Trusted root certificates (PEM)'),'.pem,.crt,.cer');
        const [extraLabel,extra]=fileField(tr('Other certificates of the chain (PEM, optional)'),'.pem,.crt,.cer');
        const check=make('button',tr('Check again'),'quiet');check.type='button';
        check.addEventListener('click',()=>run(check,async()=>{
          const payload={};
          if(roots.files[0])payload.roots=await toBase64(roots.files[0]);
          if(extra.files[0])payload.certificates=await toBase64(extra.files[0]);
          await json(base+'/'+item.number+'/check',payload);
        }));
        box.append(rootLabel,extraLabel,check);
      }
      parts.push(box);
    }
    if(found.eligible){
      const ask=make('button',tr('Prepare bytes to sign'),'secondary');ask.type='button';
      ask.addEventListener('click',()=>run(ask,async()=>{const prepared=await json(base+'/request',{});saveBytes(prepared.content_base64,prepared.filename);}));
      parts.push(ask);
    }else if(found.reason)parts.push(make('p',told(found.reason),'hint'));
    if(found.signatures.some(includable)){
      const signed=make('button',tr('Download with signatures'),'secondary');signed.type='button';
      signed.addEventListener('click',async()=>{signed.disabled=true;try{
        const ticket=await json(base+'/ticket',{}),target=new URL(ticket.url,location.origin);
        if(target.origin!==location.origin)throw new Error(tr('The download address is invalid. Prepare the export again.'));
        const link=make('a');link.href=target.href;link.download='';document.body.append(link);link.click();link.remove();
      }catch(error){toast(error.message,true);}finally{signed.disabled=false;}});
      parts.push(signed);
    }
    body.replaceChildren(...parts);
  }
  const retryButton=make('button',tr('Retry export'),'secondary');retryButton.type='button';retryButton.hidden=true;
  retryButton.id='exports-retry';find('exports-progress').append(retryButton);
  function renderTimes() {
    for(const time of root.querySelectorAll('.export-receipt time')){
      time.textContent=fmtTime(time.dateTime);time.title=time.textContent;
    }
    find('exports-last').textContent=entries.length?tr('Latest: {size} · {time}',{
      size:bytes(entries[0].bytes),time:fmtTime(entries[0].created_at)}):'';
  }
  window.addEventListener('tgwitness:time-zone',renderTimes);
  function select(name, focus=false, {history=true}={}) {
    selected = name === 'settings' ? 'settings' : 'downloads';
    for (const button of tabs) {
      const active = button.dataset.exportTab === selected;
      button.setAttribute('aria-selected',String(active));button.tabIndex=active?0:-1;
      if(active&&focus)button.focus();
    }
    find('exports-downloads').hidden=selected!=='downloads';find('report-form').hidden=selected!=='settings';
    if(history)onTab?.(selected);
  }
  for(const button of tabs) {
    button.addEventListener('click',()=>select(button.dataset.exportTab));
    button.addEventListener('keydown',event=>{
      if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
      event.preventDefault();select(event.key==='Home'?'downloads':event.key==='End'?'settings':selected==='downloads'?'settings':'downloads',true);
    });
  }
  async function load(options={}) {
    const mine=++request, owner=getSession();
    find('exports-history-refresh').disabled=true;
    try {
      const result=await json('exports/history',undefined,options);
      if(owner!==getSession()||mine!==request)return;
      const list=find('exports-history-list');entries=result.exports||[];
      const stamp=JSON.stringify(entries);
      if(list.dataset.stamp!==stamp) {
        const rows=entries.map(entry=>{
          const row=make('div','','export-receipt'),label=make('strong',entry.format==='asice'?'ASiC-E':entry.format.toUpperCase());
          const time=make('time');time.dateTime=entry.created_at;
          row.append(label,make('span',entry.encrypted?tr('Encrypted'):tr('Plain file'),'hint'),
            time,make('span',bytes(entry.bytes)));
          const hash=make('code',entry.sha256),copy=make('button',tr('Copy SHA-256'),'quiet');
          copy.type='button';copy.addEventListener('click',async()=>{
            try{await navigator.clipboard.writeText(entry.sha256);toast(tr('Hash copied.'));}catch{toast(tr('Could not copy. Select and copy the hash.'),true);}
          });
          const detail=make('details'),summary=make('summary',tr('SHA-256'));detail.append(summary,hash,copy);row.append(detail);
          if(entry.cache_warning)row.append(make('p',tr(entry.cache_warning),'hint'));
          if(entry.format==='asice'&&entry.members>1000)row.append(make('p',tr('This container holds {n} files. EU DSS with default settings refuses containers of more than 1000 files.',{n:entry.members}),'hint'));
          if(entry.available&&entry.id){const again=make('button',tr('Download again'),'secondary');again.type='button';
            again.addEventListener('click',async()=>{again.disabled=true;try{await downloadAgain(entry);}catch(error){toast(error.message,true);}finally{again.disabled=false;}});row.append(again);}
          if(entry.available&&entry.id&&!entry.encrypted&&['zip','asice'].includes(entry.format)){
            const sign=make('details','','external-signature'),body=make('div');sign.append(make('summary',tr('External signature')),body);
            sign.addEventListener('toggle',()=>{if(sign.open)void signatures(entry,body);});row.append(sign);
          }
          return row;
        });
        list.replaceChildren(...rows);list.dataset.stamp=stamp;
      }
      renderTimes();
      find('exports-history-status').textContent=entries.length?'':tr('No exports prepared yet. Choose a format above.');
    }catch(error){
      if(owner===getSession()&&mine===request&&!['AbortError','StaleView'].includes(error.name))find('exports-history-status').textContent=error.message;
    }finally{if(owner===getSession()&&mine===request)find('exports-history-refresh').disabled=false;}
  }
  find('exports-history-refresh').addEventListener('click',()=>load());
  function begin({format='zip',encrypted=false,encryption='zip',retry=null}={}) {
    const owner=getSession(), mine=++transfer;
    retryButton.hidden=true;retryButton.onclick=()=>{if(owner===getSession()&&mine===transfer)retry?.();};
    select('downloads');find('exports-progress').hidden=false;
    find('exports-next').hidden=true;
    find('exports-progress-bar').hidden=false;
    find('exports-progress-label').textContent=tr('Confirm');
    find('exports-progress-bar').removeAttribute('value');find('exports-progress-bytes').textContent='';
    return update=>{
      if(owner!==getSession()||mine!==transfer)return;
      const labels={preparing:tr('Checking journal integrity and preparing the export…'),saving:tr('Saving export…'),done:tr('Export saved.'),browser:tr('Download started. Check your browser’s downloads.'),cancelled:tr('Download cancelled.'),failed:tr('Download failed. Retry the export.')};
      if(labels[update.phase])find('exports-progress-label').textContent=labels[update.phase];
      if(update.total!==undefined)find('exports-progress-bytes').textContent=update.expected
        ? tr('{saved} of {total}',{saved:bytes(update.total),total:bytes(update.expected)}):bytes(update.total);
      const bar=find('exports-progress-bar');
      if(update.expected){bar.max=update.expected;bar.value=update.total||0;}
      if(['done','browser'].includes(update.phase)){
        bar.max=1;bar.value=1;void load();
        find('exports-next-copy').textContent=tr(format==='asice'
          ? 'The .asice file is a ZIP archive: extract it and open report.html. Review coverage gaps and personal information. README.txt explains how to check integrity with an independently obtained signing-key fingerprint.'
          : format==='zip'
          ? 'Extract the ZIP and open report.html. Review coverage gaps and personal information. README.txt explains how to check integrity with an independently obtained signing-key fingerprint.'
          : format==='html'
          ? 'Open the HTML report in your browser. Review coverage gaps and personal information before sending the unchanged file.'
          : 'Review this data file in a compatible tool. Download the signed ZIP when your recipient also needs the readable report and verification tools.');
        find('exports-next-encrypted').textContent=tr(encryption==='tgwpw'
          ? 'Open with an independently obtained verify.py: python verify.py unseal-password export.tgwpw --out output-file. Then verify the decrypted evidence.'
          : 'Open the encrypted ZIP with 7-Zip or WinRAR and the password. Keep the password separate from the file.');
        find('exports-next-encrypted').hidden=!encrypted;find('exports-next').hidden=false;
      }
      if(['failed','cancelled'].includes(update.phase)){bar.hidden=true;if(update.error)find('exports-progress-bytes').textContent=update.error;void load();}
      else bar.hidden=false;
      retryButton.hidden=update.phase!=='failed'||!retry;
    };
  }
  return {load,select,begin,get tab(){return selected;},leave(){request++;find('exports-history-refresh').disabled=false;},resetSession(){
    session=getSession();request++;transfer++;entries=[];select('downloads',false,{history:false});find('exports-progress').hidden=true;find('exports-next').hidden=true;
    retryButton.hidden=true;retryButton.onclick=null;
    find('exports-history-list').replaceChildren();delete find('exports-history-list').dataset.stamp;
    find('exports-last').textContent=find('exports-history-status').textContent='';
  },destroy(){window.removeEventListener('tgwitness:time-zone',renderTimes);},
    enter(options){if(session!==getSession())this.resetSession();return load(options);}};
}
