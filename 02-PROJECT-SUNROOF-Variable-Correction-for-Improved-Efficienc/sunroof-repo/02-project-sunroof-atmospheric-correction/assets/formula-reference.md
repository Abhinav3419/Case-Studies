# Formula reference — quick card

---

## The core equation

```
E = (A · η · Isc) × [Wbase · Pb · Mc]
```

| Symbol | Name | Unit | Source |
|--------|------|------|--------|
| E | Energy received per day | kWh | Computed |
| A | Solar panel area | m² | Installation spec |
| η | Panel efficiency | Dimensionless (0–1) | Manufacturer spec |
| Isc | Solar constant | ~1.0 kW/m² at surface | Physical constant |
| Wbase | Regional historical sunny hours | Hours/day | NREL / weather data |
| Pb | Pressure Belt Multiplier | Dimensionless | Latitude-derived |
| Mc | Marine Coastal Distance Correction | Dimensionless | Coastline distance-derived |

---

## Pb — Pressure Belt Multiplier

Based on roof's latitudinal position within Earth's global circulation cells.

| Latitude zone | Regime | Pb |
|--------------|--------|-----|
| 0°–15° | ITCZ / Hadley ascending | 1.00 |
| 15°–25° | Partial subduction | 1.05–1.10 |
| **25°–35°** | **Full subtropical HP** | **1.10–1.15** |
| 35°–60° | Ferrel cell / frontal | 0.95–1.00 |
| 60°+ | Polar cell | 0.85–0.95 |

**Why 1.15 max?** Bounded by Clearness Index (Kt) atmospheric limits — accounts for Rayleigh scattering and Airmass attenuation.

---

## Mc — Marine Coastal Distance Correction

Exponential decay model: **Mc = α · e^(−D/λ)**

| Parameter | Definition |
|-----------|-----------|
| α | Max coastal bonus (region-specific, typically 1.05–1.12) |
| D | Distance from nearest coastline (km) |
| λ | Decay constant (km) — attenuation rate |

| Distance | Effect | Mc |
|----------|--------|-----|
| 0–5 km | Sea breeze cloud gap (suppressed clouds) | 1.05–1.12 |
| 5–10 km | Transitional | ~1.00 |
| 10–20 km | Inland convergence zone (enhanced clouds) | 0.92–0.98 |
| 20+ km | No marine influence | 1.00 |

---

## Key insight

**Wc(effective) = Wbase · Pb · Mc**

This corrected Wc is a "digital twin" of the atmosphere above the roof. It captures:
- Macro-scale planetary circulation dynamics (Pb)
- Meso-scale coastal microclimate effects (Mc)

Both use only latitude and coastline distance — data available for every coordinate on Earth — making the model globally scalable with zero local infrastructure requirements.
