#!/usr/bin/env python3
"""Round-3 novelty referee: query the arXiv API and print the newest matches.

Usage: python3 -I arxiv_query.py 'QUERY' [max_results]
QUERY uses arXiv API syntax, e.g. 'all:"distinct factorials"'.
Prints submission date, arXiv id and title, newest first.
Network access via the session proxy; no other side effects.
"""
import re
import sys
import time
import urllib.parse
import urllib.request


def run(query, n=10):
    url = ("https://export.arxiv.org/api/query?search_query="
           + urllib.parse.quote(query)
           + "&sortBy=submittedDate&sortOrder=descending&max_results=%d" % n)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                t = r.read().decode("utf-8", "replace")
            break
        except Exception as e:  # rate limit or transient error
            print("  (retry after error: %s)" % e)
            time.sleep(5)
    else:
        print("  FAILED")
        return
    tot = re.search(r"<opensearch:totalResults>(\d+)<", t)
    print("== %s   [total %s]" % (query, tot.group(1) if tot else "?"))
    for e in re.findall(r"<entry>(.*?)</entry>", t, re.S):
        ti = re.sub(r"\s+", " ", re.search(r"<title>(.*?)</title>", e, re.S).group(1))
        pub = re.search(r"<published>(.*?)</published>", e).group(1)
        i = re.search(r"<id>(.*?)</id>", e).group(1).split("/abs/")[-1]
        print("   %s  %-16s %s" % (pub[:10], i, ti[:120]))


if __name__ == "__main__":
    run(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 10)
