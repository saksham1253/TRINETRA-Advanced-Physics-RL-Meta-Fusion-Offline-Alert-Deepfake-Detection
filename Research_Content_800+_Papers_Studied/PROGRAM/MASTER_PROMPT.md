# MASTER PROGRAM (RESEARCH-ONLY, PHASED, PERMISSION-GATED, SOTA-DRIVEN): Literature-Grounded Research, Derivation on Paper, Design, Procurement Planning, Anomaly Detection Research, Failure-Mode Analysis, Evidence-Backed Feature Selection and National Deployment Pathway for India

You have full context of the project we have been working on in this conversation (disaster / fire detection and response, CCTV, physics-informed models, RL, deepfake handling, offline alerting, IoT, anomaly detection) and access to my existing project folder. This document is the complete operating manual. It is split into numbered PHASES. You execute ONE phase at a time, save everything to files in the existing folder, then STOP at the phase gate and ask me for permission before starting the next phase. You start with PHASE P0 right now; no permission is needed for Phase P0.

PURPOSE. This is not a competition task. The goal is to make the design of this system as state-of-the-art-informed, evidence-backed and defensible as possible, so that it can genuinely serve people in India and be built, piloted and published responsibly. The outputs may later be reused for a hackathon, a research paper or an official proposal, but no research or design decision in this program may be shaped by a competition, a slide template or a pitch. Where evidence and persuasiveness conflict, evidence wins.

THIS RUN IS RESEARCH-ONLY. I will build the system afterwards, with a separate prompt. So in this run: no code, no training, no experiments, no simulations, no firmware, no hardware building. Everything is literature, mathematics on paper, design, planning and documentation (details in section 0.1A).

Quality target: every design decision is grounded in verified sources and in the current state of the art, with the published numbers, benchmarks and protocols we will have to meet or beat when we build. To get there, EVERY phase from P1 onward reads at least 15 NEW research papers specific to that phase's task (section 0.9, "Phase paper quota") and starts with a SOTA scan. Inside a phase, time, tokens and number of steps are NOT constraints: be as thorough and detailed as the phase needs, never summarize prematurely, never shorten a note to save time. Between phases, I stay in control.

---

## 0. HOW THIS PROGRAM RUNS (read fully before doing anything)

### 0.1 Phase-gate protocol (strict, non-negotiable)
1. Execute only the phase I have authorized. Phase P0 is pre-authorized. Every later phase starts only after I send an explicit authorization such as `GO PHASE P3`.
2. Valid replies from me at a gate: `GO PHASE Pn` (as planned), `GO PHASE Pn with changes: ...`, `REPEAT PHASE Pn` (redo or extend), `SKIP PHASE Pn`, `REORDER: ...`, `STOP`. A vague reply such as "continue" or "ok" authorizes ONLY the single next phase in your current plan, nothing beyond it. Silence is not permission.
3. At the end of each phase: (a) run the phase's exit audit, (b) write the phase report to `PROGRAM/reports/PHASE_XX_report.md`, (c) update `PROGRAM/PHASE_STATE.md`, `PROGRESS.md`, the ledgers and the handoff files, (d) send me a short gate message (format in section 0.2), (e) STOP. Do not start any work of the next phase after the gate message: no searching, no reading, no "preparation", no downloads.
4. Mid-phase checkpoints: long phases (reading) write checkpoint notes to disk regularly. These are NOT gates; keep working unless blocked. Only phase boundaries are gates.
5. Scope discipline: do not do work belonging to a later phase, and do not skip work belonging to the current phase. If you discover that something from another phase is needed, record it in `PROGRAM/PHASE_BACKLOG.md` and raise it in the gate message.
6. Resources are approved per phase. You never spend or commit money yourself: you only prepare shopping lists; I buy. Compute (GPU) is not used in this run; GPU-hour figures in this program are planning estimates for the later build.
7. Blockers inside a phase: if something is truly impossible to infer or needs my input (a missing file, a decision only I can make, a part I must buy), record it in `ASSUMPTIONS.md` or `PROGRAM/OPEN_QUESTIONS.md` with your best default, continue with the default where safe, and list the open questions in the gate message. Do not stop mid-phase to ask unless continuing could cause harm or data loss.
8. I may change my mind at any gate. Log my decisions in `PROGRAM/DECISIONS.md` (date, gate, decision, reason).
9. SEQUENCE AUTONOMY (your judgment, my approval). You choose the order in which phases are executed, because many phases depend on each other. The phase IDs in section 0.11 are stable names, not a mandatory order. In Phase P0 you write the recommended sequence with a dependency graph and reasons. At every gate you may propose a different next phase, and you may propose to split a heavy phase, merge light ones, add a phase you find necessary, or drop a phase you find unnecessary, always with reasons. You never act on a sequence change without my authorization at the gate. Rules for your sequencing: respect hard dependencies (a phase cannot start before the phases it needs, unless you state the risk and I approve); put lead-time items early (hardware ordering research, dataset-access requests, any external deadline I mention); prefer sequences that unlock decisions early; explain the trade-offs of the sequence you propose and give one alternative.

