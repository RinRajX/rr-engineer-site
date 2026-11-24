# RR Engineer (website copy)

A copy of the RR Engineer dashboard that works outside Claude. The Claude dashboard stays the main version.
Both read and write the same Google Sheet (this site through the owner's Google Apps Script) and refresh
each other automatically. An access key is needed and is never stored in this repo.

- `index.html` – dark page that shows the dashboard in a centered frame (like Claude's side panel)
- `app.html` – the dashboard, rebuilt from the Claude version with `build.py`
- `rr-shim.js` – connects the page to the Apps Script instead of Claude connectors
- Miro sync runs from the Claude dashboard; mind maps themselves are shared through the Sheet.
- Installable phone app: open the site in Chrome, ⋮ menu → Install app (or Add to home screen).
  `manifest.webmanifest` (RR) and `aa.webmanifest` (AA Prompt Library), icons in `icons/`, `sw.js` always loads the newest version and keeps a copy for offline.
- `aa.html` – AA Prompt Library (formerly AK); `ak.html` redirects there.
