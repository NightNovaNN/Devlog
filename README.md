# Devlog 

*A CLI-first dev journal for builders who actually ship.*

Devlog is a **local-first, single-file Python CLI** that lets you:

* write daily dev logs
* attach real code snippets
* search past pain
* keep everything offline & transparent

No accounts.
No cloud.
No frameworks.
Just files.

---

## Features

* **Daily dev logs** (date-based)
* **Quick entries** from terminal
* **Attach code snippets** to logs
* **Search logs + snippets**
* **Bidirectional index** (logs ↔ snippets)
* **Windows-safe** (editor + encoding handled)
* **Single file only** (`devlog.py`)

---

## Installation

Just Python. That’s it.

```bash
git clone https://github.com/NightNovaNN/Devlog
cd https://github.com/NightNovaNN/Devlog
```

(or just copy `devlog.py` anywhere)

---

## Usage

Run via Python:

```bash
python devlog.py <command>
```

### Create a new log

```bash
python devlog.py new 26-12-2025
```

### Add a log entry

```bash
python devlog.py log "New project Devlog"
```

### Add a snippet (linked to current log)

```bash
python devlog.py snippet add ssa.c --tag compiler,ssa
```

### Close a log

```bash
python devlog.py close 26-12-2025
```

### Open a log in editor

```bash
python devlog.py open 26-12-2025
```

### Search everything

```bash
python devlog.py search "undefined behavior"
```

---

## Where data is stored

Devlog is **global by default**.

On Windows:

```
C:\Users\<you>\.devlog\
```

Structure:

```
.devlog/
├─ logs/
│   └─ 26-12-2025.md
├─ snippets/
│   └─ ssa.c
├─ index.json
└─ state.json
```

* Logs are plain Markdown
* Snippets are copied files
* Index is readable JSON
* Everything is git-friendly

---

## Design Philosophy

* **CLI-first** → fast logging
* **Desktop-agnostic** → open in whatever editor you use
* **Local-only** → your notes stay yours
* **Auditable** → no hidden state
* **Hackable** → one file, readable code

This is closer to a **dev brain dump** than a note app.

---

## Windows Notes (Important)

* Windows editors may save files in `cp1252`
* Devlog auto-handles encoding when reading logs
* Files are normalized back to UTF-8 when written

No crashes. No corruption.

---

## Requirements

* Python 3.9+
* Works on:

  * Windows
  * Linux
  * macOS

---

## Planned (maybe)

* `devlog today`
* `devlog reopen`
* fuzzy search
* desktop viewer (Tauri)
* Windows `.exe` build

Keeping it small on purpose.

---

## Status

**v0.1 — usable, raw, honest**

Built for:

* compiler devs
* low-level programmers
* students learning hard stuff
* anyone who prefers terminals over dashboards

---

