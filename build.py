"""Make the website copy from the Claude dashboard's index.html.
Usage: python3 build.py <dashboard index.html> [masterbook.html]
Only adds the shim script and a no-index tag; the dashboard code itself is unchanged."""
import sys, shutil, pathlib

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
tag = '<head>\n'
assert src.count(tag) >= 1, "no <head> found"
inject = ('<head>\n<meta name="robots" content="noindex,nofollow">\n'
          '<script src="rr-shim.js"></script>\n')
out = src.replace(tag, inject, 1)
here = pathlib.Path(__file__).parent
(here / "index.html").write_text(out, encoding="utf-8")
if len(sys.argv) > 2:
    shutil.copyfile(sys.argv[2], here / "masterbook.html")
print("built", len(out), "bytes")
