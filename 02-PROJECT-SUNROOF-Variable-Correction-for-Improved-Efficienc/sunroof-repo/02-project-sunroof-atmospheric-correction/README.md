# 02 — Google Project Sunroof 2.0: Multi-Scalar Radiant Energy Mapping

**Domain:** Product Management × Applied Physics × ML Engineering
**Company:** Google (Geo / Sustainability)

---

## The problem

Google's Project Sunroof maps rooftop solar potential for 60M+ homes using satellite imagery, 3D modeling, and ML. Despite its excellent **geometric model** (shading, roof angle, orientation), it treats **atmospheric transparency** as a flat historical average — the Climatological Coefficient (Wc) is a static constant per region.

This creates a systematic "Performance Gap" between predicted and actual solar yield, with cost estimates deviating by up to 50% from market reality. The tool's data hasn't been updated since 2018.

## The solution: Two atmospheric correction layers

Rather than simply refreshing stale data, this case study corrects the **fundamental atmospheric model** by introducing two physics-grounded multipliers:

### Correction I — Pressure Belt Multiplier (Pb)

| Scale | Macro (Global Circulation) |
|-------|---------------------------|
| Physics | Subtropical high-pressure zones (~30° N/S) physically inhibit cloud formation via air subduction |
| Effect | Roofs in these zones get systematically clearer skies than regional averages capture |
| Value | Pb ≈ 1.15 (conservative peak, bounded by Clearness Index limits and Rayleigh scattering) |

### Correction II — Marine Coastal Distance (Mc)

| Scale | Meso (Coastal Microclimate) |
|-------|----------------------------|
| Physics | Sea breeze creates a "Cloud Gap" within 0–5 km of coastline; Inland Convergence Zone (10–20 km) triggers enhanced cloud formation |
| Model | Exponential decay: Mc = α · e^(−D/λ) where D = distance from coast |
| Effect | Coastal properties rewarded, inland convergence zone penalized |

### The unified formula

```
E = (A · η · Isc) × [Wbase · Pb · Mc]
```

Where the corrected **Wc(effective) = Wbase · Pb · Mc** acts as a "digital twin" of the atmosphere above the roof.

---

## Worked example

| Property | Latitude | Coast dist. | Wbase | Pb | Mc | Wc(eff) |
|----------|----------|-------------|-------|-----|-----|---------|
| **Phoenix, AZ** | 33.4°N | ~400 km | 6.5 hrs | 1.13 | 1.00 | **7.35 hrs** |
| **San Diego, CA** | 32.7°N | ~3 km | 5.8 hrs | 1.12 | 1.08 | **7.01 hrs** |
| **Riverside, CA** | 33.9°N | ~80 km | 6.0 hrs | 1.13 | 0.96 | **6.51 hrs** |

Standard model shows Phoenix ≈ Riverside. Corrected model reveals Riverside delivers **11% less** effective solar hours — a difference worth thousands of dollars over a 20-year solar investment.

---

## Strategic value

- **Mapping tool → Financial engine**: Estimates become "bankable" — accurate enough for loan underwriting without site surveys
- **Global scalability**: Both corrections use latitude + coastline distance — available for every point on Earth
- **Competitive moat**: No competing solar calculator applies atmospheric physics at this depth
- **Ecosystem fit**: Feeds directly into Google's Environmental Insights Explorer for city-level decarbonization planning

---

## Files in this case study

| File | Description |
|------|-------------|
| [`docs/case-study.docx`](./docs/case-study.docx) | Full professional write-up with problem analysis, physics-grounded solution, worked examples, strategic value, and risk mitigations |
| [`assets/formula-reference.md`](./assets/formula-reference.md) | Quick-reference formula card with all parameters and correction tables |

---

*Framework: Physics-First Product Strategy | Domain: Applied Atmospheric Science × Product Management*
