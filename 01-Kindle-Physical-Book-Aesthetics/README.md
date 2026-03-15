# 01 — Amazon Kindle: Physical Book Aesthetics

**Problem Statement:** *"You are the PM for Amazon Kindle. How would you use data to build a better reading experience for students?"*

**Main Strategy:** Instead of purely functional improvements, this solution focuses on bridging the emotional and sensory gap between physical books and digital reading — using data-driven features that simulate tactile, temporal, and auditory qualities of real paper.

---

## Solution summary

### Target user
University undergraduates (18–30) — highest growth potential, highest churn, strongest attachment to physical books.

### Core insight
Reading is an *embodied* experience. Cognitive science shows that tactile feedback, visual aging, and auditory cues strengthen memory encoding and emotional attachment. Kindle can replicate these digitally.

### Six proposed features

| # | Feature | What it does | Data signal |
|---|---------|-------------|-------------|
| 1 | **Drop-impact wrinkling** | Accelerometer detects drops; pages accumulate wrinkle textures and dirt marks | Impact events, cumulative drop count |
| 2 | **Time-based yellowing** | Page color shifts from white → ivory → yellow based on real time since first open | First-open timestamp, reading hours |
| 3 | **Ink bleed-through** | Annotations create faint mirror-image impressions on adjacent pages | Annotation coordinates, pen pressure |
| 4 | **Page-turn sound** | Synthesized paper-rustling sound varies with swipe speed and page position | Swipe velocity, page ratio |
| 5 | **Functional thickness bar** | Visual spine shows read vs. unread proportion; click to jump to any page | Page count, current position |
| 6 | **Gravity orientation** | Flipping the tablet flips the book — no auto-correction, like a real object | Gyroscope/accelerometer data |

### Prioritization (RICE)

| Priority | Features | Timeline |
|----------|----------|----------|
| **P0 — Ship first** | Page-turn sound + Page yellowing | Weeks 1–3 |
| **P1 — Next sprint** | Book thickness + Drop wrinkling | Weeks 4–8 |
| **P2 — Backlog** | Ink bleed-through + Gravity orientation | Weeks 9–14 |

### North star metric
**Weekly active reading minutes** (student cohort) — target +15% within 90 days.

---

## Files in this case study

**[>>> Open live prototype <<<](https://abhinav3419.github.io/Case-Studies/01-Kindle-Physical-Book-Aesthetics/prototype/index.html)**

| File | Description |
|------|-------------|
| [`docs/case-study.docx`](./docs/case-study.docx) | Full professional write-up (8 pages) with exec summary, feature details, RICE table, metrics, risks, roadmap, and interview presentation guide |
| [`prototype/index.html`](./prototype/index.html) | Interactive browser prototype — demo all 6 features live |
| [`assets/feature-summary.md`](./assets/feature-summary.md) | Quick-reference one-pager for interview revision |

---

## How to use the prototype

1. Open `prototype/index.html` in any modern browser
2. Click each button to demo the features:
   - **Drop tablet** — watch wrinkles and edge wear accumulate
   - **Turn page** — hear the synthesized paper sound, see thickness bar update
   - **Scribble note** — see ink bleed-through on the adjacent page
   - **Flip tablet** — gravity-consistent orientation change
3. Leave it open — page color ages in real time (watch the stats dashboard)

---



*Framework: CIRCLES + RICE | Domain: Product Management | Company: Amazon*
