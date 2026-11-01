# Landslide meta-fusion (REAL pairing) · seed 1 · n 736 (184 events, 101 blocks)

Experts: rain, caine, dfs, geo_gate · Geo-PINN: not provided · gate (calibrated FM-1 vs climatology and rain-only, cost CI): **NOT ADMITTED**

| rule | ROC-AUC | PR-AUC | recall@FPR5% | ECE | value score | miss rate @p* | false alarms @p* |
|---|---|---|---|---|---|---|---|
| FM-1 (calibrated) | 0.779 | 0.507 | 0.185 | 0.064 | 0.005 | 0.000 | 0.995 |
| FM-1 raw | 0.779 | 0.506 | 0.179 | 0.075 | 0.000 | 0.000 | 1.000 |
| FM-1 + physics shield | 0.779 | 0.507 | 0.185 | 0.064 | 0.005 | 0.000 | 0.995 |
| PHARAOH | 0.780 | 0.508 | 0.190 | 0.074 | 0.000 | 0.000 | 1.000 |
| plain mean | 0.781 | 0.513 | 0.201 | 0.063 | 0.000 | 0.000 | 1.000 |
| median | 0.774 | 0.499 | 0.163 | 0.053 | 0.009 | 0.000 | 0.991 |
| max | 0.769 | 0.512 | 0.245 | 0.114 | 0.000 | 0.000 | 1.000 |
| physics-only mean | 0.775 | 0.498 | 0.158 | 0.068 | 0.000 | 0.000 | 1.000 |
| stacked logistic (rain+physics) | 0.782 | 0.511 | 0.223 | 0.023 | 0.007 | 0.027 | 0.812 |
| single: rain | 0.783 | 0.518 | 0.239 | 0.024 | -0.029 | 0.033 | 0.812 |
| single: caine | 0.757 | 0.495 | 0.223 | 0.045 | 0.054 | 0.022 | 0.801 |
| single: dfs | 0.746 | 0.470 | 0.174 | 0.061 | 0.000 | 0.000 | 1.000 |
| single: geo_gate | 0.705 | 0.451 | 0.163 | 0.031 | -0.062 | 0.011 | 0.989 |

FM-1 − rain AUC -0.003 (95% CI -0.016 to +0.009); FM-1 − stacked -0.003 (CI -0.013 to +0.008). Mean U* 0.375; 0.0% of rows flagged uncertain (U* > 0.6).
