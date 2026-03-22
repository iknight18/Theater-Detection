# DRAMYX Pitch Deck Redesign — Design Spec

## Overview

Redesign the DRAMYX / تكتيك المسرح pitch deck from 12 slides to 17 slides. The target audience is theater professionals (directors, critics, festival organizers) and potential investors — non-technical people for whom AI-assisted theater analysis is a new concept. The goal is to create a "wow" effect that demonstrates how technology can serve theater, and to make the case for investment.

## Visual Direction: Cinematic + Smart Data

Dark cinematic slides for story/emotion sections, transitioning to clean light backgrounds for data/proof sections. The contrast itself creates dramatic tension — like moving from stage to control room.

## Design System

### Color Palette

| Token | Value | Usage |
|-------|-------|-------|
| Deep Stage | `#0a0a1a → #1a1a2e` gradient | Story & emotion slides (dark) |
| Navy Mid | `#16213e` | Dark slide secondary |
| Navy Deep | `#0f3460` | Dark slide tertiary |
| Stage Gold | `#c9a84c → #e8c55a` | Accents, highlights, animated counters |
| Warm Ivory | `#faf7f0 → #f0ebe0` | Data & proof slides (light) |
| Text Light | `#b0b8d8` | Body text on dark slides |
| Text Dark | `#333 / #444` | Body text on light slides |
| Muted Gold | `#8a7a5a` | Secondary labels on light slides |

### Typography

- **Headlines / Drama**: Amiri (serif) — used for slide titles and dramatic text
- **Body text**: Tajawal (sans-serif) — used for descriptions, bullets, cards
- **Language**: Arabic RTL throughout, `lang="ar" dir="rtl"`

### Depth & Effects

- **Spotlight glow**: Radial gradient from above (`rgba(201,168,76,0.15-0.2)`) on dark slides, simulating stage lighting
- **Glass morphism cards**: `background:rgba(255,255,255,0.05); backdrop-filter:blur(10px); border:1px solid rgba(201,168,76,0.2)` — used for feature cards on dark slides
- **Elevated cards**: `box-shadow:0 8px 32px rgba(0,0,0,0.08), 0 2px 8px rgba(0,0,0,0.04); border:1px solid rgba(201,168,76,0.15)` — used for cards on light slides
- **Gold bar divider**: `linear-gradient(90deg, transparent, #c9a84c, transparent)` — thematic separator

### Animations

- **Counter animation**: Numbers count up from 0 to target value on slide entry (e.g., 0 → +112%). Duration ~1.5s with easing.
- **Spotlight text reveal**: Text fades in with gold text-shadow glow (`0 0 20px rgba(201,168,76,0.4)`). Duration ~0.8s.
- **Staggered card entry**: Cards/items appear one by one with `translateY(20px) → 0` and `opacity:0 → 1`. Stagger delay ~150ms per item.
- **Slide transitions**:
  - Dark → dark: smooth crossfade (opacity, ~0.4s)
  - Dark → light: "curtain lift" — new slide rises from bottom (`translateY(100vh) → 0`)
  - Light → light: horizontal slide (RTL direction)
  - Light → dark: fade to black, then reveal

### Navigation

Triple input support for real presentation settings:

1. **Keyboard**: ArrowLeft = next, ArrowRight = prev (RTL), plus PageDown/PageUp, Space/Backspace, Home/End
2. **Presenter remote**: Remotes typically send PageDown/PageUp or Arrow key events — covered by keyboard listener
3. **On-screen buttons**: Semi-transparent arrow buttons on left/right edges, visible on hover (CSS `:hover` opacity transition). Not distracting during presentation but accessible when needed.
4. **Touch**: Swipe support for tablet viewing (optional enhancement).

Remove the current invisible 20% click-zone approach — replace with the visible hover buttons.

### Slide Counter

Remains in bottom-left, adapts color to slide background (light text on dark slides, dark text on light slides).

## Slide Structure — 17 Slides

### Transition Mapping Rule

Transitions are determined automatically by the CSS class of the departing and arriving slides (`slide-dark` / `slide-light`). No manual mapping needed — the JS checks both classes and applies the corresponding transition type.

### Counter Slides

Animated counters appear on: Slide 8 (كثافة الحركة +100%, المساحة المستغلة +112%).

---

### Act 1 — The Hook (Mostly dark cinematic; Slide 3 is a light exception for readability)

**Slide 1 — Cover**
- Layout: Centered, dark background with spotlight glow from above
- Content: "المختبر الرقمي الأول لهندسة وسيميولوجيا العرض والوسائط" (tagline), "تكتيك المسرح" (large Amiri title), gold bar, "DRAMYX" (brand), "د. محمد الكشو — م. فارس النفزي"
- Animation: Spotlight fades in, title reveals with glow, elements stagger in

