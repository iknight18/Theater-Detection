# DRAMYX Pitch Deck Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a 12-slide Arabic pitch deck as a single HTML file for presenting DRAMYX at theater/arts events.

**Architecture:** Single self-contained HTML file with embedded CSS and JS. Slides rendered as full-viewport sections with keyboard/click navigation and fade transitions. All images via relative paths. RTL throughout.

**Tech Stack:** HTML5, CSS3, vanilla JS, Google Fonts (Amiri + Tajawal)

**Spec:** `docs/superpowers/specs/2026-03-22-pitch-deck-design.md`

---

### Task 1: Scaffold HTML shell with slide navigation engine

**Files:**
- Create: `Presentation/pitch-deck.html`

- [ ] **Step 1: Create the HTML file with boilerplate, fonts, and slide engine**

Write `Presentation/pitch-deck.html` with:
- DOCTYPE, `<html lang="ar" dir="rtl">`
- Google Fonts import: Amiri (400, 700) + Tajawal (400, 700)
- CSS reset + base styles:
  - `* { margin:0; padding:0; box-sizing:border-box; }`
  - `body { font-family: 'Tajawal', sans-serif; overflow: hidden; background: #1a1a2e; }`
  - `.slide { width: 100vw; height: 100vh; display: none; position: absolute; top:0; left:0; aspect-ratio: 16/9; max-height: 100vh; }`
  - `.slide.active { display: flex; }`
  - Fade transition: `.slide { opacity: 0; transition: opacity 0.4s ease; }` `.slide.active { opacity: 1; }`
- 12 empty `<div class="slide" id="slide-N">` placeholder divs. These will be replaced with full content in Tasks 3-7 (each task replaces the innerHTML of the corresponding placeholder div)
- JS navigation engine:
  - `currentSlide = 0`, array of slide elements
  - `goTo(n)` — removes `.active` from current, adds to target. On `DOMContentLoaded`, call `goTo(0)` to initialize first slide (do not hardcode `active` class in HTML)
  - Arrow key listeners (Right = previous slide for RTL, Left = next)
  - Click navigation zones (left 20% = next, right 20% = previous)
  - Slide counter display (bottom-left): "1 / 12"
- Print media query: show all slides stacked, page-break between them

- [ ] **Step 2: Open in browser and verify navigation works**

Open `Presentation/pitch-deck.html` in browser. Verify:
- 12 blank slides navigable with arrow keys
- Counter updates correctly
- Fade transition visible between slides

- [ ] **Step 3: Commit**

```bash
git add Presentation/pitch-deck.html
git commit -m "scaffold pitch deck HTML with slide navigation engine"
```

---

### Task 2: Design system CSS — dark slides, light slides, shared components

**Files:**
- Modify: `Presentation/pitch-deck.html`

- [ ] **Step 1: Add design system CSS**

Add these CSS classes after the base styles:

```css
/* Design tokens */
:root {
  --navy: #1a1a2e;
  --navy-mid: #16213e;
  --navy-deep: #0f3460;
  --white-warm: #faf7f3;
  --gold: #c9a84c;
  --text-light: #b0b8d8;
  --text-dark: #333;
}

/* Slide types */
.slide-dark {
  background: linear-gradient(135deg, var(--navy) 0%, var(--navy-mid) 60%, var(--navy-deep) 100%);
  color: #fff;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  text-align: center;
  padding: 60px 80px;
}

.slide-light {
  background: var(--white-warm);
  color: var(--text-dark);
  flex-direction: column;
  padding: 50px 80px;
}

/* Typography */
.slide-title {
  font-family: 'Amiri', serif;
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 24px;
}
.slide-dark .slide-title { color: #fff; }
.slide-light .slide-title { color: var(--navy); }

.slide-subtitle {
  font-size: 22px;
  color: var(--text-light);
  font-style: italic;
  margin-bottom: 32px;
}

.slide-footer {
  position: absolute;
  bottom: 40px;
  right: 80px;
  left: 80px;
  font-size: 18px;
  text-align: center;
}
.slide-dark .slide-footer { color: var(--text-light); }
.slide-light .slide-footer { color: #666; }

/* Gold bar */
.gold-bar {
  width: 80px;
  height: 3px;
  background: var(--gold);
  margin: 20px auto;
}

/* Cards (slide 3) */
.cards-row {
  display: flex;
  gap: 30px;
  justify-content: center;
  flex-direction: row-reverse;
  margin-top: 40px;
}
.card {
  border: 2px solid var(--gold);
  border-radius: 12px;
  padding: 30px;
  flex: 1;
  max-width: 300px;
  text-align: right;
}
.card h3 {
  font-family: 'Amiri', serif;
  font-size: 22px;
  color: var(--navy);
  margin-bottom: 12px;
}
.card p { font-size: 16px; line-height: 1.8; }

/* Split layout */
.split {
  display: flex;
  flex: 1;
  gap: 40px;
  align-items: center;
  width: 100%;
  flex-direction: row-reverse;
}
.split-half {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.split-half img {
  max-width: 100%;
  max-height: 50vh;
  border-radius: 8px;
  object-fit: contain;
}

/* Full image slide */
.slide-image {
  max-width: 90%;
  max-height: 60vh;
  object-fit: contain;
  margin: 20px auto;
  display: block;
  border-radius: 8px;
}

/* Overlay for slide 2 */
.bg-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-size: cover;
  background-position: center;
  z-index: 0;
}
.bg-overlay::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(26, 26, 46, 0.75);
}
.slide-dark .slide-content { position: relative; z-index: 1; }

/* Bullet list */
.bullet-list {
  list-style: none;
  text-align: right;
  font-size: 20px;
  line-height: 2.2;
}
.bullet-list li::before {
  content: '◆';
  color: var(--gold);
  margin-left: 12px;
  font-size: 14px;
}

/* Counter */
.slide-counter {
  position: fixed;
  bottom: 15px;
  left: 30px;
  color: rgba(255,255,255,0.4);
  font-size: 14px;
  z-index: 100;
  font-family: 'Tajawal', sans-serif;
}
/* counter color is set dynamically via JS in Task 8 */
```

- [ ] **Step 2: Apply slide type classes to each slide div**

Update the 12 slide divs with their type class:
- Slides 1, 2, 4, 5, 10, 12: add `slide-dark`
- Slides 3, 6, 7, 8, 9, 11: add `slide-light`

- [ ] **Step 3: Verify in browser**

Check that dark slides show navy gradient, light slides show warm white.

- [ ] **Step 4: Commit**

```bash
git add Presentation/pitch-deck.html
git commit -m "add design system CSS with dark/light slide types and shared components"
```

---

### Task 3: Build slides 1-3 (Cover, Hook, Problem)

**Files:**
- Modify: `Presentation/pitch-deck.html`

- [ ] **Step 1: Slide 1 — الغلاف**

```html
<div class="slide slide-dark" id="slide-1">
  <div class="slide-content">
    <div style="font-size:14px;color:var(--gold);letter-spacing:2px;margin-bottom:24px">المختبر الرقمي الأول لهندسة وسيميولوجيا العرض والوسائط</div>
    <h1 style="font-family:'Amiri',serif;font-size:80px;font-weight:700;letter-spacing:4px;margin-bottom:0">تكتيك المسرح</h1>
    <div class="gold-bar"></div>
    <div style="font-size:36px;font-weight:900;letter-spacing:8px;color:var(--gold);margin-bottom:32px;font-family:Georgia,serif">DRAMYX</div>
    <div style="font-size:16px;color:var(--text-light)">د. محمد الكشو &nbsp;—&nbsp; م. فارس النفزي</div>
  </div>
</div>
```

- [ ] **Step 2: Slide 2 — Hook**

```html
<div class="slide slide-dark" id="slide-2">
  <div class="bg-overlay" style="background-image:url('../images/Kiss/anas argui - The Kiss - القبلة (of Tchekhov) , Directed by Mounir Argui [x7KCHIOzS7o - 1166x656 - 30m04s].png')"></div>
  <div class="slide-content" style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%">
    <h1 class="slide-title" style="font-size:52px;line-height:1.6;max-width:800px">ماذا يبقى من العرض المسرحي...<br>بعد أن تُطفأ الأنوار؟</h1>
  </div>
</div>
```

- [ ] **Step 3: Slide 3 — المشكلة**

