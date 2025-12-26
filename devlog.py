#!/usr/bin/env python3
import argparse
import os
import shutil
import json
import subprocess
from pathlib import Path

# ---------------- paths ----------------

BASE = Path.home() / ".devlog"
LOGS = BASE / "logs"
SNIPS = BASE / "snippets"
INDEX = BASE / "index.json"
STATE = BASE / "state.json"

# ---------------- helpers ----------------

def init():
    LOGS.mkdir(parents=True, exist_ok=True)
    SNIPS.mkdir(parents=True, exist_ok=True)

    if not INDEX.exists():
        INDEX.write_text(json.dumps({"logs": {}, "snippets": {}}, indent=2))

    if not STATE.exists():
        STATE.write_text(json.dumps({"open": None}, indent=2))


def load(path):
    return json.loads(path.read_text())


def save(path, data):
    path.write_text(json.dumps(data, indent=2))


def editor_open(path):
    editor = os.environ.get("EDITOR")

    if editor:
        subprocess.call([editor, str(path)])
        return

    # Windows fallback
    if os.name == "nt":
        os.startfile(path)
    else:
        subprocess.call(["xdg-open", str(path)])


# ---------------- commands ----------------

def cmd_new(d):
    path = LOGS / f"{d}.md"
    if path.exists():
        print(" log already exists")
        return

    path.write_text(f"# Devlog — {d}\n\nStatus: OPEN\n\n")

    index = load(INDEX)
    index["logs"][d] = {
        "status": "OPEN",
        "snippets": []
    }
    save(INDEX, index)

    state = load(STATE)
    state["open"] = d
    save(STATE, state)

    print(f" New devlog created: {d}")


def cmd_log(text):
    state = load(STATE)
    if not state["open"]:
        print(" no open devlog")
        return

    d = state["open"]
    path = LOGS / f"{d}.md"

    with path.open("a", encoding="utf-8") as f:
        f.write(f"## {text}\n\n")

    print(" entry added")


def cmd_snippet_add(file, tags):
    state = load(STATE)
    if not state["open"]:
        print(" no open devlog")
        return

    src = Path(file)
    if not src.exists():
        print(" snippet file not found")
        return

    dst = SNIPS / src.name
    shutil.copy(src, dst)

    index = load(INDEX)

    # snippet side
    prev = index["snippets"].get(src.name, {})
    logs = set(prev.get("logs", []))
    logs.add(state["open"])

    index["snippets"][src.name] = {
        "tags": tags,
        "logs": list(logs)
    }

    # log side
    if src.name not in index["logs"][state["open"]]["snippets"]:
        index["logs"][state["open"]]["snippets"].append(src.name)

    save(INDEX, index)

    print(f" snippet added: {src.name}")


def cmd_close(d):
    path = LOGS / f"{d}.md"
    if not path.exists():
        print(" log not found")
        return

    try:
        txt = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        txt = path.read_text(encoding="cp1252", errors="replace")
    txt = txt.replace("Status: OPEN", "Status: CLOSED")
    path.write_text(txt, encoding="utf-8")

    index = load(INDEX)
    if d in index["logs"]:
        index["logs"][d]["status"] = "CLOSED"
        save(INDEX, index)

    state = load(STATE)
    state["open"] = None
    save(STATE, state)

    print(f" devlog closed: {d}")


def cmd_open(d):
    path = LOGS / f"{d}.md"
    if not path.exists():
        print(" log not found")
        return

    editor_open(path)


def cmd_search(query):
    q = query.lower()
    print(" searching...\n")

    for log in LOGS.glob("*.md"):
        try:
            if q in log.read_text(encoding="utf-8").lower():
                print(f"📘 log match: {log.stem}")
        except:
            pass

    for snip in SNIPS.glob("*"):
        try:
            if q in snip.read_text(errors="ignore").lower():
                print(f"📎 snippet match: {snip.name}")
        except:
            pass


# ---------------- main ----------------

def main():
    init()

    p = argparse.ArgumentParser("devlog")
    sub = p.add_subparsers(dest="cmd")

    new = sub.add_parser("new")
    new.add_argument("date")

    log = sub.add_parser("log")
    log.add_argument("text")

    sn = sub.add_parser("snippet")
    snsub = sn.add_subparsers(dest="scmd")
    add = snsub.add_parser("add")
    add.add_argument("file")
    add.add_argument("--tag", default="")

    close = sub.add_parser("close")
    close.add_argument("date")

    op = sub.add_parser("open")
    op.add_argument("date")

    se = sub.add_parser("search")
    se.add_argument("query")

    args = p.parse_args()

    if args.cmd == "new":
        cmd_new(args.date)
    elif args.cmd == "log":
        cmd_log(args.text)
    elif args.cmd == "snippet" and args.scmd == "add":
        tags = [t.strip() for t in args.tag.split(",") if t.strip()]
        cmd_snippet_add(args.file, tags)
    elif args.cmd == "close":
        cmd_close(args.date)
    elif args.cmd == "open":
        cmd_open(args.date)
    elif args.cmd == "search":
        cmd_search(args.query)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
