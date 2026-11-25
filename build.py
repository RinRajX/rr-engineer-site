"""Make the website copy from the Claude dashboard's index.html.
Usage: python3 build.py <dashboard index.html> [masterbook.html]
app.html  = the dashboard unchanged, plus the shim script (connects to the Google script) and a no-index tag.
index.html = a dark page that shows app.html in a centered frame, like Claude's side panel."""
import sys, shutil, pathlib

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
assert '<head>\n' in src, "no <head> found"
import hashlib, json
RRV = hashlib.sha1(src.encode()).hexdigest()[:12]  # app version: the shim reloads the phone app when version.json differs
app = src.replace('<head>\n', '<head>\n<meta name="robots" content="noindex,nofollow">\n'
                  '<script>window.RRV="' + RRV + '"</script>\n<script src="rr-shim.js"></script>\n', 1)
here = pathlib.Path(__file__).parent
(here / "app.html").write_text(app, encoding="utf-8")
(here / "version.json").write_text(json.dumps({"v": RRV}), encoding="utf-8")
shell = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>RR Engineer</title>
__PWA__
<style>
html,body{margin:0;height:100%;background:#3a3d42;overflow:hidden}
#rrApp{display:block;height:100%;width:50vw;min-width:min(720px,100vw);margin:0 auto;border:0;background:#eef2f5;
box-shadow:-22px 0 40px -2px rgba(0,0,0,.9),22px 0 40px -2px rgba(0,0,0,.9),0 0 0 1px rgba(255,255,255,.12)}
html.fullw #rrApp{width:100vw;min-width:0;box-shadow:none}
@media (max-width:820px),(hover:none) and (pointer:coarse){html,body{height:100dvh}#rrApp{width:100vw;min-width:0;height:100dvh;box-shadow:none}}
</style></head>
<script>try{if(localStorage.getItem("rrPageW")==="full")document.documentElement.classList.add("fullw")}catch(e){}addEventListener("message",function(e){var d=e.data;if(d&&d.rr==="pagew")document.documentElement.classList.toggle("fullw",d.v==="full")})</script>
<body><iframe id="rrApp" src="app.html" title="RR Engineer" allow="clipboard-read; clipboard-write; fullscreen"></iframe>
__SW__</body></html>
"""
AKREDIR = '<!DOCTYPE html><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><title>AA Prompt Library</title><script>location.replace("aa.html"+location.search+location.hash)</script><a href="aa.html">AA Prompt Library</a>\n'
# Installable phone app (Chrome menu > Install app): manifest + icons + service worker (sw.js)
PWA = ('<link rel="manifest" href="{m}">\n<meta name="theme-color" content="{c}">\n'
       '<meta name="mobile-web-app-capable" content="yes">\n<meta name="apple-mobile-web-app-capable" content="yes">\n'
       '<meta name="apple-mobile-web-app-title" content="{t}">\n<link rel="icon" href="icons/{i}-192.png">\n'
       '<link rel="apple-touch-icon" href="icons/{i}-apple.png">')
SW = ('<script>var BIP=null,F=document.getElementById("rrApp");function tell(){try{F.contentWindow.postMessage({rr:"inst",can:!!BIP},"*")}catch(e){}}'
      'addEventListener("beforeinstallprompt",function(e){e.preventDefault();BIP=e;tell()});addEventListener("appinstalled",function(){BIP=null;tell()});'
      'addEventListener("message",function(e){var d=e.data||{};if(d.rr==="hello")tell();if(d.rr==="reload")location.reload();'
      'if(d.rr==="install"&&BIP){BIP.prompt();BIP.userChoice.then(function(){BIP=null;tell()},function(){})}});</script>\n'
      '<script>if("serviceWorker" in navigator)navigator.serviceWorker.register("sw.js",{updateViaCache:"none"})'
      '.then(function(r){document.addEventListener("visibilitychange",function(){if(!document.hidden)r.update()})}).catch(function(){})</script>\n')
shell = shell.replace("__SW__", SW)
rrshell = shell.replace("__PWA__", PWA.format(m="rr-manifest.json", c="#e8590c", t="RR", i="rr"))
akshell = shell.replace("__PWA__", PWA.format(m="aa-manifest.json", c="#14171a", t="AA", i="aa"))

(here / "index.html").write_text(rrshell, encoding="utf-8")
# AA (formerly AK) = the Prompt Library tab shown alone (same page, other tabs and the top bar hidden)
AKCSS = ('<style id="akOnly">#top,#pDump,#pRR,#tabLock,#tlMenu{display:none!important}'
         '#libPanel.lk,.panel.lk{filter:none!important}html.mob body{padding-bottom:0!important}</style>\n')
def akify(x, title="AA Prompt Library"):
    x = x.replace('<head>\n', '<head>\n' + AKCSS, 1)
    x = x.replace('<title>RR Engineer</title>', '<title>' + title + '</title>', 1)
    i = x.rfind('</body>')
    return x[:i] + '<script>try{setTab("lib")}catch(e){}</script>\n' + x[i:]
(here / "akapp.html").write_text(akify(app), encoding="utf-8")
(here / "aa.html").write_text(akshell.replace('src="app.html"', 'src="akapp.html"').replace('<title>RR Engineer</title>', '<title>AA Prompt Library</title>'), encoding="utf-8")
# old AK link keeps working: sends visitors to aa.html
(here / "ak.html").write_text(AKREDIR, encoding="utf-8")
if len(sys.argv) > 3:
    pathlib.Path(sys.argv[3]).write_text(akify(src), encoding="utf-8")
if len(sys.argv) > 2:
    shutil.copyfile(sys.argv[2], here / "masterbook.html")
# NOTE: the PIN gate (script id=rrGate, PIN 3223) lives inside the dashboard source index.html, so rebuilds keep it.
print("built app.html", len(app), "bytes + index.html shell")
