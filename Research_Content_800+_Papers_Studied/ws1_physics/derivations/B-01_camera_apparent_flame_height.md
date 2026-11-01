# Derivation B-01 — Camera-observed apparent flame height through smoke

Class B (robustified extension). Phase P7 · WS1a · RESEARCH-ONLY (paper derivation; no code).
Parents: **EF-01 (Heskestad flame height)**, **EF-07 (Beer–Lambert extinction)**, supporting **EF-09**.
Weakness targeted: EF-01 gives a PHYSICAL flame height $L$ from $(\dot Q,D)$, but a camera measures a
flame extent in PIXELS, biased by (i) perspective projection, (ii) partial obscuration by intervening smoke
(the flame top fades before the base), and (iii) unknown $\dot Q,D$. We derive the APPARENT (observable)
height and invert it with explicit uncertainty. Quota cross-refs: Heskestad [1]; Zukoski $Q^*$/virtual
origin [3]; Beer–Lambert + $K_m$ [8]; Jin visibility $V=C/\sigma$ [7]; IR radiometry [10].

## 1. Projection: physical height → pixels
Pinhole camera, focal length $f$ [px], flame at standoff $R$ [m], optical axis ⟂ flame plane:
$$ h_{px}=\frac{f\,L}{R}, \qquad L=\frac{R}{f}\,h_{px}. $$
With tilt angle $\theta$ of the flame axis to the image plane, the visible projected height is
$L_{proj}=L\cos\theta$ (upper bound $L$ at $\theta=0$). So uncorrected pixel height underestimates $L$ by
$\cos\theta$ and scales with the (often unknown) $R/f$.

## 2. Obscuration: how smoke truncates the apparent flame top
Let a smoke column of extinction coefficient $\sigma=K_m m_s$ (EF-07) lie between flame and camera with
path length $\ell(z)$ increasing toward the (higher, smokier) flame top. The transmitted contrast of the
flame against background at height $z$ is
$$ \mathcal C(z)=\mathcal C_0(z)\,e^{-\sigma\,\ell(z)} . $$
A detector/threshold declares "flame present" where $\mathcal C(z)\ge \mathcal C_{th}$. The APPARENT flame
top $z_{app}$ is the highest $z$ meeting this, i.e. the solution of
$$ \mathcal C_0(z_{app})\,e^{-\sigma \ell(z_{app})}=\mathcal C_{th}. $$
Hence the apparent height $L_{app}=z_{app}-z_{base}\le L$, with the deficit growing with $\sigma$ (denser/
darker smoke truncates more). Using Jin's law $V=C/\sigma$ [7], the obscuration scale is the visibility $V$:
when $\ell\sim V$, contrast falls to the threshold — a compact way to parameterize the truncation.

## 3. Forward model and inversion with uncertainty
Combine §1–§2 and EF-01 ($L=0.235\dot Q^{2/5}-1.02D$):
$$ h_{px}=\frac{f}{R}\,\big[\underbrace{(0.235\dot Q^{2/5}-1.02D)}_{EF\text{-}01}\cos\theta - \Delta_{smoke}(\sigma,\ell)\big], $$
where $\Delta_{smoke}\ge0$ is the top-truncation from §2. Because $\dot Q,D,\theta,\sigma,R/f$ are uncertain,
B-01 does NOT output a point $\dot Q$; it outputs a POSTERIOR / interval:
- treat $(\dot Q,D,\theta,\sigma,R/f)$ with priors (dimensionless $Q^*$ prior from Zukoski [3] where $R,D$
  unknown), propagate to $h_{px}$, and invert to a credible interval for $L$ (and, if $R/f$ known from
  calibration, for $\dot Q$). The width of the interval is the honest statement of what a single camera
  can and cannot say.

## 4. Dimensional check
$h_{px}=fL/R$: $[\text{px}]=[\text{px}]\cdot[\text{m}]/[\text{m}]$ ✓. $\sigma\ell$ dimensionless
($[m^{-1}][m]$) ✓. $\Delta_{smoke}$ in metres (a height deficit) ✓. EF-01 terms in metres ✓.

## 5. Reduction to parent (REQUIRED)
Set no smoke ($\sigma\to0 \Rightarrow \Delta_{smoke}\to0$), head-on view ($\theta\to0\Rightarrow\cos\theta
\to1$), and known calibration $R/f$. Then $h_{px}=(f/R)\,(0.235\dot Q^{2/5}-1.02D)$ and inverting gives
exactly $L=0.235\dot Q^{2/5}-1.02D$ — **B-01 → EF-01 in the clear-air, head-on, calibrated limit.** ✓

## 6. How it enters the system
A physics CONSISTENCY CHECK / feature for vision: does the detected flame's pixel extent, given smoke
obscuration and plausible $\dot Q^*$, agree with EF-01? Flags implausible "flames" (reflections, signage)
and gives a smoke-truncation-aware size cue. Soft feature; fallback = raw detector box when inputs unknown.

## 7. Validation plan & falsification
- Validate on lab flame-height video with measured $\dot Q,D$ (and a smoke-obscuration case) — predicted vs
  measured apparent height; build-gate vs bare EF-01 pixel-mapping. Extinction side validated with $K_m$
  measurements [8].
- **Falsified if:** apparent-height data are not better explained by EF-01+projection+extinction than by
  EF-01+projection alone, OR the truncation term shows no dependence on $\sigma$.

## 8. Honesty
Coefficients inherit EF-01/EF-07 [coeff-verify]. No performance claim (Rule 16). A single passive camera is
fundamentally limited (unknown $R,\dot Q$) — the output is an interval, not a number. Expert review required.
