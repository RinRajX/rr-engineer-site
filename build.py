"""Make the website copy from the Claude dashboard's index.html.
Usage: python3 build.py <dashboard index.html> [masterbook.html]
app.html  = the dashboard unchanged, plus the shim script (connects to the Google script) and a no-index tag.
index.html = a dark page that shows app.html in a centered frame, like Claude's side panel."""
import sys, shutil, pathlib

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
assert '<head>\n' in src, "no <head> found"
app = src.replace('<head>\n', '<head>\n<meta name="robots" content="noindex,nofollow">\n'
                  '<script src="rr-shim.js"></script>\n', 1)
here = pathlib.Path(__file__).parent
(here / "app.html").write_text(app, encoding="utf-8")
shell = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>RR Engineer</title>
<style>
html,body{margin:0;height:100%;background:#3a3d42;overflow:hidden}
#rrApp{display:block;height:100%;width:50vw;min-width:min(720px,100vw);margin:0 auto;border:0;background:#eef2f5;
box-shadow:-22px 0 40px -2px rgba(0,0,0,.9),22px 0 40px -2px rgba(0,0,0,.9),0 0 0 1px rgba(255,255,255,.12)}
</style></head>
<body><iframe id="rrApp" src="app.html" title="RR Engineer" allow="clipboard-read; clipboard-write; fullscreen"></iframe></body></html>
"""
(here / "index.html").write_text(shell, encoding="utf-8")
# AK = the Prompt Library tab shown alone (same page, other tabs and the top bar hidden)
AKCSS = ('<style id="akOnly">#top,#pDump,#pRR,#tabLock,#tlMenu{display:none!important}'
         '#libPanel.lk,.panel.lk{filter:none!important}</style>\n')
def akify(x, title="AK Prompt Library"):
    x = x.replace('<head>\n', '<head>\n' + AKCSS, 1)
    x = x.replace('<title>RR Engineer</title>', '<title>' + title + '</title>', 1)
    i = x.rfind('</body>')
    return x[:i] + '<script>try{setTab("lib")}catch(e){}</script>\n' + x[i:]
(here / "akapp.html").write_text(akify(app), encoding="utf-8")
(here / "ak.html").write_text(shell.replace('src="app.html"', 'src="akapp.html"').replace('<title>RR Engineer</title>', '<title>AK Prompt Library</title>'), encoding="utf-8")
if len(sys.argv) > 3:
    pathlib.Path(sys.argv[3]).write_text(akify(src), encoding="utf-8")
if len(sys.argv) > 2:
    shutil.copyfile(sys.argv[2], here / "masterbook.html")
print("built app.html", len(app), "bytes + index.html shell")
