# Fire meta-fusion (REAL pairing) · seed 1 · n 3410 images, 366 blocks

Experts: fire_cnn, zeroshot, clip_probe, colorhist · gate (calibrated stack vs climatology and best single `clip_probe`, cost CI): **NOT ADMITTED**

## OOF (block-grouped CV)

| rule | ROC-AUC | PR-AUC | recall@FPR5% | ECE | value score | miss @p* | false alarm @p* |
|---|---|---|---|---|---|---|---|
| stacked meta (calibrated) | 0.950 | 0.965 | 0.791 | 0.032 | 0.240 | 0.004 | 0.668 |
| stacked meta raw | 0.951 | 0.966 | 0.788 | 0.027 | 0.240 | 0.002 | 0.721 |
| FM-1 (calibrated) | 0.953 | 0.968 | 0.812 | 0.028 | 0.207 | 0.005 | 0.675 |
| plain mean | 0.945 | 0.963 | 0.806 | 0.159 | 0.000 | 0.000 | 1.000 |
| max | 0.914 | 0.946 | 0.765 | 0.221 | 0.000 | 0.000 | 1.000 |
| single: fire_cnn | 0.758 | 0.788 | 0.277 | 0.038 | 0.004 | 0.000 | 0.996 |
| single: zeroshot | 0.906 | 0.934 | 0.651 | 0.035 | -0.071 | 0.010 | 0.834 |
| single: clip_probe | 0.959 | 0.972 | 0.822 | 0.020 | 0.180 | 0.008 | 0.623 |
| single: colorhist | 0.672 | 0.702 | 0.135 | 0.034 | 0.001 | 0.000 | 0.999 |

Stack − best single AUC -0.009 (95% CI -0.017 to -0.001); recall@FPR5% -0.035 (CI -0.060 to -0.007).

## Held-out (1023 images, different dataset; experts fire_cnn, zeroshot, clip_probe)

| rule | ROC-AUC | PR-AUC | recall@FPR5% | ECE | value score | miss @p* | false alarm @p* |
|---|---|---|---|---|---|---|---|
| stacked meta (calibrated) | 1.000 | 1.000 | 1.000 | 0.027 | 0.619 | 0.000 | 0.381 |
| FM-1 | 1.000 | 1.000 | 1.000 | 0.110 | 0.011 | 0.000 | 0.989 |
| plain mean | 1.000 | 1.000 | 1.000 | 0.134 | 0.005 | 0.000 | 0.995 |
| max | 0.998 | 0.998 | 0.998 | 0.152 | 0.000 | 0.000 | 1.000 |
| single: fire_cnn | 0.978 | 0.987 | 0.915 | 0.237 | 0.000 | 0.000 | 1.000 |
| single: zeroshot | 1.000 | 1.000 | 1.000 | 0.053 | 0.416 | 0.000 | 0.584 |
| single: clip_probe | 0.998 | 0.998 | 0.997 | 0.032 | 0.568 | 0.000 | 0.432 |

Meta weights (standardized): logit_fire_cnn +0.61, logit_zeroshot +0.68, logit_clip_probe +2.19, sd -0.09, range -0.04