**Slide 2 — The Question (Hook)**
- Layout: Full-bleed background image with dark overlay
- Background image: `../images/Kiss/anas argui - The Kiss - القبلة (of Tchekhov) , Directed by Mounir Argui [x7KCHIOzS7o - 1166x656 - 30m04s].png`
- Content: "ماذا يبقى من العرض المسرحي... بعد أن تُطفأ الأنوار؟"
- Animation: Text spotlight reveal, dramatic pause effect

**Slide 3 — The Problem**
- Layout: Light slide with 3 glass-style or elevated cards
- Content: Three pain points:
  1. نقد مسرحي ذاتي — subjective criticism lacking digital standards
  2. ضياع الإرث الحركي — performance heritage lost after curtain falls
  3. غياب أدوات المقارنة — no tools for measuring adaptation fidelity
- Footer: "كل هذا يؤكد الحاجة الماسة إلى عقل رقمي يوثق ويحلل العلامات المسرحية بموضوعية ودقة"
- Animation: Cards stagger in one by one

**Slide 4 — The Story**
- Layout: Dark slide, split view with two play images side by side in gold-bordered frames
- Content: "مخرج واحد. عرضان. تحوّل جذري." — القبلة (Chekhov, the isolated individual) vs ما يراوش (Maeterlinck, the lost collective)
- Image left: `../images/Kiss/anas argui - The Kiss - القبلة (of Tchekhov) , Directed by Mounir Argui [x7KCHIOzS7o - 1166x656 - 43m31s].png`
- Image right: `../images/Blackout/8015c3a5-fc53-42fb-b4bb-6040a46c1c1d.jpg`
- Footer: "كيف نثبت هذا التحوّل بالأرقام؟"
- Animation: Two frames slide in from opposite sides

### Act 2 — The Reveal (Transition moment)

**Slide 5 — The Insight**
- Layout: Dark slide, centered dramatic text
- Content: "ماذا لو كان بإمكان الآلة... أن ترى ما يراه الناقد؟"
- Sub-text: "تقدير الوضعية • تحليل المسافات • سيمياء الإضاءة" (accessible terms)
- Animation: Spotlight text reveal with gold glow

**Slide 6 — How It Works (NEW — Simplified)**
- Layout: Dark slide, 3 large glass morphism cards horizontally (row-reverse for RTL)
- Content: Accessible 3-step metaphor, no jargon:
  1. **نشاهد** (We Watch) — "نسجّل العرض المسرحي بالكاميرا كما يراه المتفرج" — icon: Unicode 🎥
  2. **نحلّل** (We Analyze) — "الآلة ترصد حركة الممثلين، المسافات بينهم، وتوزيعهم على الركح" — icon: Unicode 🔍
  3. **نكتشف** (We Discover) — "نحصل على خرائط وأرقام تكشف ما لا تراه العين المجرّدة" — icon: Unicode 💡
- Icons: Large Unicode emoji (font-size: 48px) centered above step title. Simple and universally supported.
- Connecting flow: Gold dashed border line (`border-top: 2px dashed var(--gold)`) running behind the cards horizontally, with gold circle nodes at each step. Implemented as a positioned `::before` pseudo-element on the cards container.
- Step numbering: Gold circled numbers (①②③) above each card
- Animation: Steps appear one by one (staggered 300ms delay), connecting line draws via CSS `width` animation

**Slide 7 — Methodology (NEW)**
- Layout: Light slide (first dark→light transition — curtain lift animation). Two-column comparison table layout.
- Content: "المنهجية: لماذا هاتان المسرحيتان؟"
- Left column header: "الاختيار" (The Choice) — why these two plays:
  - Same director (Mounir Argui) → isolates directorial evolution as the variable
  - Two different source texts (Chekhov vs Maeterlinck) → different dramaturgical approaches
- Right column header: "القياس" (The Measurement) — what was measured:
  - وضعيات الأجساد (body positions)
  - المسافات بين الممثلين (inter-actor distances)
  - استغلال الفضاء الركحي (space usage)
  - كثافة الحركة (movement density)
  - الإضاءة (lighting)
- Columns use elevated card style on light background
- Animation: Left column slides in first, right column follows (staggered 200ms)

### Act 3 — The Proof (Light backgrounds, animated data)

**Slide 8 — Space Engineering**
- Layout: Light slide, large diagram image
- Content: "هندسة الفضاء: من العزلة إلى الاكتظاظ"
- Image: `Enhance_this_diagram_its_in_arabic_2k_delpmaspu.png`
- Footer with animated counters: "كثافة الحركة تضاعفت +100% — المساحة المستغلة ارتفعت +112%"
- Animation: Image fades in, counters animate from 0

**Slide 9 — Body & Proximity**
- Layout: Light slide, split view with two charts
- Content: "الجسد والزمن: من المسافة إلى الالتصاق"
- Images: `Enhance_image_in_arabic_bec4eb0ba2.jpeg` + `E9d5f849faac42cf922499cf33fa360fjpg_4b9f6d5d04.jpeg`
- Animation: Charts slide in from opposite sides

