#!/usr/bin/env python3
"""list_runs.py -- reproduction table: every log in DATA_DIR with its command line and wall time (markdown)."""
import sys, glob, os, re
D = sys.argv[1]
tot = 0.0
print("| log | command | wall (s) |")
print("|---|---|---|")
for f in sorted(glob.glob(os.path.join(D, "*.log"))):
    cmd, wall = "", ""
    for line in open(f, errors="replace"):
        if line.startswith("# command:") and not cmd:
            cmd = line[len("# command:"):].strip().replace("/home/user/erdos-404-research/", "").replace("|", "\\|")
        m = re.search(r"wall_seconds=([0-9.]+)", line)
        if m:
            wall = m.group(1)
    if wall:
        tot += float(wall)
    print(f"| `{os.path.basename(f)}` | `{cmd}` | {float(wall):.1f} |" if wall else f"| `{os.path.basename(f)}` | `{cmd}` | n/a |")
print(f"\nTotal wall time of logged runs: {tot:.0f} s ({tot/3600:.2f} h), each on one core.")
