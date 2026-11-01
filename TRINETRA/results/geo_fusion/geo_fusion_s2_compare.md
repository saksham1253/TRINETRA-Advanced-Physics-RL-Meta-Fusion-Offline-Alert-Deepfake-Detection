# Landslide meta-fusion (REAL pairing) · seed 2 · n 736 (184 events, 101 blocks)

Experts: rain, caine, dfs, geo_gate · Geo-PINN: not provided · gate (calibrated FM-1 vs climatology and rain-only, cost CI): **NOT ADMITTED**

| rule | ROC-AUC | PR-AUC | recall@FPR5% | ECE | value score | miss rate @p* | false alarms @p* |
|---|---|---|---|---|---|---|---|
| FM-1 (calibrated) | 0.778 | 0.512 | 0.201 | 0.066 | 0.020 | 0.000 | 0.980 |
| FM-1 raw | 0.780 | 0.514 | 0.201 | 0.066 | 0.004 | 0.000 | 0.996 |
| FM-1 + physics shield | 0.778 | 0.512 | 0.201 | 0.066 | 0.020 | 0.000 | 0.980 |
| PHARAOH | 0.781 | 0.513 | 0.207 | 0.067 | 0.004 | 0.000 | 0.996 |
| plain mean | 0.781 | 0.518 | 0.239 | 0.062 | 0.004 | 0.000 | 0.996 |
| median | 0.774 | 0.501 | 0.190 | 0.047 | 0.005 | 0.000 | 0.995 |
| max | 0.772 | 0.517 | 0.261 | 0.107 | 0.000 | 0.000 | 1.000 |
| physics-only mean | 0.775 | 0.506 | 0.185 | 0.063 | 0.000 | 0.000 | 1.000 |
| stacked logistic (rain+physics) | 0.779 | 0.514 | 0.228 | 0.019 | 0.020 | 0.027 | 0.799 |
| single: rain | 0.781 | 0.519 | 0.234 | 0.019 | 0.016 | 0.027 | 0.803 |
| single: caine | 0.757 | 0.502 | 0.163 | 0.046 | 0.058 | 0.022 | 0.797 |
| single: dfs | 0.749 | 0.478 | 0.179 | 0.049 | 0.000 | 0.000 | 1.000 |
| single: geo_gate | 0.714 | 0.477 | 0.179 | 0.029 | -0.085 | 0.016 | 0.976 |

FM-1 − rain AUC -0.003 (95% CI -0.015 to +0.010); FM-1 − stacked -0.001 (CI -0.011 to +0.010). Mean U* 0.375; 0.0% of rows flagged uncertain (U* > 0.6).
