# TRINETRA — detailed comparison tables (every *_compare.md of the final merge)

---
### `F_final/fusion/fusion_compare.md`

SYNTHETIC PAIRING (see docstring). sources=['fire_cnn', 'zeroshot'] fake_frac=0.0

| rule | value score | ECE | miss rate @p* | false-alarm rate @p* |
|---|---|---|---|---|
| fm1 | 0.005 ± 0.001 | 0.184 ± 0.004 | 0.000 ± 0.000 | 0.995 ± 0.001 |
| pharaoh | 0.005 ± 0.001 | 0.192 ± 0.005 | 0.000 ± 0.000 | 0.995 ± 0.001 |
| median | 0.005 ± 0.001 | 0.189 ± 0.003 | 0.000 ± 0.000 | 0.995 ± 0.001 |
| max | 0.002 ± 0.000 | 0.299 ± 0.005 | 0.000 ± 0.000 | 0.998 ± 0.000 |
| p_fire_cnn | 0.014 ± 0.001 | 0.177 ± 0.004 | 0.000 ± 0.000 | 0.985 ± 0.002 |
| p_zeroshot | 0.108 ± 0.028 | 0.151 ± 0.004 | 0.011 ± 0.005 | 0.836 ± 0.003 |


---
### `S_final/stress/stress_s0_compare.md`

# Confuser-aware retraining (leave-one-confuser-set-out) · seed 0

Confuser sets: stress_weather, stress_small_flames, stress_scenes · fire_cnn in stack: True · negative weight 1.0

| held-out confuser | model | FA @0.5 | FA @p* | FA @recall-0.90 thr | DeepFire AUC | DeepFire recall @thr |
|---|---|---|---|---|---|---|
| stress_weather | zeroshot | 0.007 | 0.325 | 0.029 | 1.000 | 1.000 |
| stress_weather | probe_base | 0.266 | 0.839 | 0.365 | 0.998 | 0.997 |
| stress_weather | probe_conf | 0.152 | 0.625 | 0.269 | 0.998 | 0.995 |
| stress_weather | fire_cnn | 0.413 | 1.000 | 0.928 | 0.983 | 1.000 |
| stress_weather | stack_base | 0.116 | 0.709 | 0.248 | 1.000 | 1.000 |
| stress_weather | stack_conf | 0.009 | 0.447 | 0.055 | 1.000 | 1.000 |
| stress_weather | gate probe_conf | FA diff -0.096 (CI -0.130 to -0.055) | AUC drop -0.0006502057613169132 | **PASS** | | |
| stress_weather | gate stack_conf | FA diff -0.193 (CI -0.257 to -0.117) | AUC drop -0.0003209876543209811 | **PASS** | | |
| stress_small_flames | zeroshot | 0.003 | 0.712 | 0.100 | 1.000 | 1.000 |
| stress_small_flames | probe_base | 0.770 | 0.992 | 0.845 | 0.998 | 0.997 |
| stress_small_flames | probe_conf | 0.468 | 0.950 | 0.650 | 0.997 | 0.995 |
| stress_small_flames | fire_cnn | 0.725 | 1.000 | 0.997 | 0.983 | 1.000 |
| stress_small_flames | stack_base | 0.542 | 1.000 | 0.792 | 1.000 | 1.000 |
| stress_small_flames | stack_conf | 0.012 | 0.993 | 0.362 | 1.000 | 1.000 |
| stress_small_flames | gate probe_conf | FA diff -0.195 (CI -0.238 to -0.154) | AUC drop 0.00029629629629635 | **PASS** | | |
| stress_small_flames | gate stack_conf | FA diff -0.430 (CI -0.479 to -0.382) | AUC drop -0.00016460905349791055 | **PASS** | | |
| stress_scenes | zeroshot | 0.010 | 0.242 | 0.031 | 1.000 | 1.000 |
| stress_scenes | probe_base | 0.030 | 0.555 | 0.060 | 0.998 | 0.997 |
| stress_scenes | probe_conf | 0.013 | 0.300 | 0.028 | 0.995 | 0.995 |
| stress_scenes | fire_cnn | 0.084 | 1.000 | 0.738 | 0.983 | 1.000 |
| stress_scenes | stack_base | 0.011 | 0.419 | 0.019 | 1.000 | 1.000 |
| stress_scenes | stack_conf | 0.005 | 0.217 | 0.014 | 1.000 | 1.000 |
| stress_scenes | gate probe_conf | FA diff -0.033 (CI -0.049 to -0.018) | AUC drop 0.00280246913580251 | **PASS** | | |
| stress_scenes | gate stack_conf | FA diff -0.005 (CI -0.013 to +0.003) | AUC drop -2.0576131687155552e-05 | **FAIL** | | |

