# 17 — HOW TYPICAL DISASTER-WARNING APPROACHES FAIL (14 patterns, category level, sourced)
Rule: we describe **approach categories**, never a named team, company or product. Sources are papers in the repo ledger
(`docs/11_paper_links.csv`). Most are **abstract-only (ABS)**, so they are quoted as "the abstract reports...". Verification status is in the CSV.

| ID | Failure pattern | What goes wrong (Hinglish) | Source (repo ledger) |
|----|-----------------|----------------------------|----------------------|
| P1 | False alarms → alert fatigue ("cry wolf") | Baar-baar galat alarm se log alarm ignore karne lagte hain | 2104.11422 (ABS), 1904.01963 (ABS), 2410.06388 (FT-partial) |
| P2 | Late or missed detection | Chhota/door ka dhuan ya shuruaati barish signal miss | 2112.08598 FIgLib/SmokeyNet (ABS), 2601.03569 (ABS) |
| P3 | Single-source fragility | Ek camera/ek model fail to poora system andha | 2310.03986 missing modalities (ABS) |
| P4 | Domain shift (new site, weather, country) | Bahar ke data par train, India me alag scene | 2404.03539 fine-grained CLIP confusion (ABS), 2502.15901 TS-OOD (ABS) |
| P5 | No uncertainty / miscalibrated scores | "90% sure" bolta hai par asal me nahi hota | 2303.12748 zero-shot VLM miscalibration (ABS), 2512.12997 (ABS) |
| P6 | Internet/power dependence | Disaster me network girta hai, cloud-only alert ruk jaata hai | 1308.2907 delay-tolerant networks survey (ABS) |
| P7 | Fake / replayed media | Purana ya fake video viral, galat response | 2007.05848 disaster misinformation (FT-partial), 2610.03380 (FT-partial) |
| P8 | Inflated evaluation (leakage, random splits, imbalance) | Same video ke frames train+test me, number jhootha bada | 2610.10946 AI4Fire leakage (ABS), 2107.13029 TruZe (ABS), 2206.09981 (FT-partial) |
| P9 | Poor last-mile delivery | Alert bana par logon tak nahi pahuncha | ws3_alerting/literature_brief.md (repo research) |
| P10 | Latency / heavy compute | Model itna bhaari ki edge par der se chale | repo bug report #14 (edge latency overclaim) |
| P11 | Sim-to-real / unvalidated decision policies | RL ko simulator me achha, asal me pata nahi | 2311.14110 OPE usefulness (FT-partial), 2106.08909 (ABS) |
| P12 | Human factors (trust, compliance) | Log warning maane ya nahi, operator overload | 1904.01963 (ABS); repo bug report #32 (uniform compliance assumption) |
| P13 | Drift and maintenance cost | Sensor/model dheere-dheere kharab, koi monitor nahi | 2404.19452 drift detection (FT-partial), 2103.00903 (ABS) |
| P14 | Privacy of CCTV | Video bahar bhejna = privacy risk | 2608.04501 privacy-preserving action recognition (ABS) |

Note: these are failure **patterns reported in the literature for approach categories**. They are not statements about any specific deployed system.
<!-- END -->
