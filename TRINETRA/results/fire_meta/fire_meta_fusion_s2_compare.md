# Fire meta-fusion (REAL pairing) · seed 2 · n 3410 images, 366 blocks

Experts: fire_cnn, zeroshot, clip_probe, colorhist · gate (calibrated stack vs climatology and best single `clip_probe`, cost CI): **NOT ADMITTED**

## OOF (block-grouped CV)

| rule | ROC-AUC | PR-AUC | recall@FPR5% | ECE | value score | miss @p* | false alarm @p* |
|---|---|---|---|---|---|---|---|
| stacked meta (calibrated) | 0.955 | 0.968 | 0.803 | 0.023 | 0.207 | 0.006 | 0.648 |
| stacked meta raw | 0.955 | 0.969 | 0.803 | 0.029 | 0.226 | 0.001 | 0.761 |
| FM-1 (calibrated) | 0.951 | 0.967 | 0.809 | 0.029 | 0.016 | 0.014 | 0.628 |
| plain mean | 0.945 | 0.963 | 0.797 | 0.156 | 0.000 | 0.000 | 1.000 |
| max | 0.913 | 0.946 | 0.768 | 0.215 | 0.000 | 0.000 | 1.000 |
| single: fire_cnn | 0.764 | 0.797 | 0.286 | 0.036 | 0.007 | 0.000 | 0.993 |
| single: zeroshot | 0.906 | 0.934 | 0.651 | 0.035 | -0.071 | 0.010 | 0.834 |
| single: clip_probe | 0.959 | 0.972 | 0.822 | 0.020 | 0.180 | 0.008 | 0.623 |
| single: colorhist | 0.685 | 0.714 | 0.161 | 0.036 | 0.001 | 0.000 | 0.999 |

Stack − best single AUC -0.005 (95% CI -0.011 to +0.001); recall@FPR5% -0.021 (CI -0.046 to +0.003).

## Held-out (1023 images, different dataset; experts fire_cnn, zeroshot, clip_probe)

| rule | ROC-AUC | PR-AUC | recall@FPR5% | ECE | value score | miss @p* | false alarm @p* |
|---|---|---|---|---|---|---|---|
| stacked meta (calibrated) | 0.999 | 1.000 | 1.000 | 0.028 | 0.555 | 0.000 | 0.445 |
| FM-1 | 1.000 | 1.000 | 1.000 | 0.117 | 0.000 | 0.000 | 1.000 |
| plain mean | 1.000 | 1.000 | 1.000 | 0.148 | 0.000 | 0.000 | 1.000 |
| max | 0.998 | 0.998 | 0.998 | 0.158 | 0.000 | 0.000 | 1.000 |
| single: fire_cnn | 0.954 | 0.973 | 0.776 | 0.237 | 0.000 | 0.000 | 1.000 |
| single: zeroshot | 1.000 | 1.000 | 1.000 | 0.053 | 0.416 | 0.000 | 0.584 |
| single: clip_probe | 0.998 | 0.998 | 0.997 | 0.032 | 0.568 | 0.000 | 0.432 |

Meta weights (standardized): logit_fire_cnn +0.55, logit_zeroshot +0.71, logit_clip_probe +2.21, sd -0.12, range -0.10