Mean FA at equal recall: probe 0.423 -> 0.316; stack 0.353 -> 0.143. Admitted (probe): True.


---
### `S_final/stress/stress_s1_compare.md`

# Confuser-aware retraining (leave-one-confuser-set-out) · seed 1

Confuser sets: stress_weather, stress_small_flames, stress_scenes · fire_cnn in stack: True · negative weight 1.0

| held-out confuser | model | FA @0.5 | FA @p* | FA @recall-0.90 thr | DeepFire AUC | DeepFire recall @thr |
|---|---|---|---|---|---|---|
| stress_weather | zeroshot | 0.007 | 0.325 | 0.029 | 1.000 | 1.000 |
| stress_weather | probe_base | 0.266 | 0.839 | 0.372 | 0.998 | 0.997 |
| stress_weather | probe_conf | 0.152 | 0.616 | 0.270 | 0.998 | 0.995 |
| stress_weather | fire_cnn | 0.773 | 1.000 | 0.882 | 0.978 | 0.998 |
| stress_weather | stack_base | 0.099 | 0.750 | 0.261 | 1.000 | 1.000 |
| stress_weather | stack_conf | 0.008 | 0.529 | 0.084 | 1.000 | 1.000 |
| stress_weather | gate probe_conf | FA diff -0.102 (CI -0.139 to -0.058) | AUC drop -0.0006502057613169132 | **PASS** | | |
| stress_weather | gate stack_conf | FA diff -0.177 (CI -0.234 to -0.108) | AUC drop -0.0002839506172840345 | **PASS** | | |
| stress_small_flames | zeroshot | 0.003 | 0.712 | 0.100 | 1.000 | 1.000 |
| stress_small_flames | probe_base | 0.770 | 0.992 | 0.855 | 0.998 | 0.997 |
| stress_small_flames | probe_conf | 0.468 | 0.950 | 0.667 | 0.997 | 0.995 |
| stress_small_flames | fire_cnn | 0.840 | 1.000 | 0.948 | 0.978 | 0.998 |
| stress_small_flames | stack_base | 0.448 | 1.000 | 0.770 | 1.000 | 1.000 |
| stress_small_flames | stack_conf | 0.015 | 0.997 | 0.433 | 1.000 | 1.000 |
| stress_small_flames | gate probe_conf | FA diff -0.188 (CI -0.237 to -0.144) | AUC drop 0.00029629629629635 | **PASS** | | |
| stress_small_flames | gate stack_conf | FA diff -0.337 (CI -0.379 to -0.295) | AUC drop -0.00014814814814823052 | **PASS** | | |
| stress_scenes | zeroshot | 0.010 | 0.242 | 0.031 | 1.000 | 1.000 |
| stress_scenes | probe_base | 0.030 | 0.552 | 0.068 | 0.998 | 0.997 |
| stress_scenes | probe_conf | 0.013 | 0.294 | 0.025 | 0.995 | 0.995 |
| stress_scenes | fire_cnn | 0.605 | 1.000 | 0.846 | 0.978 | 0.998 |
| stress_scenes | stack_base | 0.011 | 0.490 | 0.030 | 1.000 | 1.000 |
| stress_scenes | stack_conf | 0.005 | 0.318 | 0.018 | 1.000 | 1.000 |
| stress_scenes | gate probe_conf | FA diff -0.043 (CI -0.058 to -0.028) | AUC drop 0.00280246913580251 | **PASS** | | |
| stress_scenes | gate stack_conf | FA diff -0.013 (CI -0.023 to -0.003) | AUC drop -2.8806584362217613e-05 | **PASS** | | |

