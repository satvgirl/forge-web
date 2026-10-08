"""Waitlist signups: who is new since the last run, and counts per ?src= label.

Run:  python3 campaign/signups.py          new signups since the last run
      python3 campaign/signups.py --all    everyone on the list
Uses your wrangler login to read the WAITLIST KV namespace (same data as
GET /api/waitlist/export). Remembers which addresses it has already reported in
.signups-state.json (holds email addresses) and appends a counts-only line per
run to signups.log. Both files are gitignored.

Output (stable, for scripts): `NEW <n>` or `NO CHANGE`, `TOTAL <n>`, one
`SOURCE <label> <count>` per source, then one `SIGNUP <email> <joined> <source>`
per new signup (every signup with --all). Email addresses appear only on
SIGNUP lines.
"""
import collections
import datetime
import json
import os
import subprocess
import sys
import time

NS = "623c0ebdf23542fc90c35286f7396197"  # WAITLIST, see wrangler.toml
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
STATE = os.path.join(HERE, ".signups-state.json")
LOG = os.path.join(HERE, "signups.log")


def wrangler(*args, attempts=3):
    for attempt in range(1, attempts + 1):
        try:
            result = subprocess.run(["npx", "wrangler", *args, "--namespace-id", NS, "--remote"],
                                    capture_output=True, text=True, cwd=REPO, timeout=90)
        except subprocess.TimeoutExpired:  # wrangler occasionally hangs on the network
            result = subprocess.CompletedProcess(args, 124, "", "timed out after 90 s")
        if result.returncode == 0:
            # wrangler prints a login banner before the JSON.
            out = result.stdout
            start = min(i for i in (out.find("["), out.find("{")) if i >= 0)
            return json.loads(out[start:])
        if attempt < attempts:
            time.sleep(3)
    sys.exit(f"wrangler {' '.join(args[:3])} failed after {attempts} tries "
             f"(login expired or offline?): {(result.stderr or result.stdout).strip()[-300:]}")


def main():
    show_all = "--all" in sys.argv[1:]
    keys = [k["name"] for k in wrangler("kv", "key", "list")]
    entries = []
    for key in keys:
        entry = wrangler("kv", "key", "get", key)
        entries.append((key, entry.get("joinedAt") or "", entry.get("source") or "(none)"))
    sources = collections.Counter(source for _, _, source in entries)

    try:
        seen = set(json.load(open(STATE))["seen"])
    except (OSError, ValueError, KeyError):
        seen = set()  # first run (or the old counts-only state): report everyone once
    new = sorted((e for e in entries if e[0] not in seen), key=lambda e: e[1])
    json.dump({"seen": sorted(seen | {k for k, _, _ in entries})}, open(STATE, "w"))

    print(f"NEW {len(new)}" if new else "NO CHANGE")
    print(f"TOTAL {len(entries)}")
    for label, count in sources.most_common():
        print(f"SOURCE {label} {count}")
    for email, joined, source in (sorted(entries, key=lambda e: e[1]) if show_all else new):
        print(f"SIGNUP {email} {joined} {source}")
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(LOG, "a") as log:
        log.write(f"{stamp} total={len(entries)} new={len(new)} " +
                  " ".join(f"{k}={v}" for k, v in sources.most_common()) + "\n")


if __name__ == "__main__":
    main()