**Slide 10 — The Digital Dashboard**
- Layout: Light slide, centered radar chart
- Content: "اللوحة الرقمية الشاملة: من الفردية المعزولة إلى التيه الجماعي"
- Image: `Enhance_arabic_diagram_2345ea7c81.jpeg`
- Footer: "من مسرح المرآة إلى مسرح الاشتباك"
- Animation: Chart scales up from center

**Slide 11 — AI on Stage**
- Layout: Light slide, split view
- Content: "الذكاء الاصطناعي على خشبة المسرح"
- Image left: `../results/with_distances/yolov8/baseline/Kiss/anas argui - The Kiss - القبلة (of Tchekhov) , Directed by Mounir Argui [x7KCHIOzS7o - 1166x656 - 15m42s].png`
- Image right: `Make_diagram_in_arabic_3861df9675.jpeg`
- Footer: "تحليل آلي لحركة الممثلين والمسافات بين الأجساد"
- Animation: Left image with scan-line overlay effect, right chart fades in

### Act 4 — The Vision (Dark for platform/roadmap, light for vision/team, dark closing)

**Slide 12 — DRAMYX Platform**
- Layout: Dark slide, split — mockup image on one side, feature list on other
- Content: "تكتيك المسرح — DRAMYX"
- Features (bullet list): خرائط حرارية للفضاء الركحي, رادار الشخصية, تحليل الإضاءة والوسائط, محرك مقارنة العروض
- Image: `a2296007-bfb6-4504-9ac3-05d46f2b5419.jpg`
- Animation: Glass cards stagger in alongside mockup

**Slide 13 — Use Cases (NEW)**
- Layout: Dark slide, 4 glass morphism cards in a grid
- Content: "من يستفيد من تكتيك المسرح؟"
  1. **المهرجانات** — objective evaluation tools for jury panels
  2. **الجامعات** — teaching tool for theater studies programs
  3. **المخرجون** — self-analysis of staging choices
  4. **الأرشيف الثقافي** — preserving performance heritage digitally
- Animation: Cards stagger in with glass effect

**Slide 14 — Roadmap (NEW)**
- Layout: Dark slide, horizontal timeline with 3 phases
- Content: "خارطة الطريق"
  1. **المرحلة الأولى (2026)** — Research prototype, 2 plays analyzed, publish findings
  2. **المرحلة الثانية (2027)** — Platform MVP, 20+ plays, festival partnerships
  3. **المرحلة الثالثة (2028+)** — Global database, API for researchers, multi-language
- Animation: Timeline draws itself left-to-right (RTL: right-to-left), nodes light up sequentially

**Slide 15 — The Vision**
- Layout: Light slide, 3 vision pillars + team info
- Content: "الرؤية: المرجع العالمي المعتمد"
  - رقمنة المسرح — preserving heritage for future generations
  - تطوير النقد — objective, scientific standards
  - قاعدة بيانات عالمية — digital archive of theatrical performance
- Team: د. محمد الكشو (مخرج وباحث مسرحي), م. فارس النفزي (مهندس ذكاء اصطناعي), مسرح المدينة بتونس
- Animation: Pillars stagger in, team section fades up

**Slide 16 — The Team (NEW — expanded)**
- Layout: Light slide, two elevated cards side by side
- Content:
  - Card 1: **د. محمد الكشو** — مخرج مسرحي وباحث أكاديمي، المشرف العلمي على المشروع. خبرة في الإخراج والسيميولوجيا المسرحية.
  - Card 2: **م. فارس النفزي** — مهندس ذكاء اصطناعي، مسؤول عن تطوير المنصة التقنية وأنظمة التحليل الآلي.
  - Below cards: **المؤسسة**: مسرح المدينة بتونس (institutional affiliation, centered, gold accent)
- Animation: Cards slide in from opposite sides, institution fades up

**Slide 17 — Closing**
- Layout: Dark slide, centered dramatic text
- Content: "لنحوّل سحر المسرح إلى علم باقٍ"
- Contact: feresnefzi18@gmail.com
- Branding: DRAMYX — © 2026
- Animation: Final spotlight reveal, gold glow

## Navigation Implementation

```
Keyboard events to capture:
- ArrowLeft → next slide (RTL)
- ArrowRight → prev slide (RTL)
- PageDown / Space → next slide (presenter remote)
- PageUp / Backspace → prev slide (presenter remote)
- Home → first slide
- End → last slide

On-screen buttons:
- Left edge: "→" arrow (next in RTL), right edge: "←" arrow (prev in RTL)
- Default opacity: 0, hover opacity: 0.6
- Size: ~40px circle, semi-transparent white/dark depending on slide background
- Position: vertically centered, 20px from edge
- Transition: opacity 0.3s ease
```

## Technical Notes

- Single HTML file, self-contained (inline CSS + JS)
- No external dependencies beyond Google Fonts (Amiri, Tajawal)
- Images referenced from current relative paths (existing images in Presentation/ and ../images/, ../results/)
- CSS animations using `@keyframes` — no JS animation libraries
- Counter animation via JS `requestAnimationFrame` on slide entry
- All text in Arabic, RTL layout
- Print styles preserved for PDF export
