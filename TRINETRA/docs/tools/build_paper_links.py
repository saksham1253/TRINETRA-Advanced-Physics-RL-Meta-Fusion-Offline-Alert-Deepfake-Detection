"""Build docs/11_paper_links.csv from the repo ledgers (FROM-REPO) and verify a random >=15% sample
against the arXiv API (title match). Run from TRINETRA/: python docs/tools/build_paper_links.py"""
import csv, glob, json, random, re, time, urllib.request, xml.etree.ElementTree as ET, datetime
rows = {}
def norm(t): return re.sub(r"[^a-z0-9]", "", (t or "").lower())
def add(pid, title, src, extra):
    pid = (pid or "").strip().replace("arXiv:", "")
    if not pid and not title: return
    key = pid if re.match(r"^\d{4}\.\d{4,5}$", pid) else ("t:" + norm(title))
    r = rows.setdefault(key, {"id": pid, "title": title, "authors": "", "year": "", "venue": "", "doi": "",
        "arxiv_id": pid if re.match(r"^\d{4}\.\d{4,5}$", pid) else "", "read_depth": "", "theme": "",
        "used_in": "", "repo_path": set(), "verification": "FROM-REPO"})
    r["repo_path"].add(src)
    for k, v in extra.items():
        if v and not r.get(k): r[k] = v
for r in csv.DictReader(open("analysis/02_paper_ledger.csv", encoding="utf-8", errors="replace")):
    add(r["id"], r["title"], "analysis/02_paper_ledger.csv", {"authors": r.get("authors"), "year": r.get("year"),
        "venue": r.get("venue"), "read_depth": r.get("read_depth"), "theme": r.get("axis"), "used_in": r.get("relevance_component")})
for f in sorted(glob.glob("PROGRAM/phase_papers/P*_papers.csv")):
    for r in csv.DictReader(open(f, encoding="utf-8", errors="replace")):
        add(r.get("paper_id") or r.get("id"), r.get("title"), f, {"read_depth": r.get("read_depth"),
            "theme": r.get("theme") or r.get("axis") or r.get("focus") or r.get("workstream"),
            "used_in": r.get("workstream") or r.get("relevance") or r.get("why_matters_this_phase")})
allr = list(rows.values())
for r in allr:
    r["url"] = f"https://arxiv.org/abs/{r['arxiv_id']}" if r["arxiv_id"] else ""
    r["pdf"] = f"https://arxiv.org/pdf/{r['arxiv_id']}" if r["arxiv_id"] else ""
    if not r["url"]: r["verification"] = "MISSING-LINK"
ax = [r for r in allr if r["arxiv_id"]]
random.Random(0).shuffle(ax)
sample = ax[: max(1, int(0.2 * len(ax)) + 1)]
ok = bad = mism = 0; log = []
for i in range(0, len(sample), 20):
    chunk = sample[i:i + 20]
    url = "http://export.arxiv.org/api/query?max_results=50&id_list=" + ",".join(r["arxiv_id"] for r in chunk)
    try:
        xml = urllib.request.urlopen(url, timeout=60).read()
    except Exception as e:
        log.append(f"chunk {i} failed {e}"); continue
    ns = {"a": "http://www.w3.org/2005/Atom"}
    got = {}
    for e in ET.fromstring(xml).findall("a:entry", ns):
        eid = e.find("a:id", ns).text.rsplit("/", 1)[-1].split("v")[0]
        got[eid] = (e.find("a:title", ns).text or "").strip()
    for r in chunk:
        t = got.get(r["arxiv_id"])
        if not t or "Error" in t: r["verification"] = "LINK-FAILED"; bad += 1; log.append(f"{r['arxiv_id']} not resolved")
        else:
            r["arxiv_title"] = re.sub(r"\s+", " ", t)
            a = set(re.findall(r"[a-z0-9]{3,}", t.lower())); b = set(re.findall(r"[a-z0-9]{3,}", (r["title"] or "").lower()))
            score = len(a & b) / max(1, len(b))
            if norm(t)[:40] == norm(r["title"])[:40]:
                r["verification"] = "VERIFIED " + datetime.date.today().isoformat(); ok += 1
            elif score >= 0.5:
                r["verification"] = "VERIFIED-ABBREV-TITLE " + datetime.date.today().isoformat(); ok += 1
            else:
                r["verification"] = "ID-TITLE-MISMATCH (check by hand)"; mism += 1
                log.append(f"{r['arxiv_id']} | repo: {r['title'][:80]} | arXiv: {r['arxiv_title'][:80]}")
    time.sleep(3)
cols = ["id", "title", "authors", "year", "venue", "doi", "arxiv_id", "url", "pdf", "read_depth", "theme", "used_in", "repo_path", "verification", "arxiv_title"]
with open("docs/11_paper_links.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for r in sorted(allr, key=lambda r: (r["theme"] or "", r["id"])):
        r = dict(r); r["repo_path"] = ";".join(sorted(r["repo_path"])); w.writerow({k: r.get(k, "") for k in cols})
stats = {"total_unique": len(allr), "with_arxiv": len(ax), "sampled": len(sample), "verified": ok, "link_failed": bad,
         "title_mismatch": mism, "missing_link": sum(1 for r in allr if not r["arxiv_id"]),
         "read_depth": {d: sum(1 for r in allr if (r["read_depth"] or "unknown") == d) for d in sorted({r["read_depth"] or "unknown" for r in allr})},
         "themes": {t: sum(1 for r in allr if (r["theme"] or "unknown") == t) for t in sorted({r["theme"] or "unknown" for r in allr})}}
json.dump({"stats": stats, "log": log}, open("docs/tools/paper_verify_log.json", "w"), indent=1)
print(json.dumps(stats, indent=1)); print("\n".join(log[:40]))
