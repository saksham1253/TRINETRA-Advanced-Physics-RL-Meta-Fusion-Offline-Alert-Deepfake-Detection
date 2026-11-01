# Derivation B-05 — Aliasing-aware flicker-band feature

Class B (robustified extension). Phase P7 · WS1a · RESEARCH-ONLY (paper derivation; no code).
Parent: **EF-08 (flame puffing frequency $f\approx1.5\,D^{-1/2}$)**. Supporting physics: Nyquist–Shannon
sampling. Weakness targeted: the puffing band (~1.5–5 Hz for $D\in[0.1,1]$ m) is **under-sampled / aliased
by low-frame-rate CCTV** (10–15 fps), so a naive FFT of the pixel-intensity time series reports a WRONG
apparent frequency and the physics feature becomes misleading. Quota cross-refs: Cetegen & Ahmed flicker
[11]; swirl/wind band-broadening [13]; derivative/signal-fidelity caution [33].

## 1. Set-up
A flame region's mean brightness oscillates near the true puffing frequency $f_0(D)=1.5\,D^{-1/2}$
(EF-08). A camera samples at frame rate $f_s$ (fps). Sampling maps any true frequency $f_0$ to an OBSERVED
(aliased) frequency $f_{obs}$ in the baseband $[0, f_s/2]$ (Nyquist).

## 2. Aliasing relation (the correction)
For ideal uniform sampling, the observed frequency is the fold of $f_0$ about multiples of $f_s$:
$$ f_{obs} = \big|\, f_0 - f_s\,\mathrm{round}(f_0/f_s)\,\big| . $$
Equivalently $f_{obs}=|((f_0+f_s/2)\bmod f_s)-f_s/2|$. The **forward map** $f_0\mapsto f_{obs}$ is many-to-one:
multiple true frequencies $\{f_0^{(k)} = |f_{obs} + k f_s|,\ k=0,1,2,\dots\}$ all alias to the same $f_{obs}$.
So from one $f_{obs}$ alone the true $f_0$ is NOT identifiable when $f_0>f_s/2$.

## 3. Robustified feature (what we actually compute)
Instead of "estimate $f_0$ from a single FFT peak", B-05 does a **physics-constrained consistency test**:
1. Predict the plausible true-frequency set from EF-08 over the credible size range
   $D\in[D_{min},D_{max}]$: $\;\mathcal F_0=[1.5\,D_{max}^{-1/2},\,1.5\,D_{min}^{-1/2}]$.
2. Map that band THROUGH the camera: $\mathcal F_{obs}=\{\,\mathrm{alias}(f_0,f_s): f_0\in\mathcal F_0\,\}$
   (a union of folded sub-bands, computed from §2).
3. Feature = energy of the measured spectrum inside $\mathcal F_{obs}$ divided by total band energy
   (a dimensionless "flicker-consistency" score in $[0,1]$), plus a flag when $f_s<2f_{0,max}$ (aliasing
   regime) so downstream logic knows $f_0$ is unidentifiable and must not be reported as a frequency.
4. Mitigations enabled by the derivation: raise $f_s$ above $2f_{0,max}$ where possible; use **non-uniform /
   multi-rate sampling** (two cameras or jittered capture) to break the alias degeneracy and recover $f_0$.

## 4. Dimensional check
All terms are frequencies [Hz]; $\mathrm{alias}(\cdot)$ maps Hz→Hz into $[0,f_s/2]$; the consistency score
is an energy ratio (dimensionless) ✓.

## 5. Reduction to parent (REQUIRED)
As $f_s\to\infty$ (or any $f_s>2f_{0,max}$, the non-aliased regime): $\mathrm{round}(f_0/f_s)=0$ ⇒
$f_{obs}=f_0$, the forward map becomes the identity, $\mathcal F_{obs}=\mathcal F_0$, and the consistency
feature reduces to "is the measured peak at the EF-08 frequency?" — i.e. **B-05 → EF-08 exactly when the
sampling rate is adequate.** ✓

## 6. How it enters the system
A camera/IR flicker feature for flame-vs-nuisance (moving person, headlight, swaying foliage) that is HONEST
about aliasing: it reports a consistency score + an identifiability flag, never a fabricated frequency.
Enters as a soft feature with fallback = ignore flicker when the aliasing flag is set.

## 7. Validation plan & falsification
- Validate against published puffing-frequency data ([11]) resampled at CCTV rates (10/15/25/30 fps) to
  confirm the alias map; build-gate: the consistency feature must separate flame from matched nuisance
  motion better than a raw-FFT-peak feature on held-out video. Note [13]: swirl/wind BROADEN the band — the
  feature uses a band, not a line, which absorbs this.
- **Falsified if:** the alias map does not predict observed FFT peaks of real flicker video at low fps, OR
  the consistency feature gives no separation improvement over raw-FFT.

## 8. Honesty
EF-08 coefficient 1.5 is [coeff-verify]. No performance claim (Rule 16); build-time validation required.
