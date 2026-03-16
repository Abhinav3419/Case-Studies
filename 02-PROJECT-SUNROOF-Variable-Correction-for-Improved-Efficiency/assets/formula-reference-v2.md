# Formula reference — refined model (v2)

---

## The unified equation

```
E = (A · η · Isc) × [Wbase · Pb · Mc(D, φ)]
```

| Symbol | Name | Unit | Source |
|--------|------|------|--------|
| E | Energy received per day | kWh | Computed |
| A | Solar panel area | m² | Installation spec |
| η | Panel efficiency | Dimensionless (0–1) | Manufacturer spec |
| Isc | Solar constant | ~1.0 kW/m² at surface | Physical constant |
| Wbase | Regional historical sunny hours | Hours/day | NREL / weather data |
| Pb | Pressure Belt Multiplier | Dimensionless | Latitude-derived |
| Mc(D,φ) | Marine Coastal Distance Correction | Dimensionless | Coast distance + zone |

---

## Pb — Pressure Belt Multiplier (unchanged)

| Latitude zone | Regime | Pb |
|--------------|--------|-----|
| 0°–15° | ITCZ / Hadley ascending | 1.00 |
| 15°–25° | Partial subduction | 1.05–1.10 |
| **25°–35°** | **Full subtropical HP** | **1.10–1.15** |
| 35°–60° | Ferrell cell / frontal | 0.95–1.00 |
| 60°+ | Polar cell | 0.85–0.95 |

---

## Mc — REFINED Marine Coastal Distance Correction (v2)

### The refined formula

```
Mc(D, φ) = 1 + α(φ) · e^(−D/λ(φ))
```

Where D = distance from nearest coastline (km), and α(φ) and λ(φ) are **zone-dependent parameters** calibrated against NASA POWER satellite data from 27 global locations.

For D > 300 km: Mc = 1.00 (no marine influence).

### Calibrated parameters

| Zone | Latitude range | α(φ) | λ(φ) km | Physical interpretation |
|------|---------------|------|---------|------------------------|
| **Subtropical HP** | 25°–35° N/S | **−0.040** | **79** | Negative α: subtropical coasts have slight thermal inversion suppressing surface heating; long λ means effect penetrates far inland. Coasts are marginally penalized, convergence zone is correctly captured. |
| **Tropical** | 0°–25° N/S | **+0.025** | **15** | Positive α: sea breeze provides modest cloud-gap bonus at coast; short λ means rapid decay within 15 km — consistent with tropical convective dynamics overriding marine effects quickly. |
| **Mid-latitude** | 35°–60° N/S | **+0.055** | **3** | Positive α: Mediterranean/oceanic coasts get a clearness bonus; very short λ (3 km) reflects that mid-latitude frontal systems dominate beyond the immediate coastline. |
| **Equatorial** | 0°–15° N/S | **+0.015** | **10** | Very weak positive α: ITCZ convection overwhelms coastal effects. Negligible practical impact. |
| **Polar** | 60°+ N/S | **+0.010** | **5** | Minimal coastal effect at high latitudes. Included for model completeness. |

### Key insight from calibration

**Subtropical HP coasts have negative α.** This was unexpected but physically correct — in arid subtropical zones (Phoenix, Riyadh, Marrakech), the deep inland desert has *higher* clearness than the coast because coastal humidity and occasional marine stratus reduce transparency. The old model assumed all coasts benefit — the data shows subtropical arid coasts are actually slightly penalized.

**Tropical and mid-latitude coasts have positive α.** The sea breeze cloud-gap effect is real in these zones but with different penetration depths — tropical effects die within 15 km (convection takes over), while mid-latitude effects are confined to just 3 km from the coastline.

---

## Validation summary

| Metric | Flat baseline (ClearSky × 0.80) | Old model (Pb + fixed Mc) | Refined model (Pb + Mc(D,φ)) |
|--------|--------------------------------|---------------------------|-------------------------------|
| Average error across 20 locations | 9.9% | 7.0% | **6.5%** |
| Relative improvement vs baseline | — | 29% | **34%** |
| Pearson r (Pb×Mc vs actual Kt) | — | 0.73 | 0.73 |
| Data source | — | — | NASA POWER API (27 calibration + 20 validation locations) |

---

## What changed from v1

| Aspect | v1 (Original) | v2 (Refined) |
|--------|--------------|--------------|
| Mc formula | Mc = α · e^(−D/λ) with fixed α, λ | Mc(D,φ) = 1 + α(φ) · e^(−D/λ(φ)) with zone-dependent params |
| α values | Single universal α ≈ 0.05–0.12 | Zone-specific: −0.040 (SubtropHP) to +0.055 (MidLat) |
| λ values | Single universal λ ≈ 10–15 km | Zone-specific: 3 km (MidLat) to 79 km (SubtropHP) |
| Coastal assumption | All coasts benefit (positive bonus) | SubtropHP coasts slightly penalized; Tropical/MidLat coasts benefit |
| Calibration data | None (theoretical) | 27 locations, NASA POWER satellite data |
| Patent strength | Theoretical framework | **Empirically validated framework** |

---

*Validated against NASA POWER satellite irradiance data | March 2026*
*Copyright © 2026 Abhinav Pandey. All rights reserved.*