Mean FA at equal recall: probe 0.431 -> 0.321; stack 0.354 -> 0.178. Admitted (probe): True.


---
### `S_final/stress/stress_s2_compare.md`

# Confuser-aware retraining (leave-one-confuser-set-out) · seed 2

Confuser sets: stress_weather, stress_small_flames, stress_scenes · fire_cnn in stack: True · negative weight 1.0

| held-out confuser | model | FA @0.5 | FA @p* | FA @recall-0.90 thr | DeepFire AUC | DeepFire recall @thr |
|---|---|---|---|---|---|---|
| stress_weather | zeroshot | 0.007 | 0.325 | 0.029 | 1.000 | 1.000 |
| stress_weather | probe_base | 0.266 | 0.839 | 0.368 | 0.998 | 0.997 |
| stress_weather | probe_conf | 0.152 | 0.620 | 0.262 | 0.998 | 0.995 |
| stress_weather | fire_cnn | 0.604 | 1.000 | 0.946 | 0.954 | 0.998 |
| stress_weather | stack_base | 0.097 | 0.713 | 0.225 | 0.999 | 1.000 |
| stress_weather | stack_conf | 0.009 | 0.478 | 0.061 | 1.000 | 1.000 |
| stress_weather | gate probe_conf | FA diff -0.106 (CI -0.145 to -0.057) | AUC drop -0.0006502057613169132 | **PASS** | | |
| stress_weather | gate stack_conf | FA diff -0.164 (CI -0.213 to -0.103) | AUC drop -0.0004732510288065761 | **PASS** | | |
| stress_small_flames | zeroshot | 0.003 | 0.712 | 0.100 | 1.000 | 1.000 |
| stress_small_flames | probe_base | 0.770 | 0.992 | 0.850 | 0.998 | 0.997 |
| stress_small_flames | probe_conf | 0.468 | 0.950 | 0.677 | 0.997 | 0.995 |
| stress_small_flames | fire_cnn | 0.855 | 1.000 | 1.000 | 0.954 | 0.998 |
| stress_small_flames | stack_base | 0.480 | 1.000 | 0.750 | 0.999 | 1.000 |
| stress_small_flames | stack_conf | 0.010 | 0.993 | 0.370 | 0.999 | 0.998 |
| stress_small_flames | gate probe_conf | FA diff -0.173 (CI -0.218 to -0.135) | AUC drop 0.00029629629629635 | **PASS** | | |
| stress_small_flames | gate stack_conf | FA diff -0.380 (CI -0.433 to -0.330) | AUC drop -0.00013991769547327948 | **PASS** | | |
| stress_scenes | zeroshot | 0.010 | 0.242 | 0.031 | 1.000 | 1.000 |
| stress_scenes | probe_base | 0.030 | 0.555 | 0.062 | 0.998 | 0.997 |
| stress_scenes | probe_conf | 0.013 | 0.297 | 0.028 | 0.995 | 0.995 |
| stress_scenes | fire_cnn | 0.466 | 1.000 | 0.989 | 0.954 | 0.998 |
| stress_scenes | stack_base | 0.013 | 0.477 | 0.022 | 0.999 | 1.000 |
| stress_scenes | stack_conf | 0.005 | 0.224 | 0.015 | 0.999 | 1.000 |
| stress_scenes | gate probe_conf | FA diff -0.035 (CI -0.050 to -0.021) | AUC drop 0.00280246913580251 | **PASS** | | |
| stress_scenes | gate stack_conf | FA diff -0.007 (CI -0.016 to +0.000) | AUC drop 0.00013991769547327948 | **FAIL** | | |

Mean FA at equal recall: probe 0.427 -> 0.322; stack 0.332 -> 0.149. Admitted (probe): True.


---
### `X_final/crossmodal/crossmodal_s0_compare.md`

