#!/usr/bin/env python3
"""Round-4 novelty referee: run a batch of arXiv API queries.

Usage: python3 -I arxiv_batch.py QUERYFILE [max_results] [pause_seconds]
QUERYFILE has one arXiv API query per line (lines starting with # are skipped),
e.g.  all:"distinct factorials"
For each query it prints the UTC time, the total hit count and the newest
matches (submission date, arXiv id, title), newest first.
Waits pause_seconds (default 3.5) between requests, and backs off on HTTP 429. Network access goes through
the session proxy; the script has no other side effects.
"""
import datetime
import re
import sys
import time
import urllib.parse
import urllib.request


def run(query, n):
    url = ("https://export.arxiv.org/api/query?search_query="
           + urllib.parse.quote(query)
           + "&sortBy=submittedDate&sortOrder=descending&max_results=%d" % n)
    t = None
    for _ in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                t = r.read().decode("utf-8", "replace")
            break
        except Exception as e:  # rate limit or transient error
            print("  (retry after error: %s)" % e)
            time.sleep(30)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
    if t is None:
        print("== [%s UTC] %s   FAILED" % (now, query))
        return
    tot = re.search(r"<opensearch:totalResults[^>]*>(\d+)<", t)
    print("== [%s UTC] %s   [total %s]" % (now, query, tot.group(1) if tot else "?"))
    for e in re.findall(r"<entry>(.*?)</entry>", t, re.S):
        m = re.search(r"<title>(.*?)</title>", e, re.S)
        if not m:
            continue
        ti = re.sub(r"\s+", " ", m.group(1))
        pub = re.search(r"<published>(.*?)</published>", e).group(1)
        i = re.search(r"<id>(.*?)</id>", e).group(1).split("/abs/")[-1]
        print("   %s  %-18s %s" % (pub[:10], i, ti[:130]))


def main():
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    pause = float(sys.argv[3]) if len(sys.argv) > 3 else 3.5
    with open(sys.argv[1], encoding="utf-8") as f:
        qs = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    for q in qs:
        run(q, n)
        sys.stdout.flush()
        time.sleep(pause)


if __name__ == "__main__":
    main()
