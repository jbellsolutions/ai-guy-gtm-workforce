#!/usr/bin/env python3
"""Fetch an optional source at its locked revision; never install or activate it."""
import argparse,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('component',choices=['data-box','browser-box']);p.add_argument('--destination',type=Path,required=True);a=p.parse_args()
if a.destination.exists():raise SystemExit('Destination exists; preserve and inspect it instead of overwriting.')
entry=next(x for x in json.loads((R/'sources.lock.json').read_text()) if x['repo'].endswith('/'+a.component))
try:
    subprocess.run(['git','clone','--no-checkout',entry['repo'],str(a.destination)],check=True)
    subprocess.run(['git','checkout','--detach',entry['commit']],cwd=a.destination,check=True)
except subprocess.CalledProcessError:
    raise SystemExit('Could not fetch '+a.component+'. This is a private AI Guy repository; confirm `gh auth status` shows an account with access, or skip this optional component.')
print('Pinned source fetched. Read its SKILL/README, configure selected services and run a bounded smoke test before activation.')