# Cross-modal fire fusion · seed 0 · stack on 3410 REAL-paired OOF rows (this session's zeroshot/clip OOF (aligned))

## Video (FireSense, temporal validator window 5, min 3 frames, thr 0.5)

| stream | detect raw | detect validated | FA videos raw | FA videos validated | detected / FA videos (validated) | FA frames |
|---|---|---|---|---|---|---|
| fire_cnn | 0.792 | 0.625 | 0.720 | 0.600 | 15/24 · 15/25 | 646 |
| zeroshot | 1.000 | 0.958 | 0.320 | 0.120 | 23/24 · 3/25 | 117 |
| clip_probe | 1.000 | 1.000 | 0.720 | 0.680 | 24/24 · 17/25 | 771 |
| stack | 1.000 | 1.000 | 0.640 | 0.520 | 24/24 · 13/25 | 624 |
| mean | 1.000 | 1.000 | 0.520 | 0.400 | 24/24 · 10/25 | 437 |
| vote_2of3 | 1.000 | 1.000 | 0.600 | 0.440 | 24/24 · 11/25 | 382 |

Best stream by (detect − FA), validated: **zeroshot**.

## Confusers / held-out sets (false-alarm rate at 0.5 and at p*)

| set | fire_cnn | zeroshot | clip_probe | stack | mean | vote_2of3 |
|---|---|---|---|---|---|---|
| stress_weather (neg 1000, pos 0) | 0.413 / 1.000 | 0.007 / 0.325 | 0.266 / 0.839 | 0.116 / 0.680 | 0.048 / 0.999 | 0.158 / 0.371 |
| stress_small_flames (neg 600, pos 0) | 0.725 / 1.000 | 0.003 / 0.712 | 0.770 / 0.992 | 0.542 / 0.998 | 0.357 / 1.000 | 0.573 / 0.908 |
| stress_scenes (neg 800, pos 0) | 0.084 / 1.000 | 0.010 / 0.242 | 0.030 / 0.555 | 0.011 / 0.389 | 0.009 / 0.988 | 0.014 / 0.184 |
| heldout_firedataset (neg 185, pos 638) | 0.076 / 1.000 | 0.022 / 0.303 | 0.032 / 0.189 | 0.022 / 0.173 | 0.022 / 0.957 | 0.022 / 0.157 |
| heldout_homefire (neg 33, pos 1267) | 0.545 / 1.000 | 0.212 / 0.909 | 0.394 / 0.879 | 0.333 / 0.909 | 0.303 / 1.000 | 0.333 / 0.848 |


---
### `X_final/crossmodal/crossmodal_s1_compare.md`

# Cross-modal fire fusion · seed 1 · stack on 3410 REAL-paired OOF rows (this session's zeroshot/clip OOF (aligned))

## Video (FireSense, temporal validator window 5, min 3 frames, thr 0.5)

| stream | detect raw | detect validated | FA videos raw | FA videos validated | detected / FA videos (validated) | FA frames |
|---|---|---|---|---|---|---|
| fire_cnn | 1.000 | 1.000 | 1.000 | 1.000 | 24/24 · 25/25 | 2035 |
| zeroshot | 1.000 | 0.958 | 0.320 | 0.120 | 23/24 · 3/25 | 117 |
| clip_probe | 1.000 | 1.000 | 0.720 | 0.680 | 24/24 · 17/25 | 771 |
| stack | 1.000 | 1.000 | 0.640 | 0.560 | 24/24 · 14/25 | 622 |
| mean | 1.000 | 1.000 | 0.600 | 0.520 | 24/24 · 13/25 | 596 |
| vote_2of3 | 1.000 | 1.000 | 0.720 | 0.720 | 24/24 · 18/25 | 749 |

Best stream by (detect − FA), validated: **zeroshot**.

## Confusers / held-out sets (false-alarm rate at 0.5 and at p*)

