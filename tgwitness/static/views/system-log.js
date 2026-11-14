export function createSystemLog({root,tr,json,getState,getSession,options,formatTime,toast,download}) {
  const find=id=>root.querySelector('#'+id), listeners=new AbortController();
  let after=0,request=0,session=getSession();
  const active=()=>getState().view==='system-log'&&!!getState().me?.admin;
  function resetSession(){session=getSession();after=0;request++;find('access-console').replaceChildren();find('console-state').textContent='';}
  async function load(){
    if(!active())return;
    if(session!==getSession())resetSession();
    const started=getSession(),serial=++request,view=options(),pre=find('access-console');
    const result=await json('access/console?after='+after,undefined,{root:true,...view});
    if(!active()||started!==getSession()||serial!==request||view.signal?.aborted)return;
    if(result.lines.length&&result.lines[0].n<=after)pre.replaceChildren();
    for(const line of result.lines){
      const last=pre.lastElementChild,key=line.level+'|'+line.source+'|'+line.text,at=Date.parse(line.at);
      if(last?.dataset.key===key&&at-Number(last.dataset.first)<=5000){
        const repeat=Number(last.dataset.repeat)+1;last.dataset.repeat=String(repeat);
        last.textContent=formatTime(last.dataset.at)+' '+line.level.padEnd(7)+' '+line.text+' '+tr('(×{n} in {ms} ms)',{n:repeat,ms:Math.max(0,at-Number(last.dataset.first))})+'\n';
        continue;
      }
      const item=root.ownerDocument.createElement('span');item.className='console-line '+line.level.toLowerCase();
      Object.assign(item.dataset,{key,first:String(at),at:line.at,repeat:'1'});
      item.textContent=formatTime(line.at)+' '+line.level.padEnd(7)+' '+line.text+'\n';pre.append(item);
    }
    while(pre.childElementCount>3000)pre.firstElementChild.remove();
    after=result.last;
    find('console-state').textContent=tr('{n} recent log lines',{n:pre.childElementCount});
    if(result.lines.length&&find('console-follow').checked)pre.scrollTop=pre.scrollHeight;
  }
  find('console-refresh').addEventListener('click',()=>load().catch(error=>{if(error.name!=='StaleView')toast(error.message,true);}),{signal:listeners.signal});
  find('console-flight').addEventListener('click',async event=>{
    const button=event.currentTarget;if(button.disabled)return;button.disabled=true;
    try{if(await download?.('flight','tgwitness-flight-'+new Date().toISOString().replace(/[:.]/g,'-')+'.jsonl',false,true)!==false)toast(tr('Flight record saved.'));}
    catch(error){if(error.name!=='StaleView')toast(error.message,true);}
    finally{button.disabled=false;}
  },{signal:listeners.signal});
  return {load,enter:load,leave(){request++;},resetSession,destroy(){listeners.abort();resetSession();}};
}
