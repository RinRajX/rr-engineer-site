# RR Engineer (website copy)

A copy of the RR Engineer dashboard that works outside Claude.
The Claude dashboard stays the main version; this site reads and writes the same Google Sheet
through the owner's Google Apps Script. An access key is needed and is never stored in this repo.

- `index.html` – the dashboard, rebuilt from the Claude version with `build.py`
- `rr-shim.js` – connects the page to the Apps Script instead of Claude connectors
- Miro sync, Drive file uploads and the Discuss tray work only in the Claude dashboard.