| set | fire_cnn | zeroshot | clip_probe | stack | mean | vote_2of3 |
|---|---|---|---|---|---|---|
| stress_weather (neg 1000, pos 0) | 0.773 / 1.000 | 0.007 / 0.325 | 0.266 / 0.839 | 0.105 / 0.679 | 0.093 / 1.000 | 0.245 / 0.407 |
| stress_small_flames (neg 600, pos 0) | 0.840 / 1.000 | 0.003 / 0.712 | 0.770 / 0.992 | 0.457 / 1.000 | 0.432 / 1.000 | 0.660 / 0.933 |
| stress_scenes (neg 800, pos 0) | 0.605 / 1.000 | 0.010 / 0.242 | 0.030 / 0.555 | 0.011 / 0.420 | 0.013 / 1.000 | 0.030 / 0.196 |
| heldout_firedataset (neg 185, pos 638) | 0.173 / 1.000 | 0.022 / 0.303 | 0.032 / 0.189 | 0.022 / 0.146 | 0.022 / 0.995 | 0.022 / 0.157 |
| heldout_homefire (neg 33, pos 1267) | 0.909 / 1.000 | 0.212 / 0.909 | 0.394 / 0.879 | 0.333 / 0.909 | 0.333 / 1.000 | 0.364 / 0.848 |


---
### `X_final/crossmodal/crossmodal_s2_compare.md`

# Cross-modal fire fusion · seed 2 · stack on 3410 REAL-paired OOF rows (this session's zeroshot/clip OOF (aligned))

## Video (FireSense, temporal validator window 5, min 3 frames, thr 0.5)

| stream | detect raw | detect validated | FA videos raw | FA videos validated | detected / FA videos (validated) | FA frames |
|---|---|---|---|---|---|---|
| fire_cnn | 1.000 | 0.958 | 0.960 | 0.960 | 23/24 · 24/25 | 1805 |
| zeroshot | 1.000 | 0.958 | 0.320 | 0.120 | 23/24 · 3/25 | 117 |
| clip_probe | 1.000 | 1.000 | 0.720 | 0.680 | 24/24 · 17/25 | 771 |
| stack | 1.000 | 1.000 | 0.680 | 0.520 | 24/24 · 13/25 | 642 |
| mean | 1.000 | 1.000 | 0.600 | 0.440 | 24/24 · 11/25 | 595 |
| vote_2of3 | 1.000 | 1.000 | 0.720 | 0.720 | 24/24 · 18/25 | 732 |

Best stream by (detect − FA), validated: **zeroshot**.

## Confusers / held-out sets (false-alarm rate at 0.5 and at p*)

| set | fire_cnn | zeroshot | clip_probe | stack | mean | vote_2of3 |
|---|---|---|---|---|---|---|
| stress_weather (neg 1000, pos 0) | 0.604 / 1.000 | 0.007 / 0.325 | 0.266 / 0.839 | 0.096 / 0.686 | 0.057 / 1.000 | 0.198 / 0.377 |
| stress_small_flames (neg 600, pos 0) | 0.855 / 1.000 | 0.003 / 0.712 | 0.770 / 0.992 | 0.477 / 1.000 | 0.418 / 1.000 | 0.663 / 0.927 |
| stress_scenes (neg 800, pos 0) | 0.466 / 1.000 | 0.010 / 0.242 | 0.030 / 0.555 | 0.013 / 0.440 | 0.011 / 1.000 | 0.025 / 0.193 |
| heldout_firedataset (neg 185, pos 638) | 0.259 / 1.000 | 0.022 / 0.303 | 0.032 / 0.189 | 0.022 / 0.173 | 0.022 / 1.000 | 0.027 / 0.157 |
| heldout_homefire (neg 33, pos 1267) | 0.909 / 1.000 | 0.212 / 0.909 | 0.394 / 0.879 | 0.333 / 0.879 | 0.333 / 1.000 | 0.364 / 0.848 |


---
### `X_final/fusion/fusion_compare.md`

SYNTHETIC PAIRING (see docstring). sources=['fire_cnn', 'zeroshot'] fake_frac=0.0

