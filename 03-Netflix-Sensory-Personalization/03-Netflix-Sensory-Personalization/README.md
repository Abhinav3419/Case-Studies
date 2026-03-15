# 03 — Netflix Sensory Personalization: Four Context-Aware Features Beyond the Algorithm

**Domain:** Product Management × Behavioral Psychology × Sensor Engineering
**Company:** Netflix

---

## The Problem Statement:

Netflix's recommendation engine is world-class — collaborative filtering, content-based filtering, contextual bandits, reinforcement learning, and graph neural networks. These algorithms save Netflix over $1 billion annually in subscriber retention.

But every one of them operates exclusively within the **digital content-interaction layer** — they analyze what you watched, when you paused, what you searched for. They do not consider the **physical, environmental, or physiological context** surrounding the viewer at the moment of decision.

## The Solution: Four context-aware features

### Feature I — Gen-Pulse (Generational social proof engine)

| What it does | Surfaces real-time generational viewing analytics as social proof badges |
|---|---|
| Example | "72% of Gen Z binged this in under 48 hours" |
| Data source | Existing date-of-birth + viewing behavior data |
| Why it's new | No streaming app segments social proof by generational cohort |

### Feature II — Sense-Stream (Scene-synced haptic feedback)

| What it does | Delivers tactile sensations (explosions, punches, rain) synced to on-screen events |
|---|---|
| Model | Exponential decay: H(t) = H_peak · e^(−t/τ) |
| Data source | Haptic metadata track encoded alongside video stream |
| Why it's new | No streaming platform has a haptic layer. 4.1B haptic-equipped devices already exist. |

### Feature III — Atmosphere (Weather-responsive UI)

| What it does | Reads local weather and adapts home screen with ambient animations + mood-aligned suggestions |
|---|---|
| Example | Rainy weather → subtle drizzle animation + romantic/cozy content surfaced |
| Override | If user dislikes the suggested genre, animation still plays but content push is suppressed |
| Why it's new | No streaming app reads weather data for personalization |

### Feature IV — Pulse-Rec (Biometric mood sensing)

| What it does | Reads stress indicators from wearables; surfaces calming/comedic content when stress is detected |
|---|---|
| Data source | Heart rate + HRV from Apple Watch / Fitbit / Garmin via HealthKit / Health Connect APIs |
| Privacy | On-device processing only. Netflix servers receive only binary "stress: true/false" — never raw health data |
| Why it's new | No streaming or media app connects health data to content recommendations |

---

## Prioritization (RICE)

| Priority | Feature | Rationale |
|----------|---------|-----------|
| **P0** | Gen-Pulse | 100% existing data, no permissions needed, ships in one A/B cycle |
| **P1** | Atmosphere | Lightweight weather API, independent UI layer, no privacy concerns |
| **P1** | Sense-Stream | Requires haptic metadata authoring but leverages existing device hardware |
| **P2** | Pulse-Rec | ~25% wearable penetration currently; ship after context-aware paradigm is proven |

## North star metric

**Monthly active engagement hours per subscriber** — target +8% within 90 days of Gen-Pulse launch.

---

## Files in this case study

| File | Description |
|------|-------------|
| [`docs/case-study.docx`](./docs/case-study.docx) | Full professional write-up with problem analysis, four feature specifications, behavioral science backing, RICE prioritization, metrics, and risk mitigations |
| [`assets/feature-reference.md`](./assets/feature-reference.md) | Quick-reference card for all four features |

---

*Framework: CIRCLES + RICE + Behavioral Psychology | Domain: Product Management × Sensor Engineering*
