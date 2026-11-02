// Step-by-step setup (wizard.py): one question per page, each page its own address, and the answers kept
// in the workspace so a closed tab returns to the same step. Applying goes through /api/setup/wizard/apply,
// which writes the same settings and signed journal records as their own forms.
import {renderScales} from "./setup.js?v=4";

const STEP_TYPES=["channels","groups","private","bots"];
const KIND_TYPE={channel:"channels",supergroup:"groups",group:"groups",private:"private",bot:"bots"};
const EVENTS=["messages","edits","deletions","reactions","membership"];
const LIST_LIMIT=400;

export function createWizard(context){
  const {root,tr,trn,json,node,toast,getState,refreshStatus,signedIn,authCard,setAuthStep,avatarNode,humanSize,
    fmtFull,record,openAccountExport,openExtra,leaveTo,may,askConfirm,stateBadge,healthLines,healthNames}=context;
  let data=null,answers={},step="goal",session=null;
  let dialogs=null,dialogsLoading=false,dialogsError="",search="",typeFilter="";
  let preview=null,previewKey="",routeDraft=null,routeNote=null,outsideOpen=false,live=null,skipConnection=false;
  let authHome=null,shownSignedIn=null,afterRender=null;

  const titles={goal:tr("What do you need?"),connection:tr("How will TgWitness reach Telegram?"),
    account:tr("Which Telegram account?"),chats:tr("Which chats to record?"),saving:tr("What to save"),
    place:tr("Where will it run?"),summary:tr("Check and start")};
  const shortNames={goal:tr("Goal"),connection:tr("Connection"),account:tr("Account"),chats:tr("Chats"),
    saving:tr("What to save"),place:tr("Where it runs"),summary:tr("Summary")};
  const goalNames={copy:tr("Save a copy of my account"),watch:tr("Watch chats"),evidence:tr("Collect evidence for a case")};
  const purposeNames={personal:tr("For myself"),investigation:tr("An investigation")};
  const modeNames={selected:tr("Chosen chats"),folder:tr("Telegram folder"),account:tr("Whole account")};
  const mediaNames={none:tr("Do not save files"),small:tr("Files up to 20 MB"),standard:tr("Files up to 100 MB"),
    all:tr("Everything up to 1 GB")};
  const historyNames={none:tr("No earlier messages"),recent:tr("The last {n} messages of each chat",{n:100}),
    all:tr("All available history")};
  const eventNames={messages:tr("New messages"),edits:tr("Message edits"),deletions:tr("Message deletions"),reactions:tr("Reactions"),
    membership:tr("Members joining and leaving")};
  const typeNames={channels:tr("Channels"),groups:tr("Groups"),private:tr("Private chats"),bots:tr("Bots")};

  // ---------- shell ----------
  const shell=node("div","wizard"),head=node("header","wizard-head");
  const count=node("p","wizard-count"),bar=node("div","wizard-bar"),fill=node("span");
  bar.setAttribute("role","progressbar");bar.setAttribute("aria-valuemin","0");bar.append(fill);
  head.append(node("span","eyebrow",tr("STEP-BY-STEP SETUP")),count,bar);
  const layout=node("div","wizard-layout"),list=node("ol","wizard-steps"),page=node("section","wizard-page card");
  list.setAttribute("aria-label",tr("Setup steps"));
  layout.append(list,page);
  const nav=node("footer","wizard-nav"),back=button("secondary",tr("← Back")),next=button("primary",tr("Next →"));
  const navNote=node("p","wizard-nav-note");navNote.setAttribute("role","status");
  nav.append(back,navNote,next);
  shell.append(head,layout,nav);
  root.replaceChildren(shell);
  back.addEventListener("click",()=>{const i=steps().indexOf(step);if(i>0)go(steps()[i-1]);});
  next.addEventListener("click",()=>{if(!ready(step))return;const i=steps().indexOf(step);if(i<steps().length-1)go(steps()[i+1]);});

  function button(cls,text){const b=node("button",cls,text);b.type="button";return b;}
  async function work(control,task){
    if(control?.disabled)return;
    if(control){control.disabled=true;control.setAttribute("aria-busy","true");}
    try{return await task();}
    catch(error){if(error?.name!=="StaleView")toast(error.message,true);}
    finally{if(control){control.disabled=false;control.removeAttribute("aria-busy");}}
  }
  const status=()=>getState().status;
  const steps=()=>answers.goal==="copy"?["goal","connection","account","summary"]:
    ["goal","connection","account","chats","saving","place","summary"];
  const kind=()=>answers.goal==="evidence"?"evidence":answers.goal==="watch"?(answers.purpose||"investigation"):null;
  const connectionOk=()=>!!data?.checks?.connection?.ok&&data.checks.connection.kind===data.route?.kind;

  // ---------- what each step needs ----------
  function ready(name){
    if(name==="goal")return !!answers.goal&&(answers.goal!=="watch"||!!answers.purpose);
    if(name==="connection")return connectionOk()||skipConnection||signedIn();
    if(name==="account")return signedIn()&&(answers.goal==="copy"||!!answers.account_kind);
    if(name==="chats"){
      const c=answers.chats;if(!c)return false;
      if(c.mode==="selected")return c.chat_ids.length>0;
      if(c.mode==="folder")return c.folder_id!==null&&c.folder_id!==undefined;
      return c.acknowledged&&answers.account_kind!=="main";
    }
    if(name==="saving")return !!answers.saving;
    if(name==="place")return !!answers.place;
    return true;
  }
  function reachable(name){
    const order=steps(),i=order.indexOf(name);
    return i>=0&&order.slice(0,i).every(ready);
  }
  function why(name){
    if(name==="goal")return answers.goal==="watch"?tr("Choose what the record is for."):tr("Choose what you need.");
    if(name==="connection")return tr("Check the connection first, or skip it for now.");
    if(name==="account")return !signedIn()?tr("Sign in to Telegram to continue."):tr("Say whether this is a separate account.");
    if(name==="chats"){
      const c=answers.chats;
      return c?.mode==="account"?(answers.account_kind==="main"?tr("The whole account can be recorded only on a separate account."):tr("Confirm that this is a separate account.")):
        c?.mode==="folder"?tr("Choose a folder."):tr("Choose at least one chat.");
    }
    if(name==="place")return tr("Choose where TgWitness runs.");
    return "";
  }

  // ---------- progress on the server ----------
  function cleanAnswers(){
    const a={goal:answers.goal||null,purpose:answers.goal==="watch"?answers.purpose||null:null,
      connection:answers.connection||null,account_kind:answers.account_kind||null,chats:answers.chats||null,
      saving:answers.saving||null,place:answers.place||null};
    if(a.chats)a.chats={mode:a.chats.mode,chat_ids:[...new Set(a.chats.chat_ids)],folder_id:a.chats.folder_id??null,
      types:{...a.chats.types},acknowledged:!!a.chats.acknowledged};
    return a;
  }
  let saving=Promise.resolve();
  function persist(){
    if(!may("settings")||status()?.demo)return saving;
    const body={step,answers:cleanAnswers()};
    saving=saving.then(()=>json("setup/wizard",body).then(result=>{data={...result,checks:result.checks};renderSteps();}))
      .catch(error=>{if(error?.name!=="StaleView")toast(error.message,true);});
    return saving;
  }

  // ---------- navigation ----------
  function go(name,{history=true,focus=true}={}){
    if(!steps().includes(name))name=steps()[0];
    if(!reachable(name))name=steps().find(s=>!ready(s))||name;
    step=name;
    // Opening the wizard only reads; the step is saved once the person moves.
    if(history)persist();
    render();
    if(history)record();
    if(focus)page.querySelector("h1")?.focus({preventScroll:false});
  }

  // ---------- rendering ----------
  function renderSteps(){
    const order=steps(),i=order.indexOf(step);
    count.textContent=tr("Step {n} of {total}",{n:i+1,total:order.length});
    const percent=Math.round(100*(i+1)/order.length);
    fill.style.width=percent+"%";bar.setAttribute("aria-valuemax","100");bar.setAttribute("aria-valuenow",String(percent));
    bar.setAttribute("aria-valuetext",count.textContent);
    list.replaceChildren(...order.map((name,index)=>{
      const item=node("li","wizard-step"),done=index<i&&ready(name)||name!==step&&name!=="summary"&&ready(name)&&reachable(name);
      item.classList.toggle("current",name===step);item.classList.toggle("done",done);
      const link=button("wizard-step-link","");
      link.append(node("span","wizard-step-mark",done?"✓":String(index+1)),node("span","",shortNames[name]));
      link.disabled=!reachable(name);
      if(name===step)link.setAttribute("aria-current","step");
      link.addEventListener("click",()=>go(name));
      item.append(link);return item;
    }));
    back.hidden=i<=0;
    const last=i===order.length-1;next.hidden=last;
    next.disabled=!ready(step);
    navNote.textContent=!last&&!ready(step)?why(step):"";
  }
  function render(){
    if(!data)return;
    if(step!=="account")restoreAuth();
    renderSteps();
    const h=node("h1","",titles[step]);h.tabIndex=-1;
    const body=node("div","wizard-body");
    ({goal:renderGoal,connection:renderConnection,account:renderAccount,chats:renderChats,saving:renderSaving,
      place:renderPlace,summary:renderSummary})[step](body);
    page.replaceChildren(h,body);
    page.dataset.step=step;root.dataset.step=step;
    const after=afterRender;afterRender=null;after?.();
  }

  function group(label){const box=node("div","wizard-choices");box.setAttribute("role","radiogroup");box.setAttribute("aria-label",label);return box;}
  function option(box,name,value,{title,when,recommended=false,help="",checked=false,disabled=false,onPick}){
    const wrap=node("div","wizard-option"),label=node("label","wizard-choice"),input=node("input");
    input.type="radio";input.name=name;input.value=value;input.checked=checked;input.disabled=disabled;
    const text=node("span","wizard-choice-text"),top=node("span","wizard-choice-top");
    top.append(node("strong","",title));
    if(recommended)top.append(node("span","wizard-tag",tr("Recommended")));
    text.append(top);if(when)text.append(node("small","",when));
    label.append(input,text);wrap.append(label);
    if(help){
      const more=node("details","wizard-help"),summary=node("summary","","?");
      summary.setAttribute("aria-label",tr("More about: {title}",{title}));summary.title=tr("More");
      more.append(summary,node("p","",help));wrap.append(more);
    }
    input.addEventListener("change",()=>{if(input.checked)onPick(value);});
    box.append(wrap);return input;
  }
  function notice(kind,text){const box=node("div","wizard-notice "+kind);box.append(node("p","",text));return box;}

  // ---------- 1. goal ----------
  function renderGoal(body){
    body.append(node("p","hint",tr("Pick the closest answer. We suggest the settings for it; you can change each one later.")));
    const goals=group(titles.goal);
    const pick=value=>{
      if(answers.goal!==value){answers.goal=value;answers.saving=null;answers.chats=null;answers.purpose=value==="watch"?answers.purpose||null:null;}
      persist();render();
    };
    option(goals,"wizard-goal","copy",{title:goalNames.copy,checked:answers.goal==="copy",onPick:pick,
      when:tr("A one-off download of the chats and history the account can read now. No continuous recording."),
      help:tr("For example, to keep your own chats before you delete the app or change phones. Messages deleted before the download cannot be recovered.")});
    option(goals,"wizard-goal","watch",{title:goalNames.watch,checked:answers.goal==="watch",recommended:true,onPick:pick,
      when:tr("New messages, edits and deletions in the chats you choose, kept as they happen."),
      help:tr("For example, scam groups you report to abuse teams: TgWitness keeps what was posted even after it is edited or deleted.")});
    option(goals,"wizard-goal","evidence",{title:goalNames.evidence,checked:answers.goal==="evidence",onPick:pick,
      when:tr("Everything is kept with strict integrity settings, for police, a court or a platform."),
      help:tr("Independent timestamps are switched on and sending messages from the panel is switched off, so the record holds up when someone challenges it.")});
    body.append(goals);
    if(answers.goal==="watch"){
      body.append(node("h2","wizard-sub",tr("What is the record for?")));
      const purposes=group(tr("What is the record for?"));
      const choose=value=>{answers.purpose=value;answers.saving=null;answers.chats=null;persist();render();};
      option(purposes,"wizard-purpose","personal",{title:purposeNames.personal,checked:answers.purpose==="personal",onPick:choose,
        when:tr("Only the chats you choose, without people's profiles, files up to 20 MB.")});
      option(purposes,"wizard-purpose","investigation",{title:purposeNames.investigation,checked:answers.purpose==="investigation",
        recommended:true,onPick:choose,
        when:tr("Reports to abuse teams: a separate account, new chats and bots added as they appear, files up to 100 MB.")});
      body.append(purposes);
    }
    const expert=button("text-link wizard-expert",tr("I am experienced, I will set it up myself"));
    expert.addEventListener("click",()=>work(expert,async()=>{
      data=await json("setup/wizard/skip",{reason:"expert"});
      await refreshStatus();leaveTo("start");
    }));
    body.append(expert);
  }

  // ---------- 2. connection ----------
  function routeName(route){
    if(!route?.kind)return tr("Not chosen");
    const where=route.host?" · "+route.host+":"+route.port:"";
    return ({direct:tr("Direct connection"),socks5:tr("SOCKS5 proxy"),http:tr("HTTP proxy"),mtproxy:tr("Your MTProto proxy"),
      mtproxy_auto:tr("Public proxies")}[route.kind]||route.kind)+where;
  }
  function problemText(code){
    return {direct_unreachable:tr("Telegram does not open directly from this computer. Use a proxy."),
      proxy_unreachable:tr("The proxy does not answer or refused the connection. Check its address, port and password."),
      bad_secret:tr("The MTProto secret is wrong. Copy the link again from the proxy's owner."),
      no_public_proxy:tr("None of the public proxies answered. Try your own proxy."),
      blocked_by_ip_mode:tr("The IP protection mode does not allow this route. Choose a proxy."),
      rate_limited:tr("Telegram asked to wait. Try again in a few minutes.")}[code]||tr("The connection check failed.");
  }
  function parseProxy(text){
    const value=text.trim();if(!value)return null;
    if(/^(tg:\/\/proxy|https?:\/\/(t|telegram)\.me\/proxy)\?/i.test(value))return {kind:"mtproxy",link:value};
    let url;try{url=new URL(/^[a-z0-9+.-]+:\/\//i.test(value)?value:"socks5://"+value);}catch{return {error:true};}
    const scheme=url.protocol.replace(":","").toLowerCase();
    const kindOf={socks5:"socks5",socks5h:"socks5",socks:"socks5",http:"http",https:"http"}[scheme];
    const port=Number(url.port||(kindOf==="http"?8080:1080));
    if(!kindOf||!url.hostname||!Number.isInteger(port)||port<1||port>65535)return {error:true};
    return {kind:kindOf,host:url.hostname.replace(/^\[|\]$/g,""),port,
      username:decodeURIComponent(url.username||""),password:decodeURIComponent(url.password||"")};
  }
  async function routeConfig(){
    const choice=answers.connection;
    if(choice==="direct")return {kind:"direct"};
    if(choice==="public")return {kind:"mtproxy_auto"};
    if(choice!=="mtproxy"&&choice!=="socks5"&&choice!=="http")return null;
    const draft=routeDraft||{};
    if(draft.parsed?.kind==="mtproxy"){
      const r=await json("network/parse-link",{link:draft.parsed.link});
      return {kind:"mtproxy",host:r.host,port:r.port,secret:r.secret};
    }
    if(draft.parsed&&!draft.parsed.error)return {kind:draft.parsed.kind,host:draft.parsed.host,port:draft.parsed.port,
      username:draft.parsed.username,password:draft.parsed.password};
    throw new Error(tr("Paste a proxy link or address first."));
  }
  async function pauseIfRunning(){
    if(!status().collector.running)return true;
    if(!(await askConfirm(tr("Pause observation to change the route? New messages, edits and deletion notices are not collected while paused, and an unfinished sign-in is cancelled when the route is saved."),{confirmText:tr("Pause observation")})))return false;
    await json("collector/stop",{});await refreshStatus();return true;
  }
  async function checkConnection(){
    routeNote={state:"running",text:tr("Checking the connection to Telegram…")};render();
    const r=await json("setup/wizard/check-connection",{});
    data.checks={...data.checks,connection:r};data.route=r.route;data.policy=r.policy;
    routeNote=null;skipConnection=false;
    await refreshStatus();render();
    return r;
  }
  async function saveAndCheck(control){
    await work(control,async()=>{
      if(answers.connection==="keep"){await checkConnection();return;}
      if(answers.connection==="check"){
        if(!(await pauseIfRunning()))return;
        await json("setup/wizard/route",{kind:"direct"});
        const r=await checkConnection();
        if(!r.ok)routeNote={state:"failed",text:tr("Telegram does not open directly from this computer. A proxy is needed: enter your own, or use a public one as a fallback.")};
        render();return;
      }
      const config=await routeConfig();if(!config)return;
      if(!(await pauseIfRunning()))return;
      const r=await json("setup/wizard/route",config);data.route=r.route;data.policy=r.policy;
      await checkConnection();
    });
  }
  function renderConnection(body){
    const route=data.route||{},check=data.checks?.connection,known=signedIn()||!!check?.ok;
    if(!answers.connection)answers.connection=known?"keep":null;
    body.append(node("p","hint",tr("TgWitness connects to Telegram from this computer. If Telegram is blocked here, use a proxy.")));
    const routes=group(titles.connection);
    const pick=value=>{answers.connection=value;routeNote=null;persist();render();};
    if(known)option(routes,"wizard-route","keep",{title:tr("Keep the current connection"),when:routeName(route),
      checked:answers.connection==="keep",recommended:true,onPick:pick});
    option(routes,"wizard-route","direct",{title:tr("Directly"),checked:answers.connection==="direct",recommended:!known,onPick:pick,
      when:tr("If Telegram opens here without a VPN. Telegram sees this computer's address."),
      help:tr("The simplest and fastest route. Choose a proxy instead if Telegram should not learn where TgWitness runs.")});
    const own=["mtproxy","socks5","http"].includes(answers.connection);
    option(routes,"wizard-route","mtproxy",{title:tr("Through my proxy"),checked:own,onPick:pick,
      when:tr("An MTProto link (tg://proxy or t.me/proxy), SOCKS5 or HTTP. Telegram sees the proxy, not this computer."),
      help:tr("Paste the link or address exactly as you received it, for example socks5://user:password@host:1080. We read the type, address, port and password from it.")});
    option(routes,"wizard-route","check",{title:tr("I do not know: check for me"),checked:answers.connection==="check",onPick:pick,
      when:tr("We try a direct connection first (Telegram sees this computer's address). If it fails, we suggest a proxy.")});
    body.append(routes);
    if(own){
      const field=node("div","wizard-field"),label=node("label","",tr("Proxy link or address")),input=node("input");
      input.id="wizard-proxy";label.htmlFor=input.id;input.type="password";input.autocomplete="off";input.spellcheck=false;
      input.placeholder="tg://proxy?…  ·  socks5://user:password@host:1080";input.value=routeDraft?.text||"";
      const parsed=node("p","hint wizard-parsed");parsed.setAttribute("role","status");
      const show=()=>{
        const p=routeDraft?.parsed;
        parsed.textContent=!p?"":p.error?tr("This is not a proxy link or address."):p.kind==="mtproxy"?tr("MTProto proxy link"):
          (p.kind==="http"?tr("HTTP proxy"):tr("SOCKS5 proxy"))+" · "+p.host+":"+p.port+(p.username?" · "+tr("with a login"):"");
        parsed.classList.toggle("error",!!p?.error);
      };
      input.addEventListener("input",()=>{routeDraft={text:input.value,parsed:parseProxy(input.value)};
        const usable=!!routeDraft.parsed&&!routeDraft.parsed.error;
        if(usable)answers.connection=routeDraft.parsed.kind;
        const run=page.querySelector(".wizard-run");if(run)run.disabled=!usable;
        show();});
      field.append(label,input,parsed);body.append(field);show();
    }
    const actions=node("div","wizard-actions");
    const run=button("primary wizard-run",answers.connection==="keep"?tr("Check the connection"):tr("Save and check"));
    run.disabled=!answers.connection||own&&!(routeDraft?.parsed&&!routeDraft.parsed.error);
    run.addEventListener("click",()=>saveAndCheck(run));actions.append(run);
    body.append(actions);
    if(status().collector.running&&answers.connection!=="keep")
      body.append(notice("warning",tr("Observation is running. Changing the route pauses it first; you will be asked.")));
    const result=node("div","wizard-result");result.setAttribute("role","status");result.setAttribute("aria-live","polite");
    if(routeNote?.state==="running")result.append(node("p","wizard-progress",routeNote.text));
    else if(check&&check.kind===route.kind){
      if(check.ok){
        result.append(notice("success",tr("Connected to Telegram in {ms} ms · {route}",{ms:check.elapsed_ms??"?",route:routeName(route)})));
        if(route.kind==="mtproxy_auto")result.append(notice("warning",tr("Public proxies are run by strangers. They see that this computer uses Telegram (not the content) and may stop at any time. Your own proxy is better; the protection scale counts this as a penalty.")));
      }else{
        const box=notice("error",problemText(check.code));
        const more=node("details","wizard-detail");more.append(node("summary","",tr("Details")),node("code","",check.detail||""));box.append(more);
        result.append(box);
        if(routeNote?.state==="failed")result.append(node("p","",routeNote.text));
        const ways=node("div","wizard-actions");
        const mine=button("secondary",tr("Enter my proxy"));mine.addEventListener("click",()=>{answers.connection="mtproxy";routeNote=null;render();page.querySelector("#wizard-proxy")?.focus();});
        const pub=button("secondary",tr("Use public proxies (fallback)"));
        pub.addEventListener("click",()=>work(pub,async()=>{
          answers.connection="public";
          if(!(await pauseIfRunning()))return;
          const r=await json("setup/wizard/route",{kind:"mtproxy_auto"});data.route=r.route;data.policy=r.policy;
          await checkConnection();
        }));
        ways.append(mine,pub);result.append(ways);
      }
    }
    body.append(result);
    if(connectionOk()&&data.policy?.outside_route==="none"&&kind()!=="personal"&&answers.goal!=="copy")body.append(outsideBox());
    if(!connectionOk()&&!signedIn()){
      const skip=button("text-link",tr("Skip for now, I will set it up later"));
      skip.addEventListener("click",()=>{skipConnection=true;go("account");});
      body.append(node("p","hint",tr("Without a checked connection, sign-in may fail.")),skip);
    }
  }
  // Timestamps and notifications leave Telegram: a hidden address sends them only through a SOCKS5 or HTTP proxy.
  function outsideBox(){
    const box=notice("warning",tr("Timestamps, notifications and the off-site copy cannot be sent now: an MTProto proxy carries only Telegram traffic, and this computer's address stays hidden. Set a SOCKS5 or HTTP proxy for these requests, or leave them off."));
    const open=button("secondary small",tr("Set a proxy for these requests"));
    open.addEventListener("click",()=>{outsideOpen=!outsideOpen;render();});
    box.append(open);
    if(outsideOpen){
      const form=node("form","wizard-outside");
      const field=(id,label,attrs={})=>{const wrap=node("div","wizard-field"),l=node("label","",label),i=node("input");i.id=id;l.htmlFor=id;Object.assign(i,attrs);wrap.append(l,i);form.append(wrap);return i;};
      const address=field("wizard-outside-proxy",tr("SOCKS5 or HTTP proxy address"),{placeholder:"socks5://user:password@host:1080",autocomplete:"off",spellcheck:false,type:"password",required:true});
      const save=node("button","primary small",tr("Save"));save.type="submit";form.append(save);
      form.addEventListener("submit",event=>{event.preventDefault();work(save,async()=>{
        const p=parseProxy(address.value);
        if(!p||p.error||p.kind==="mtproxy")throw new Error(tr("Enter a SOCKS5 or HTTP proxy, for example socks5://user:password@host:1080."));
        data.policy=await json("network/policy",{exposure:data.policy.exposure,outside_enabled:true,
          outside_proxy:{kind:p.kind,host:p.host,port:p.port,username:p.username,password:p.password},remove_outside_proxy:false});
        outsideOpen=false;toast(tr("Saved. Requests outside Telegram go through this proxy."));render();
      });});
      box.append(form);
    }
    return box;
  }

  // ---------- 3. account ----------
  function restoreAuth(){
    if(authHome&&authCard.parentNode!==authHome.parentNode){authHome.after(authCard);}
  }
  function renderAccount(body){
    const s=status(),account=s.collector.account;
    if(signedIn()){
      restoreAuth();
      const who=node("div","wizard-account");
      if(account)who.append(avatarNode(account.id,account.username||account.first_name||tr("Account"),"lg"));
      const text=node("div");
      text.append(node("strong","",tr("Signed in to Telegram")),
        node("span","",account?(account.username?"@"+account.username+" · ":"")+"ID "+account.id:""));
      who.append(text);body.append(notice("success",tr("Telegram accepted the sign-in.")),who);
      body.append(node("p","hint",tr("To use another account, add a workspace under Accounts: each account keeps its own journal.")));
    }else{
      body.append(node("p","hint",tr("Sign in with a phone number, a QR code or account files. The code comes in Telegram.")));
      // The account page's own sign-in form, moved here while this step is open: one sign-in, one set of checks.
      const slot=node("div","wizard-auth"),mounted=root.contains(authCard);body.append(slot);
      if(!authHome){authHome=document.createComment("auth-card");authCard.before(authHome);}
      slot.append(authCard);
      const pending=["login_required","password_required","qr_required"].includes(s.collector.phase);
      // The form finds its parts by id, so it is reset once it is on the page.
      if(!mounted&&!pending)afterRender=()=>setAuthStep("credentials");
    }
    shownSignedIn=signedIn();
    if(answers.goal==="copy")return;
    body.append(node("h2","wizard-sub",tr("Is this a separate account or your main one?")));
    const kinds=group(tr("Is this a separate account or your main one?"));
    const pick=value=>{answers.account_kind=value;if(value==="main"&&answers.chats&&answers.chats.mode!=="selected")answers.chats={...answers.chats,mode:"selected",acknowledged:false};persist();render();};
    option(kinds,"wizard-account-kind","dedicated",{title:tr("A separate account"),recommended:true,checked:answers.account_kind==="dedicated",onPick:pick,
      when:tr("Made for recording: it joins only the chats you want to keep."),
      help:tr("Recording sees everything the account sees, including private chats of other people. A separate account keeps your own chats out of the journal and does not risk your main account.")});
    option(kinds,"wizard-account-kind","main",{title:tr("My main account"),checked:answers.account_kind==="main",onPick:pick,
      when:tr("The account you use every day.")});
    body.append(kinds);
    if(answers.account_kind==="main")body.append(notice("warning",tr("Your own private chats can end up in the journal and in exports. Only chosen chats can be recorded on a main account; the whole account and folders stay off. The protection scale counts a main account as a penalty.")));
  }

  // ---------- 4. chats ----------
  function chatsDefaults(){
    const s=status(),scope=data.current?.scope||s.scope||{mode:"selected"},preset=data.presets?.[kind()];
    const enabled=s.targets.filter(t=>t.enabled).map(t=>t.chat_id);
    const mode=answers.account_kind==="main"?"selected":preset?.chats||"selected";
    return {mode,chat_ids:enabled,folder_id:scope.folder_id??null,
      types:{channels:true,groups:true,private:true,bots:true,...(scope.types||{})},acknowledged:false};
  }
  async function loadDialogs(force=false){
    if(dialogsLoading||(dialogs&&!force))return;
    dialogsLoading=true;dialogsError="";if(step==="chats")render();
    try{dialogs=await json("dialogs");}
    catch(error){if(error?.name!=="StaleView")dialogsError=error.message;}
    finally{dialogsLoading=false;if(step==="chats")render();}
  }
  function willRecord(){
    const c=answers.chats;if(!c||!dialogs)return c?.mode==="selected"?c.chat_ids.length:null;
    if(c.mode==="selected")return c.chat_ids.length;
    if(c.mode==="folder")return dialogs.folders.find(f=>f.id===c.folder_id)?.chats??null;
    return dialogs.dialogs.filter(d=>c.types[KIND_TYPE[d.kind]]).length;
  }
  function renderChats(body){
    if(!answers.chats)answers.chats=chatsDefaults();
    const c=answers.chats,main=answers.account_kind==="main";
    if(!dialogs&&!dialogsLoading&&!dialogsError)loadDialogs();
    const modes=group(titles.chats);
    const pick=value=>{answers.chats={...c,mode:value,acknowledged:value===c.mode?c.acknowledged:false};persist();render();};
    option(modes,"wizard-scope","selected",{title:modeNames.selected,checked:c.mode==="selected",recommended:kind()!=="investigation"||main,onPick:pick,
      when:tr("Only the chats you tick below.")});
    option(modes,"wizard-scope","folder",{title:modeNames.folder,checked:c.mode==="folder",disabled:main,onPick:pick,
      when:main?tr("Only on a separate account."):tr("The chats of one Telegram folder, including chats added to it later.")});
    option(modes,"wizard-scope","account",{title:modeNames.account,checked:c.mode==="account",disabled:main,
      recommended:kind()==="investigation"&&!main,onPick:pick,
      when:main?tr("Only on a separate account."):tr("Every chat, group, channel and bot the account sees, and new ones as they appear.")});
    body.append(modes);
    const loading=node("p","wizard-progress");loading.setAttribute("role","status");
    if(dialogsLoading)loading.textContent=tr("Loading the account's chats…");
    body.append(loading);
    if(dialogsError){
      const box=notice("error",tr("The chat list could not be loaded: {error}",{error:dialogsError}));
      const again=button("secondary small",tr("Try again"));again.addEventListener("click",()=>{dialogsError="";loadDialogs(true);});
      box.append(again);body.append(box);
    }
    if(c.mode==="selected")body.append(chatPicker());
    if(c.mode==="folder"&&dialogs){
      const field=node("div","wizard-field"),label=node("label","",tr("Folder")),select=node("select");
      select.id="wizard-folder";label.htmlFor=select.id;
      select.append(new Option(tr("Choose a folder"),""));
      for(const f of dialogs.folders)select.append(new Option((f.title||tr("Folder {id}",{id:f.id}))+" · "+trn("{n} chat","{n} chats",f.chats),String(f.id)));
      select.value=c.folder_id===null?"":String(c.folder_id);
      select.addEventListener("change",()=>{c.folder_id=select.value===""?null:Number(select.value);persist();render();});
      field.append(label,select);body.append(field);
      if(!dialogs.folders.length)body.append(node("p","hint",tr("This account has no Telegram folders. Create one in Telegram, then press Refresh list.")));
    }
    if(c.mode!=="selected"&&!main){
      const types=node("details","wizard-types");types.append(node("summary","",tr("Kinds of chats")));
      for(const type of STEP_TYPES){
        const l=node("label","check-label"),input=node("input");input.type="checkbox";input.checked=c.types[type];
        input.addEventListener("change",()=>{c.types={...c.types,[type]:input.checked};persist();render();page.querySelector(".wizard-types").open=true;});
        l.append(input,node("span","",typeNames[type]));types.append(l);
      }
      body.append(types);
      const warn=notice("warning",tr("Folder and whole-account modes record private chats and messages of third parties. Use them only on a dedicated account, for a lawful purpose, and keep the data protected."));
      const l=node("label","check-label"),input=node("input");input.type="checkbox";input.id="wizard-acknowledge";input.checked=!!c.acknowledged;
      input.addEventListener("change",()=>{c.acknowledged=input.checked;persist();renderSteps();});
      l.append(input,node("span","",tr("I understand, and this is a separate account")));warn.append(l);body.append(warn);
    }
    const total=willRecord(),counter=node("p","wizard-counter");counter.setAttribute("role","status");
    counter.textContent=total===null?"":c.mode==="account"?trn("Will be recorded: {n} chat, and new ones as they appear","Will be recorded: {n} chats, and new ones as they appear",total):
      trn("Will be recorded: {n} chat","Will be recorded: {n} chats",total);
    const refresh=button("quiet small",tr("Refresh list"));refresh.addEventListener("click",()=>work(refresh,()=>loadDialogs(true)));
    const foot=node("div","wizard-chat-foot");foot.append(counter,refresh);body.append(foot);
    if(dialogs?.may_be_truncated)body.append(node("p","hint",tr("The list shows the first {n} chats of the account. Others are added when they become active.",{n:dialogs.limit})));
  }
  function chatPicker(){
    const c=answers.chats,box=node("div","wizard-picker");
    if(!dialogs)return box;
    const tools=node("div","wizard-picker-tools"),find=node("input");
    find.type="search";find.placeholder=tr("Search chats");find.setAttribute("aria-label",tr("Search chats"));find.value=search;
    const chips=node("div","wizard-filter");chips.setAttribute("role","group");chips.setAttribute("aria-label",tr("Kinds of chats"));
    for(const [value,label] of [["",tr("All")],...STEP_TYPES.map(t=>[t,typeNames[t]])]){
      const b=button("filter"+(typeFilter===value?" active":""),label);b.setAttribute("aria-pressed",String(typeFilter===value));
      b.addEventListener("click",()=>{typeFilter=value;render();});chips.append(b);
    }
    tools.append(find,chips);box.append(tools);
    const rows=node("ul","wizard-chat-list");rows.setAttribute("aria-label",tr("The account's chats"));
    const chosen=new Set(c.chat_ids);
    const fillRows=()=>{
      const q=search.trim().toLocaleLowerCase();
      const found=dialogs.dialogs.filter(d=>(!typeFilter||KIND_TYPE[d.kind]===typeFilter)&&(!q||(d.title||"").toLocaleLowerCase().includes(q)));
      rows.replaceChildren(...found.slice(0,LIST_LIMIT).map(d=>{
        const li=node("li"),l=node("label","wizard-chat"),input=node("input");
        input.type="checkbox";input.checked=chosen.has(d.chat_id);input.value=String(d.chat_id);
        input.addEventListener("change",()=>{
          if(input.checked)chosen.add(d.chat_id);else chosen.delete(d.chat_id);
          c.chat_ids=[...chosen];persist();renderSteps();
          const total=page.querySelector(".wizard-counter");if(total)total.textContent=trn("Will be recorded: {n} chat","Will be recorded: {n} chats",chosen.size);
        });
        const text=node("span","wizard-chat-text");
        text.append(node("strong","",d.title||tr("Chat {id}",{id:d.chat_id})),
          node("small","",typeNames[KIND_TYPE[d.kind]]+(d.archived?" · "+tr("archived"):"")));
        l.append(input,avatarNode(d.chat_id,d.title||"?"),text);li.append(l);return li;
      }));
      if(found.length>LIST_LIMIT)rows.append(node("li","hint",tr("Showing {shown} of {total}. Narrow the search to see the rest.",{shown:LIST_LIMIT,total:found.length})));
      if(!found.length)rows.append(node("li","hint",tr("No chats match.")));
    };
    find.addEventListener("input",()=>{search=find.value;fillRows();});
    fillRows();box.append(rows);return box;
  }

  // ---------- 5. saving ----------
  function renderSaving(body){
    if(!answers.saving)answers.saving={...(data.presets?.[kind()]?.saving||{})};
    const a=answers.saving;
    body.append(node("p","hint",tr("Suggested for: {goal}. Change anything you like.",{goal:answers.goal==="watch"?purposeNames[kind()]:goalNames[answers.goal]})));
    body.append(node("h2","wizard-sub",tr("Events")));
    const events=node("div","wizard-checks");
    for(const name of EVENTS){
      const l=node("label","check-label"),input=node("input");input.type="checkbox";input.checked=!!a[name];
      input.addEventListener("change",()=>{a[name]=input.checked;persist();});
      l.append(input,node("span","",eventNames[name]));events.append(l);
    }
    body.append(events);
    body.append(node("h2","wizard-sub",tr("Photos and files")));
    const media=group(tr("Photos and files"));
    const pickMedia=value=>{a.media=value;persist();render();};
    option(media,"wizard-media","none",{title:mediaNames.none,checked:a.media==="none",onPick:pickMedia,when:tr("A note says a file was sent, without the file.")});
    option(media,"wizard-media","small",{title:mediaNames.small,checked:a.media==="small",onPick:pickMedia,when:tr("Photos, voice and short videos.")});
    option(media,"wizard-media","standard",{title:mediaNames.standard,checked:a.media==="standard",onPick:pickMedia,when:tr("Photos up to 20 MB, videos up to 100 MB.")});
    option(media,"wizard-media","all",{title:mediaNames.all,checked:a.media==="all",onPick:pickMedia,when:tr("Videos and documents up to 1 GB each. Needs a lot of disk space.")});
    body.append(media);
    const free=status().collector.disk_free_bytes;
    if(free!=null)body.append(node("p","hint",tr("Free on this disk: {size}. Downloads pause before the disk fills up.",{size:humanSize(free)})));
    body.append(node("h2","wizard-sub",tr("Earlier messages")));
    const history=group(tr("Earlier messages"));
    const pickHistory=value=>{a.history=value;persist();};
    option(history,"wizard-history","none",{title:historyNames.none,checked:a.history==="none",onPick:pickHistory,when:tr("Recording starts now.")});
    option(history,"wizard-history","recent",{title:historyNames.recent,checked:a.history==="recent",onPick:pickHistory,when:tr("Quick: a short context for each chat.")});
    option(history,"wizard-history","all",{title:historyNames.all,checked:a.history==="all",onPick:pickHistory,when:tr("Can take hours for large chats. You can pause it.")});
    body.append(history,node("p","hint",tr("Messages deleted before recording started cannot be recovered.")));
    body.append(node("h2","wizard-sub",tr("Proof")));
    const l=node("label","check-label wizard-proof"),input=node("input");input.type="checkbox";input.checked=!!a.timestamps;
    input.addEventListener("change",()=>{a.timestamps=input.checked;persist();render();});
    const text=node("span");text.append(node("strong","",tr("Independent timestamps")),
      node("small","",tr("Timestamp services confirm when each checkpoint existed. Only a hash leaves this computer.")));
    l.append(input,text);body.append(l);
    if(a.timestamps&&data.policy?.outside_route==="none")body.append(notice("warning",tr("Timestamps cannot be sent with the current connection: requests outside Telegram are blocked. Set a proxy for them on the Connection step.")));
  }

  // ---------- 6. place ----------
  function renderPlace(body){
    if(!answers.place)answers.place=status().assurance?"server":null;
    const places=group(titles.place);
    const pick=value=>{answers.place=value;persist();render();};
    option(places,"wizard-place","computer",{title:tr("This computer"),checked:answers.place==="computer",recommended:true,onPick:pick,
      when:tr("Records while the computer is on and online. Gaps are marked in the journal.")});
    option(places,"wizard-place","server",{title:tr("A server that is always on (24/7)"),checked:answers.place==="server",onPick:pick,
      when:tr("Your own server, or one created under Extras → Server 24/7.")});
    body.append(places);
    if(answers.place==="server"){
      body.append(notice("info",tr("Reliability points are counted only after the server is checked. Until then the scale shows the server as not checked.")));
      const open=button("secondary small",tr("Open Server 24/7"));open.addEventListener("click",()=>openExtra("cloud"));
      body.append(open);
    }
  }

  // ---------- 7. summary ----------
  async function loadPreview(force=false){
    const key=JSON.stringify(cleanAnswers());
    if(!force&&preview&&previewKey===key)return;
    previewKey=key;preview=null;
    try{preview=await json("setup/wizard/preview",cleanAnswers());}
    catch(error){if(error?.name!=="StaleView")preview={ready:false,step:"summary",message:error.message};}
    if(step==="summary"&&previewKey===key)render();
  }
  function row(box,name,label,value,extra=""){
    const item=node("div","wizard-row"),text=node("div");
    text.append(node("span","wizard-row-label",label),node("strong","",value));
    if(extra)text.append(node("small","",extra));
    const change=button("text-link",tr("Change"));change.setAttribute("aria-label",tr("Change: {item}",{item:label}));
    change.addEventListener("click",()=>go(name));
    item.append(text,change);box.append(item);
  }
  function renderSummary(body){
    if(live){renderLive(body);return;}
    const s=status(),account=s.collector.account,copy=answers.goal==="copy";
    const rows=node("div","wizard-summary");
    row(rows,"goal",shortNames.goal,goalNames[answers.goal]||"—",answers.goal==="watch"?purposeNames[kind()]:"");
    const check=data.checks?.connection;
    row(rows,"connection",shortNames.connection,routeName(data.route),
      connectionOk()?tr("Checked: {ms} ms",{ms:check.elapsed_ms??"?"}):tr("Not checked"));
    row(rows,"account",shortNames.account,account?(account.username?"@"+account.username:"ID "+account.id):tr("Not signed in"),
      copy?"":answers.account_kind==="main"?tr("Main account"):tr("A separate account"));
    if(!copy){
      const c=answers.chats||{},n=willRecord();
      row(rows,"chats",shortNames.chats,modeNames[c.mode]||"—",n===null?"":trn("{n} chat","{n} chats",n));
      const a=answers.saving||{};
      row(rows,"saving",shortNames.saving,EVENTS.filter(e=>a[e]).map(e=>eventNames[e]).join(", ")||"—",
        [mediaNames[a.media],historyNames[a.history],a.timestamps?tr("Independent timestamps"):""].filter(Boolean).join(" · "));
      row(rows,"place",shortNames.place,answers.place==="server"?tr("A server that is always on (24/7)"):tr("This computer"));
    }
    body.append(rows);
    if(copy){
      body.append(node("p","hint",tr("Next, choose the chats, dates and files to include, then download a signed archive.")));
      const exportButton=button("primary wizard-start",tr("Open account export"));
      exportButton.disabled=!signedIn();
      exportButton.addEventListener("click",()=>work(exportButton,async()=>{
        data=await json("setup/wizard/skip",{reason:"copy"});await refreshStatus();await openAccountExport();
      }));
      body.append(exportButton);return;
    }
    if(data.drift?.length&&data.finished_at){
      const names={scope:tr("chats to record"),monitoring:tr("events"),media:tr("files"),timestamps:tr("timestamps")};
      body.append(notice("warning",tr("Changed by hand after setup: {parts}. Starting again here sets them back as shown above.",{parts:data.drift.map(k=>names[k]).join(", ")})));
    }
    loadPreview();
    if(!preview){body.append(node("p","wizard-progress",tr("Preparing the summary…")));return;}
    if(!preview.ready){
      const box=notice("error",tr(preview.message));
      if(steps().includes(preview.step)&&preview.step!=="summary"){const fix=button("secondary small",tr("Fix it"));fix.addEventListener("click",()=>go(preview.step));box.append(fix);}
      body.append(box);return;
    }
    const changes=changeList();
    if(changes.length){
      body.append(node("h2","wizard-sub",tr("What will change")));
      const ul=node("ul","wizard-changes");for(const text of changes)ul.append(node("li","",text));body.append(ul);
    }
    body.append(node("h2","wizard-sub",tr("Protection: now → after")));
    const scales=node("div","level-scales wizard-scales");
    renderScales(scales,{assessment:preview.scales.now,levels:data.setup.levels},{tr,node,after:preview.scales.after});
    body.append(scales);
    const later=data.setup.recommended[preview.goal]?.steps||[];
    if(later.length){
      body.append(node("h2","wizard-sub",tr("Later, with your own accounts")));
      const extras={alerts:["alerts",tr("Problem notifications")],replica:["evidence",tr("Off-site copy")],server:["cloud",tr("Server 24/7")],
        gateway:["cloud",tr("Cloudflare Gateway DNS")],code:["github",tr("Code check")],witness:["bot",tr("Witness bot")]};
      const ul=node("ul","wizard-next");
      for(const name of later){const li=node("li"),b=button("text-link",extras[name][1]+" →");b.addEventListener("click",()=>openExtra(extras[name][0]));li.append(b);ul.append(li);}
      body.append(ul);
    }
    const running=s.collector.running;
    const start=button("primary wizard-start",running?tr("Apply settings"):tr("Start recording"));
    start.disabled=!may("collect")&&!running||!signedIn();
    start.addEventListener("click",()=>work(start,begin));
    body.append(start);
    if(!signedIn())body.append(node("p","hint",tr("Sign in to Telegram on the Account step first.")));
  }
  function changeList(){
    const p=preview,out=[];
    if(p.now.scope.mode!==p.after.scope.mode)out.push(tr("Chats to record: {before} → {after}",{before:modeNames[p.now.scope.mode],after:modeNames[p.after.scope.mode]}));
    else if(JSON.stringify(p.now.scope)!==JSON.stringify(p.after.scope))out.push(tr("The folder, the kinds of chats or what is saved from a new chat change"));
    if(p.enable)out.push(trn("{n} chat starts recording","{n} chats start recording",p.enable));
    if(p.pause)out.push(trn("{n} chat is paused","{n} chats are paused",p.pause));
    for(const e of EVENTS)if(p.now.monitoring[e]!==p.after.monitoring[e])out.push(eventNames[e]+": "+tr(p.after.monitoring[e]?"on":"off"));
    if(p.now.media!==p.after.media)out.push(tr("Files: {before} → {after}",{before:mediaNames[p.now.media],after:mediaNames[p.after.media]}));
    if(p.now.timestamps!==p.after.timestamps)out.push(tr("Independent timestamps")+": "+tr(p.after.timestamps?"on":"off"));
    if(p.parameters.dialog_limit)out.push(tr("Chats read from the account's list: {before} → {after}",{before:p.parameters.dialog_limit.now.toLocaleString(),after:p.parameters.dialog_limit.after.toLocaleString()}));
    return out;
  }

  // ---------- applying, then the live check ----------
  async function begin(){
    await loadPreview(true);
    if(!preview?.ready){render();return;}
    const result=await json("setup/wizard/apply",cleanAnswers());
    data=result;preview=null;
    await refreshStatus();
    live={started:Date.now(),history:answers.saving?.history||"none",snapshots:{done:0,total:0,failed:0},error:"",done:false};
    if(!status().collector.running){
      try{await json("collector/start",{});}
      catch(error){live.error=error.message;}
      await refreshStatus();
    }
    render();
    watch();
    if(!live.error)loadHistory();
  }
  async function loadHistory(){
    const mine=live;
    if(mine.history==="all"){
      try{await json("history/start",{});}catch(error){mine.historyError=error.message;}
      return;
    }
    if(mine.history!=="recent")return;
    const targets=status().targets.filter(t=>t.enabled).map(t=>t.chat_id);
    mine.snapshots.total=targets.length;render();
    for(const chat_id of targets){
      if(live!==mine||step!=="summary")return;
      try{await json("snapshot",{chat_id,limit:data.recent_messages||100});}catch{mine.snapshots.failed++;}
      mine.snapshots.done++;if(step==="summary"&&live===mine)render();
    }
  }
  let watching=null;
  function watch(){
    clearTimeout(watching);
    const tick=async()=>{
      if(!live||step!=="summary")return;
      try{await refreshStatus();}catch{}
      const ok=checks().every(c=>c.state==="working"||c.state==="off");
      if(ok&&Date.now()-live.started>4000)live.done=true;
      render();
      if(!live.done&&Date.now()-live.started<120000)watching=setTimeout(tick,2000);
      else live.done=true;
    };
    watching=setTimeout(tick,1500);
  }
  function checks(){
    const h=status().health||{};
    return ["connection","intake","sources","media"].map(name=>({name,...(h[name]||{state:"unknown"})}));
  }
  function renderLive(body){
    const box=node("div","wizard-live");box.setAttribute("aria-live","polite");
    body.append(node("p","",live.done?tr("Setup is applied."):tr("Checking that recording works…")));
    if(live.error)body.append(notice("error",tr("Observation did not start: {error}",{error:live.error})));
    for(const part of checks()){
      const item=node("div","wizard-check");
      item.append(stateBadge(part.state),node("strong","",healthNames[part.name]),node("span","",healthLines(part.name,part)[0]||""));
      box.append(item);
    }
    if(live.history==="recent"&&live.snapshots.total){
      const item=node("div","wizard-check");
      item.append(stateBadge(live.snapshots.done<live.snapshots.total?"running":"working"),node("strong","",tr("Earlier messages")),
        node("span","",tr("{done} of {total} chats",{done:live.snapshots.done,total:live.snapshots.total})+(live.snapshots.failed?" · "+tr("not loaded: {n}",{n:live.snapshots.failed}):"")));
      box.append(item);
    }
    if(live.history==="all")box.append(node("p","hint",live.historyError?tr("History did not start: {error}",{error:live.historyError}):tr("All available history is loading in the background; progress is under Sources.")));
    body.append(box);
    if(live.done){
      body.append(node("h2","wizard-sub",tr("Done! What next:")));
      const actions=node("div","wizard-actions");
      for(const [view,label] of [["chats",tr("Open chats")],["observations",tr("Open the journal")],["evidence",tr("How to export")]]){
        const b=button(view==="chats"?"primary":"secondary",label);b.addEventListener("click",()=>leaveTo(view));actions.append(b);
      }
      body.append(actions);
    }
  }

  // ---------- view lifecycle ----------
  async function load(wanted=null,preset=null){
    const fresh=session!==getState().workspaceRevision+":"+getState().profile;
    if(fresh){session=getState().workspaceRevision+":"+getState().profile;data=null;answers={};dialogs=null;preview=null;live=null;routeDraft=null;skipConnection=false;}
    let result;
    try{result=await json("setup/wizard");}
    catch(error){
      if(error?.name==="StaleView")throw error;
      // Without the saved progress there is nothing safe to show: say why and offer to try again.
      const h=node("h1","",tr("The setup could not be opened"));h.tabIndex=-1;
      const again=button("secondary",tr("Try again"));again.addEventListener("click",()=>work(again,()=>load(wanted)));
      page.replaceChildren(h,notice("error",error.message),again);
      return;
    }
    data=result;
    if(fresh||!Object.keys(answers).length)answers=structuredClone(result.answers||{});
    // Opened for a goal (Sources → Investigation mode): that goal is chosen, the rest follows from it.
    const changed=preset&&(answers.goal!==preset.goal||answers.purpose!==preset.purpose);
    if(changed){Object.assign(answers,preset);answers.saving=null;answers.chats=null;}
    const target=wanted||(fresh?result.step:step)||"goal";
    step=steps().includes(target)?target:"goal";
    go(step,{history:false,focus:!!wanted});
    if(changed)persist();
    record({replace:true});
  }
  return {
    load,
    open(name){if(data)go(name||step,{history:false});},
    get step(){return step;},
    // A status refresh redraws a page only where its facts changed; typing and focus elsewhere stay as they are.
    updateStatus(){
      if(!data)return;
      if(step==="account"&&signedIn()!==shownSignedIn)render();
      else renderSteps();
    },
    leave(){restoreAuth();clearTimeout(watching);},
    resetSession(){restoreAuth();clearTimeout(watching);session=null;data=null;answers={};dialogs=null;live=null;preview=null;},
  };
}