| rule | value score | ECE | miss rate @p* | false-alarm rate @p* |
|---|---|---|---|---|
| fm1 | 0.005 ± 0.001 | 0.184 ± 0.004 | 0.000 ± 0.000 | 0.995 ± 0.001 |
| pharaoh | 0.005 ± 0.001 | 0.192 ± 0.005 | 0.000 ± 0.000 | 0.995 ± 0.001 |
| median | 0.005 ± 0.001 | 0.189 ± 0.003 | 0.000 ± 0.000 | 0.995 ± 0.001 |
| max | 0.002 ± 0.000 | 0.299 ± 0.005 | 0.000 ± 0.000 | 0.998 ± 0.000 |
| p_fire_cnn | 0.014 ± 0.001 | 0.177 ± 0.004 | 0.000 ± 0.000 | 0.985 ± 0.002 |
| p_zeroshot | 0.108 ± 0.028 | 0.151 ± 0.004 | 0.011 ± 0.005 | 0.836 ± 0.003 |


---
### `X_final/stress/stress_s0_compare.md`

# Confuser-aware retraining (leave-one-confuser-set-out) · seed 0

Confuser sets: stress_weather, stress_small_flames, stress_scenes · fire_cnn in stack: True · negative weight 1.0

| held-out confuser | model | FA @0.5 | FA @p* | FA @recall-0.90 thr | DeepFire AUC | DeepFire recall @thr |
|---|---|---|---|---|---|---|
| stress_weather | zeroshot | 0.007 | 0.325 | 0.029 | 1.000 | 1.000 |
| stress_weather | probe_base | 0.266 | 0.839 | 0.365 | 0.998 | 0.997 |
| stress_weather | probe_conf | 0.152 | 0.625 | 0.269 | 0.998 | 0.995 |
| stress_weather | fire_cnn | 0.413 | 1.000 | 0.928 | 0.983 | 1.000 |
| stress_weather | stack_base | 0.116 | 0.709 | 0.248 | 1.000 | 1.000 |
| stress_weather | stack_conf | 0.009 | 0.447 | 0.055 | 1.000 | 1.000 |
| stress_weather | gate probe_conf | FA diff -0.096 (CI -0.130 to -0.055) | AUC drop -0.0006502057613169132 | **PASS** | | |
| stress_weather | gate stack_conf | FA diff -0.193 (CI -0.257 to -0.117) | AUC drop -0.0003209876543209811 | **PASS** | | |
| stress_small_flames | zeroshot | 0.003 | 0.712 | 0.100 | 1.000 | 1.000 |
| stress_small_flames | probe_base | 0.770 | 0.992 | 0.845 | 0.998 | 0.997 |
| stress_small_flames | probe_conf | 0.468 | 0.950 | 0.650 | 0.997 | 0.995 |
| stress_small_flames | fire_cnn | 0.725 | 1.000 | 0.997 | 0.983 | 1.000 |
| stress_small_flames | stack_base | 0.542 | 1.000 | 0.792 | 1.000 | 1.000 |
| stress_small_flames | stack_conf | 0.012 | 0.993 | 0.362 | 1.000 | 1.000 |
| stress_small_flames | gate probe_conf | FA diff -0.195 (CI -0.238 to -0.154) | AUC drop 0.00029629629629635 | **PASS** | | |
| stress_small_flames | gate stack_conf | FA diff -0.430 (CI -0.479 to -0.382) | AUC drop -0.00016460905349791055 | **PASS** | | |
| stress_scenes | zeroshot | 0.010 | 0.242 | 0.031 | 1.000 | 1.000 |
| stress_scenes | probe_base | 0.030 | 0.555 | 0.060 | 0.998 | 0.997 |
| stress_scenes | probe_conf | 0.013 | 0.300 | 0.028 | 0.995 | 0.995 |
| stress_scenes | fire_cnn | 0.084 | 1.000 | 0.738 | 0.983 | 1.000 |
| stress_scenes | stack_base | 0.011 | 0.419 | 0.019 | 1.000 | 1.000 |
| stress_scenes | stack_conf | 0.005 | 0.217 | 0.014 | 1.000 | 1.000 |
| stress_scenes | gate probe_conf | FA diff -0.033 (CI -0.049 to -0.018) | AUC drop 0.00280246913580251 | **PASS** | | |
| stress_scenes | gate stack_conf | FA diff -0.005 (CI -0.013 to +0.003) | AUC drop -2.0576131687155552e-05 | **FAIL** | | |

