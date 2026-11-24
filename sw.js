/* RR Engineer app: always loads the newest version from the web; the saved copy is used only when offline.
   Data (Google Sheet via Apps Script) is never cached, so sync works exactly as before. */
var C="rr-app";
var SHELL=["./","index.html","aa.html","ak.html","app.html","akapp.html","masterbook.html","rr-shim.js",
 "manifest.webmanifest","aa.webmanifest","icons/rr-192.png","icons/rr-512.png","icons/aa-192.png","icons/aa-512.png"];
self.addEventListener("install",function(e){
  self.skipWaiting();
  e.waitUntil(caches.open(C).then(function(c){return Promise.all(SHELL.map(function(u){
    return fetch(u,{cache:"no-cache"}).then(function(r){if(r.ok)return c.put(u,r)}).catch(function(){})}))}));
});
self.addEventListener("activate",function(e){e.waitUntil(self.clients.claim())});
self.addEventListener("fetch",function(e){
  var q=e.request;
  if(q.method!=="GET"||new URL(q.url).origin!==location.origin)return; /* Google script, fonts, etc. go straight to the network */
  e.respondWith(fetch(q,{cache:"no-cache"}).then(function(r){
    if(r&&r.ok){var k=r.clone();caches.open(C).then(function(c){c.put(q,k)})}
    return r;
  }).catch(function(){
    return caches.match(q,{ignoreSearch:true}).then(function(m){return m||caches.match("index.html")});
  }));
});