```html
<div class="slide slide-light" id="slide-3">
  <h2 class="slide-title" style="text-align:center;margin-top:60px">المشكلة: بين الذاتية والضياع</h2>
  <div class="cards-row">
    <div class="card">
      <h3>نقد مسرحي ذاتي</h3>
      <p>يفتقر النقد المسرحي الحالي إلى معايير رقمية موحّدة وموضوعية، مما يؤدي إلى أحكام ذاتية تفتقر للدقة.</p>
    </div>
    <div class="card">
      <h3>ضياع الإرث الحركي</h3>
      <p>تفقد العروض المسرحية قيمتها التوثيقية بمجرد انتهائها، ويضيع معها الإرث الحركي والسينوغرافي الثمين.</p>
    </div>
    <div class="card">
      <h3>غياب أدوات المقارنة</h3>
      <p>لا توجد أدوات دقيقة لقياس مدى نجاح تحويل الأعمال الأدبية أو السينمائية إلى عروض مسرحية.</p>
    </div>
  </div>
  <div class="slide-footer">كل هذا يؤكد الحاجة الماسة إلى "عقل رقمي" يوثق ويحلل العلامات المسرحية بموضوعية ودقة.</div>
</div>
```

- [ ] **Step 4: Verify slides 1-3 in browser**

Check cover typography, hook background image loads with overlay, problem cards layout.

- [ ] **Step 5: Commit**

```bash
git add Presentation/pitch-deck.html
git commit -m "add slides 1-3: cover, hook, and problem statement"
```

---

### Task 4: Build slides 4-5 (Story and Reveal)

**Files:**
- Modify: `Presentation/pitch-deck.html`

- [ ] **Step 1: Slide 4 — القصة**

```html
<div class="slide slide-dark" id="slide-4">
  <div class="slide-content" style="width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <h2 class="slide-title" style="margin-bottom:8px">مخرج واحد. عرضان. تحوّل جذري.</h2>
    <div class="gold-bar" style="margin-bottom:40px"></div>
    <div class="split" style="max-width:1000px">
      <div class="split-half">
        <img src="../images/Kiss/anas argui - The Kiss - القبلة (of Tchekhov) , Directed by Mounir Argui [x7KCHIOzS7o - 1166x656 - 43m31s].png" alt="القبلة" style="max-height:35vh;border:2px solid var(--gold)">
        <h3 style="font-family:'Amiri',serif;font-size:28px;margin-top:16px;color:var(--gold)">القبلة</h3>
        <p style="color:var(--text-light);font-size:18px">تشيخوف — الفرد المنعزل</p>
      </div>
      <div class="split-half">
        <img src="../images/Blackout/8015c3a5-fc53-42fb-b4bb-6040a46c1c1d.jpg" alt="ما يراوش" style="max-height:35vh;border:2px solid var(--gold)">
        <h3 style="font-family:'Amiri',serif;font-size:28px;margin-top:16px;color:var(--gold)">ما يراوش</h3>
        <p style="color:var(--text-light);font-size:18px">ميترلينك — الجماعة التائهة</p>
      </div>
    </div>
    <div class="slide-footer" style="color:var(--text-light)">كيف نثبت هذا التحوّل بالأرقام؟</div>
  </div>
</div>
```

- [ ] **Step 2: Slide 5 — الكشف**

```html
<div class="slide slide-dark" id="slide-5">
  <div class="slide-content" style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%">
    <h1 class="slide-title" style="font-size:50px;line-height:1.6;max-width:850px">ماذا لو كان بإمكان الآلة...<br>أن ترى ما يراه الناقد؟</h1>
    <div class="gold-bar"></div>
    <p style="color:var(--text-light);font-size:20px;letter-spacing:4px;margin-top:16px">تقدير الوضعية &nbsp;•&nbsp; تحليل المسافات &nbsp;•&nbsp; سيمياء الإضاءة</p>
  </div>
</div>
```

- [ ] **Step 3: Verify slides 4-5 in browser**

Check split layout with images, text contrast, reveal slide dramatic feel.

- [ ] **Step 4: Commit**

```bash
git add Presentation/pitch-deck.html
git commit -m "add slides 4-5: story comparison and the reveal transition"
```

---

### Task 5: Build slides 6-8 (Data slides — heatmaps, proxemics, radar)

**Files:**
- Modify: `Presentation/pitch-deck.html`

- [ ] **Step 1: Slide 6 — هندسة الفضاء**

```html
<div class="slide slide-light" id="slide-6">
  <h2 class="slide-title" style="text-align:center">هندسة الفضاء: من العزلة إلى الاكتظاظ</h2>
  <img src="Enhance_this_diagram_its_in_arabic_2k_delpmaspu.png" alt="هندسة الفضاء الركحي" class="slide-image" style="max-height:65vh">
  <div class="slide-footer">كثافة الحركة تضاعفت 100% — المساحة المستغلة ارتفعت 112%</div>
</div>
```