Mean FA at equal recall: probe 0.423 -> 0.316; stack 0.353 -> 0.143. Admitted (probe): True.


---
### `X_final/stress/stress_s1_compare.md`

# Confuser-aware retraining (leave-one-confuser-set-out) · seed 1

Confuser sets: stress_weather, stress_small_flames, stress_scenes · fire_cnn in stack: True · negative weight 1.0

| held-out confuser | model | FA @0.5 | FA @p* | FA @recall-0.90 thr | DeepFire AUC | DeepFire recall @thr |
|---|---|---|---|---|---|---|
| stress_weather | zeroshot | 0.007 | 0.325 | 0.029 | 1.000 | 1.000 |
| stress_weather | probe_base | 0.266 | 0.839 | 0.372 | 0.998 | 0.997 |
| stress_weather | probe_conf | 0.152 | 0.616 | 0.270 | 0.998 | 0.995 |
| stress_weather | fire_cnn | 0.773 | 1.000 | 0.882 | 0.978 | 0.998 |
| stress_weather | stack_base | 0.099 | 0.750 | 0.261 | 1.000 | 1.000 |
| stress_weather | stack_conf | 0.008 | 0.529 | 0.084 | 1.000 | 1.000 |
| stress_weather | gate probe_conf | FA diff -0.102 (CI -0.139 to -0.058) | AUC drop -0.0006502057613169132 | **PASS** | | |
| stress_weather | gate stack_conf | FA diff -0.177 (CI -0.234 to -0.108) | AUC drop -0.0002839506172840345 | **PASS** | | |
| stress_small_flames | zeroshot | 0.003 | 0.712 | 0.100 | 1.000 | 1.000 |
| stress_small_flames | probe_base | 0.770 | 0.992 | 0.855 | 0.998 | 0.997 |
| stress_small_flames | probe_conf | 0.468 | 0.950 | 0.667 | 0.997 | 0.995 |
| stress_small_flames | fire_cnn | 0.840 | 1.000 | 0.948 | 0.978 | 0.998 |
| stress_small_flames | stack_base | 0.448 | 1.000 | 0.770 | 1.000 | 1.000 |
| stress_small_flames | stack_conf | 0.015 | 0.997 | 0.433 | 1.000 | 1.000 |
| stress_small_flames | gate probe_conf | FA diff -0.188 (CI -0.237 to -0.144) | AUC drop 0.00029629629629635 | **PASS** | | |
| stress_small_flames | gate stack_conf | FA diff -0.337 (CI -0.379 to -0.295) | AUC drop -0.00014814814814823052 | **PASS** | | |
| stress_scenes | zeroshot | 0.010 | 0.242 | 0.031 | 1.000 | 1.000 |
| stress_scenes | probe_base | 0.030 | 0.552 | 0.068 | 0.998 | 0.997 |
| stress_scenes | probe_conf | 0.013 | 0.294 | 0.025 | 0.995 | 0.995 |
| stress_scenes | fire_cnn | 0.605 | 1.000 | 0.846 | 0.978 | 0.998 |
| stress_scenes | stack_base | 0.011 | 0.490 | 0.030 | 1.000 | 1.000 |
| stress_scenes | stack_conf | 0.005 | 0.318 | 0.018 | 1.000 | 1.000 |
| stress_scenes | gate probe_conf | FA diff -0.043 (CI -0.058 to -0.028) | AUC drop 0.00280246913580251 | **PASS** | | |
| stress_scenes | gate stack_conf | FA diff -0.013 (CI -0.023 to -0.003) | AUC drop -2.8806584362217613e-05 | **PASS** | | |

Mean FA at equal recall: probe 0.431 -> 0.321; stack 0.354 -> 0.178. Admitted (probe): True.


