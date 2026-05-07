# HR Records Manager

A bilingual (EN/RO) single-file web application for tracking personnel file entry progress across a public institution. Built for a real deployment at a Romanian city hall, managing the digitization of ~874 employee records across 5 operators.

> **This repository contains a demo version with fictional data.**  
> No real individuals or institutions are represented.

---

## Live Demo

Open `hr_dosare_manager_DEMO.html` directly in any browser — no installation required.  
Or visit the [GitHub Pages demo →](https://sorinhus.github.io/MRU_Tracker/hr_file_manager_DEMO.html)

---

## Screenshots

| Dashboard | Record table |
|---|---|
| *Progress per operator, priority breakdown, top departments* | *Filterable table with inline actions* |

---

## Features

- **Bilingual UI** — switch between English and Romanian instantly, including all labels, filters, table headers, export columns and notifications
- **Priority system** — P1 (Management & Elected officials) tracked separately from P2 (Execution staff)
- **5-operator workflow** — records distributed across operators; each operator sees their own queue grouped by department
- **Real-time progress tracking** — mark records as completed with one click; progress bars update live on the dashboard
- **Reassign records** — move individual records or bulk selections between operators via modal
- **Filtering & search** — filter by type, status, operator, completion; full-text search across name, role, department and post ID
- **Sortable table** — click any column header to sort ascending/descending
- **Export to CSV** — exports current filtered view; column headers respect active language
- **Network sync** (production mode) — Python HTTP server syncs progress across all operators in real time via shared `progress.json`; changes are persisted automatically
- **Auto-discovery** — clients open the HTML file locally and the app finds the server on the LAN automatically
- **Auto-shortcut** — server generates `OPEN_APP.bat` on startup with the correct network IP for colleagues

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vanilla HTML + CSS + JavaScript (no frameworks, no dependencies) |
| Backend | Python 3 standard library (`http.server`) |
| Storage | JSON file (`progress.json`) |
| Distribution | Single `.html` file — works offline, no build step |

---

## Project Structure

```
hr-records-manager/
├── hr_file_manager_DEMO.html     # Full application — open directly in browser
├── server_demo.py                # Lightweight Python HTTP server for network sync
├── START_SERVER.bat              # Windows launcher for the server
└── README.md
```

---

## Running Locally

### Standalone (demo mode)
Just open `hr_dosare_manager_DEMO.html` in your browser. Progress is stored in memory for the session only.

### With network sync
Requires Python 3 (no additional packages).

```bash
# Start the server
python server_demo.py

# Or on Windows: double-click START_SERVER.bat
```

The browser opens automatically at `http://localhost:8080`.  
A file `OPEN_APP.bat` is created in the same folder — share it with colleagues so they can connect from their machines with one double-click.

---

## How It Works

### Data model
Each record contains: employee name, department, position number, role, classification grade, education level, seniority step, post ID, assignment status, operator assignment, and completion flag.

### Operator assignment logic
- **Execution staff (FP)** — distributed across 5 operators using greedy bin-packing by department, keeping whole departments together so each operator becomes familiar with their area
- **Contract staff** — consolidated under a single operator (Operator 2) due to simpler record structure
- **Management staff** — follows the FP operator of their department; management on contract follows Operator 2
- **Unattached directors / elected officials** — distributed evenly across operators

### Network sync
Progress is saved to `progress.json` on every action (mark complete, reassign). All connected clients poll for updates every 15 seconds and apply changes from other operators automatically. The sync status indicator in the top bar shows connection state in real time.

---

## Real-World Context

This tool was built to coordinate the entry of **874 personnel files** into an HR management system (MRU) at a Romanian public institution. Key constraints that shaped the design:

- **No internet access** — all resources inline, server runs on the local network
- **No software installation** — operators use standard browsers; only one machine needs Python
- **Mixed staff types** — Romanian public sector distinguishes between civil servants (*funcționari publici*) and contract staff (*personal contractual*), each with different record structures and priorities
- **Shared network folder** — all files live on a mapped network drive (`Z:\`); the server reads and writes from the same location

---

## License

MIT — free to use and adapt.