- [ ] **Step 2: Slide 7 — البروكسمية والزمن**

```html
<div class="slide slide-light" id="slide-7">
  <h2 class="slide-title" style="text-align:center">الجسد والزمن: من المسافة إلى الالتصاق</h2>
  <div class="split" style="flex:1;margin-top:20px">
    <div class="split-half">
      <img src="Enhance_image_in_arabic_bec4eb0ba2.jpeg" alt="مقارنة البروكسمية" style="max-height:55vh;max-width:100%;object-fit:contain">
    </div>
    <div class="split-half">
      <img src="E9d5f849faac42cf922499cf33fa360fjpg_4b9f6d5d04.jpeg" alt="تحليل الزمن والإيقاع" style="max-height:55vh;max-width:100%;object-fit:contain">
    </div>
  </div>
</div>
```

- [ ] **Step 3: Slide 8 — النتائج الشاملة**

```html
<div class="slide slide-light" id="slide-8">
  <h2 class="slide-title" style="text-align:center">اللوحة الرقمية الشاملة: من الفردية المعزولة إلى التيه الجماعي</h2>
  <img src="Enhance_arabic_diagram_2345ea7c81.jpeg" alt="رادار الشخصية" class="slide-image" style="max-height:62vh">
  <div class="slide-footer">من مسرح المرآة إلى مسرح الاشتباك</div>
</div>
```

- [ ] **Step 4: Verify slides 6-8 in browser**

Check all images load, proper sizing within viewport, text readability on light background.

- [ ] **Step 5: Commit**

```bash
git add Presentation/pitch-deck.html
git commit -m "add slides 6-8: heatmaps, proxemics/rhythm, and radar chart results"
```

---

### Task 6: Build slides 9-10 (AI outputs and Platform)

**Files:**
- Modify: `Presentation/pitch-deck.html`

- [ ] **Step 1: Slide 9 — مخرجات AI**

```html
<div class="slide slide-light" id="slide-9">
  <h2 class="slide-title" style="text-align:center">الذكاء الاصطناعي على خشبة المسرح</h2>
  <div class="split" style="flex:1;margin-top:20px">
    <div class="split-half">
      <img src="../results/with_distances/yolov8/baseline/Kiss/anas argui - The Kiss - القبلة (of Tchekhov) , Directed by Mounir Argui [x7KCHIOzS7o - 1166x656 - 15m42s].png" alt="تقدير الوضعية" style="max-height:55vh;max-width:100%;object-fit:contain;border-radius:8px">
    </div>
    <div class="split-half">
      <img src="Make_diagram_in_arabic_3861df9675.jpeg" alt="توزيع المسافات" style="max-height:55vh;max-width:100%;object-fit:contain;border-radius:8px">
    </div>
  </div>
  <div class="slide-footer">تحليل آلي لحركة الممثلين والمسافات بين الأجساد</div>
</div>
```

- [ ] **Step 2: Slide 10 — المنصة**

```html
<div class="slide slide-dark" id="slide-10">
  <div class="slide-content" style="width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <h2 class="slide-title" style="margin-bottom:8px">تكتيك المسرح — DRAMYX</h2>
    <div class="gold-bar" style="margin-bottom:30px"></div>
    <div class="split" style="max-width:1100px;align-items:center">
      <div class="split-half" style="flex:1.2">
        <img src="a2296007-bfb6-4504-9ac3-05d46f2b5419.jpg" alt="اللوحة الرقمية الشاملة" style="max-height:50vh;max-width:100%;object-fit:contain;border-radius:8px;border:1px solid rgba(201,168,76,0.3)">
      </div>
      <div class="split-half" style="flex:0.8;text-align:right">
        <ul class="bullet-list" style="font-size:22px">
          <li>خرائط حرارية للفضاء الركحي</li>
          <li>رادار الشخصية (Spider Chart)</li>
          <li>تحليل الإضاءة والوسائط</li>
          <li>محرك مقارنة العروض</li>
        </ul>
      </div>
    </div>
  </div>
</div>
```

- [ ] **Step 3: Verify slides 9-10 in browser**

Check pose estimation image loads via relative path, dashboard image displays, bullet list readable on dark background.

- [ ] **Step 4: Commit**

```bash
git add Presentation/pitch-deck.html
git commit -m "add slides 9-10: AI outputs and platform overview"
```

---

### Task 7: Build slides 11-12 (Vision and Closing)

**Files:**
- Modify: `Presentation/pitch-deck.html`