### 0.1A RESEARCH-ONLY RULES (apply in every phase)
NOT allowed in this run:
- Writing, running or modifying any project code: model code, training scripts, notebooks, firmware, simulation code, data pipelines, evaluation harnesses, test code.
- Training or fine-tuning any model; running any experiment, benchmark, ablation or simulation; reproducing any paper's results from its code.
- Downloading large datasets or model weights (only what is needed to read a dataset's documentation or metadata).
- Building, flashing or testing hardware, or asking me to do so.
- Modifying any pre-existing project file. Existing project code and earlier results may be READ (read-only) to understand the system; earlier results are reported as "pre-existing", never re-run, never presented as new.
- Producing numbers that look like our own results. Every number comes from a verified source. GPU-hour and INR figures are labeled planning estimates.
Allowed and expected:
- Everything research: finding, verifying and reading papers (the Reading Engine, the quota per phase, SOTA scans, novelty checks, ledgers, registers, contradiction register, synthesis, failure-mode catalogue).
- Mathematical derivations on paper (symbolic, step by step, with units and limiting cases), written as documents; formulas are written in LaTeX text inside .md files.
- Dataset and benchmark research: existence, licenses, sizes, splits and known flaws verified from official pages and papers (status wording: "verified from official documentation; inspection deferred to the build phase").
- Hardware research and procurement planning: component research, datasheets, verified Indian prices and links, the BOM, the shopping list, the INR 2000 prototype budget plan, the safety protocol document. No building or testing.
- Design documents, specifications, protocols and plans: architectures, interfaces and data formats, pre-registered evaluation protocols, experiment plans, acceptance criteria, planning-level GPU-hour budgets, verification checklists, threat models, demonstration plans, the deployment pathway and pilot design.
- Bookkeeping that is not project code: listing folders, copying files to backups, computing file hashes, writing documents, and tiny tool-availability probes (web search, page and PDF fetching, file writing, sub-agent availability).
If you are unsure whether something counts as code work, treat it as code work, do not do it, and list it in the build handoff instead.

### 0.2 Gate message format (send at the end of every phase, in plain language)
- Phase finished: name and ID; status (complete / complete with deviations / partial). State "No code was written or run in this phase" (or list exactly which bookkeeping steps or tool probes were used).
- What was produced: list of files created or updated (paths).
- Key findings: the 5 to 10 most important findings, with numbers and their sources, clearly separating "paper reports" from "pre-existing project results".
- SOTA position: what the SOTA scan found (best published methods, benchmarks, numbers and their protocols and known flaws), and what that means for our design and for the targets we will have to meet when building. Never claim that our design is SOTA or better than SOTA; claim only what the evidence supports (rule 16).
- Paper quota: number of NEW papers read in this phase (Tier 1, 2, 3 counts) versus the minimum of 15; the file listing them; what changed in our design because of them; any shortfall and the honest reason.
- Counts: total papers (baseline, new, by read tier), datasets verified, features, INR planned vs 2000.
- Audit results: error rates found and fixed.
- Handoff status: what was added to `HANDOFF/` (section 0.4A).
- Deviations from the plan, problems, and risks.
- Open questions and assumptions that need my input.
- Proposal for the next phase: which phase you recommend next and WHY (dependency and sequencing logic), the alternative, its objective, expected outputs, expected effort, and any suggested changes to the plan.
- The exact line I should reply with to authorize it (for example `GO PHASE P9`), plus the alternatives (change / skip / reorder / stop).
Keep the gate message short (about one screen); the details live in the report file.

### 0.3 File persistence and folder rules
- Work INSIDE my existing project folder. Locate it yourself (the folder holding my papers and any earlier outputs). Do not create a new unrelated root. State the path you chose in the Phase P0 report. If two candidate folders exist and you cannot tell which is correct, pick the one with the most project content, record the choice, and list it as an open question.
- NON-DESTRUCTIVE: never delete, overwrite, move or rename my existing files. If an existing file must change (for example an earlier ledger), copy it to `PROGRAM/backups/<date>_<name>` first, then edit, and record the change in `PROGRAM/CHANGELOG.md`. New work goes into new files and the standard layout (section 0.10).
- EVERYTHING is saved to files, nothing lives only in chat: notes, ledgers, registers, decisions, plans, reports, logs, SOTA scans, quota lists, handoff files, and the gate messages themselves (`PROGRAM/gate_messages/`).
- Save as you go, not at the end. Each paper note, ledger row and queue status is written to disk the moment that paper is finished. A crash must lose at most one paper or one small step.
- `PROGRAM/PHASE_STATE.md` is the single source of truth for control: current phase ID and name, status (not started / in progress / awaiting gate / authorized-next), the last authorization received (verbatim) with its date, what is in progress, the current recommended sequence, and the next planned step. Update it at every start, checkpoint and end.
- Large files (PDFs) are referenced by path and hash in manifests rather than copied. Keep human-readable `.md` for narrative and `.csv` or `.json` for ledgers and registers.

### 0.4 Crash and resume protocol
At the start of every session or after any interruption: read `PROGRAM/MASTER_PROMPT.md` (the saved copy of this prompt) fully, then `PROGRAM/PHASE_STATE.md`, then `PROGRESS.md`. Look for items marked "in progress". Verify the state from the files themselves (counts from the files, not from any document's claims). Repair whatever the interruption damaged (re-verify the last few notes written, reconcile ledger vs notes vs queue vs the phase quota list), log it in `PROGRAM/INCIDENTS.md`, and continue the authorized phase from where it stopped. Never restart finished work. Never start a phase that has not been authorized. Retry failed fetches a few times with backoff; then mark the item "fetch-failed" with the reason and move on; never invent content you could not access. At the start of EVERY phase also re-read `PROGRAM/MASTER_PROMPT.md` instead of relying on memory.

### 0.4A The build handoff package (mandatory, updated at the end of every phase)
Because I will build later with a separate prompt, keep `HANDOFF/` current. `HANDOFF/BUILD_HANDOFF.md` records, per workstream: what is to be built, the chosen methods and the papers they follow (IDs), datasets with verified links and licenses, interfaces and data formats, the pre-registered evaluation protocol and acceptance criteria, published baselines and targets to match first, hyperparameter defaults with sources, planning-level GPU-hour estimate and Kaggle fit, verification checklists, known pitfalls from the failure-mode catalogue, open decisions, and the recommended order of building. Also keep `HANDOFF/OPEN_DECISIONS.md` (choices only I can make) and `HANDOFF/RISKS_FOR_BUILD.md`.

### 0.5 HARD HONESTY RULES (non-negotiable, apply in every phase)
1. REAL SOURCES ONLY. Never invent or "recall from memory" a paper, author list, dataset fact, link, number, quote, equation source, datasheet value, price, law, standard or table reference. Every citation needs a verifiable identifier (DOI / arXiv ID / stable URL), title, all authors (or issuing body for reports and standards), year, venue, and you must have actually located it through a real source in this session. If it cannot be verified it does not exist for this project and must not appear in any ledger or report.
2. NO FAKE FEATURES. Every feature must trace to at least one real paper or dataset. Your own idea is allowed only if labeled "novel hypothesis, unvalidated".
3. NO FABRICATED NUMBERS. Report only what a verified source states (with the table/figure/page you actually looked at) or what pre-existing project files contain (labeled pre-existing). Nothing is "our measurement" in this run.
4. Separate CONFIRMED (by a verified source) / LIKELY / HYPOTHESIS / INFEASIBLE in every report. Keep "Paper X, Table N reports ..." visibly separate from pre-existing project results and from your own reasoning.
5. If papers conflict, record the conflict in the contradiction register. Do not silently pick a side.
6. If something requested is physically or practically impossible, say so plainly, explain why, and propose the closest feasible alternative backed by literature.
7. NO FEATURE CREEP WITHOUT EVIDENCE. Every added feature must pass the admission rules (Phase P17). Never describe a feature as working or improving anything: it is only "supported by evidence X, not yet built or tested".
8. NO PADDING. Never add irrelevant papers to reach a count or a quota. If relevance runs thin, widen to adjacent fields whose techniques transfer. If you still cannot reach a target or quota, report the exact number reached and why.
9. READ-ONLY. See section 0.1A.
10. DO NOT OVERSTATE READING. A paper is "full-text" only if you actually read the method, experiments and limitations. Skimming = "partial". Abstract or snippet only = "abstract-only". Mislabeling read depth is a violation.
11. MEMORY IS NOT A SOURCE. Knowledge from training is only a lead for where to search. It becomes usable only after you find and read the actual source. Topic names listed anywhere in this prompt (including names of agencies, laws and standards) are search directions, not citations.
12. Quote sparingly (short quotes only when exact wording matters); paraphrase everything else. Never copy long passages from papers, datasheets, standards or documentation.
13. HARDWARE AND PRICE HONESTY. Every price, specification, range, current draw and capability of a component comes from a verified datasheet or a live seller listing you actually opened (with URL and date). No assumed prices. Manufacturer or paper figures are labeled as such; real-world performance of our own build is not claimed because nothing is built yet.
14. THE NUMBER OF PHYSICS MODELS IS NOT FIXED. It is decided by evidence (Phase P7). Do not force a count up or down.
15. PHASE HONESTY. Never claim a phase is complete if its acceptance criteria are not met; report partial completion plainly.
16. SOTA HONESTY. "State of the art" is a claim about a specific benchmark and protocol. In this run we make no performance claims about our own system. We may say that our design is informed by, or targets, the published state of the art, and we state the benchmark, protocol and numbers we will need to meet. Published numbers can be inflated by flawed protocols (for example threshold tuned on test data, leakage, lenient metrics); when the literature criticizes a benchmark or metric, say so and prefer the stricter protocol in our plans.
17. QUOTA HONESTY. A paper counts toward a phase quota only if it is genuinely NEW (section 0.9 novelty check), genuinely relevant to the phase, and read at Tier 1, 2 or 3 with a faithful note. Abstract-only, fetch-failed, duplicates of earlier-read papers, versions of an already-read paper, government or standards documents, and irrelevant filler do not count.
18. PUBLIC-CLAIMS HONESTY. Any statement about impact (lives, injuries, losses, response time, cost savings, coverage) must come from a verified source with date, or be explicitly labeled "projected" with the assumptions shown. Never overstate. Novelty claims must be tied to verified gaps in the literature and labeled "proposed design, not yet built or validated".
19. LIFE-SAFETY RESPONSIBILITY. This system could influence decisions that affect people's safety. Never present it as a replacement for certified fire detection and alarm systems, emergency services or official public warning systems: it is designed to complement them. Treat both false alarms and missed detections as real harms; require human oversight for high-stakes alerts; state clearly in every design document what the system must not be relied upon for until it is validated and independently reviewed.
20. PHYSICS CLASSIFICATION. Every relation, formula or model in this program is classified and the class label travels with it everywhere (derivations, registers, handoff, final report, any material built from them):
- CLASS A (established): appears in verified sources; cite source and equation number.
- CLASS B (derived): follows from Class A relations by algebra we show step by step under stated assumptions; every step checked; it may not appear in any paper as such. Not "validated" merely because the algebra is correct.
- CLASS C (novel closure or assumption): a modeling choice, empirical closure, coupling or combination not found in the literature. It is a HYPOTHESIS, unvalidated until compared with real published experimental data.
Nothing in Class B or C may be described as established physics, as validated, or as "a new law". Class C is never presented without its assumption, its regime of validity and the data that would falsify it.
21. NOVELTY CLAIMS ARE SEARCH CLAIMS. Never write "does not exist in any paper". Write "not found in the N sources searched" and list the queries, indexes, dates and the closest papers found, with how ours differs. Prefer honest extensions of established models over invented novelty; never manufacture novelty.

### 0.6 Global constraints
- COMPUTE (planning only): the later build will use Kaggle only. In this run, verify the CURRENT Kaggle limits from official documentation (weekly GPU quota, per-session time limit, GPU type, RAM, disk, output size limit, internet rules, dataset size limits) with source link and access date, and plan a budget of about 30 GPU hours for the whole later build, shared by every workstream (including anomaly detection) and feature, with at least a 15% reserve. These are planning estimates.
- PROTOTYPE HARDWARE BUDGET (IoT): the entire IoT prototype must cost at most INR 2000 including GST, shipping and every part needed to make it work and be demonstrated (microcontrollers, sensors, camera, radios, buzzer/strobe, power, wires, breadboard/PCB, enclosure, cables). Assume I own nothing unless I say so in `ASSUMPTIONS.md`; parts I might own (phone charger, USB cable, laptop) are listed separately as "assumed owned" and excluded from the total. Verify current Indian prices from real listings (several sellers), record the cheapest reliable option and one alternative, keep about 10% contingency. Separately, the deployment-pathway phase studies cost at scale for real deployments (only with verified prices).
- One shared deduplicated `paper_ledger.csv` and `REFERENCES.md` for the whole project. Government reports, standards and datasheets are logged in the same ledger with their type, but only research papers count toward quotas.
- SAFETY (hard rule, for the later build): no uncontrolled fire. The safety protocol you write specifies safe, supervised stimuli only (incense/agarbatti smoke, small controlled heat sources at safe distance, hot-air or heated-object sources, steam, cooking-like nuisance sources, recorded video on a screen for the camera path), outdoors or ventilated, with an extinguisher or water at hand and an adult present; low-voltage USB/5 V only; no bare lithium cells; protected modules or USB power banks. Never instruct anything that could start or spread a real fire.
- Ethics, privacy and law: no identifiable private individuals in any material; respect dataset licenses; do not produce or distribute deceptive media; alerting designs must be consent-based and abuse-resistant; anomaly detection on people or on social accounts must respect privacy and avoid profiling individuals; legal and regulatory findings are research notes, not legal advice, and are flagged for review by a qualified professional.

### 0.7 Multi-agent orchestration (inside any authorized phase)
If you can spawn sub-agents, spawn as many as are useful, in parallel: an orchestrator (you) owning the plan, ledgers, merges and integration; literature agents split by theme; one research agent per workstream (more where literature is large; at least two for IoT: sensing/physics and embedded/networking; at least two for anomaly detection: video and time-series/OOD); specialists: baseline-paper reader, dataset discovery and verification, SOTA-scan agent, novelty-check agent (guards the paper quota), citation verification auditor, reading-faithfulness auditor, hardware-BOM and price-verification agent, safety reviewer, India-context and regulation researcher, feature scouts, red-team reviewer (attacks the designs on paper), consistency auditor. Agents write only to their own folder and to shared ledgers through append-only entries (agent name + timestamp). The orchestrator merges, deduplicates (DOI / arXiv ID / URL / normalized title) and resolves conflicts. No agent edits another agent's notes; corrections go through the auditor. Agents never cross phase boundaries and never act without the phase being authorized. If you cannot spawn agents, emulate the same structure sequentially; the auditor pass must be a separate, fresh pass that re-opens sources.

### 0.8 Search depth standard (applies to every searching phase)
- Many query variants per topic: synonyms, acronyms, method names, problem names, plus modifiers such as "failure", "limitations", "robust", "benchmark", "survey", "negative results", "reproducibility", "comparison", "ablation", "cross-dataset", "generalization", "real-world deployment", "low-cost", "field test", "critique", "pitfalls", "evaluation protocol", "India".
- Multiple indexes: arXiv, Semantic Scholar, Google Scholar-style search, OpenReview, ACL Anthology, IEEE Xplore, ACM DL, ScienceDirect, Springer, MDPI, Wiley, PubMed, NASA NTRS, NIST, fire-science journals (Fire Safety Journal, Fire Technology, Combustion and Flame, Proceedings of the Combustion Institute, Int. J. of Wildland Fire, Fire and Materials), disaster-management and risk journals, remote-sensing and geoscience journals, CVPR/ICCV/ECCV/WACV/NeurIPS/ICML/ICLR/AAAI/KDD, IEEE TIFS/TPAMI/TIP/TNNLS, networking and IoT venues (INFOCOM, SIGCOMM, MobiCom, SenSys, IPSN, IEEE Internet of Things Journal, IEEE Sensors Journal, Sensors/MDPI, IEEE Access), TinyML venues, time-series and anomaly-detection venues, and workshop tracks.
- Snowball: backward citations and forward citations from strong papers; mine survey reference lists; follow related-work sections of the strongest recent papers.
- Check Papers With Code, HuggingFace, GitHub and Kaggle pages for leaderboards, official implementations (to note that they exist, not to run them), weights and datasets; record licenses.
- Datasheets, standards, official government documents and documentation are valid sources for hardware facts, regulatory facts and statistics. Log them in the ledger with type = "datasheet / standard / government report / documentation", URL, document version/date and access date. They never substitute for peer-reviewed evidence about system performance and they do NOT count toward the paper quota.
- Paywalled papers: look for legal open versions (arXiv, author pages, institutional repositories). If only the abstract is reachable, the item is "abstract-only" and labeled so everywhere.
- Quality filter: prefer peer-reviewed or well-cited work, but include strong preprints and label their status. Record retractions, corrections and superseding versions.

### 0.9 THE READING ENGINE, THE PHASE PAPER QUOTA AND THE SOTA SCAN (used by every phase from P1 onward)

**Tiers.** TIER 1 DEEP (the most relevant 40 to 60 papers overall): full text including appendix/supplement; equations checked step by step or re-derived on paper; datasets and splits studied as described; official code noted if it exists; limitations and implicit assumptions analyzed. TIER 2 FULL: method, experiments, results and limitations read; complete structured note. TIER 3 PARTIAL: abstract, introduction, method overview, main results and limitations; note says which sections were not read. TIER 4 ABSTRACT-ONLY: only when the full text is genuinely unreachable; never the sole evidence for a design choice, formula, number or claim; never counts toward a quota. For the foundation set: at least 60% at Tier 2 or deeper, the rest Tier 3. Datasheets and standards are read for the specific values used; the note records which values came from which page.

**PHASE PAPER QUOTA (every phase except P0).** In every phase you must read AT LEAST 15 NEW research papers that serve that phase's specific task and that are needed to reach state-of-the-art-informed quality in that phase's work. The quota is a minimum, not a target to stop at: heavy phases (physics, CCTV, anomaly detection, deepfake, alerting, RL, IoT research) should read considerably more, and no phase may stop reading while it still has important unanswered questions. Rules:
- NOVELTY CHECK (mandatory before reading each candidate): the paper must not already be in `paper_ledger.csv` (any status), in the baseline papers folder, in `analysis/10_reading_queue.csv` as already noted/audited, in the search log as already read, in `PROGRAM/manifests/novelty_index.csv`, or in notes from earlier agents or from me (including the roughly 99 papers read before the earlier interruption). Match by DOI, arXiv ID, URL and normalized title; a preprint and its published version, or two arXiv versions, are the SAME paper. Log the check result in the phase quota file. If unsure whether it was already read, treat it as read and pick another.
- The papers must be relevant to THIS phase's task (the phase definitions list the quota topics) and chosen for SOTA value: the strongest recent work (last 2 to 3 years prioritized for fast-moving topics), the benchmark and leaderboard papers, the best critiques and negative-result papers, and the seminal papers the field's best work builds on that you have not yet read.
- Each counted paper has a complete structured note (schema below), a ledger row tagged `phase_quota=<phase ID>`, and a row in `PROGRAM/phase_papers/<PHASE_ID>_new_papers.csv` (id, title, tier, date read, why it matters for this phase, the actionable takeaway, and the novelty-check result).
- Only Tier 1, 2 or 3 research papers count. Datasheets, standards, government reports, documentation, blog posts, abstract-only items, fetch-failed items and filler do not count.
- Papers counted toward the foundation target in Phases P2 and P3 also count toward those phases' quotas. Papers read in one phase never count again for another phase's quota.
- Use the new papers: each phase report states, per quota paper or per group, what changed in the phase's design, protocol, baselines, metrics or decisions because of it. A paper that changes nothing should be justified or replaced.
- If the field genuinely lacks 15 relevant new papers for a phase, widen to adjacent fields; if that still fails, report the exact number and why. Do not pad.
- Exit audit includes a quota audit: a fresh pass re-checks the novelty of every counted paper (re-run the lookup), the read tier, and the note faithfulness for at least 20% of them (all of them if the phase has 15 to 20).

**SOTA SCAN (first task of every phase from P1 onward).** Write `PROGRAM/sota/<PHASE_ID>_sota_scan.md`: what the current best published methods, benchmarks and numbers are for this phase's task, from leaderboards, recent surveys, recent top-venue papers and strong open implementations (each with a verified identifier, date, the exact benchmark, split, metric and protocol); what the known flaws of those benchmarks and metrics are; what the realistic bar is for a build under our later limits (Kaggle and hardware); and which published methods we should use as baselines and targets. At the end of the phase, add a "SOTA targets and protocol plan" section to the phase report: the published numbers we will need to meet or beat, under which protocol, and what a fair comparison will require. No claims about our own performance (rule 16).

**Queue.** `analysis/10_reading_queue.csv`: id, title, source index, discovered-via (query or citation chain), tags (workstream, technical question, phase), priority score, status (queued / fetching / reading / noted / audited / fetch-failed / rejected-irrelevant), tier. Priority = relevance to the key technical questions x evidence strength (venue, citations, reproducibility) x recency (for fast-moving topics) x novelty relative to what is already read. Surveys are read early because they seed the queue. Every rejected-irrelevant item gets a one-line reason.

**Per-paper note (mandatory schema).** Identification and status: id, type (paper / preprint / datasheet / standard / government report / documentation), title, ALL authors (or issuing body), year, venue, version read, status (peer-reviewed / preprint / retracted / corrected / superseded-by), date accessed, access route, read_depth (tier) and exactly which sections were read, phase_quota tag. Content, in your own words: problem and why it matters; core idea/method at a level someone could re-implement later (architecture, equations, circuit or protocol details); data (datasets, sizes, splits, how splits were made, whether cross-site/cross-camera/cross-generator evaluation exists or only in-dataset, preprocessing, augmentation); baselines and whether they were tuned fairly; metrics and key results WITH table/figure reference (only what you saw); training recipe, hyperparameters and compute (for hardware papers: sensors, MCU, power, deployment conditions); assumptions (stated and unstated); stated limitations and failure modes (inferred ones labeled "inferred"); reproducibility (code, weights, license, red flags such as leakage, tuning on test, missing seeds, cherry-picked examples, unfair baselines, lab-only conditions, lenient metrics). Relevance to us: component, workstream and technical question informed; actionable takeaway (the concrete design choice, protocol, safeguard, component choice or metric it suggests for OUR system); transferability (how close the setting is to ours, including to Indian conditions; if far, "transfer hypothesis"); confidence in the note (high/medium/low) and why; conflicts with other papers (links into the contradiction register).

**Registers (kept current while reading).** `analysis/07_claims_table.csv` (claim paraphrased, paper id, table/figure, setting, metric, value as stated, evidence type, caveats, applicability; abstract-only claims marked "abstract-level"). `analysis/08_equations_register.md` (statement in LaTeX text, symbol table with units, class A/B/C, assumptions and regime of validity, source id and equation number, whether re-derived on paper, which verification checks are planned). `analysis/09_hyperparameter_register.md` (training recipes, losses, schedules, batch sizes, augmentations, compute, with paper ids, for later planning). Citation graph (key references and key citers of every strong paper, IDs at least).

**Batch cycle.** Start with batches of about 10 papers (about 20 to 30 once stable). For each batch: write the planned IDs to `PROGRESS.md` as "in progress"; run the novelty check; locate and verify each item (resolve identifier, confirm title/authors/year/venue, check retraction or newer version, find the best legal full text); read per tier and write the full note immediately; update registers; append the ledger row (deduplicate) and queue status immediately; update the phase quota file and the novelty index; cross-check against papers already read (new agreement, conflict, gap); mark the batch "done". Every 5 batches write an interim synthesis and re-prioritize the queue.

**Anti-hallucination controls.** Two-pass rule: every ledger row and note is re-checked by a different agent or a fresh pass that re-opens the source and confirms identifier, title/authors/year/venue, that every number and table reference appears in the source, that the method summary is faithful, and that the limitations are real. Failures are fixed or removed and the rate is logged in `analysis/11_reading_audit.md`. Spot audit: random 10% of notes per batch plus 100% of Tier 1 key numbers; if a batch's error rate exceeds 5%, redo the batch. Any number, equation or quote in a downstream document must trace back to a note with a table/equation/page reference; untraceable items are removed. When sources disagree about a fact, prefer the primary source and record the discrepancy.

**Contradiction register and gap map.** `analysis/06_contradiction_register.md`: each entry has the question, the papers on each side, their settings, which seems better supported and why, and what study of ours could resolve it in the build phase. Never average away disagreement. Gap map: things we plan that no paper validates; things the field validated that we do not plan; areas where evidence is weak or only exists in other domains. The gap map is also the raw material for honest research-contribution claims (Phase P19).

**Reading-time rules.** Take as much time as needed. If a paper is too technical to fully understand, say what you did not understand rather than guessing. "The paper claims X; I could not verify Y" is a good note.

### 0.9A DATASET REGISTRY RULES (apply in every phase)
- `DATASETS.md` is the ONE living registry for every dataset, benchmark, corpus, simulator environment and public data source that this project might use, in every workstream. It is never split across other files; other documents only point to it by dataset ID.
- Every phase that finds or decides to use a dataset (for example IoT sensor data in P6, physics experimental data in P7, CCTV and fire data in P8, anomaly benchmarks in P9, forensic and social-media data in P11, network traces in P12, RL environments and evacuation data in P15, India-specific data in P19) must add or update its entry in `DATASETS.md` in that same phase, with a dated change note in `PROGRAM/CHANGELOG.md`. Before finishing a phase, check that nothing it relied on is missing from the registry.
- The top of `DATASETS.md` has a QUICK LINKS table, one row per dataset: ID, name, workstream(s), direct link, COST (free / free with registration / free on request / paid / unclear), license, access method, size, "Kaggle-available yes/no", STATUS (selected for the plan / backup / rejected / rejected-paid / candidate), and verification date. Sort it by workstream, with selected datasets first.
- COST must be verified from the official source. Never assume a dataset is free. If cost or license is unclear, write "unclear" and say what to check. Datasets that need registration, an institutional email, a request form or approval get a "start early" flag, and are also listed in `PROGRAM/LEAD_TIME_ITEMS.md` with the exact steps I must do myself.
- Each dataset keeps a link to its introducing paper, mirror links if any, and a fallback alternative if the link dies.
- Below the quick-links table, give the full entry per dataset (as defined in Phase P5), plus: why it is in the plan, which model or protocol uses it, which split or protocol applies, and its role (train / validation / held-out generalization test).
- A selected-datasets summary at the very end lists only STATUS = selected, grouped by workstream, as the shopping list for the build phase. For datasets that are large, also give the size, so I can plan storage before the build.
- Never download datasets in this run (rule in 0.1A). The registry contains links, verified metadata and plans only.
- FREE-ONLY RULE: only free datasets may have STATUS = selected. Datasets that cost money are listed with STATUS = rejected-paid and a one-line reason, never selected. "Free with registration" or "free on request" count as free but carry the "start early" flag. Free to download does not always mean free to reuse: record the license and any restriction on redistribution, commercial use or publication for every dataset.
- GOVERNMENT AND AGENCY PORTALS (for example ISRO's Bhuvan and NRSC portals, NASA Earthdata, FIRMS, GIBS and similar): for each product record the portal, the exact product name and version, the direct link, the access status (open download / login or registration required / approval or request required / restricted to certain users or regions), the terms of use, the resolution and coverage, and the verification date. Never assume a government dataset is open; verify its terms from the portal itself.

### 0.10 Standard directory layout (create inside my existing folder; reuse anything that already exists)
```
<existing_project_folder>/
  PROGRESS.md  ASSUMPTIONS.md  FINAL_REPORT.md
  paper_ledger.csv  REFERENCES.md  DATASETS.md  FEATURES.md
  KAGGLE_BUDGET.md  HARDWARE_BUDGET.md
  PROGRAM/    MASTER_PROMPT.md  PHASE_PLAN.md  PHASE_STATE.md  PHASE_BACKLOG.md
              DECISIONS.md  OPEN_QUESTIONS.md  INCIDENTS.md  CHANGELOG.md  RISK_REGISTER.md
              LEAD_TIME_ITEMS.md
              reports/  gate_messages/  backups/  logs/  manifests/
              sota/            (one SOTA scan per phase)
              phase_papers/    (one new-paper quota list per phase)
  analysis/   00_system_model.md  01_baseline_papers.md  02_search_log.md
              03_paper_notes/  04_synthesis.md  05_failure_mode_catalogue.md
              06_contradiction_register.md  07_claims_table.csv  08_equations_register.md
              09_hyperparameter_register.md  10_reading_queue.csv  11_reading_audit.md
  ws1_physics/  ws2_deepfake/  ws3_alerting/  ws4_cctv/  ws5_rl/  ws6_robustness/  ws7_iot/  ws8_anomaly/
  HANDOFF/    BUILD_HANDOFF.md  OPEN_DECISIONS.md  RISKS_FOR_BUILD.md
  DEPLOYMENT/ (India deployment pathway, standards, pilot design, research-contribution plan; Phase P19)
```
If an earlier session or an earlier version of this program already created any of these (for example `analysis/` with notes from the first 99 papers, or a `PROGRAM/` folder from an older phase map), keep and extend them; never overwrite.

### 0.11 PHASE MAP (stable IDs; the recommended sequence is yours to propose, section 0.1 rule 9)
| ID | Name | Main outcome | Hard dependencies |
|---|---|---|---|
| P0 | Setup, inventory, backup, state reconciliation, plan | Safe working base, true counts, phase plan and recommended sequence (PRE-AUTHORIZED, start now) | none |
| P1 | Baseline papers and system model | Every paper in my folder read; system model; key technical questions | P0 |
| P2 | Literature foundation I | Foundation papers: core methods, CCTV/fire, evaluation, robustness, uncertainty | P1 |
| P3 | Literature foundation II | Foundation papers: physics, media forensics, alerting/networks, RL, IoT, anomaly detection basics, safety, adjacent; reach 250 to 400 | P2 |
| P4 | Synthesis | Consensus/disagreement, failure-mode catalogue, gaps, design-change list | P3 |
| P5 | Dataset registry and compute budget plan | DATASETS.md, KAGGLE_BUDGET.md plan with verified limits | P3 (P4 helpful) |
| P6 | WS7a: IoT research, component selection, BOM, safety | Verified BOM under INR 2000, shopping list, safety protocol | P3 |
| P7 | WS1a: physics models on paper | Model-set decision (N by evidence), full derivations, validation plan | P3, P5 |
| P8 | WS4: CCTV detection research and design | Evidence-based model selection, failure taxonomy, protocol, plan | P5, P7 (soft) |
| P9 | WS8a: anomaly detection research, scope and evaluation protocol | Scope decision, SOTA scan, pre-registered protocol, design | P4, P5 (P8, P6 soft) |
| P10 | WS8b: anomaly detection specification | Ready-to-build spec per anomaly family, experiment plan | P9, P8 |
| P11 | WS2: deepfake and misinformation design | Detector pipeline design, degradation protocol, decision policy | P5, P7 (soft) |
| P12 | WS3: offline alerting | IP-idea verdict, tiered architecture, simulation specification, threat model | P3 (P6 soft) |
| P13 | WS7b: IoT design and build manual | Firmware and wiring specification, test and demonstration protocol (documents only) | P6, P12 (soft), P10 (soft) |
| P14 | WS1b: meta-fusion design | Calibrated fusion design across physics models, vision, sensors and anomaly scores | P7, P8; P10, P13 (soft) |
| P15 | WS5: reinforcement learning design | Environment design, algorithm choice, training plan and budget | P7, P12, P14 (soft) |
| P16 | WS6: robustness audit plan | Failure-mode catalogue applied to the design and to existing code (read-only), prioritized fix and test plan | core designs exist |
| P17 | Feature discovery and admission | FEATURES.md backlog with evidence and costs | core designs stable |
| P18 | Feature specifications and measurement plans | Ready-to-build feature specs with pre-registered decision rules | P17 |
| P19 | India deployment pathway, standards and regulation, pilot design and research-contribution plan | What it takes to deploy this responsibly in India, what is genuinely novel and publishable | P1 to P18 as you judge (especially P6, P12) |
| P20 | Final quality gates and final research report | Audits and FINAL_REPORT.md | everything wanted |

Every phase P1 to P20 carries the 15-paper quota and a SOTA scan (section 0.9).

---

# PHASE P0: SETUP, INVENTORY, BACKUP, STATE RECONCILIATION AND PLAN (START NOW)

**Objective.** Create a safe, fully documented working base inside my existing folder, find out the true state of everything that already exists (including the roughly 99 papers already read before a server error interrupted an earlier run), verify the research tools you actually have, and produce the phase plan and recommended sequence. No new papers are searched or read in this phase (Phase P0 is exempt from the quota). No project code is written or changed.

**Entry.** None (pre-authorized).

**Tasks (do all, in order, write each output to disk as you go).**

0.0 SAVE THIS PROMPT
- First action: save this entire message, word for word, to `PROGRAM/MASTER_PROMPT.md` inside my existing project folder (create `PROGRAM/` if needed; if the file already exists, save the new version as `MASTER_PROMPT_v2.md` and never overwrite the old one). If you cannot save files, tell me immediately.

0.1 LOCATE AND INVENTORY THE FOLDER
- Find the project folder. List the full tree with file counts, total sizes, file types and last-modified dates. Identify and describe: the papers folder (how many PDFs, naming scheme, duplicates), earlier reading notes and ledgers, earlier analysis outputs, prompts or mission files, existing project code and results (read-only), hardware notes, a `PROGRAM/` folder from an earlier version of this program (if any), and anything unexpected (temp files, partial files, files modified during the interruption).
- Write `PROGRAM/manifests/folder_inventory.md` and `PROGRAM/manifests/file_manifest.csv` (path, size, last modified, SHA-256 hash for files under a sensible size limit, hash skipped for very large files with a note).
- Flag problems: unreadable PDFs, corrupted or zero-byte files, duplicate papers (same DOI or near-identical title), files with ambiguous names, papers that are not relevant to the project.

0.2 NON-DESTRUCTIVE BACKUP
- Before editing anything that already exists, snapshot all existing notes, ledgers, progress files, prompt files and small text outputs into `PROGRAM/backups/<date>_pre_program/` with a manifest. Do not copy huge PDFs; record their paths and hashes in the manifest instead. Confirm the backup is complete by comparing hashes. State exactly what is and is not covered.

0.3 RESEARCH TOOL CAPABILITY CHECK
- Test, with tiny real actions, and record in `PROGRAM/ENVIRONMENT_CHECK.md`: web search; fetching a web page; fetching and reading a PDF; reaching arXiv, Semantic Scholar, publisher pages, government and standards-body sites, GitHub, Kaggle, Hugging Face and seller sites (note any blocked domains); writing files; ability to spawn sub-agents and how many in parallel; context and session limits you can observe; any rate limits. Do not run project code or GPU checks.
- For each capability, state what the program depends on it for and the fallback if it is missing. The 15-new-papers-per-phase quota depends heavily on web search and PDF reading: if either is missing, say so loudly, because I must fix that before Phase P1.

0.4 RECOVER PROJECT CONTEXT
- From the conversation and the folder, write `analysis/00_context_recovered.md`: the project's purpose (real-world benefit to India, see PURPOSE above) and scope; what is already decided (for example the originally identified physics models, the IP-alerting idea, the CCTV, RL, deepfake, IoT and anomaly-detection components, the planned Kaggle 30-hour budget, the INR 2000 prototype budget, and any external events or deadlines I have mentioned, such as a hackathon, treated as scheduling facts only); what is still open; which things you could not recover and what you assumed. List the originally identified physics models explicitly (name, phenomenon, governing equations, variables, assumptions) if they can be recovered; if they cannot, say so. Do not start deriving anything.

0.5 RECONCILE THE EARLIER READING (the interrupted run)
- Find every paper note, ledger, queue file, register and progress file produced earlier. Count the real state from files, not from what any document claims: complete notes (all schema fields present, read depth stated, table/figure references present), partial/truncated/malformed notes, ledger rows vs notes (matches and orphans in both directions), duplicates (DOI / arXiv ID / URL / normalized title), baseline papers (from my folder) vs new papers, read-tier distribution, queue statuses, the batch that was in progress when the error happened (use modification times and log entries).
- Repair: re-verify the last batch and any suspect note against the sources (identifier, authors, year, venue, every number and table reference); fix, finish, or move back to the queue as "queued" if it cannot be trusted. Never keep an unverified note just to preserve the count. Reconcile ledger, notes and queue so all three agree. Check the registers for rows tied to incomplete notes.
- Audit a random 10% of ALL existing notes (plus every Tier 1 note's key numbers) with a fresh pass that re-opens the sources. Log the error rate in `analysis/11_reading_audit.md`. If the rate exceeds 5%, flag the affected batches for redo in the backlog (do not redo them now).
- Build the NOVELTY INDEX: `PROGRAM/manifests/novelty_index.csv` (DOI, arXiv ID, URL, normalized title, source of the entry) covering every paper already read or in the folder or ledger, so the novelty check for the per-phase quota is fast and reliable. Every later phase updates it.
- Write `analysis/RESUME_STATE_<date>.md`: true counts, discrepancies found, what was repaired, what is flagged.
- If a `PROGRAM/` folder from an earlier version of this program exists (for example an older phase map with different phase numbers), do NOT redo finished phases: map the old phase numbers to the new IDs in `PROGRAM/DECISIONS.md`, mark what is already complete, and update `PHASE_PLAN.md` and `PHASE_STATE.md` accordingly.

0.6 INITIALIZE THE INFRASTRUCTURE
- Create the standard directory layout (section 0.10) without disturbing existing files.
- Initialize or merge: `paper_ledger.csv` (with the full per-paper schema as columns, including type, read_depth and phase_quota), `REFERENCES.md`, `DATASETS.md` (with the QUICK LINKS table header from section 0.9A), `analysis/10_reading_queue.csv`, the three registers, `analysis/06_contradiction_register.md`, `analysis/02_search_log.md` (import any earlier query logs), `ASSUMPTIONS.md`, `PROGRAM/DECISIONS.md`, `PROGRAM/OPEN_QUESTIONS.md`, `PROGRAM/INCIDENTS.md` (log the earlier server error), `PROGRAM/CHANGELOG.md`, `PROGRESS.md`, `PROGRAM/PHASE_STATE.md`, empty `PROGRAM/sota/` and `PROGRAM/phase_papers/` folders with a template file for the quota list, and the `HANDOFF/` files.
- Define and document the file naming and ID conventions (paper IDs, note file names, REF-IDs, dataset IDs, feature IDs, claim IDs), so every later phase uses them consistently.

0.7 BUILD THE PHASE PLAN, THE RECOMMENDED SEQUENCE AND THE RISK REGISTER
- Write `PROGRAM/PHASE_PLAN.md`: for every phase P1 to P20: objective, entry conditions, detailed tasks, quota topics for the 15 new papers, expected output files, acceptance criteria, exit audit, dependencies on earlier phases, and the main risks. Use the phase definitions below as the baseline and refine them with what you learned in Phase P0 (how many papers already exist, which themes are already saturated, what the research tools can actually do, any external deadline I mention). Flag any phase that should be split, merged, dropped or reordered, with reasons.
- RECOMMENDED SEQUENCE (your decision, section 0.1 rule 9): draw the dependency graph, propose the order in which you would run the phases and why (for example why IoT research and BOM can come early: procurement lead time; why meta-fusion design comes after the CCTV, IoT and anomaly designs; where anomaly detection fits best; why the India deployment pathway should start early enough to influence design choices such as languages, power and connectivity assumptions, and standards), give one alternative sequence and its trade-offs, and state the exact first gate proposal. I still authorize every phase.
- Write `PROGRAM/RISK_REGISTER.md`: top risks (research-tool limits, paywalled papers, the 15-paper quota in thin topics, hardware price changes and lead time, external deadlines, fire safety for the later build, life-safety and liability considerations, scope creep, time) with likelihood, impact and mitigation.
- Write `PROGRAM/LEAD_TIME_ITEMS.md`: things that take calendar time (ordering parts, requesting dataset access, applying for registrations, contacting experts, ethics-review processes for a later pilot, deadlines I mention) so I can start them early; propose, do not execute.

0.8 DEFINE THE KEY TECHNICAL QUESTIONS DRAFT (preliminary, no searching)
- From the recovered context only, draft a first list of the technical questions the project depends on (detection quality, false-alarm control, calibration and uncertainty, anomaly and open-set detection, physics validity, generalization across cameras/sites/generators, evaluation leakage, robustness, latency, offline operation, privacy, alert fatigue, RL reward hacking, edge/TinyML feasibility, low-cost sensor reliability, compute budget, hardware budget, fitness for Indian conditions such as languages, power and connectivity, standards and regulation). Save in `analysis/00_key_questions_draft.md`. It will be finalized in Phase P1.

0.9 PHASE P0 EXIT AUDIT
- Verify: the prompt copy and the backup exist and hashes match; the layout exists; ledger, notes, queue and novelty index agree; every created file is non-empty and consistent; `PHASE_STATE.md` is accurate; no existing file was overwritten or deleted (compare against the manifest); no new papers were searched or read; no project code was written or run.
- Write `PROGRAM/reports/PHASE_00_report.md` with all of the above, the chosen folder path, the tool capabilities, the true literature counts, the repair log, the phase plan and recommended sequence summary, the risk register summary, the open questions and the assumptions.

**Outputs of Phase P0.** `PROGRAM/` (master prompt copy, plan, state, decisions, open questions, incidents, changelog, risk register, lead-time items, manifests including the novelty index, backups, reports, gate messages, sota and phase_papers folders), `PROGRAM/ENVIRONMENT_CHECK.md`, `analysis/00_context_recovered.md`, `analysis/RESUME_STATE_<date>.md`, `analysis/00_key_questions_draft.md`, initialized ledgers, registers, queue, `DATASETS.md` and `HANDOFF/` files, `PROGRESS.md`, `ASSUMPTIONS.md`.

**Acceptance criteria.** Prompt saved; folder inventoried and backed up; true literature counts established and the earlier reading audited; novelty index built; infrastructure created without destroying anything; research-tool capabilities verified and documented; phase plan, recommended sequence and risk register written; gate message prepared. Then STOP and ask me for permission for the first phase of your recommended sequence (normally P1), proposing its approach and any changes to the plan.

---

# PHASE P1: BASELINE PAPERS AND SYSTEM MODEL

**Objective.** Read every paper that is already in my folder (the baseline), build a written model of the current system and idea, and finalize the key technical questions that will drive all later searching.

**Entry.** `GO PHASE P1`; Phase P0 complete.

**Quota topics (15 NEW papers, in addition to the baseline reading).** Methodology for designing and evaluating end-to-end safety-critical ML and early-warning systems; recent end-to-end fire/disaster detection and response system papers and surveys (to compare our architecture with the state of the art); system-level reliability, false-alarm and alert-fatigue studies; evaluation methodology for multi-component ML pipelines.

**Tasks.**
1. SOTA scan for end-to-end disaster/fire early-warning systems.
2. Read every baseline paper in my folder through the Reading Engine at Tier 2 or deeper (Tier 1 for the most central ones), skipping those that already have verified full-text notes from Phase P0 reconciliation. Baseline papers do NOT count toward the quota.
3. Read the existing project's code, configs, docs and results (read-only). Build `analysis/00_system_model.md`: architecture, data flow, assumptions, failure surfaces, external dependencies, which parts were designed from which paper, what pre-existing results exist versus what is untested, and the state of each workstream.
4. Write `analysis/01_baseline_papers.md`: a readable overview of the baseline set (themes covered, strongest papers, gaps, contradictions, relevance to each workstream).
5. Finalize `analysis/00_key_questions.md`: the technical questions the project depends on, each with why it matters, what evidence would answer it, and which workstream it belongs to. Tag every baseline paper with the questions it informs. Record initial gaps to guide later searching.
6. Produce a first theme-coverage matrix (themes from Phases P2 and P3 vs papers read so far) so the foundation reading can be balanced.
7. Read the 15+ quota papers and record what each changed in the system model or question list.
8. Update the handoff files.

**Outputs.** Notes in `analysis/03_paper_notes/`, updated ledger/queue/registers/novelty index, `analysis/00_system_model.md`, `analysis/01_baseline_papers.md`, `analysis/00_key_questions.md`, theme-coverage matrix, SOTA scan, quota list, report.

**Acceptance.** Every baseline paper has a verified note or an explicit "unreadable/fetch-failed" status with reason; system model complete; questions finalized; quota met; audit of 10% of new notes passes (error rate under 5%).

**Exit.** Quota audit, audit, report, gate message, STOP.

---

# PHASE P2: LITERATURE FOUNDATION I (core methods, CCTV/fire, evaluation, robustness, uncertainty)

**Objective.** Build the first half of the foundation set of NEW papers (not in my folder, not already in the ledger). Together Phases P2 and P3 must reach at least 250 and up to 400 verified new papers in total (counting the new papers already read before the interruption); this phase aims for roughly 40 to 60% of that. These papers also satisfy this phase's quota.

**Entry.** `GO PHASE P2`; Phase P1 complete.

**Theme scope.**
- Core method papers for the main techniques used, and foundational/seminal papers.
- Fire, smoke and wildfire detection; CCTV and surveillance analytics; disaster response; early-warning systems (recent state of the art, last 2 to 3 years prioritized, including preprints).
- Surveys and systematic reviews (mine their reference lists).
- Failure analysis, negative results, limitations and critique papers.
- Robustness, adversarial, distribution-shift, corruption, edge-case and stress-test papers.
- Evaluation and benchmark papers, including metric, leakage and protocol critiques.
- Uncertainty, calibration, conformal prediction, selective prediction, out-of-distribution detection.
- Efficiency, latency and deployment papers for vision (edge, compression, streaming).

**Tasks.** SOTA scan for fire/smoke/CCTV detection and for the evaluation and robustness themes. Run the full search standard (section 0.8), seed and prioritize the reading queue, then run the batch cycle until the phase target is reached, balancing themes (no theme above about 25% of the whole foundation set unless the project genuinely depends on it). Keep `analysis/02_search_log.md` complete (every query and source). Write interim syntheses every 5 batches. Maintain the claims, equations and hyperparameter registers, the citation graph, the contradiction register and the novelty index. Update the handoff files.

**Outputs.** Notes, ledger, queue, registers, search log, interim syntheses, SOTA scan, quota list, `PROGRESS.md` counts, report with theme distribution and tier distribution.

**Acceptance.** Phase target count reached or honestly reported (and the quota of 15 is exceeded by construction); at least 60% at Tier 2 or deeper; audit error rate under 5%; theme distribution documented against the plan.

**Exit.** Quota audit, audit, report, gate message (including how far toward 250 we are and what Phase P3 should emphasize), STOP.

---

# PHASE P3: LITERATURE FOUNDATION II (physics, media forensics, alerting, RL, IoT, anomaly detection basics, safety, adjacent)

**Objective.** Complete the foundation set to at least 250 and up to 400 verified NEW papers in total.

**Entry.** `GO PHASE P3`; Phase P2 complete.

**Theme scope.**
- Physics and hybrid modeling: fire science and combustion, plume and flame theory, radiative transfer, smoke optics and camera radiometry, fluid dynamics, sensor physics, physics-informed and physics-guided machine learning, scientific ML, PINN failure modes.
- Media forensics, deepfake detection, provenance (C2PA and watermarking), misinformation and crisis informatics, social-media degradation, adversarial robustness of detectors.
- Alerting and networks: Cell Broadcast and public warning systems (including India), CAP, mesh and short-range radio (ESP-NOW, BLE, LoRa, Wi-Fi mesh, Zigbee), geo-fencing without IP, alert fatigue, secure alerting.
- Reinforcement learning for emergency response, evacuation and resource allocation; safe and robust RL; deep-RL evaluation methodology; vectorized and GPU-accelerated environments.
- IoT and embedded: wireless sensor networks for fire detection, multi-sensor fire detection and false-alarm suppression, low-cost sensor characterization, TinyML on microcontrollers, energy and reliability engineering, secure embedded messaging, low-cost embedded vision.
- Anomaly detection basics (the deep dive is Phases P9 and P10): surveys and seminal papers for video anomaly detection, time-series anomaly detection, out-of-distribution detection, and anomaly-detection evaluation critiques.
- Safety, reliability, bias/fairness, privacy and security papers.
- Adjacent-field papers whose techniques transfer.

**Tasks.** SOTA scan for physics-informed ML, media forensics, alerting, RL and TinyML themes. Same reading cycle as Phase P2, with the distribution guard applied to the combined set; re-prioritize using the Phase P2 interim syntheses and the gap map; if relevance runs thin, widen to adjacent fields rather than padding. Report the exact count if 250 cannot honestly be reached. Update the handoff files.

**Outputs.** As Phase P2, plus a final foundation-set distribution table (theme x tier x workstream), `REFERENCES.md` grouped by theme with a top-30 must-read list and reasons.

**Acceptance.** 250 to 400 verified new papers (or an honest shortfall report with reasons); at least 60% at Tier 2 or deeper; audit error rate under 5%.

**Exit.** Quota audit, audit, report, gate message, STOP.

---

# PHASE P4: SYNTHESIS

**Objective.** Turn the whole literature (baseline plus new) into usable knowledge that drives design.

**Entry.** `GO PHASE P4`; Phase P3 complete.

**Quota topics (15 NEW papers).** Papers chosen to resolve the contradictions and fill the gaps that the synthesis itself exposes; meta-research and critique papers about evaluation practice in the relevant fields; recent papers that challenge the consensus you are about to write down.

**Tasks.**
1. SOTA scan of the consensus positions you are about to record (check that they are still current).
2. `analysis/04_synthesis.md`: cluster papers by theme and by project component; consensus vs disagreement map; techniques the field shows work better than what we use (evidence strength and transferability); gaps (what we plan that nothing validates; what the field validated that we do not plan).
3. Finalize `analysis/06_contradiction_register.md` with the studies that could resolve each important contradiction in the build phase.
4. `analysis/05_failure_mode_catalogue.md`: known failure modes, attack and stress patterns, leakage patterns, evaluation mistakes, numerical issues, reproducibility traps, embedded and sensor failure modes, anomaly-detection pitfalls, each linked to supporting papers (feeds the robustness phase).
5. "What would change our design": 10 to 20 concrete design changes the literature argues for, ranked, each with the evidence and the workstream it affects.
6. Per-workstream briefing documents (`ws1_physics/` to `ws8_anomaly/` each get `literature_brief.md`: the most relevant papers, key claims with references, open questions) so later phases start from curated knowledge.
7. Update the key-questions file with answers found, answers still open, and new questions.
8. Read the 15+ quota papers and record what they changed.
9. Full ledger and reading audit: re-verify a random 10% of the entire ledger, run the traceability check (every number and claim in the synthesis links to a note), log the rate.
10. Update the handoff files.

**Outputs.** The files above, plus SOTA scan, quota list and the audit log.

**Acceptance.** Every claim in the synthesis traces to a note with a table/equation/page reference; contradictions and gaps documented; design-change list ranked; quota met.

**Exit.** Quota audit, audit, report, gate message (with the top design changes for my decision), STOP.

---

# PHASE P5: DATASET REGISTRY AND COMPUTE BUDGET PLAN

**Objective.** Find and verify the datasets the project can use and fix the Kaggle compute plan for the later build.

**Entry.** `GO PHASE P5`; Phase P3 complete (P4 helpful).

**Quota topics (15 NEW papers).** The introducing papers of the datasets and benchmarks you evaluate for use (dataset and benchmark papers count when read at Tier 3 or deeper and genuinely new), dataset-documentation and benchmark-critique papers (label noise, leakage, duplicates, bias, license practice), and compute-efficient training papers relevant to the Kaggle budget.

**Tasks.**
1. SOTA scan of benchmarks and leaderboards per workstream (which datasets are the community standard, which are criticized).
2. Build `DATASETS.md`: as many relevant, REAL, accessible datasets as you can find across all workstreams: fire and smoke images and video; thermal and IR; CCTV and surveillance; video anomaly detection benchmarks; deepfake and manipulated-media sets (images, video, audio); misinformation and disaster-social-media sets (crisis-tweet and multimodal crisis collections, including multilingual and Indian-language sets if they exist); audio; multi-sensor fire and nuisance-source sensor datasets for the IoT workstream; time-series and sensor-fault anomaly datasets and benchmarks (with the benchmark flaws the literature reports); network and intrusion/spoofing traces; bot and coordinated-behavior datasets; fire-spread and wildfire data (including data covering Indian regions where available); satellite and remote-sensing imagery and active-fire products; weather and reanalysis; terrain and land cover; physics and combustion experimental data; RL environments and evacuation/crowd data; benchmarks. Note explicitly how well each dataset represents Indian conditions (scenes, climate, camera quality, building types, languages) and where there is a domain gap.
3. For EACH dataset record: name, version, workstream(s), modality, size, number of samples and classes, annotation type and quality; direct source link (Kaggle / Zenodo / HuggingFace / GitHub / institutional page / government portal) and the introducing paper (DOI / arXiv); license and usage restrictions; access method (open / registration / request form / paywalled); known issues (label noise, duplicates, bias in geography/weather/camera/sensor, leakage risks, domain gap such as lab vs real, foreign vs Indian conditions, expensive vs cheap sensors, anomaly-benchmark flaws); recommended split protocol (group by video / camera / site / generator / session / time) and how it would fit Kaggle storage; verification status ("link checked on <date>, resolves yes/no"; "stats verified from official documentation; inspection deferred to the build phase"). Facts (size, classes, license) come only from the official source. Do NOT list a dataset you could not verify exists. Do not download datasets. Fill the QUICK LINKS table and the selected-datasets summary exactly as defined in section 0.9A, including the COST column and the free-only rule, and give the final count of datasets by cost category in the phase report.
4. Group by workstream, mark which are directly on Kaggle, add the download method for each (as text, for the later build), a dataset-to-model mapping matrix, and cross-dataset evaluation plans (which datasets are train-only, which are held out for generalization tests). Flag datasets that need registration or request forms so I can start those early.
5. Build `KAGGLE_BUDGET.md` as a PLAN: verified current Kaggle limits with links and access dates; a planning table of GPU hours (total about 30 including at least 15% reserve) across WS1, WS2, WS4, WS5, WS7 TinyML, WS8 anomaly detection and the fusion layer, using the hyperparameter register for first estimates (all labeled estimates); session-scheduling strategy, checkpoint/resume strategy, what would run on CPU, efficiency techniques the literature supports; seed-count policy per experiment; prioritized cut-list.
6. Read the 15+ quota papers and record what they changed.
7. Audit: re-check 10% of dataset entries (links, stats, licenses) from the sources.
8. Update the handoff files.

**Outputs.** `DATASETS.md`, `KAGGLE_BUDGET.md`, dataset-verification log, SOTA scan, quota list, report.

**Acceptance.** Only verified datasets listed; only free datasets selected; budget plan sums to about 30 hours with reserve; limits sourced; quota met.

**Exit.** Quota audit, audit, report, gate message (including which datasets need early access requests), STOP.

---

# PHASE P6: WS7a, IoT RESEARCH, COMPONENT SELECTION, BOM AND SAFETY PROTOCOL

**Objective.** Decide, with evidence, what hardware the prototype should use under INR 2000, produce a verified shopping list so I can order parts early, and write the safety protocol for the later build. No building.

**Entry.** `GO PHASE P6`; Phase P3 complete (P5 helpful).

**Quota topics (15 NEW papers; aim for about 30).** Wireless-sensor-network and IoT fire detection; multi-sensor fusion and false-alarm suppression; low-cost smoke, gas, flame and temperature sensor characterization; rate-of-rise and fixed-temperature logic; TinyML on microcontrollers; ESP-NOW, BLE, LoRa and Wi-Fi mesh measured performance; embedded vision on low-cost modules; lightweight message authentication on microcontrollers; energy and reliability engineering; on-device anomaly and sensor-fault detection; low-cost sensing deployments in developing regions (heat, dust, humidity, power cuts).

**Tasks.**
1. SOTA scan of low-cost multi-sensor fire detection and TinyML fire detection (published systems, their sensors, costs and reported results with conditions).
2. Research through the Reading Engine, adding the datasheets and standards relied upon to the ledger (they do not count toward the quota).
3. Find the physics link: which physics relations could run on the device (for example rate-of-rise, smoke-concentration growth rate, ceiling-jet transport-delay logic, sensor time-constant compensation) and what the literature says about their usefulness with cheap sensors. Treat any new on-device rule as a hypothesis.
4. Find open multi-sensor fire and nuisance-source datasets and published low-cost fire-detection prototypes with reported results, as baselines with their conditions stated (add datasets to `DATASETS.md` under the rules of section 0.9A).
5. Component selection and budget: evaluate candidates (search directions, not decisions): ESP32-class boards; low-cost camera modules for ESP32-class boards; smoke/gas modules; flame sensors; temperature/humidity/pressure sensors; low-cost IR or thermal options (check whether any fits; if not, give the closest affordable alternative, for example an IR thermopile point sensor instead of a thermal array); particulate sensors; buzzer, bright LED strobe or siren output; low-power radio modules; power sources and regulators; breadboard, wires, protoboard, enclosure materials. For every part: purpose, why chosen over alternatives (evidence from papers and datasheets), datasheet-verified specs including operating temperature and humidity range relevant to Indian conditions, live Indian seller listing URL, price with GST and shipping, date checked, a second source, availability and failure risk. Totals are recomputed from verified listings, never estimated. Produce `ws7_iot/BOM.md` and `HARDWARE_BUDGET.md` with total, contingency, a prioritized cut-list if over INR 2000, and "assumed owned" items listed separately. Decide the node architecture (number of nodes, trade-off between node count and sensor quality) from evidence.
6. `ws7_iot/SAFETY.md` by the safety reviewer: the safe-stimulus test protocol for the later build, ventilation, supervision, extinguisher/water at hand, low-voltage power only, protected power sources, no unattended heated-source testing, hazard list, stop conditions, based on verified guidance.
7. Preliminary design in `ws7_iot/design.md`: sensing layer, on-device logic (including a lightweight anomaly and sensor-fault layer to be specified in P10), alerting (local access point or ESP-NOW/mesh, local dashboard with no internet), signed messages with replay protection, offline mode, power design (including behavior during power cuts), calibration procedure (as a protocol), and the acceptance criteria for the later prototype (cost at or below INR 2000 with verified listings; demonstration fully offline; a false-alarm-suppression comparison with repeated trials; alert latency and radio reach measured; signed-message spoof rejection demonstrated; all claims from our own logs).
8. Prepare the shopping list for me (`ws7_iot/SHOPPING_LIST.md`): exact items, quantities, links, prices, dates, alternatives. You do not order anything.
9. Read the 15+ quota papers and record what they changed in the component choices and design.
10. Update the handoff files.

**Outputs.** `ws7_iot/literature_map.md`, `ws7_iot/BOM.md`, `HARDWARE_BUDGET.md`, `ws7_iot/SAFETY.md`, `ws7_iot/design.md`, `ws7_iot/SHOPPING_LIST.md`, ledger additions, SOTA scan, quota list, report.

**Acceptance.** Every price and spec has a verified source and date; total at or below INR 2000 including contingency or a clear cut-list; safety protocol complete; quota met.

**Exit.** Quota audit, audit (re-check prices on a sample of listings), report, gate message, STOP. I can order parts while later research phases proceed.

---

# PHASE P7: WS1a, PHYSICS MODEL SET AND DERIVATIONS ON PAPER

**Objective.** Decide which physics models the project uses (count N by evidence, not fixed at six), derive them fully on paper, cross-check them against the literature, and write the plan for validating them later.

**Entry.** `GO PHASE P7`; Phases P3 and P5 complete.

**Quota topics (15 NEW papers; aim for about 30).** Fire plume, flame, smoke transport and fire-growth experiments and correlations; radiative transfer and smoke optics relevant to cameras; thermal-camera radiometry; flame flicker and puffing frequency studies; wildland and structure fire spread models; sensor physics (detector response, ceiling jet); physics-informed ML methods and PINN failure-mode and mitigation papers; physics-guided features for vision.

**Tasks.**
1. SOTA scan for physics-informed and physics-guided fire modeling and for fire-growth and smoke-transport modeling (published validation cases and numbers).
2. Recover the originally identified models (from the Phase P0 context) and list them explicitly. Using the literature, build a candidate map of phenomena relevant to fire/smoke/disaster detection from CCTV and low-cost sensors (plume dynamics, flame geometry and flicker, smoke optical properties and camera radiometry, heat transfer and thermal signatures, smoke/gas transport to a sensor, fire growth, spread dynamics, sensor response physics, and others the literature supports). Add candidates beyond the original set where evidence supports.
3. Two-layer model set: established models plus robustified extensions.
(a) LAYER 1, ESTABLISHED MODELS (Class A). First build `ws1_physics/established_formula_inventory.md`: every established relation and model from the literature that is relevant to fire/smoke/disaster detection from CCTV and low-cost sensors, including the originally identified models recovered from the project context. For each: statement, symbols and units, source and equation number, regime of validity, the assumptions it needs, and its KNOWN WEAKNESSES: where it fails or is poorly supported (papers' stated limitations, conflicting results, regimes outside the experiments it was fitted on, assumptions our setting violates such as non-ideal environments, low-cost sensor lag and noise, camera measurement effects). These established models are part of the model set; they are the baselines and the parents of everything new.
(b) LAYER 2, ROBUSTIFIED EXTENSIONS (Class B or C). New models are derived ON THE BASIS of Layer 1 models, each aimed at a documented weakness. "Robustify" means concrete things, for example: extending the regime of validity; adding explicit uncertainty and sensitivity terms; including sensor or camera response (time constants, noise, saturation, measurement physics) so the model predicts what is actually observed; handling missing or poorly known parameters through priors or dimensionless formulations; combining several established relations consistently; correcting a known bias with a derived term. Each extension must declare its parent(s), the weakness it targets and why the derivation addresses it. Do not invent extensions without a documented weakness; prefer honest, modest extensions over exotic ones.
(c) LINEAGE TABLE in `ws1_physics/formula_class_table.md`: one row per model: ID, class (A, B or C), parent model(s), weakness addressed, derivation reference, sources of every building block, and validation status. Every extension must show on paper that it REDUCES to its parent in the appropriate limit.
(d) ADMISSION. Classify every candidate as Class A, B or C (rule 20). Layer 1 models are admitted if they are relevant, usable by the system and have verified sources. A Layer 2 model is admitted only if: (1) built from verified Class A building blocks, each cited with equation number, with the full derivation shown; (2) it yields a measurable quantity or constraint usable by the system (feature, prior, consistency check, simulator, residual loss, anomaly-residual signal); (3) it adds non-redundant information over its parent (analyze on paper); (4) a validation plan exists naming real published experimental data it can be compared against, with the error level that would count as acceptable, and a pre-registered build-phase measurement gate that compares it against its parent (the extension must earn its place; if it does not beat or match its parent where the weakness matters, the parent is used). Extensions with no realistic route to validation are demoted to documentation only.
(e) Additional requirements for every Layer 2 model: independent re-derivation by a second agent or fresh pass with discrepancies resolved; hand-checked dimensional consistency and limiting cases; a plain statement of the one assumption or coupling that makes it new and what observation would falsify it; a novelty search log in `ws1_physics/novelty_log.md` (queries, indexes, dates, closest papers found, how ours differs, rule 21); a design in which the system still works if the extension is switched off or wrong (it enters as a feature, prior or consistency check with its own uncertainty, never as a hard dependency until validated, falling back to its parent); a recommendation that a qualified fire-science or heat-transfer expert reviews the derivation before any external use.
(f) Record admitted / demoted / rejected with reasons and the class in `ws1_physics/model_set_decision.md`, including N (counting Layer 1 and Layer 2 models separately) and why. Keep the set as small as the evidence allows and as large as it usefully needs.
4. Search directions (verify against real sources; these are not citations): axisymmetric buoyant plume theory and flame-height correlations; heat release rate and fire-growth models; smoke production, transport, zone and field models; radiative and convective heat transfer, view factors, Stefan-Boltzmann relations; pyrolysis and Arrhenius-type kinetics; flame spread including wildland spread-rate models, elliptical/Huygens propagation and cellular-automata formulations; flame flicker/puffing frequency scaling with source size; light extinction and scattering by smoke and what a camera measures; thermal-camera radiometry (emissivity, atmospheric attenuation); sensor physics (smoke, gas, temperature and flame sensors, rate-of-rise behavior, ceiling-jet and plume transport time to a detector); dimensionless groups.
5. For EACH admitted model, write a derivation document (Layer 1 models: the derivation outline and the source's assumptions; Layer 2 models: the complete derivation): (a) derive from first principles step by step in full: assumptions, conservation laws, constitutive relations, boundary and initial conditions, nondimensionalization, Buckingham Pi, scaling arguments, limiting cases; every algebraic step shown; (b) cross-check against literature, citing a verified source for every non-trivial relation and logging it in the equations register; (c) perform dimensional-consistency and limiting-case checks by hand and document them, and write a verification checklist for the build phase (expected units, signs, limits, known analytic solutions); (d) write the validation plan: which published experimental data or canonical benchmark cases the model should be compared against later, with sources and what error level counts as acceptable per the literature; (e) decide how the model should enter the learning system (hard constraint, soft PINN residual, feature generator, simulator for synthetic data, or prior) and which models could run on the IoT device, justified by physics-informed ML literature and PINN failure modes (stiffness, loss imbalance, spectral bias, causality violations, poor extrapolation, non-identifiability) with only literature-supported mitigations; (f) analyze uncertainty on paper: sensitivity of the output to each parameter, identifiability, noise propagation, regime of validity, and what the model must NOT be used for.
6. Plan the later ablations (single-model, leave-one-out, greedy forward/backward selection, grouped by phenomenon family; all pairs only if N is small; every Layer 2 model against its Layer 1 parent).
7. Add any physics experimental datasets found to `DATASETS.md` under the rules of section 0.9A.
8. Read the 15+ quota papers and record what they changed in the model set and derivations.
9. Update the handoff files.

**Outputs.** `ws1_physics/established_formula_inventory.md`, `ws1_physics/model_set_decision.md`, `ws1_physics/formula_class_table.md` (lineage table), `ws1_physics/novelty_log.md`, `ws1_physics/derivations/` (one document per admitted model; Layer 2 documents show the reduction to the parent), `ws1_physics/validation_plan.md`, `ws1_physics/verification_checklists.md`, additions to the equations register, SOTA scan, quota list, report.

**Acceptance.** Every admitted model has a full derivation (Layer 1: the derivation outline and the source's assumptions; Layer 2: the complete derivation), a verified source for every non-trivial relation, hand-checked dimensional consistency and limits, a validation plan naming real published data (or an honest statement that none exists), and a documented regime of validity. Every Layer 2 model has a documented parent, a targeted weakness, and a derivation that reduces to the parent in the stated limit. Quota met.

**Exit.** Quota audit, audit, report, gate message, STOP.

---

# PHASE P8: WS4, CCTV-BASED DETECTION: RESEARCH, MODEL SELECTION AND PROTOCOL

**Objective.** Select, with evidence, the CCTV fire/smoke/disaster detection approach and write the evaluation protocol and plan, so the later build is straightforward and honest.

**Entry.** `GO PHASE P8`; Phase P5 complete (P7 soft).

**Quota topics (15 NEW papers; aim for about 40).** Recent fire/smoke detection with CNNs, YOLO-family, transformers, video transformers, temporal and open-vocabulary models; early and small-smoke detection; night/IR/thermal fire detection; steam-vs-smoke and false-positive reduction; leakage-safe evaluation for surveillance video; compression and low-resolution robustness (typical of low-cost CCTV); edge deployment (quantization, distillation, cascades); camera tamper and adversarial attacks; privacy in CCTV analytics; self-supervised/semi-supervised and synthetic data for fire video.

**Tasks.**
1. SOTA scan: best published fire/smoke detectors and benchmarks with their protocols, and known flaws (for example near-duplicate frames across splits, single-site data).
2. Literature map (`ws4_cctv/literature_map.md`): classical (color, motion, flicker, frequency-domain, background subtraction) vs deep learning (CNN, YOLO-family, transformers, video transformers, temporal models, anomaly detection, foundation and open-vocabulary detectors); early-stage and small-smoke detection as the explicit hard case.
3. CCTV-specific failure taxonomy (`ws4_cctv/failure_taxonomy.md`): night and IR cameras, low light, glare, rain, fog, dust and haze, steam vs smoke, sunsets, red clothing, lights and reflections, camera shake, compression, low resolution, occlusion, domain shift between cameras and sites; for each, what the literature says and how a failure-case test set should be assembled later.
4. Acceptance criteria, decided now: the operating point (maximum tolerable false alarms per camera-day, maximum time-to-detection) and what cross-site performance would be acceptable, grounded in the literature and in alarm-practice standards where they exist.
5. Model selection justified by evidence (`ws4_cctv/model_selection.md`): alternatives, evidence, expected budget fit; a shortlist with the published baselines to reproduce first.
6. Pre-registered evaluation protocol (`ws4_cctv/evaluation_protocol.md`): leakage-safe splits grouped by video/camera/site; metrics beyond accuracy (time-to-detection, false alarms per camera-day, precision-recall at the operating point, calibration); confidence intervals over seeds; classical vs deep vs physics-informed variants (using Phase P7 relations such as plume growth and flicker frequency ranges as features, priors or consistency checks).
7. Edge deployment plan: quantization, distillation, early-exit, cascades; the latency-vs-accuracy questions to answer later; the low-cost camera module in the IoT build.
8. Label-scarcity strategies (active learning, self-supervised, semi-supervised) and synthetic data with sim-to-real gap evidence: what the literature supports for our case.
9. Privacy (face blurring, on-device processing) and adversarial/tamper attacks on cameras (blinding, replayed-video spoofing) with defenses, as design requirements.
10. Interfaces with the deepfake workstream (is the stream real or replayed?), alerting (detection-to-alert handoff, confirmation windows, de-duplication), IoT sensors and anomaly detection (the supervised detector's blind spots are the anomaly layer's target).
11. Add any CCTV, fire and smoke datasets found to `DATASETS.md` under the rules of section 0.9A.
12. Read the 15+ quota papers and record what they changed.
13. Update the handoff files.

**Outputs.** `ws4_cctv/` (literature map, failure taxonomy, model selection, evaluation protocol, plan), SOTA scan with the "SOTA targets and protocol plan" section, quota list, report.

**Acceptance.** Model choice justified by cited evidence; protocol complete and leakage-safe; acceptance criteria written before any build; negative evidence and criticisms documented; quota met.

**Exit.** Quota audit, audit, report, gate message, STOP.

---

# PHASE P9: WS8a, ANOMALY DETECTION: RESEARCH, SCOPE, EVALUATION PROTOCOL AND DESIGN

**Objective.** Decide exactly where anomaly detection belongs in this project, learn what the state of the art really is (including which published numbers cannot be trusted), pre-register a rigorous evaluation protocol, and design the anomaly layer.

**Entry.** `GO PHASE P9`; Phases P4 and P5 complete (P8 and P6 soft).

**Why this phase matters.** A supervised fire detector only knows the fire it was trained on. Anomaly detection covers what it does not know: unseen hazard types and unusual scenes, camera failure or tampering, sensor faults and drift, inputs outside the training distribution, spoofed or replayed alerts, and coordinated or sudden misinformation surges. It can also reduce false alarms by recognizing nuisance sources as "normal for this site". It must be evaluated far more carefully than most published work.

**Quota topics (at least 15 NEW papers; aim for about 40 across P9 and P10, with P9 carrying most).**
- Video anomaly detection: unsupervised and weakly supervised methods, reconstruction/prediction-based, memory-augmented, one-class, flow-based, diffusion-based, self-supervised and transformation-based, pretrained-feature and nearest-neighbor approaches, vision-language-model-based detection, optical-flow and pose-based approaches, surveys and recent leaderboard papers.
- Multivariate time-series and sensor anomaly detection: statistical methods (z-score, EWMA, CUSUM, ARIMA residuals), isolation-based, density-based, matrix-profile, deep reconstruction/prediction, transformer and graph-based, contrastive, foundation models for time series, change-point detection, sensor-fault vs real-event discrimination.
- Out-of-distribution detection and model monitoring: confidence-based, distance-based (Mahalanobis, nearest-neighbor on features), energy-based, ensemble and Bayesian methods, open-set recognition, drift detection.
- Uncertainty and thresholding for anomaly scores: extreme value theory, conformal anomaly detection, calibration of anomaly scores, false-alarm-rate control.
- Evaluation critiques: lenient or inflated metrics (for example point-adjust style protocols), thresholds tuned on test data, mislabeled or trivial benchmarks, event-based and range-based metrics, delay-aware metrics, anomaly-injection pitfalls, realistic anomaly rates, cross-site evaluation.
- Physics-residual-based and model-based anomaly detection, anomaly detection in cyber-physical systems.
- Network and alerting anomalies: intrusion, spoofing, replay and denial-of-service detection in IoT and mesh networks; node-misbehavior detection.
- Social-media anomalies: burst and event detection, coordinated inauthentic behavior, bot detection, with privacy-preserving approaches.
- Data-quality anomalies: label-noise and outlier detection in training data, near-duplicate and corrupted-frame detection.
- Edge anomaly detection: lightweight detectors for microcontrollers, TinyML autoencoders and statistical detectors with reported memory and latency.

**Tasks.**
1. SOTA scan: write `PROGRAM/sota/P9_sota_scan.md` for each anomaly family (video, time series, OOD, network, social, edge): the best published methods and numbers with exact benchmark, split, metric and protocol; the benchmark and metric criticisms; the realistic bar for a build under our limits. Include a "what the literature says about simple baselines" section (how often simple methods match deep ones under strict protocols).
2. Scope decision (`ws8_anomaly/scope_decision.md`): decide, with evidence, which anomaly families are in scope and in what priority. For each: what counts as an anomaly in this project (concrete examples), what data exists or could be collected, what the detector would trigger (alert, abstain, escalate, health warning), the cost of a miss vs a false alarm, and why it is or is not worth the later Kaggle and hardware budget. Define the relation to the supervised detectors: when anomaly detection should lead, when it should only support, and what open-set behavior to expect. Candidate families: (a) video: unusual events, unknown hazards, camera failure, tampering; (b) sensor time series: unusual readings, sensor faults and drift vs real events; (c) model health: OOD inputs to the vision and fusion models, drift monitoring; (d) physics consistency: residuals of the admitted physics models as anomaly scores; (e) alert/network: spoofing, replay, DoS, node misbehavior; (f) social media: surges and coordinated amplification; (g) data quality in our own datasets.
3. Literature map (`ws8_anomaly/literature_map.md`) by family: methods, assumptions, data needs, compute cost, edge feasibility, known failure modes, evidence strength, with links into the ledger.
4. Evaluation critique and protocol (`ws8_anomaly/evaluation_protocol.md`), PRE-REGISTERED now, before any build: metrics (event-level detection with detection delay, false alarms per camera-day or sensor-day, precision-recall and AUC variants, range-based or delay-aware scores, calibration of scores, performance at a fixed false-alarm budget); splits (time-ordered and site-grouped, never random frame-level splits, no leakage of normal-period statistics into test); threshold selection rules (on validation or by a documented statistical rule, never on test); anomaly-rate realism; synthetic anomaly injection rules (clearly labeled SYNTHETIC, varied in type and magnitude, never the only evidence, with the literature's warnings about injection bias); the strict-versus-lenient scoring policy (strict scores are the primary numbers; a lenient protocol may be reported only to compare with published work, labeled, with the strict score beside it); seeds and confidence intervals; ablations; mandatory simple baselines to run FIRST (for example statistical thresholds, EWMA/CUSUM, nearest-neighbor on pretrained features, isolation forest) so we can tell whether complexity earns its keep; stress tests (new camera or site, lighting and weather change, sensor aging, nuisance sources, gradual drift, adversarial and tamper cases); acceptance criteria per family (what false-alarm rate and detection delay count as success).
5. Datasets for anomaly detection: update `DATASETS.md` (via backup and changelog, under the rules of section 0.9A) with verified free anomaly benchmarks and the data we will need (normal-only footage from CCTV sites, our own IoT normal-operation logs, public multivariate and sensor-fault datasets, network traces, social-media burst datasets), noting each dataset's known flaws; propose how to collect normal-only data for our own sites and sensors safely in the later build; define the "normal" reference data policy (how much, how often it must be refreshed, how seasonal and daily patterns are handled).
6. Design (`ws8_anomaly/design.md`): the architecture of the anomaly layer: per-family detectors; feature sources (pretrained vision features, physics residuals, sensor features); score normalization and calibration across detectors; thresholding with false-alarm control (extreme value theory or conformal approaches if supported by the evidence); how anomaly scores feed the meta-fusion layer (P14) and the alert decision policy (P12): abstain, escalate to human review, lower or raise alert tier, trigger a "sensor health" warning; alert-fatigue controls; drift monitoring and refresh policy; the edge-feasible subset for the ESP32-class node with literature-based memory and latency expectations; privacy rules (no profiling of individuals or accounts); failure modes of the anomaly layer itself and how it degrades.
7. Planning: planning-level GPU-hour estimate per anticipated experiment for the later build, Kaggle fit, hardware-free vs hardware-dependent parts, the order of work, and the cut-list.
8. Read the 15+ quota papers (more is expected) and record, per family, what each changed in the scope, protocol or design.
9. Update the handoff files.

**Outputs.** `ws8_anomaly/scope_decision.md`, `ws8_anomaly/literature_map.md`, `ws8_anomaly/evaluation_protocol.md` (pre-registered), `ws8_anomaly/design.md`, `ws8_anomaly/build_plan.md`, `ws8_anomaly/literature_brief.md`, dataset additions, SOTA scan, quota list, report.

**Acceptance.** Scope decided with reasons; every published number used as a target comes with its protocol and criticisms; the protocol is complete and pre-registered; simple baselines are planned first; the design covers integration with fusion and alerting; quota met.

**Exit.** Quota audit, audit, report, gate message (with decisions I must make about scope), STOP.

---

# PHASE P10: WS8b, ANOMALY DETECTION: IMPLEMENTATION SPECIFICATION AND EXPERIMENT PLAN

**Objective.** Turn the P9 design into a complete, ready-to-build specification per anomaly family, with every choice grounded in the best available evidence. Nothing is implemented, run or measured.

**Entry.** `GO PHASE P10`; Phase P9 complete; Phase P8 complete or consciously skipped.

**Quota topics (15 NEW papers).** Implementation-level details and SOTA recipes for the families chosen in P9 (method papers with training and thresholding recipes, strong reimplementation and reproducibility studies, ablation studies), efficient and edge anomaly detection, anomaly-score calibration and false-alarm control, and papers needed to settle open design questions from P9. Papers read in P9 do not count again.

**Tasks.**
1. SOTA scan update for the exact methods in the spec (check for newer results since P9) and the list of published baselines to reproduce first, with the numbers they should reach under their own protocols.
2. For each in-scope anomaly family, write a build specification in `ws8_anomaly/spec/`: the method and why (evidence), inputs and outputs, data needed and splits, normal-reference data policy, features, model architecture and hyperparameter defaults with sources, training and thresholding recipe, score calibration, strict metrics and the exact evaluation procedure from the P9 protocol, simple baselines to implement first, ablations, stress tests, acceptance criteria, known pitfalls from the failure-mode catalogue, planning-level GPU hours and Kaggle fit, verification checklist.
3. Edge specification: the lightweight detector(s) for the ESP32-class node (for example EWMA/CUSUM plus a small model) with literature-based memory, latency and accuracy-loss expectations and the measurements to take later.
4. Integration specification: the interfaces and data formats that deliver anomaly scores and health flags to the meta-fusion layer (P14), the alert decision policy (P12) and the dashboard (P13); expected end-to-end behavior (abstain, escalate, health warning) described as scenarios; alert-fatigue budget logic.
5. Failure analysis on paper (`ws8_anomaly/failure_analysis.md`): what the anomaly layer is expected to miss or falsely flag, which anomalies are indistinguishable from benign changes, privacy and misuse risks, with citations.
6. SOTA targets and protocol plan: the published numbers to be met, the protocol differences to watch, and what a fair comparison needs.
7. Read the 15+ quota papers and record what they changed.
8. Update the handoff files (this phase is the main input for the later anomaly-detection build prompt).

**Outputs.** `ws8_anomaly/spec/` (one document per family), edge and integration specifications, failure analysis, SOTA scan with the targets section, quota list, report.

**Acceptance.** Each spec is complete enough that someone could build it without further research; every default has a source; strict metrics are primary; quota met.

**Exit.** Quota audit, audit, report, gate message, STOP.

---

# PHASE P11: WS2, DEEPFAKE AND MISINFORMATION: RESEARCH AND DESIGN

**Objective.** Design the pipeline that decides how much to trust social-media-sourced disaster information, with evidence for every component.

**Entry.** `GO PHASE P11`; Phase P5 complete (P7 soft).

**Quota topics (15 NEW papers; aim for about 40).** AI-generated image/video/audio detection (GAN, diffusion, face-swap); frequency and spectral artifact detectors; foundation-model-feature and universal detectors; cross-generator generalization; provenance and watermarking (C2PA, invisible watermarks) and their attacks; out-of-context media and reverse-search methods; recompression and social-platform degradation studies; adversarial attacks and defenses for forensic detectors; crisis informatics and multi-source corroboration, including multilingual and Indian-language settings; misinformation source credibility; fairness and calibration of detectors.

**Tasks.**
1. SOTA scan for synthetic-media detection with cross-generator and degraded-media protocols.
2. Literature map and detection coverage: detection of AI-generated and manipulated images, video and audio (GAN, diffusion, face-swap; frequency-domain and spectral artifacts; spatio-temporal inconsistencies; physiological signals; foundation-model-feature and CLIP-style universal detectors); watermark and provenance approaches (C2PA, content credentials, invisible watermarks) and their limits; AI-generated disaster and fire imagery specifically (what is known, what is not); out-of-context and recycled media (reverse image search, near-duplicate and perceptual hashing, temporal and geolocation consistency, shadow/sun-angle/weather consistency, metadata/EXIF and its limits, caption-vs-image consistency, keyframe matching).
3. Physics-based plausibility checks using the admitted physics models (growth rate, flicker frequency range, plume rise, smoke opacity vs distance): search whether this is validated; if not, record it as "novel hypothesis, unvalidated" and write the study design that would test it later (real fire videos vs synthetic/AI-generated).
4. Social-media degradation: platform recompression chains, resizing, cropping, screenshots, re-uploads, filters; document verified platform behavior and specify the degradation protocol for later robustness evaluation.
5. Generalization across generators and unseen manipulations; cross-generator and cross-dataset protocols; continual learning, test-time adaptation and data-diversity strategies with evidence.
6. Adversarial robustness (perturbations, anti-forensics, laundering through compression or regeneration) and defenses; a paper red-team of the design.
7. System-level resolution design: source credibility, account/network signals (using the anomaly layer's social signals only within the privacy rules), crowd corroboration, multi-source and multi-modal corroboration (social report vs CCTV detection vs IoT alarm vs satellite fire detection vs weather), claim verification (including text in Indian languages and code-mixed text), confidence scoring, human-in-the-loop escalation, and the decision policy for low-confidence items with an explicit cost matrix for false positives vs false negatives (show analytically how the threshold moves with cost).
8. Fairness, bias, calibration and uncertainty requirements; metrics (AUC, average precision, TPR at fixed low FPR, cross-generator accuracy, robustness curves vs compression quality, calibration error) and the pre-registered evaluation protocol.
9. Planned experiments for the build phase (at least one cross-generator evaluation, one degradation robustness curve, one adversarial test, one ablation of the physics-plausibility signal, one end-to-end decision-policy study), with planning-level compute estimates.
10. Add forensic and misinformation datasets (free ones only for selection) to `DATASETS.md` under the rules of section 0.9A.
11. Read the 15+ quota papers and record what they changed.
12. Update the handoff files.

**Outputs.** `ws2_deepfake/` (literature map, system design with decision policy and cost matrix, robustness plan, evaluation protocol, experiment plan), SOTA scan with targets section, quota list, report.

**Acceptance.** Every component justified by cited evidence; decision policy explicit; protocol covers cross-generator and degradation evaluation; no deceptive media created; quota met.

**Exit.** Quota audit, audit, report, gate message, STOP.

---

# PHASE P12: WS3, OFFLINE LOCAL-AREA ALERTING

**Objective.** Settle the "IP address" idea honestly and design a feasible tiered offline alerting architecture, with a simulation specification for the build phase.

**Entry.** `GO PHASE P12`; Phases P3 and P4 complete (P6 soft).

**Original wish.** A CCTV camera detects a fire nearby and the software alerts everyone near the area without internet using their IP addresses.

**Quota topics (15 NEW papers; aim for about 40).** Public warning systems and Cell Broadcast (including India's systems and CAP); alert effectiveness, alert fatigue and false-alarm cost studies; ESP-NOW, BLE, LoRa, Wi-Fi mesh and Zigbee measured range and reliability; opportunistic and delay-tolerant networking for disasters; emergency communication in infrastructure-down scenarios; secure and authenticated alert broadcast; geo-fencing and proximity alerting; network simulation methodology (ns-3 and similar) and its validation.

**Tasks.**
1. SOTA scan for disaster-area communication and public-warning systems.
2. Rigorous feasibility analysis (`ws3_alerting/feasibility_analysis.md`): why IP addresses do not encode physical location; how NAT, DHCP, carrier-grade NAT, VPNs and mobile networks break the idea; what "offline" means for IP-based communication; who could and could not be reached by address. Give a clear verdict.
3. Evaluate real feasible options (with real sources) on range, reachability of ordinary phones, latency, reliability, power, cost, privacy, abuse risk and regulatory path: same-LAN/Wi-Fi alerting (UDP broadcast, multicast, mDNS/DNS-SD, WebSocket/SSE from a local server, captive-portal alerts, local push gateways, and what ordinary phones actually receive in the background); mesh and short-range radio (802.11s, ESP-NOW-style, Wi-Fi Direct/Aware, BLE advertising and mesh, LoRa/LoRaWAN/Meshtastic-style, Zigbee) with real ranges and throughput from sources, not marketing; cellular broadcast needing no per-user addressing (Cell Broadcast, Wireless Emergency Alerts, EU-Alert, India's cell-broadcast and CAP-based public alerting: technical and regulatory path and whether a private party can use it, stating clearly if only authorized agencies can); physical channels (sirens, strobes, PA systems, SMS gateways which need cellular not internet, FM/RDS signaling); standards (CAP, IPAWS-style architectures, interoperability, message design); geo-fencing without IP; opt-in, consent-based, privacy-preserving registry designs.
4. Security and abuse (`ws3_alerting/threat_model.md`): spoofed alerts, replay, alert fatigue, false alarms, DoS, insider misuse; authentication and signing, key management, rate limiting; use the network-anomaly findings of P9/P10 where available; privacy law considerations (research, not legal advice).
5. Tiered architecture (`ws3_alerting/architecture.md`): Tier 1 local siren and strobe, Tier 2 local LAN/mesh/BLE push, Tier 3 cellular broadcast or SMS when available, official channels where only authorities may use them; graceful degradation; a decision policy tying alert tier to detection confidence and uncertainty (inputs from CCTV, fusion, IoT sensors and the anomaly layer, with deepfake-pipeline verification when media is involved), with human oversight for high-stakes alerts (rule 19).
6. Simulation SPECIFICATION (`ws3_alerting/simulation_spec.md`): what to simulate later (reach vs distance and node density, latency distribution, node failure, interference, partition, spoof attempts), with simulator choice justified by literature, parameter values sourced from verified papers and datasheets, and the validation approach. Nothing is simulated now.
7. Add network and alerting traces (free ones only for selection) to `DATASETS.md` under the rules of section 0.9A.
8. Read the 15+ quota papers and record what they changed.
9. Update the handoff files.

**Outputs.** `ws3_alerting/` (feasibility, architecture, simulation spec, threat model), SOTA scan with targets section, quota list, report.

**Acceptance.** Clear verdict on the IP idea; every capability claim sourced; simulation parameters traceable to sources; quota met.

**Exit.** Quota audit, audit, report, gate message, STOP.

---

# PHASE P13: WS7b, IoT DESIGN AND BUILD MANUAL (DOCUMENTS ONLY)

**Objective.** Write the complete design and build manual for the prototype so that I can build it later without further research. Nothing is built, flashed or tested now.

**Entry.** `GO PHASE P13`; Phase P6 complete (P12 and P10 soft).

**Quota topics (15 NEW papers).** Sensor calibration and compensation methods for low-cost gas/smoke/temperature sensors; experimental protocols and standards-based test practice for fire detectors; TinyML deployment and quantization on ESP32-class devices; embedded firmware reliability (watchdog, brownout, ADC/Wi-Fi interaction); field-test methodology and statistical analysis for small-sample hardware experiments; on-device anomaly and sensor-fault detection; low-power radio measurement methodology.

**Tasks.**
1. SOTA scan of published low-cost IoT fire-detection prototypes with measured results and their test conditions (the baseline our later measurements will be compared with).
2. Firmware SPECIFICATION (no code): modules, state machine, data formats, timing and duty cycling, local logging, local dashboard content (live curves, current state, alert tier, fused confidence and uncertainty, anomaly and sensor-health flags from the P10 edge spec, event log), offline operation, signed alert messages with replay protection, watchdog and fault handling, with the literature behind each choice and the library choices to evaluate (versions to be pinned at build time).
3. Hardware documents: wiring descriptions and pin maps (as text and tables, with diagram specifications for a designer), power design, enclosure and mounting plan within budget, step-by-step assembly instructions I can follow later, expected sensor readings and troubleshooting.
4. Calibration protocol per sensor (baseline, warm-up, per-unit gain/offset, humidity/temperature compensation where the literature supports it).
5. Test protocol for the later build, following `ws7_iot/SAFETY.md`: sensor characterization (warm-up, noise floor, response and recovery, humidity/temperature dependence, repeatability, drift); detection tests with safe stimuli (steam, cooking-like vapor, dust puff, incense smoke at safe distance, warm objects) with repeated trials and session-based splits; the comparison design (single-sensor threshold vs rate-of-rise vs multi-sensor fusion vs TinyML vs physics-informed logic vs the anomaly layer); networking tests (latency, packet loss, reach vs distance, node removal, spoofed/replayed message rejection); camera-path test if budget allows; statistics appropriate for small samples; data-logging format. All as protocol, none executed.
6. Demonstration package (`ws7_iot/DEMONSTRATION_PLAN.md`): a 3 to 5 minute repeatable demonstration script for stakeholders, experts or evaluators (stimulus, sensing, on-device decision, local alert on buzzer/strobe and dashboard, offline operation shown by disconnecting internet, spoof rejection, a slide of measured numbers to be filled after the build), a backup plan for demonstration failures, a one-page architecture figure specification, a list of photos to take, and an honest "what the prototype will and will not prove" statement (`ws7_iot/LIMITATIONS.md`). Results sections are written as "to be filled after the build".
7. Integration notes: how sensor streams will feed the fusion layer and alert logic and how the deepfake policy treats IoT alarms as corroborating evidence (data formats).
8. Re-verify the BOM prices (prices change) and update `HARDWARE_BUDGET.md`.
9. Read the 15+ quota papers and record what they changed.
10. Update the handoff files.

**Outputs.** `ws7_iot/` (firmware spec, hardware documents, calibration protocol, test protocol, demonstration plan, limitations), updated `HARDWARE_BUDGET.md`, SOTA scan with targets section, quota list, report.

**Acceptance.** A person could build and test the prototype from these documents alone; every choice has a source; budget re-verified; no measurement claims; quota met.

**Exit.** Quota audit, audit, report, gate message, STOP.

---

# PHASE P14: WS1b, META-FUSION DESIGN

**Objective.** Design the calibrated fusion of the admitted physics models, learned detectors, sensors and anomaly scores, with the evaluation plan for the build phase.

**Entry.** `GO PHASE P14`; Phases P7 and P8 complete (P10 and P13 soft).

**Quota topics (15 NEW papers).** Multi-sensor and multi-model fusion (stacking, mixture of experts, Bayesian model averaging, Dempster-Shafer, Kalman/particle filters); uncertainty-aware gating and abstention; conformal prediction; deep ensembles and calibration; handling correlated and missing models; fusion of anomaly scores and supervised scores; proper scoring rules; fusion in safety-critical detection systems.

**Tasks.**
1. SOTA scan for uncertainty-aware multi-source fusion and calibration benchmarks.
2. Survey fusion methods in depth (stacking, mixture of experts, Bayesian model averaging, Dempster-Shafer, uncertainty-aware gating, conformal prediction, deep ensembles, late/early/hybrid sensor fusion, Kalman/extended/particle filters, learned meta-learners, calibration by temperature scaling and isotonic regression, ECE and alternatives, proper scoring rules such as log-loss, Brier and CRPS, prediction-interval coverage).
3. Acceptance criteria decided now: what improvement over the best single model, on which cross-site metric, with what seed variance, will count as "fusion works" in the build phase.
4. Design `ws1_physics/fusion_design.md`: each model outputs a prediction plus an uncertainty; anomaly scores and sensor-health flags enter as inputs or as abstention triggers; the fuser is calibrated; it degrades gracefully when any subset of models is missing or out-of-regime; correlated models are not double-counted (a Layer 2 physics model and its Layer 1 parent are highly correlated by construction); one badly failing model cannot dominate; it can abstain and escalate when evidence is weak; it scales to N models without overfitting. Analyze the design on paper (for example theoretical behavior under correlated errors, missing inputs, miscalibration).
5. Ablation and stress-test plan (`ws1_physics/ablation_plan.md`): single-model, leave-one-out, greedy forward/backward selection, grouped by phenomenon family, all pairs if N is small, with and without physics inputs, with and without anomaly inputs, parent vs extension, fused vs best single; sensor noise, missing modalities, adversarial inputs, distribution shift (new camera, site, weather), rare events, correlated failures.
6. Interfaces: the fused confidence and uncertainty delivered to the alert decision policy (P12) and the verification policy (P11).
7. Read the 15+ quota papers and record what they changed.
8. Update the handoff files.

**Outputs.** `ws1_physics/` fusion design, ablation plan, SOTA scan with targets section, quota list, report.

**Acceptance.** Pre-registered acceptance criteria; design justified by cited evidence; stress-test plan complete; quota met.

**Exit.** Quota audit, audit, report, gate message, STOP.

---

# PHASE P15: WS5, REINFORCEMENT LEARNING DESIGN

**Objective.** Design the RL component including its environment, and plan its training within the later Kaggle budget. Nothing is trained or simulated now.

**Entry.** `GO PHASE P15`; Phases P7 and P12 complete (P14 soft).

**Quota topics (15 NEW papers; aim for about 40).** RL and optimization for evacuation, emergency response and resource allocation; fire-spread and crowd simulators and environments; reward design and reward hacking; safe and constrained RL; multi-agent RL; model-based and offline RL; GPU-accelerated and vectorized environments; deep-RL evaluation methodology and statistical reporting; sim-to-real and domain randomization.

**Tasks.**
1. SOTA scan for RL in emergency response and evacuation and for sample-efficient RL under small compute budgets.
2. Pin down what the agent is for (resource allocation, evacuation routing, camera or sensor control, alert dispatch, response planning) in `ws5_rl/env_design.md`, including why RL is justified over simpler baselines. Specify strong non-RL baselines (heuristics, optimization, planning) to be built first; state the condition under which RL would not be worth it. Any RL recommendation that could affect real emergency response is advisory only, with human decision-makers (rule 19).
3. Environment design from literature: state/observation/action spaces, reward design and reward-hacking pitfalls, partial observability, multi-agent formulations, simulator fidelity vs speed; review existing disaster, evacuation, crowd and fire-spread simulators and RL environments (Gymnasium-compatible, PettingZoo, cellular-automata fire models, crowd simulators) and decide reuse vs build; say how the admitted physics models would drive dynamics and what is simplified; optionally model the IoT sensor-node layout, alert tiers and anomaly-triggered escalations.
4. Methods: vectorized and GPU-accelerated environments, model-based RL, offline RL, curriculum learning, imitation and behavior-cloning pretraining, reward shaping with evidence; choose algorithms (PPO, SAC, DQN variants, MARL methods) on evidence, with a planning-level GPU-hour estimate (`ws5_rl/training_plan.md`).
5. Robustness and evaluation protocol: domain randomization, distribution shift, adversarial/robust RL, safe RL and constraints; evaluation across many seeds with confidence intervals and statistically sound aggregate metrics following the deep-RL evaluation-methodology literature; worst-case and rare-event evaluation; acceptance criteria decided now.
6. Practical plan: checkpoint and resume across Kaggle sessions, session time-limit handling, minimal-overhead logging.
7. Add RL environments and evacuation/crowd data (free ones only for selection) to `DATASETS.md` under the rules of section 0.9A.
8. Read the 15+ quota papers and record what they changed.
9. Update the handoff files.

**Outputs.** `ws5_rl/` (env design, training plan, evaluation protocol), SOTA scan with targets section, quota list, report.

**Acceptance.** Non-RL baselines specified; evaluation protocol with multi-seed statistics; budget within the plan; quota met.

**Exit.** Quota audit, audit, report, gate message, STOP.

---

# PHASE P16: WS6, ROBUSTNESS AUDIT PLAN (READ-ONLY)

**Objective.** Apply the failure-mode knowledge to the design and to the existing code (read-only) and produce a prioritized plan for what to test and fix when building.

**Entry.** `GO PHASE P16`; the core designs exist.

**Quota topics (15 NEW papers).** Testing and debugging of ML systems; data-leakage and evaluation-bug studies; numerical-stability and reproducibility issues in deep learning and PINNs; metamorphic and property-based testing for ML; fuzzing and fault injection for embedded and IoT firmware; adversarial and corruption robustness benchmarks; monitoring and drift detection in production ML; software-quality and assurance studies for scientific and safety-critical code.

**Tasks.**
1. SOTA scan for ML-system testing, robustness benchmarks and reproducibility practice.
2. Maintain and extend `ws6_robustness/failure_mode_catalogue.md` starting from the Phase P4 catalogue (including the anomaly-detection pitfalls).
3. Review every design document produced so far against the catalogue (a paper red-team): for each failure mode, is the design vulnerable, and what protective measure does the literature recommend?
4. Read the existing project code and pipelines (read-only) against the catalogue. Report findings as LIKELY or RISK with file and line, reasoning and the supporting paper; never as "confirmed", since nothing is reproduced. Cover: logic errors, data leakage between train/val/test (including near-duplicate frames, shared videos and normal-period leakage in anomaly detection), label errors, class-imbalance handling, normalization or channel-order mistakes, evaluation bugs (wrong averaging, thresholds chosen on test, lenient anomaly scoring used as the primary number), error handling, input validation, silent failures, nondeterminism and seed misuse, numerical instability, unit mismatches in physics code, coordinate and geometry and time-zone bugs, library misuse, config mistakes, security issues (unsigned alerts, secrets in code), brittle assumptions about camera or sensor inputs, and firmware-design risks (watchdog resets, ADC noise and Wi-Fi/ADC conflicts, brownouts, blocking loops, timer overflow, unbounded buffers, sensor warm-up drift).
5. Prioritized `ws6_robustness/audit_findings.md` and a prioritized test-and-fix plan for the build phase: what to reproduce first, expected test types (regression, adversarial, edge-case, stress), the measurements that will decide whether a fix helps, monitoring requirements (data and prediction drift, confidence drift, latency, false-alarm rate, device health), fallbacks and graceful degradation, with the literature behind each.
6. Red-team log on paper (`ws6_robustness/red_team_log.md`): attacks considered against each workstream, expected impact, mitigation.
7. Read the 15+ quota papers and record what they changed.
8. Update the handoff files.

**Outputs.** `ws6_robustness/` (catalogue, design-review findings, code-review findings, test-and-fix plan, red-team log), SOTA scan, quota list, report. No code is modified.

**Acceptance.** Every finding has a status of LIKELY or RISK with reasoning and a source; the plan is prioritized; quota met.

**Exit.** Quota audit, audit, report, gate message, STOP.

---

# PHASE P17: FEATURE DISCOVERY AND ADMISSION

**Objective.** Find additional valuable features supported by evidence and decide which to carry into the build plan. No implementation.

**Entry.** `GO PHASE P17`; the core designs are stable (core phases complete or consciously skipped).

**Quota topics (15 NEW papers; expect many more).** The recent papers the feature scouts find in each direction below; the 15 minimum counts only papers that are new and read at Tier 3 or deeper.

**Tasks.**
1. SOTA scan: for each workstream, what recent techniques the state of the art uses that we do not.
2. Feature scouts (at least one per workstream, including anomaly detection, plus one cross-cutting scout for integration, deployment, operator UX and monitoring) read recent papers (last 2 to 3 years prioritized), surveys, leaderboards, Papers With Code pages, and the limitation sections of papers already read, and ask what technique, module, signal, loss, data source, safeguard or evaluation method has been shown to improve this kind of system that we are missing. Directions (adapt to evidence): uncertainty and calibration (conformal prediction, deep ensembles, evidential methods, selective prediction/abstention); robustness (test-time adaptation, domain generalization, adversarial training, corruption robustness, OOD detection); anomaly detection upgrades (foundation-model features, vision-language anomaly scoring, continual normality updates); data efficiency (self-supervised pretraining, semi-supervised, active learning, synthetic data with sim-to-real evidence, label-noise handling); multimodal and temporal signals (thermal/IR, audio, sensor fusion, optical-flow and flicker-frequency features, physics-guided features); efficiency (distillation, pruning, quantization, early-exit, cascades, efficient backbones) within Kaggle, edge and microcontroller limits; provenance and trust (C2PA, watermark checks, source-credibility scoring, multi-source corroboration); alerting and operations (alert prioritization, de-duplication, escalation, alert-fatigue mitigation, human-in-the-loop review, explainability for operators, drift monitoring, multilingual alert delivery); IoT (sensor self-diagnosis and drift compensation, adaptive thresholds, node health monitoring, low-power duty cycling, mesh self-healing); RL (curriculum, model-based, offline, safe-RL constraints, domain randomization, reward-hacking checks); tooling (experiment tracking, reproducibility, automated regression and adversarial test suites).
3. Admission rules: a feature enters only if (1) it traces to at least one real, verified paper, datasheet and/or dataset read at least at method-and-results level (abstract-only evidence means "weak evidence", lower priority); (2) the evidence is relevant to our setting (otherwise "transfer hypothesis"); (3) a cost estimate exists (planning-level GPU hours, INR if hardware, engineering effort, latency, memory, complexity, new failure modes); (4) it does not conflict with another feature or a hard constraint (Kaggle budget plan, INR 2000 prototype cap, offline operation, privacy, safety, free-only datasets), with paper disagreements recorded; (5) own ideas not found in the literature are allowed only as "novel hypothesis, unvalidated" and must pass the same measurement gate later.
4. `FEATURES.md` for every candidate (selected, rejected or pending): ID, name, one-line description, workstream(s), component; status (proposed / approved-for-build-plan / rejected); supporting sources with verified identifiers and evidence strength (strong / medium / weak / transfer-hypothesis / novel-hypothesis); the exact claim the source makes with table/figure reference; cost; dependencies and conflicts; planned ablation design, metrics, seeds or trials; final decision and reason. Rejections are valuable output and are listed with reasons.
5. Prioritize by (expected benefit x evidence strength) / cost into waves: Wave 1 high-evidence low-cost, Wave 2 medium, Wave 3 speculative only if budget remains. Pre-register the decision rule for every feature for the build phase (keep only if the improvement exceeds seed-to-seed or trial-to-trial variance and the cost is justified; a feature that helps one benchmark but hurts cross-dataset or cross-camera performance is NOT a win). Features must never consume the 15% GPU reserve, the hardware contingency, or starve core work.
6. Read the 15+ quota papers and record what they changed.
7. Update the handoff files.

**Outputs.** `FEATURES.md`, scout notes, new ledger entries, wave plan with planning-level budgets, SOTA scan, quota list, report.

**Acceptance.** Every candidate has verified support or is rejected; costs and decision rules pre-registered; quota met.

**Exit.** Quota audit, audit, report, gate message (I choose which waves and features go into the build plan), STOP.

---

# PHASE P18: FEATURE SPECIFICATIONS AND MEASUREMENT PLANS

**Objective.** For the features I approved at the P17 gate, write ready-to-build specifications and measurement plans. Nothing is implemented or measured.

**Entry.** `GO PHASE P18` naming the wave(s) and features.

**Quota topics (15 NEW papers).** Implementation-level papers for the specific approved features: official method papers, reproduction and ablation studies, known pitfalls and hyperparameter guidance for each, plus critiques of the feature's reported gains. Papers read in P17 do not count again.

**Tasks.** SOTA scan for each approved feature (current best implementation and reported gains). For each feature write a specification: design and where it plugs in, configuration or build flag design, inputs and outputs, hyperparameter defaults with sources, ablation design (same split, same seeds, feature on vs off, stress conditions), metrics, the pre-registered decision rule, planning-level cost, risks and the new failure modes it may introduce (feed to the robustness catalogue). Read the 15+ quota papers and record what they changed. Update the handoff files.

**Outputs.** Updated `FEATURES.md`, `features/` specification documents, SOTA scan with targets section, quota list, report.

**Acceptance.** Each approved feature has a complete spec and decision rule; quota met.

**Exit.** Quota audit, audit, report, gate message, STOP.

---

# PHASE P19: INDIA DEPLOYMENT PATHWAY, STANDARDS AND REGULATION, PILOT DESIGN AND RESEARCH-CONTRIBUTION PLAN

**Objective.** Work out what it would take to deploy this system responsibly in India, and identify what is genuinely new and publishable. A system that could influence real emergency decisions needs more than good models: it needs the right standards, regulation, partners, human oversight, local fit and a careful pilot.

**Entry.** `GO PHASE P19`; enough of the earlier phases complete (you recommend which in the preceding gate; ideally P6 and P12 are done and P19 is started early enough to influence design choices).

**Quota topics (15 NEW research papers; aim for about 30).** Disaster early-warning and emergency-management studies in India and South Asia; community-based early warning case studies; fire-incident epidemiology and causes in India and comparable countries; effectiveness, trust and human factors of public warnings and alerts; low-cost IoT and sensing deployments in developing regions (power cuts, heat, dust, connectivity); multilingual crisis informatics and misinformation in Indian languages; ethics, accountability and assurance of AI in emergency management and safety-critical systems; privacy-preserving public-safety surveillance; cost-effectiveness evaluation of early-warning and fire-protection interventions; pilot and field-evaluation methodology for safety technologies.

**Tasks.**
1. SOTA scan: existing Indian and international deployed systems and programs relevant to fire and disaster early warning, public alerting and surveillance analytics (what they do, how they are governed, what is known about their performance), with verified sources. Include official government and agency documents as non-quota sources.
2. India context (`DEPLOYMENT/india_context.md`): the disaster-management and fire-service landscape (national, state and local agencies and their roles), who operates public alerting and how, who owns or operates CCTV in cities and private premises, typical connectivity, power reliability and camera quality, languages and literacy, fire-incident patterns and statistics from official sources (with dates). Names of agencies, laws and standards that come to mind are search leads only (rule 11): verify each against official sources before including it.
3. Standards and regulation (`DEPLOYMENT/standards_and_regulation.md`): which Indian standards, building and fire-safety codes, telecom and public-alerting rules, data-protection law, surveillance and CCTV rules, and electronics or radio certification requirements apply to the components of this system (fire detection and alarm devices, radio operation, alert broadcast, personal data in video, social-media data); what a private or academic party may and may not do (for example, who can use official public-alert channels); what certification a fire-detection product would need to be treated as a safety device, and why this system should present itself as complementary until certified. Everything is a research note with sources, flagged for review by a qualified legal or standards professional; none of it is legal advice.
4. Stakeholders and partners (`DEPLOYMENT/stakeholders_and_partners.md`): the types of experts and bodies whose input is needed (fire services, disaster-management authorities, meteorological and remote-sensing agencies, universities and research labs, local administrations, telecom operators, community organizations, disability and accessibility groups), what each could contribute and what we would ask them, ordered by importance. Propose only; contact no one.
5. Pilot design (`DEPLOYMENT/pilot_design.md`): a safe, supervised, staged pilot protocol for the later build: shadow mode first (the system observes and logs, never triggers real alerts), then advisory mode with human review, with explicit success metrics tied to the pre-registered protocols (false alarms per day, time-to-detection, uptime), stopping rules, incident handling, consent and privacy measures, ethics-review requirements, site selection criteria, and what evidence would be needed before any automated public alert. Pilot methodology comes from the literature.
6. Adoption barriers and fit (`DEPLOYMENT/adoption_barriers.md`): language and accessibility requirements for alerts, trust and alert fatigue, training needs, maintenance and spare-parts realities, power and connectivity failures, vandalism and theft, interoperability with existing CCTV and fire panels; the design changes these imply for earlier workstreams (feed them into the handoff and open decisions).
7. Cost and scaling (`DEPLOYMENT/cost_scaling.md`): per-node and per-site cost structure for a real deployment compared with the INR 2000 prototype, using only verified prices and price breaks with dates; maintenance and connectivity costs; what is unknown and how to find out. Cost-effectiveness claims only with verified sources.
8. Responsible release (`DEPLOYMENT/responsible_release.md`): misuse and dual-use analysis (spoofed alerts, surveillance abuse, deepfake tooling), what should be open-sourced and what should be released with safeguards, license choices and their consequences, data governance for any data we collect, model cards and datasheets to produce at build time.
9. Research contributions and publication plan (`DEPLOYMENT/research_contributions.md`, `DEPLOYMENT/publication_plan.md`): from the gap map and the SOTA scans, list the contributions that look genuinely new (each tied to verified gaps, labeled "proposed, not yet validated"), including candidate benchmarks, datasets, protocols or open resources we could release; for each, what experiment would validate it in the build phase and what result would count; suitable venues with their scopes and deadlines (verified); the order in which results should be published; what would make the work credible to reviewers (strict protocols, open code and data, honest negatives). For every physics contribution, state its class (A, B or C), its parent model and where the parent fails, its validation status and roadmap against specific published data, suitable fire-science venues (verified), and the experts who should review it. Class C items are listed as hypotheses, never as results.
10. Honest limits (`DEPLOYMENT/what_this_system_is_not.md`): a plain statement of what the system must not be relied upon for and which preconditions (validation, independent review, certification, official approval) must be met before real-world reliance (rule 19).
11. Add India-specific free datasets to `DATASETS.md` under the rules of section 0.9A (including ISRO/NRSC and other government portals with their access status).
12. Read the 15+ quota papers and record what they changed in the design and the handoff.
13. Update the handoff files (including design changes the deployment study implies).

**Outputs.** `DEPLOYMENT/` (all documents above), SOTA scan, quota list, report.

**Acceptance.** Every statement about India, standards, regulation, costs and impact traces to a verified source or is labeled as unverified and flagged for expert review; the pilot design is staged and safe; contributions are tied to verified gaps; quota met.

**Exit.** Quota audit, audit, report, gate message (including the experts and decisions I need to arrange), STOP.

---

# PHASE P20: FINAL QUALITY GATES AND FINAL RESEARCH REPORT

**Objective.** Verify the research outputs and deliver the final report.

**Entry.** `GO PHASE P20`.

**Quota topics (15 NEW papers).** Reporting and reproducibility standards for ML and scientific work; the latest state-of-the-art results for each task we target (to ensure the targets in the handoff are current); meta-evaluation and benchmark-critique papers relevant to the metrics we plan to use.

**Tasks (quality gates).**
1. Final SOTA scan: refresh the published numbers we target and update the targets tables in the handoff, with every protocol difference spelled out (rule 16).
2. Ledger audit: re-verify a random sample of at least 10% of all ledger entries and dataset links (identifier resolves, title/authors/year match, notes faithful); fix or remove failures; log the rate.
3. Reading-faithfulness audit: a separate agent or fresh pass re-reads 10% of notes (all Tier 1 key numbers) against the sources.
4. Quota audit across all phases: confirm every phase met its minimum of 15 NEW papers (re-run the novelty lookups for a sample, check tiers, check that each phase report shows what the papers changed); list any phase that fell short and why.
5. Traceability audit: every number, equation and claim in the synthesis, the design documents, the feature registry, the deployment documents and the final report links back to a note or a verified source with a table/equation/page reference.
6. Consistency audit: names, dataset sizes, numbers and plans identical everywhere.
7. Link and price audit: every URL and price listing re-checked; record dates; flag changed prices, changed dataset terms and changed regulations; confirm no dataset with STATUS = selected is paid.
8. Completeness review of the handoff: each workstream's spec is complete enough to write a build prompt without further research; list the gaps.
9. Safety and responsibility review: confirm `ws7_iot/SAFETY.md` is consistent with the test protocols and the demonstration plan, and that rule 19 appears in every design that could influence real alerts.
10. Independent review: a fresh pass reads the whole output as a skeptical reviewer and lists unsupported claims, contradictions, SOTA claims that violate rule 16, impact claims that violate rule 18, and missing pieces; resolve them all. Specifically check that no Class B or C formula is described anywhere as established or validated, and that every novelty statement is phrased as a search claim.
11. Read the 15+ quota papers and record what they changed.

**`FINAL_REPORT.md` states plainly:** what was researched and decided (per workstream), with the key evidence; the final number N of physics models and why (Layer 1 and Layer 2, admitted, demoted, rejected, with classes and lineage); the anomaly-detection scope and design and the strict protocol; which claims are CONFIRMED (by sources) / LIKELY / HYPOTHESIS / INFEASIBLE including the verdict on the IP-address alerting idea; literature counts (baseline papers read; foundation new papers verified and whether the 250 minimum was reached with exact number and reasons if not; the per-phase quota table with the count of new papers per phase; workstream papers; datasheets, standards and government reports; read-depth distribution; datasets verified, by cost category); audit results and corrections; contradictions found in the literature and how they were handled; the IoT plan (final BOM total vs INR 2000 with verified listings and dates, node architecture, what the prototype will and will not prove); the feature summary (selected, rejected, with evidence and planned cost); the planning-level Kaggle budget; the SOTA targets table; the India deployment pathway, regulatory findings (flagged for expert review) and pilot design; the research contributions and publication plan; the build handoff status and recommended build order; everything uncertain, unfinished or needing my input.

**Exit.** Report, gate message announcing completion, and the list of next steps for me (for example: order parts, request dataset access, consult the experts and bodies you identified, then request the build prompt using `HANDOFF/BUILD_HANDOFF.md`; any slides, hackathon submission or paper can be produced afterwards from the final report and the handoff).

---

# BEGIN NOW

Start PHASE P0 immediately; its first action is saving this entire prompt to `PROGRAM/MASTER_PROMPT.md`. Do not start any other phase until I reply with an explicit authorization. This run is research-only: write no code, run nothing beyond bookkeeping and tool probes, train nothing, build nothing. Work inside my existing project folder, save everything to files, never delete or overwrite anything of mine, keep every claim real and verified, and remember that from Phase P1 onward every phase reads at least 15 NEW papers, starts with a SOTA scan, ends with a quota audit and updates the build handoff. The purpose is real-world benefit to India, not a competition: evidence beats persuasiveness, and this is a life-safety domain (rule 19). In Phase P0 you also decide and propose the order in which the phases should run (section 0.1 rule 9). When Phase P0 is finished, send the gate message described in section 0.2, containing the true literature counts after reconciliation, the research-tool capabilities (especially whether web search and PDF reading work, since the quota depends on them), the proposed phase plan and recommended sequence with the alternative, the open questions, and the exact reply I should send to authorize the first phase of your recommended sequence. Then wait.