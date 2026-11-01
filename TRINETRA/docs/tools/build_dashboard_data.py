"""Regenerate ../src/data/trinetra.json (Figma Make dashboard) from the handoff files. Run from TRINETRA/."""
import csv, json, re
ds = list(csv.DictReader(open("docs/09b_dataset_links.csv", encoding="utf-8")))
state = json.load(open("HANDOFF/STATE.json"))
gaps = []
for line in open("docs/GAP_LIST.md", encoding="utf-8"):
    m = re.match(r"^\| (G-\d+) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$", line.strip())
    if m: gaps.append(dict(id=m[1], gap=m[2], evidence=m[3], triage=m[4], status=m[5]))
paper = json.load(open("docs/tools/paper_verify_log.json"))["stats"]
nxt = [l[3:].strip() for l in open("HANDOFF/NEXT_ACTION.md", encoding="utf-8") if re.match(r"^\d\. ", l)]
bugs = []
for line in open("docs/BUG_STATUS.md", encoding="utf-8"):
    m = re.match(r"^\| (B-\d+) \| (.*?) \| (.*?) \| (.*?) \|$", line.strip())
    if m: bugs.append(dict(id=m[1], bug=m[2], fix=m[3], status=m[4]))
import os
results = json.load(open("results/results.json")) if os.path.exists("results/results.json") else None
out = dict(bugs=bugs, results=results, state=state, datasets=ds, gaps=gaps, papers={k: paper[k] for k in ("total_unique", "with_arxiv", "sampled", "verified", "title_mismatch", "link_failed")}, next=nxt)
json.dump(out, open("../src/data/trinetra.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(len(ds), "datasets", len(gaps), "gaps", len(nxt), "next")
