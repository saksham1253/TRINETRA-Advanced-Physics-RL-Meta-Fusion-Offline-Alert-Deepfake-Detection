# OPEN QUESTIONS (needs user input) — MASTER_PROMPT §0.1 rule 7 / §0.2

Each has a best-default so work can continue safely. Surfaced in gate messages.

> **UPDATE 2026-10-05 — USER ANSWERED OQ-01…OQ-06 at the P0 gate. Recorded in
> DECISIONS.md D-007/D-008. All six RESOLVED. Answers inline below.**

## OQ-01 — Canonical root confirmation
Q: Confirm writable `default-workspace\` is the canonical program root and
`C:\Users\Dell\Downloads\trinetra\` is read-only source-of-truth.
Default: proceed as such (DECISIONS D-001).
**ANSWER (user): default — `default-workspace\` canonical, `trinetra\` read-only.
STATUS: RESOLVED.**

## OQ-02 — Do the 235 ABS papers count toward P2/P3 quota?
Q: §0.9 says abstract-only does NOT count toward a phase quota, and the foundation needs
≥60% Tier-2+. The 235 unique papers are ALL abstract-only. Should P2/P3 (a) re-read the
existing corpus at Tier-2+ to make it count, or (b) treat the 235 as a verified discovery
backlog and read NEW+existing to the quota from scratch?
Default: treat 235 as a verified queue; in P2/P3 promote the most load-bearing (~40–60) to
Tier-2+ full-text reads first, then extend.
**ANSWER (user): the 235 already-studied (abstract-only) papers must be PROPERLY RE-STUDIED
FIRST to proper (Tier-2+) depth, THEN study MORE extra papers on top. The 235 remain
NON-QUOTA (baseline re-study); the phase quota is NEW papers read ON TOP of them. STATUS:
RESOLVED.**

## OQ-03 — Integrity hashing without a shell
Q: SHA-256/size/mtime are INFEASIBLE (no shell). Acceptable to proceed with line-count
proxy for file identity?
Default: yes (DECISIONS D-003).
**ANSWER (user): read papers at TRUE full-text (depth), not just identity. Full-text route
SOLVED via ar5iv / arXiv-HTML through web_fetch (D-008). Line-count proxy for FILE IDENTITY
still accepted. STATUS: RESOLVED.**

## OQ-04 — Single-agent execution
Q: Sub-agent/parallel spawning is unavailable; the "two-pass different agent" anti-
hallucination rule is emulated by a fresh re-open pass in the same agent. Acceptable?
Default: yes — fresh-pass re-verification, logged in 11_reading_audit.md.
**ANSWER (user): default — fresh re-open audit pass is acceptable. STATUS: RESOLVED.**

## OQ-05 — Indian supplier price verification blocked
Q: Supplier pages return 403 (Cloudflare), so all ₹ BOM figures are [EST]. The ≤₹2000/node
gate cannot be enforced from live listings this session. Accept [EST] now and hard-verify
in P6, or should the user supply reachable listing URLs / a snapshot?
Default: carry [EST], hard-verify in P6 against ≥2 live listings.
**ANSWER (user): BOM price verification route found (Wayback Machine API +
archive.org/wayback/available + non-Cloudflare distributors). Deferred to P6 as planned.
STATUS: RESOLVED (route identified; execution in P6).**

## OQ-06 — First phase to authorize
Q: Recommended first phase is P1 (problem framing / scope / key questions). Authorize?
Default: await explicit "GO PHASE P1".
**ANSWER (user): "go with phase P1 ... all out chale jaa now good to go" — PHASE P1
AUTHORIZED (one phase only; stop at P1 gate). STATUS: RESOLVED — P1 IN PROGRESS.**
