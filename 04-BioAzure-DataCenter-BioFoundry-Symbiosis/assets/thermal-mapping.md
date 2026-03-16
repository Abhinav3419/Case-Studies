# Thermal mapping — quick reference

---

## The thermal match

```
Data Center Output:  45–50°C  (liquid-cooled GPU waste heat)
                        ↓
                  [Plate Heat Exchanger — 90%+ efficiency]
                        ↓
Bio-Foundry Input:  30–40°C  (bioreactor incubation, media prep, HVAC)
```

**No heat pump needed for core processes.** District heating requires a heat pump to boost to 60–75°C. Bio-foundries don't.

---

## Process-level alignment

| Process | Temp needed | DC heat (45–50°C) | Direct match? | Heat pump? |
|---------|------------|-------------------|--------------|-----------|
| Bioreactor incubation | 30–37°C | YES | DIRECT | No |
| Media preparation | 30–40°C | YES | DIRECT | No |
| Seed train | 30–37°C | YES | DIRECT | No |
| Cleanroom HVAC | 20–25°C | YES | DIRECT | No |
| Purification (UF/DF) | 25–35°C | YES | DIRECT | No |
| Spray-drying inlet | 40–80°C | PARTIAL | Lower range only | Small boost for upper |
| CIP/SIP cleaning | 60–80°C | PRE-HEAT | DC pre-heats to 50°C | Yes (+15–30°C) |

**Score: 5/7 direct, 2/7 partial** — vs district heating where 0/1 is direct (always needs heat pump)

---

## Why this beats district heating

| Factor | District heating | Bio-foundry |
|--------|-----------------|-------------|
| Temperature gap | 15–30°C boost needed | 0°C gap (direct use) |
| Heat pump CAPEX | $2–5M per MW thermal | $0 for core processes |
| Annual load factor | ~50% (seasonal) | ~95% (24/7/365) |
| Revenue predictability | Weather-dependent | Contracted PPA |
| Piping distance | 1–5 km typical | 50–200 meters (co-located) |

---

## Financial snapshot (20 MW IT + 5,000 m³ bio-foundry)

| Line item | Annual impact |
|-----------|--------------|
| Bio-foundry heating cost saved | $1.7M–$3.2M |
| DC cooling OPEX saved | $1.5M–$3M |
| DC heat revenue (thermal PPA) | $0.8M–$1.5M |
| **Combined net benefit** | **$3M–$6M/year** |

---

*Copyright © 2026 Abhinav Pandey. All rights reserved.*
