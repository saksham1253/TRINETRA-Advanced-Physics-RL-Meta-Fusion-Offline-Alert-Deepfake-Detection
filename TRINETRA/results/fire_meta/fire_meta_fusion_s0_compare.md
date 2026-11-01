# Fire meta-fusion (REAL pairing) · seed 0 · n 3410 images, 366 blocks

Experts: fire_cnn, zeroshot, clip_probe, colorhist · gate (calibrated stack vs climatology and best single `clip_probe`, cost CI): **NOT ADMITTED**

## OOF (block-grouped CV)

| rule | ROC-AUC | PR-AUC | recall@FPR5% | ECE | value score | miss @p* | false alarm @p* |
|---|---|---|---|---|---|---|---|
| stacked meta (calibrated) | 0.949 | 0.965 | 0.815 | 0.019 | 0.107 | 0.008 | 0.695 |
| stacked meta raw | 0.953 | 0.967 | 0.813 | 0.022 | 0.146 | 0.003 | 0.775 |
| FM-1 (calibrated) | 0.946 | 0.964 | 0.812 | 0.040 | -0.040 | 0.016 | 0.645 |
| plain mean | 0.942 | 0.960 | 0.795 | 0.157 | 0.000 | 0.000 | 1.000 |
| max | 0.915 | 0.947 | 0.761 | 0.195 | 0.000 | 0.000 | 1.000 |
| single: fire_cnn | 0.755 | 0.811 | 0.351 | 0.110 | 0.001 | 0.001 | 0.986 |
| single: zeroshot | 0.906 | 0.934 | 0.651 | 0.035 | -0.071 | 0.010 | 0.834 |
| single: clip_probe | 0.959 | 0.972 | 0.822 | 0.020 | 0.180 | 0.008 | 0.623 |
| single: colorhist | 0.680 | 0.694 | 0.110 | 0.067 | 0.001 | 0.000 | 0.999 |

Stack − best single AUC -0.010 (95% CI -0.015 to -0.005); recall@FPR5% -0.020 (CI -0.055 to +0.006).

## Held-out (1023 images, different dataset; experts fire_cnn, zeroshot, clip_probe)

| rule | ROC-AUC | PR-AUC | recall@FPR5% | ECE | value score | miss @p* | false alarm @p* |
|---|---|---|---|---|---|---|---|
| stacked meta (calibrated) | 1.000 | 1.000 | 1.000 | 0.026 | 0.632 | 0.000 | 0.368 |
| FM-1 | 1.000 | 1.000 | 1.000 | 0.110 | 0.056 | 0.000 | 0.944 |
| plain mean | 1.000 | 1.000 | 1.000 | 0.140 | 0.035 | 0.000 | 0.965 |
| max | 0.998 | 0.998 | 0.998 | 0.107 | 0.000 | 0.000 | 1.000 |
| single: fire_cnn | 0.983 | 0.989 | 0.880 | 0.260 | 0.000 | 0.000 | 1.000 |
| single: zeroshot | 1.000 | 1.000 | 1.000 | 0.053 | 0.416 | 0.000 | 0.584 |
| single: clip_probe | 0.998 | 0.998 | 0.997 | 0.032 | 0.568 | 0.000 | 0.432 |

Meta weights (standardized): logit_fire_cnn +0.53, logit_zeroshot +0.75, logit_clip_probe +2.16, sd +0.02, range -0.09
