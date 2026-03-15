# Feature reference — Quick Card

---

## The core Thesis

Netflix's Algorithms Answer: *"What should you watch?"*
These features answer: *"What should you watch right now, given who you are, what you're feeling, and what's happening around you?"*

---

## Feature matrix

| # | Feature | Context dimension | Data source | Device requirement | Permission needed |
|---|---------|-------------------|-------------|-------------------|-------------------|
| 1 | Gen-Pulse | Identity (generation) | Date of birth + viewing data | None | None |
| 2 | Sense-Stream | Sensory (touch) | Haptic metadata track | Haptic-capable device | Toggle on/off |
| 3 | Atmosphere | Environment (weather) | Weather API (city-level) | Any device | Coarse location |
| 4 | Pulse-Rec | Physiology (stress) | Heart rate + HRV from wearable | Smartwatch/fitness band | HealthKit/Health Connect |

---

## Gen-Pulse badge examples

- "72% of Gen Z binged this in under 48 hours"
- "Millennials and Boomers both rated 4.5+ — rare crossover hit"
- "Trending #1 among Gen X this week"
- "85% of Millennials who started this finished in one weekend"
- "Gen Alpha's most rewatched show this month"

---

## Sense-Stream haptic taxonomy

| Event | Pattern | Duration |
|-------|---------|----------|
| Explosion | Sharp peak + exponential decay: H(t) = Hp · e^(−t/τ) | 400–800ms |
| Punch | Square pulse tap | 50–100ms |
| Rain | Random low-amplitude patter | Continuous |
| Heartbeat tension | Sinusoidal 60–80 BPM | Scene duration |
| Jump scare | Impulse spike | 30–50ms |

---

## Atmosphere weather-to-mood mapping

| Weather | UI effect | Content push |
|---------|-----------|-------------|
| Rainy | Drizzle drops on home screen | Romance, drama, cozy content |
| Sunny | Warm golden light wash | Adventure, comedy, travel |
| Snowy | Gentle snowflakes | Holiday, family, comfort rewatches |
| Stormy | Lightning flicker on edges | Horror, dark thriller |
| Cloudy | Soft muted palette | Indie, documentaries, biopics |

**Override rule:** Animation always plays. Content push only if aligned with user's established preferences.

---

## Pulse-Rec stress detection flow

```
Wearable → HealthKit/Health Connect API
    → Read HR + HRV at app launch
    → Compare to user's personal baseline
    → If HR > baseline + 15 BPM AND HRV depressed
        → Flag session as "stress-detected"
        → Surface "Unwind" content row
    → Binary signal only — no raw health data leaves device
```

---

## Key competitive differentiators

- **Gen-Pulse**: No streaming app segments social proof by generation
- **Sense-Stream**: No streaming platform has a haptic layer (MPEG-I Haptics standard published Jan 2025)
- **Atmosphere**: No streaming app reads weather for personalization
- **Pulse-Rec**: No media app connects health data to content recommendations