- [ ] **Step 1: Slide 11 — الرؤية والفريق**

```html
<div class="slide slide-light" id="slide-11">
  <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%">
    <h2 class="slide-title" style="text-align:center;margin-bottom:40px">الرؤية: المرجع العالمي المعتمد</h2>
    <div style="display:flex;gap:40px;flex-direction:row-reverse;max-width:900px;margin-bottom:50px">
      <div style="flex:1;text-align:center;padding:20px">
        <div style="font-size:36px;color:var(--gold);margin-bottom:12px">🏛️</div>
        <h3 style="font-family:'Amiri',serif;font-size:22px;color:var(--navy);margin-bottom:8px">رقمنة المسرح</h3>
        <p style="font-size:16px;line-height:1.8;color:#555">حفظ الإرث للأجيال القادمة</p>
      </div>
      <div style="flex:1;text-align:center;padding:20px">
        <div style="font-size:36px;color:var(--gold);margin-bottom:12px">📐</div>
        <h3 style="font-family:'Amiri',serif;font-size:22px;color:var(--navy);margin-bottom:8px">تطوير النقد</h3>
        <p style="font-size:16px;line-height:1.8;color:#555">معايير موضوعية وعلمية</p>
      </div>
      <div style="flex:1;text-align:center;padding:20px">
        <div style="font-size:36px;color:var(--gold);margin-bottom:12px">🌐</div>
        <h3 style="font-family:'Amiri',serif;font-size:22px;color:var(--navy);margin-bottom:8px">قاعدة بيانات عالمية</h3>
        <p style="font-size:16px;line-height:1.8;color:#555">أرشيف رقمي للأداء المسرحي</p>
      </div>
    </div>
    <div class="gold-bar"></div>
    <div style="margin-top:24px;text-align:center">
      <p style="font-size:18px;color:var(--navy);font-weight:700">الفريق</p>
      <p style="font-size:16px;color:#555;margin-top:8px;line-height:2">
        د. محمد الكشو — مخرج وباحث مسرحي<br>
        م. فارس النفزي — مهندس ذكاء اصطناعي<br>
        <span style="color:var(--gold)">مسرح المدينة بتونس</span>
      </p>
    </div>
  </div>
</div>
```

- [ ] **Step 2: Slide 12 — الخاتمة**

```html
<div class="slide slide-dark" id="slide-12">
  <div class="slide-content" style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%">
    <h1 class="slide-title" style="font-size:52px;line-height:1.6">لنحوّل سحر المسرح<br>إلى علم باقٍ</h1>
    <div class="gold-bar" style="margin:24px auto"></div>
    <p style="font-size:18px;color:var(--text-light);margin-top:16px">feresnefzi18@gmail.com</p>
    <div style="margin-top:40px;font-size:12px;color:rgba(255,255,255,0.3);letter-spacing:4px">
      <span style="color:var(--gold);font-weight:700">DRAMYX</span> — © 2026
    </div>
  </div>
</div>
```

- [ ] **Step 3: Verify slides 11-12 in browser**

Check vision cards layout, team section, closing slide typography.

- [ ] **Step 4: Commit**

```bash
git add Presentation/pitch-deck.html
git commit -m "add slides 11-12: vision/team and closing"
```

---

### Task 8: Polish and print styles

**Files:**
- Modify: `Presentation/pitch-deck.html`

- [ ] **Step 1: Add print styles**

```css
@media print {
  .slide {
    display: flex !important;
    opacity: 1 !important;
    position: relative !important;
    page-break-after: always;
    height: 100vh;
    width: 100%;
  }
  .slide-counter { display: none; }
}
```

- [ ] **Step 2: Update slide counter color based on slide type**

In the JS `goTo(n)` function, add logic:
```js
const counter = document.querySelector('.slide-counter');
if (slides[n].classList.contains('slide-light')) {
  counter.style.color = 'rgba(0,0,0,0.3)';
} else {
  counter.style.color = 'rgba(255,255,255,0.4)';
}
```

- [ ] **Step 3: Full walkthrough**

Navigate all 12 slides in browser:
- Verify every image loads
- Verify RTL text renders correctly
- Verify transitions are smooth
- Verify counter color adapts to slide type
- Test keyboard navigation (full cycle)
- Test print/PDF export (Ctrl+P)

- [ ] **Step 4: Commit**

```bash
git add Presentation/pitch-deck.html
git commit -m "add print styles and polish slide counter"
```
