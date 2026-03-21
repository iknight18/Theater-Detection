# DRAMYX Pitch Deck — Design Spec

## Overview

An Arabic pitch deck (12 slides, ~10 min) for presenting DRAMYX / تكتيك المسرح at theater/arts and academic events. The hidden goal is to attract investors through credibility, not a direct ask.

**Approach:** Hybrid "Dramatic Data" — cinematic storytelling opening, real AI data as the reveal, grand vision closing.

**Audience:** Theater professionals, festival organizers, cultural institutions, researchers, cultural ministry stakeholders.

**Tone:** Elegant, authoritative, culturally grounded. Not a startup pitch — a research presentation that happens to unveil a powerful platform.

## Design System

- **Color palette:** Navy/dark blue (#1a1a2e, #16213e) for cinematic slides, warm white (#faf7f3) for data slides, gold (#c9a84c) for accents
- **Typography:** Amiri (Google Fonts) for Arabic headings, Tajawal for body text
- **Direction:** RTL throughout
- **Alternating pattern:** Dark cinematic slides (1, 2, 4, 5, 10, 12) ↔ Light data slides (3, 6, 7, 8, 9, 11)
- **Format:** Single self-contained HTML file with embedded slide navigation

## Slide-by-Slide Spec

### Slide 1 — الغلاف (Cover)
- **Type:** Dark
- **Content:**
  - "تكتيك المسرح" large heading
  - "DRAMYX" subtitle
  - "المختبر الرقمي الأول لهندسة وسيميولوجيا العرض والوسائط"
  - Authors: د. محمد الكشو — م. فارس النفزي
  - Gold divider bar
- **Image:** None — pure typographic design
- **Duration:** ~15s

### Slide 2 — الافتتاح / Hook
- **Type:** Dark with image overlay
- **Content:**
  - Large centered text: "ماذا يبقى من العرض المسرحي... بعد أن تُطفأ الأنوار؟"
  - Nothing else — the question and the image
- **Image:** `images/Kiss/anas argui - The Kiss - القبلة (of Tchekhov) , Directed by Mounir Argui [x7KCHIOzS7o - 1166x656 - 30m04s].png` with dark overlay (good wide stage shot with separated actors)
- **Duration:** ~30s

### Slide 3 — المشكلة
- **Type:** Light
- **Content:** 3 gold-bordered cards:
  1. **نقد ذاتي:** النقد المسرحي يفتقر لمعايير رقمية موضوعية
  2. **ضياع الإرث الحركي:** العروض تفقد قيمتها التوثيقية فور انتهائها
  3. **غياب المقارنة:** لا أدوات لقياس التحولات بين العروض
- **Footer:** "كل هذا يؤكد الحاجة إلى عقل رقمي يوثق ويحلل"
- **Image:** None
- **Duration:** ~45s

### Slide 4 — القصة (The Story)
- **Type:** Dark
- **Content:**
  - Header: "مخرج واحد. عرضان. تحوّل جذري."
  - Split layout:
    - Right: "القبلة" — تشيخوف — الفرد المنعزل + `images/Kiss/anas argui - The Kiss - القبلة (of Tchekhov) , Directed by Mounir Argui [x7KCHIOzS7o - 1166x656 - 43m31s].png` (ensemble on stage)
    - Left: "ما يراوش" — ميترلينك — الجماعة التائهة + `images/Blackout/8015c3a5-fc53-42fb-b4bb-6040a46c1c1d.jpg` (clustered group with blue lighting)
  - Footer: "كيف نثبت هذا التحوّل بالأرقام؟"
- **Duration:** ~60s

### Slide 5 — الكشف (The Reveal)
- **Type:** Dark, dramatic
- **Content:**
  - Large centered text: "ماذا لو كان بإمكان الآلة... أن ترى ما يراه الناقد؟"
  - Small subtitle: "تقدير الوضعية • تحليل المسافات • سيمياء الإضاءة"
- **Image:** None — pure dramatic text
- **Duration:** ~20s

### Slide 6 — هندسة الفضاء الركحي
- **Type:** Light
- **Content:**
  - Title: "هندسة الفضاء: من العزلة إلى الاكتظاظ"
  - Footer: "كثافة الحركة تضاعفت 100% — المساحة المستغلة ارتفعت 112%"
- **Image:** `Enhance_this_diagram_its_in_arabic_2k_delpmaspu.png` (heatmaps comparing القبلة vs ما يراوش stage space usage)
- **Duration:** ~60s

### Slide 7 — البروكسمية والزمن
- **Type:** Light
- **Content:**
  - Title: "الجسد والزمن: من المسافة إلى الالتصاق"
  - Split layout with two diagrams
- **Images:**
  - Right half: `Enhance_image_in_arabic_bec4eb0ba2.jpeg` (proxemics comparison 2.5m vs 0.3m)
  - Left half: `E9d5f849faac42cf922499cf33fa360fjpg_4b9f6d5d04.jpeg` (time/rhythm analysis)
- **Duration:** ~60s

### Slide 8 — النتائج الشاملة
- **Type:** Light
- **Content:**
  - Title: "اللوحة الرقمية الشاملة: من الفردية المعزولة إلى التيه الجماعي"
  - Footer: "من مسرح المرآة إلى مسرح الاشتباك"
- **Image:** `Enhance_arabic_diagram_2345ea7c81.jpeg` (full radar chart with +300%, +112.5% stats)
- **Duration:** ~45s

### Slide 9 — مخرجات AI الحقيقية
- **Type:** Light
- **Content:**
  - Title: "الذكاء الاصطناعي على خشبة المسرح"
  - Split layout
  - Footer: "تحليل آلي لحركة الممثلين والمسافات بين الأجساد"
- **Images:**
  - Right: `results/with_distances/yolov8/baseline/Kiss/anas argui - The Kiss - القبلة (of Tchekhov) , Directed by Mounir Argui [x7KCHIOzS7o - 1166x656 - 15m42s].png` (actors with skeleton overlays and distance lines)
  - Left: `Make_diagram_in_arabic_3861df9675.jpeg` (Arabic histogram of pairwise distance distribution)
- **Duration:** ~60s

### Slide 10 — المنصة
- **Type:** Dark
- **Content:**
  - Title: "تكتيك المسرح — DRAMYX"
  - 4 bullet points:
    - خرائط حرارية للفضاء الركحي
    - رادار الشخصية (Spider Chart)
    - تحليل الإضاءة والوسائط
    - محرك مقارنة العروض
- **Image:** `a2296007-bfb6-4504-9ac3-05d46f2b5419.jpg` (comprehensive digital dashboard with all axes)
- **Duration:** ~60s

### Slide 11 — الرؤية والفريق
- **Type:** Light
- **Content:**
  - Title: "الرؤية: المرجع العالمي المعتمد"
  - 3 vision points:
    - رقمنة المسرح — حفظ الإرث للأجيال القادمة
    - تطوير النقد — معايير موضوعية وعلمية
    - قاعدة بيانات عالمية — أرشيف رقمي للأداء المسرحي
  - Team section:
    - د. محمد الكشو — مخرج وباحث مسرحي
    - م. فارس النفزي — مهندس ذكاء اصطناعي
    - مسرح المدينة بتونس
- **Image:** None
- **Duration:** ~30s

### Slide 12 — الخاتمة
- **Type:** Dark
- **Content:**
  - Large centered text: "لنحوّل سحر المسرح إلى علم باقٍ"
  - Contact: feresnefzi18@gmail.com
  - Gold divider + "DRAMYX © 2026"
- **Image:** None
- **Duration:** ~30s

## Image Assets Map

| Source | Files Used |
|--------|-----------|
| `Presentation/Enhance_this_diagram_its_in_arabic_2k_delpmaspu.png` | Slide 6 — stage heatmaps |
| `Presentation/Enhance_image_in_arabic_bec4eb0ba2.jpeg` | Slide 7 — proxemics diagram |
| `Presentation/E9d5f849faac42cf922499cf33fa360fjpg_4b9f6d5d04.jpeg` | Slide 7 — time/rhythm |
| `Presentation/Enhance_arabic_diagram_2345ea7c81.jpeg` | Slide 8 — radar chart |
| `Presentation/Make_diagram_in_arabic_3861df9675.jpeg` | Slide 9 — histogram |
| `Presentation/a2296007-bfb6-4504-9ac3-05d46f2b5419.jpg` | Slide 10 — dashboard |
| `images/Kiss/...- 30m04s].png` | Slide 2 — hook background (wide stage, separated actors) |
| `images/Kiss/...- 43m31s].png` | Slide 4 — القبلة ensemble shot |
| `images/Blackout/8015c3a5-...1d.jpg` | Slide 4 — ما يراوش clustered group, blue lighting |
| `results/with_distances/yolov8/baseline/Kiss/...- 15m42s].png` | Slide 9 — pose estimation with skeletons + distance lines |

## Technical Implementation

- Single self-contained HTML file with CSS and JS
- Keyboard navigation (arrow keys) + click navigation
- All images embedded as relative paths (the HTML file lives in `Presentation/` alongside the image assets; theater photos referenced via `../images/` and `../results/`)
- Print-friendly / exportable to PDF
- RTL layout throughout
- Responsive aspect ratio (16:9)
- Slide transitions: subtle fade

## Non-Goals

- No animations or complex transitions
- No video embedding
- No external dependencies (fonts loaded from Google Fonts only)
- No interactive features beyond slide navigation
