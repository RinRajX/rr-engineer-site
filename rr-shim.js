/* RR Engineer website copy: replaces Claude-only connections with your Google Apps Script.
   No secrets in this file. The access key is typed once and kept only in this browser. */
(function(){
  var API="https://script.google.com/macros/s/AKfycbzorbsyndGaDEAYtu8t5JG0wKTv-xn1fJS3OkiiLlO95xug447KR-cL5H-L7MilQDBq/exec";
  var K="rrSiteKey",ready=null;
  function getKey(){try{return localStorage.getItem(K)||""}catch(e){return""}}
  function setKey(v){try{v?localStorage.setItem(K,v):localStorage.removeItem(K)}catch(e){}}

  async function call(op,args,key){
    var r,j;
    try{r=await fetch(API,{method:"POST",headers:{"Content-Type":"text/plain;charset=utf-8"},body:JSON.stringify({key:key||getKey(),op:op,args:args||{}})})}
    catch(e){throw{code:"server_unavailable",message:"Google couldn't be reached."}}
    if(!r.ok)throw{code:"server_unavailable",message:"Google answered "+r.status};
    try{j=await r.json()}catch(e){throw{code:"upstream_error",message:"Unreadable answer from Google."}}
    if(j&&j.error==="denied"){throw{code:"denied",message:"Access key rejected."}}
    if(j&&j.error)throw{code:"tool_error",message:/bad op/.test(j.error)&&/^drive_/.test(op)?"Files need the updated Google script (see setup note).":String(j.error)};
    return (j&&j.result)||{};
  }

  var UE={valueInputOption:"USER_ENTERED"};
  async function sheets(name,a){
    a=a||{};
    switch(name){
      case "get_values":return call("get",{range:a.range,opts:{}});
      case "update_values":return call("update",{range:a.range,body:{values:a.values},opts:UE});
      case "append_values":return call("append",{range:a.range,body:{values:a.values},opts:UE});
      case "update_spreadsheet":return call("batch",{body:{requests:a.requests}});
      case "get_spreadsheet":return call("meta",{opts:a.fields?{fields:[].concat(a.fields).join(",")}:{}});
    }
    throw{code:"tool_error",message:"Not available on the website: "+name};
  }

  var mcp={callTool:async function(server,name,input){
    if(server==="Google Sheets"){
      try{return{payload:await sheets(name,input)}}
      catch(e){if(e&&e.code==="denied"){setKey("");e={code:"tool_error",message:"Your access key was rejected. Reload the page and enter it again."}}throw e}
    }
    if(server==="Miro")throw{code:"tool_error",message:"Miro is updated from the Claude dashboard. Your map is saved to the Sheet and shows in both copies."};
    if(server==="Google Drive"){
      if(name==="create_file")return{payload:await call("drive_create",{name:input.title,mime:input.contentMimeType,b64:input.base64Content})};
      if(name==="download_file_content")return{payload:await call("drive_get",{id:input.fileId})};
    }
    throw{code:"tool_error",message:server+" works only in the Claude dashboard."};
  }};

  var downloads={save:async function(o){
    var b=o.data instanceof Blob?o.data:new Blob([String(o.data==null?"":o.data)],{type:"text/plain"});
    var u=URL.createObjectURL(b),a=document.createElement("a");
    a.href=u;a.download=o.filename||"download";document.body.appendChild(a);a.click();a.remove();
    setTimeout(function(){URL.revokeObjectURL(u)},4000);
  }};

  function bodyReady(){return document.body?Promise.resolve():new Promise(function(r){document.addEventListener("DOMContentLoaded",r)})}

  function askKey(){
    return bodyReady().then(function(){return new Promise(function(done){
      var w=document.createElement("div");
      w.id="rrKeyBox";
      w.innerHTML='<style>#rrKeyBox{position:fixed;inset:0;z-index:99999;background:rgba(20,26,33,.55);display:flex;align-items:center;justify-content:center;font:14px system-ui,sans-serif}'+
        '#rrKeyBox .c{background:#fff;color:#111;border:1px solid #111;border-radius:10px;padding:22px;width:min(360px,92vw);box-shadow:0 10px 30px rgba(0,0,0,.25)}'+
        '#rrKeyBox h2{margin:0 0 4px;font-size:19px}#rrKeyBox h2 b{color:#e8590c}#rrKeyBox p{margin:0 0 12px;color:#333}'+
        '#rrKeyBox input{width:100%;box-sizing:border-box;padding:9px 10px;background:#fff;color:#000;border:1px solid #000;border-radius:6px;font-size:14px}'+
        '#rrKeyBox button{margin-top:12px;width:100%;padding:9px;border:1px solid #000;border-radius:6px;background:#e8590c;color:#fff;font-weight:600;cursor:pointer}'+
        '#rrKeyBox button:hover{transform:translateY(-1px);box-shadow:0 4px 10px rgba(0,0,0,.2)}#rrKeyBox .m{min-height:18px;margin-top:8px;color:#c0262d;font-size:13px}</style>'+
        '<form class="c"><h2>RR <b>Engineer</b></h2><p>Enter your access key (only needed once in this browser).</p>'+
        '<input type="password" autocomplete="off" placeholder="Access key"><button type="submit">Open</button><div class="m"></div></form>';
      document.body.appendChild(w);
      var f=w.querySelector("form"),i=w.querySelector("input"),m=w.querySelector(".m"),btn=w.querySelector("button");
      i.focus();
      f.onsubmit=function(ev){
        ev.preventDefault();var k=i.value.trim();if(!k)return;
        btn.disabled=true;m.style.color="#333";m.textContent="Checking…";
        call("meta",{opts:{fields:"spreadsheetId"}},k).then(function(){setKey(k);w.remove();done()},function(e){
          btn.disabled=false;m.style.color="#c0262d";m.textContent=e&&e.code==="denied"?"Wrong key. Try again.":(e&&e.message)||"Could not check the key.";
        });
      };
    })});
  }

  function ensureKey(){if(!ready)ready=getKey()?Promise.resolve():askKey();return ready}

  window.claude={use:async function(name){
    if(name==="mcp"){await ensureKey();return mcp}
    if(name==="downloads")return downloads;
    return null; /* db (Discuss tray) stays in this browser on the website */
  }};
})();
