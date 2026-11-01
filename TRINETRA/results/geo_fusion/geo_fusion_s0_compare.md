# Landslide meta-fusion (REAL pairing) · seed 0 · n 736 (184 events, 101 blocks)

Experts: rain, caine, dfs, geo_gate · Geo-PINN: not provided · gate (calibrated FM-1 vs climatology and rain-only, cost CI): **NOT ADMITTED**

| rule | ROC-AUC | PR-AUC | recall@FPR5% | ECE | value score | miss rate @p* | false alarms @p* |
|---|---|---|---|---|---|---|---|
| FM-1 (calibrated) | 0.779 | 0.509 | 0.185 | 0.070 | 0.011 | 0.000 | 0.989 |
| FM-1 raw | 0.780 | 0.509 | 0.179 | 0.077 | 0.002 | 0.000 | 0.998 |
| FM-1 + physics shield | 0.779 | 0.509 | 0.185 | 0.070 | 0.011 | 0.000 | 0.989 |
| PHARAOH | 0.781 | 0.509 | 0.185 | 0.076 | 0.002 | 0.000 | 0.998 |
| plain mean | 0.781 | 0.512 | 0.196 | 0.067 | 0.002 | 0.000 | 0.998 |
| median | 0.774 | 0.501 | 0.163 | 0.052 | 0.004 | 0.000 | 0.996 |
| max | 0.773 | 0.512 | 0.223 | 0.107 | 0.000 | 0.000 | 1.000 |
| physics-only mean | 0.776 | 0.502 | 0.190 | 0.065 | 0.000 | 0.000 | 1.000 |
| stacked logistic (rain+physics) | 0.780 | 0.504 | 0.223 | 0.030 | -0.016 | 0.033 | 0.799 |
| single: rain | 0.781 | 0.510 | 0.217 | 0.028 | -0.020 | 0.033 | 0.803 |
| single: caine | 0.756 | 0.495 | 0.190 | 0.039 | 0.053 | 0.022 | 0.803 |
| single: dfs | 0.747 | 0.475 | 0.196 | 0.052 | 0.000 | 0.000 | 1.000 |
| single: geo_gate | 0.709 | 0.479 | 0.196 | 0.036 | -0.056 | 0.011 | 0.984 |

FM-1 − rain AUC -0.002 (95% CI -0.014 to +0.011); FM-1 − stacked -0.001 (CI -0.011 to +0.009). Mean U* 0.376; 0.0% of rows flagged uncertain (U* > 0.6).