---
### `X_final/stress/stress_s2_compare.md`

# Confuser-aware retraining (leave-one-confuser-set-out) · seed 2

Confuser sets: stress_weather, stress_small_flames, stress_scenes · fire_cnn in stack: True · negative weight 1.0

| held-out confuser | model | FA @0.5 | FA @p* | FA @recall-0.90 thr | DeepFire AUC | DeepFire recall @thr |
|---|---|---|---|---|---|---|
| stress_weather | zeroshot | 0.007 | 0.325 | 0.029 | 1.000 | 1.000 |
| stress_weather | probe_base | 0.266 | 0.839 | 0.368 | 0.998 | 0.997 |
| stress_weather | probe_conf | 0.152 | 0.620 | 0.262 | 0.998 | 0.995 |
| stress_weather | fire_cnn | 0.604 | 1.000 | 0.946 | 0.954 | 0.998 |
| stress_weather | stack_base | 0.097 | 0.713 | 0.225 | 0.999 | 1.000 |
| stress_weather | stack_conf | 0.009 | 0.478 | 0.061 | 1.000 | 1.000 |
| stress_weather | gate probe_conf | FA diff -0.106 (CI -0.145 to -0.057) | AUC drop -0.0006502057613169132 | **PASS** | | |
| stress_weather | gate stack_conf | FA diff -0.164 (CI -0.213 to -0.103) | AUC drop -0.0004732510288065761 | **PASS** | | |
| stress_small_flames | zeroshot | 0.003 | 0.712 | 0.100 | 1.000 | 1.000 |
| stress_small_flames | probe_base | 0.770 | 0.992 | 0.850 | 0.998 | 0.997 |
| stress_small_flames | probe_conf | 0.468 | 0.950 | 0.677 | 0.997 | 0.995 |
| stress_small_flames | fire_cnn | 0.855 | 1.000 | 1.000 | 0.954 | 0.998 |
| stress_small_flames | stack_base | 0.480 | 1.000 | 0.750 | 0.999 | 1.000 |
| stress_small_flames | stack_conf | 0.010 | 0.993 | 0.370 | 0.999 | 0.998 |
| stress_small_flames | gate probe_conf | FA diff -0.173 (CI -0.218 to -0.135) | AUC drop 0.00029629629629635 | **PASS** | | |
| stress_small_flames | gate stack_conf | FA diff -0.380 (CI -0.433 to -0.330) | AUC drop -0.00013991769547327948 | **PASS** | | |
| stress_scenes | zeroshot | 0.010 | 0.242 | 0.031 | 1.000 | 1.000 |
| stress_scenes | probe_base | 0.030 | 0.555 | 0.062 | 0.998 | 0.997 |
| stress_scenes | probe_conf | 0.013 | 0.297 | 0.028 | 0.995 | 0.995 |
| stress_scenes | fire_cnn | 0.466 | 1.000 | 0.989 | 0.954 | 0.998 |
| stress_scenes | stack_base | 0.013 | 0.477 | 0.022 | 0.999 | 1.000 |
| stress_scenes | stack_conf | 0.005 | 0.224 | 0.015 | 0.999 | 1.000 |
| stress_scenes | gate probe_conf | FA diff -0.035 (CI -0.050 to -0.021) | AUC drop 0.00280246913580251 | **PASS** | | |
| stress_scenes | gate stack_conf | FA diff -0.007 (CI -0.016 to +0.000) | AUC drop 0.00013991769547327948 | **FAIL** | | |

Mean FA at equal recall: probe 0.427 -> 0.322; stack 0.332 -> 0.149. Admitted (probe): True.


---
### `dir__work/fire_meta_fusion_s0_compare.md`

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


---
### `dir__work/fire_meta_fusion_s1_compare.md`

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


---
### `dir__work/fire_meta_fusion_s2_compare.md`

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


---
### `repo/geo_fusion/geo_fusion_s0_compare.md`

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


---
### `repo/geo_fusion/geo_fusion_s1_compare.md`

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


---
### `repo/geo_fusion/geo_fusion_s2_compare.md`

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

