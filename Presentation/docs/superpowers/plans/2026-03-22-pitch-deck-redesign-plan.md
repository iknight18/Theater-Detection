# DRAMYX Pitch Deck Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the DRAMYX pitch deck from 12 to 17 slides with cinematic + smart data visual direction, new content sections, rich animations, and triple-input navigation.

**Architecture:** Single self-contained HTML file (`pitch-deck.html`) with inline CSS and JS. No build tools. No external dependencies beyond Google Fonts. The file is structured in three inline blocks: `<style>` (design system + animations + slide layouts), `<body>` (17 slides as `div.slide` elements + nav buttons), `<script>` (navigation, transitions, counter animations, slide lifecycle).

**Tech Stack:** HTML5, CSS3 (keyframes, transitions, backdrop-filter), vanilla JS (requestAnimationFrame for counters, keyboard/touch events), Google Fonts (Amiri, Tajawal).

**Spec:** `docs/superpowers/specs/2026-03-22-pitch-deck-redesign-design.md`

**Verification:** After each task, open `pitch-deck.html` in a browser and visually verify the slides work. Navigate with arrow keys and check animations trigger on slide entry.

---

### Task 1: Design System Foundation — CSS Reset, Tokens, Base Styles

Replace the existing CSS in `pitch-deck.html` with the new design system. This task sets up all reusable styles but does not touch slide content yet.

**Files:**
- Modify: `pitch-deck.html` — replace everything inside `<style>` tag (lines 10–232)

- [ ] **Step 1: Replace CSS variables and reset**

Replace the `:root` block and reset with updated design tokens:

```css
/* ── Reset ── */
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: 'Tajawal', sans-serif;
  overflow: hidden;
  background: #0a0a1a;
}

:root {
  --deep-stage: #0a0a1a;
  --navy: #1a1a2e;
  --navy-mid: #16213e;
  --navy-deep: #0f3460;
  --ivory: #faf7f0;
  --ivory-dark: #f0ebe0;
  --gold: #c9a84c;
  --gold-light: #e8c55a;
  --text-light: #b0b8d8;
  --text-dark: #333;
  --text-dark-secondary: #444;
  --muted-gold: #8a7a5a;
}
```

- [ ] **Step 2: Add slide base and variant styles**

```css
/* ── Slide base ── */
.slide {
  width: 100vw;
  height: 100vh;
  position: absolute;
  top: 0; left: 0;
  display: flex;
  visibility: hidden;
  opacity: 0;
  transition: none;
}
.slide.active {
  visibility: visible;
  opacity: 1;
}
.slide.exiting {
  visibility: visible;
}

/* ── Dark slides ── */
.slide-dark {
  background: linear-gradient(135deg, var(--deep-stage) 0%, var(--navy) 40%, var(--navy-mid) 100%);
  color: #fff;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  text-align: center;
  padding: 60px 80px;
}

/* ── Light slides ── */
.slide-light {
  background: linear-gradient(160deg, var(--ivory) 0%, var(--ivory-dark) 100%);
  color: var(--text-dark);
  flex-direction: column;
  padding: 50px 80px;
}
```

- [ ] **Step 3: Add typography styles**

```css
/* ── Typography ── */
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
  font-style: italic;
  margin-bottom: 32px;
}
.slide-dark .slide-subtitle { color: var(--text-light); }
.slide-light .slide-subtitle { color: var(--muted-gold); }
```

- [ ] **Step 4: Add depth effect styles — spotlight, glass cards, elevated cards**

```css
/* ── Spotlight glow ── */
.spotlight {
  position: absolute;
  top: -10%;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 50%;
  background: radial-gradient(ellipse, rgba(201,168,76,0.15), transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* ── Glass morphism card (dark slides) ── */
.glass-card {
  background: rgba(255,255,255,0.05);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(201,168,76,0.2);
  border-radius: 12px;
  padding: 30px;
}

/* ── Elevated card (light slides) ── */
.elevated-card {
  background: #fff;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.08), 0 2px 8px rgba(0,0,0,0.04);
  border: 1px solid rgba(201,168,76,0.15);
}

/* ── Gold bar ── */
.gold-bar {
  width: 80px;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  margin: 20px auto;
}
```

- [ ] **Step 5: Add layout helpers — split, cards-row, bullet-list, footer, bg-overlay**

```css
/* ── Footer ── */
.slide-footer {
  position: absolute;
  bottom: 40px;
  right: 80px; left: 80px;
  font-size: 18px;
  text-align: center;
}
.slide-dark .slide-footer { color: var(--text-light); }
.slide-light .slide-footer { color: #666; }

/* ── Split layout ── */
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

/* ── Cards row ── */
.cards-row {
  display: flex;
  gap: 30px;
  justify-content: center;
  flex-direction: row-reverse;
  margin-top: 40px;
}

/* ── Bullet list ── */
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

/* ── Background overlay ── */
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
  background: rgba(10, 10, 26, 0.75);
}
.slide-content {
  position: relative;
  z-index: 1;
}

/* ── Standalone image ── */
.slide-image {
  max-width: 90%;
  max-height: 60vh;
  object-fit: contain;
  margin: 20px auto;
  display: block;
  border-radius: 8px;
}
```

- [ ] **Step 6: Add animation keyframes**

```css
/* ── Animations ── */
@keyframes spotlightReveal {
  from { opacity: 0; text-shadow: 0 0 0 transparent; }
  to { opacity: 1; text-shadow: 0 0 20px rgba(201,168,76,0.4); }
}
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes scaleIn {
  from { opacity: 0; transform: scale(0.8); }
  to { opacity: 1; transform: scale(1); }
}
@keyframes slideInLeft {
  from { opacity: 0; transform: translateX(-40px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes slideInRight {
  from { opacity: 0; transform: translateX(40px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes drawLine {
  from { width: 0; }
  to { width: 100%; }
}
@keyframes scanLine {
  0% { top: 0; }
  100% { top: 100%; }
}

/* ── Scan-line overlay for AI output images ── */
.scan-overlay {
  position: relative;
  overflow: hidden;
}
.scan-overlay::after {
  content: '';
  position: absolute;
  left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, transparent, var(--gold), transparent);
  opacity: 0;
  top: 0;
}
.slide.active .scan-overlay::after {
  opacity: 0.6;
  animation: scanLine 2s ease-in-out 0.5s forwards;
}

/* ── Slide entry animations (applied via JS adding .animate class) ── */
.slide.active .anim-spotlight { animation: spotlightReveal 0.8s ease forwards; }
.slide.active .anim-fade-up { animation: fadeInUp 0.6s ease forwards; }
.slide.active .anim-scale { animation: scaleIn 0.5s ease forwards; }
.slide.active .anim-slide-left { animation: slideInLeft 0.6s ease forwards; }
.slide.active .anim-slide-right { animation: slideInRight 0.6s ease forwards; }
.anim-draw-line { width: 0; }
.slide.active .anim-draw-line { animation: drawLine 1s ease 0.3s forwards; }

/* Stagger delays — elements start hidden, animation reveals them via fill-mode: forwards */
.stagger-1 { animation-delay: 0s !important; animation-fill-mode: forwards !important; }
.stagger-2 { animation-delay: 0.15s !important; animation-fill-mode: forwards !important; }
.stagger-3 { animation-delay: 0.3s !important; animation-fill-mode: forwards !important; }
.stagger-4 { animation-delay: 0.45s !important; animation-fill-mode: forwards !important; }
.stagger-5 { animation-delay: 0.6s !important; animation-fill-mode: forwards !important; }
/* Hide staggered elements until their slide is active and animation runs */
.slide:not(.active) [class*="stagger-"] { opacity: 0; }
```

- [ ] **Step 7: Add navigation button styles and slide counter**

```css
/* ── Navigation buttons ── */
.nav-btn {
  position: fixed;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: none;
  font-size: 20px;
  cursor: pointer;
  z-index: 60;
  opacity: 0;
  transition: opacity 0.3s ease, background 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}
.nav-btn:hover { opacity: 0.6; }
body:hover .nav-btn { opacity: 0.15; }
body:hover .nav-btn:hover { opacity: 0.6; }

.nav-btn-next { left: 20px; }
.nav-btn-prev { right: 20px; }

/* Adapt to slide background */
.nav-btn-dark {
  background: rgba(255,255,255,0.15);
  color: #fff;
}
.nav-btn-light {
  background: rgba(0,0,0,0.1);
  color: #333;
}

/* ── Slide counter ── */
.slide-counter {
  position: fixed;
  bottom: 15px;
  left: 30px;
  font-size: 14px;
  z-index: 100;
  font-family: 'Tajawal', sans-serif;
  transition: color 0.3s ease;
}

/* ── Print ── */
@media print {
  .slide {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    position: relative !important;
    page-break-after: always;
    height: 100vh;
    width: 100%;
  }
  .slide-counter, .nav-btn { display: none; }
}
```

- [ ] **Step 8: Verify in browser**

Open `pitch-deck.html` in a browser. The existing slides should still render (content untouched), but now with the updated design tokens, deeper backgrounds, and new card styles. Some layout may look off because slide content hasn't been updated yet — that's expected.

- [ ] **Step 9: Commit**

```bash
git add pitch-deck.html
git commit -m "redesign CSS foundation: tokens, depth effects, animations, nav buttons"
```

---

### Task 2: Navigation System — Keyboard, Remote, Buttons, Transitions

Replace the existing navigation JS with the new system supporting keyboard, presenter remote, on-screen buttons, and context-aware transitions.

**Files:**
- Modify: `pitch-deck.html` — replace `<script>` block and navigation HTML elements

- [ ] **Step 1: Replace navigation HTML**

Remove the old `.nav-zone` divs and replace with button elements. Place these just before `<div class="slide-counter">`:

```html
<!-- Navigation buttons -->
<button class="nav-btn nav-btn-next nav-btn-dark" id="btnNext" onclick="nextSlide()" aria-label="Next slide">→</button>
<button class="nav-btn nav-btn-prev nav-btn-dark" id="btnPrev" onclick="prevSlide()" aria-label="Previous slide">←</button>

<!-- Slide counter -->
<div class="slide-counter" id="slideCounter">1 / 17</div>
```

- [ ] **Step 2: Write the new navigation JS**

Replace entire `<script>` block:

```javascript
const TOTAL = 17;
let currentSlide = 0;
let isTransitioning = false;

// Slide type map: true = light, false = dark (1-based index)
const lightSlides = new Set([3, 7, 8, 9, 10, 11, 15, 16]);

const slides = Array.from({ length: TOTAL }, (_, i) =>
  document.getElementById('slide-' + (i + 1))
);
const counter = document.getElementById('slideCounter');
const btnNext = document.getElementById('btnNext');
const btnPrev = document.getElementById('btnPrev');

function getTransitionType(fromIdx, toIdx) {
  const fromLight = lightSlides.has(fromIdx + 1);
  const toLight = lightSlides.has(toIdx + 1);
  if (!fromLight && !toLight) return 'crossfade';
  if (!fromLight && toLight) return 'curtain-lift';
  if (fromLight && toLight) return 'horizontal';
  if (fromLight && !toLight) return 'fade-black';
  return 'crossfade';
}

function updateNavColors() {
  const isLight = lightSlides.has(currentSlide + 1);
  const darkClass = 'nav-btn-dark';
  const lightClass = 'nav-btn-light';

  [btnNext, btnPrev].forEach(btn => {
    btn.classList.remove(darkClass, lightClass);
    btn.classList.add(isLight ? lightClass : darkClass);
  });

  counter.style.color = isLight ? '#555' : 'rgba(255,255,255,0.6)';
}

function goTo(n) {
  if (isTransitioning) return;
  n = Math.max(0, Math.min(TOTAL - 1, n));
  if (n === currentSlide) return;

  isTransitioning = true;
  const from = slides[currentSlide];
  const to = slides[n];
  const type = getTransitionType(currentSlide, n);

  // Mark departing slide so it stays visible during transition
  from.classList.add('exiting');

  // Reset any previous transition styles
  to.style.transition = 'none';
  to.style.transform = '';
  to.style.opacity = '0';

  switch (type) {
    case 'crossfade':
      from.style.transition = 'opacity 0.4s ease';
      from.style.opacity = '0';
      to.style.transition = 'opacity 0.4s ease';
      to.classList.add('active');
      requestAnimationFrame(() => {
        requestAnimationFrame(() => { to.style.opacity = '1'; });
      });
      break;

    case 'curtain-lift':
      to.style.transform = 'translateY(100%)';
      to.style.opacity = '1';
      to.classList.add('active');
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          to.style.transition = 'transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
          to.style.transform = 'translateY(0)';
        });
      });
      break;

    case 'horizontal':
      const dir = n > currentSlide ? '-100%' : '100%';
      to.style.transform = `translateX(${n > currentSlide ? '100%' : '-100%'})`;
      to.style.opacity = '1';
      to.classList.add('active');
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          from.style.transition = 'transform 0.5s ease';
          from.style.transform = `translateX(${dir})`;
          to.style.transition = 'transform 0.5s ease';
          to.style.transform = 'translateX(0)';
        });
      });
      break;

    case 'fade-black':
      from.style.transition = 'opacity 0.3s ease';
      from.style.opacity = '0';
      setTimeout(() => {
        to.classList.add('active');
        to.style.transition = 'opacity 0.3s ease';
        requestAnimationFrame(() => {
          requestAnimationFrame(() => { to.style.opacity = '1'; });
        });
      }, 300);
      break;
  }

  const transitionDuration = type === 'fade-black' ? 600 : type === 'curtain-lift' ? 600 : 500;
  setTimeout(() => {
    from.classList.remove('active', 'exiting');
    from.style.transition = 'none';
    from.style.transform = '';
    from.style.opacity = '0';
    currentSlide = n;
    counter.textContent = (currentSlide + 1) + ' / ' + TOTAL;
    updateNavColors();
    triggerSlideAnimations(currentSlide);
    isTransitioning = false;
  }, transitionDuration);
}

function nextSlide() { if (currentSlide < TOTAL - 1) goTo(currentSlide + 1); }
function prevSlide() { if (currentSlide > 0) goTo(currentSlide - 1); }

// Animated counters
function animateCounters(slideEl) {
  const counters = slideEl.querySelectorAll('[data-counter]');
  counters.forEach(el => {
    const target = parseInt(el.dataset.counter, 10);
    const prefix = el.dataset.prefix || '';
    const suffix = el.dataset.suffix || '';
    let start = 0;
    const duration = 1500;
    const startTime = performance.now();
    function update(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      const current = Math.round(start + (target - start) * eased);
      el.textContent = prefix + current + suffix;
      if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
  });
}

function triggerSlideAnimations(idx) {
  const slide = slides[idx];
  // Re-trigger CSS animations by removing and re-adding the active class trick
  // is not needed since we add active fresh each time.
  // Trigger JS counter animations
  animateCounters(slide);
}

// Keyboard navigation
document.addEventListener('keydown', function(e) {
  switch(e.key) {
    case 'ArrowLeft': case 'PageDown': case ' ':
      e.preventDefault(); nextSlide(); break;
    case 'ArrowRight': case 'PageUp': case 'Backspace':
      e.preventDefault(); prevSlide(); break;
    case 'Home':
      e.preventDefault(); goTo(0); break;
    case 'End':
      e.preventDefault(); goTo(TOTAL - 1); break;
  }
});

// Touch swipe support
let touchStartX = 0;
document.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; });
document.addEventListener('touchend', e => {
  const diff = e.changedTouches[0].clientX - touchStartX;
  if (Math.abs(diff) > 50) {
    // RTL: swipe left = next, swipe right = prev
    if (diff < 0) nextSlide();
    else prevSlide();
  }
});

// Initialize
document.addEventListener('DOMContentLoaded', function() {
  slides[0].classList.add('active');
  slides[0].style.opacity = '1';
  counter.textContent = '1 / ' + TOTAL;
  updateNavColors();
  triggerSlideAnimations(0);
});
```

- [ ] **Step 3: Verify navigation in browser**

Open `pitch-deck.html`. Test:
- Arrow keys navigate between slides
- PageDown/PageUp work (simulates presenter remote)
- Space bar advances, Backspace goes back
- Home goes to slide 1, End to last slide
- Hover over left/right edges shows navigation buttons
- Transitions vary based on slide type (dark↔light)

- [ ] **Step 4: Commit**

```bash
git add pitch-deck.html
git commit -m "add triple-input navigation with context-aware transitions"
```

---

### Task 3: Slides 1–4 — Act 1 (The Hook)

Rebuild the first 4 slides with the new design system. These are mostly dark cinematic slides (except slide 3 which is light).

**Files:**
- Modify: `pitch-deck.html` — replace slide 1–4 HTML content

- [ ] **Step 1: Rebuild Slide 1 — Cover**

```html
<!-- ═══════ SLIDE 1 — الغلاف ═══════ -->
<div class="slide slide-dark" id="slide-1">
  <div class="spotlight"></div>
  <div class="slide-content" style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%">
    <div class="anim-fade-up stagger-1" style="font-size:14px;color:var(--gold);letter-spacing:2px;margin-bottom:24px">المختبر الرقمي الأول لهندسة وسيميولوجيا العرض والوسائط</div>
    <h1 class="anim-spotlight stagger-2" style="font-family:'Amiri',serif;font-size:80px;font-weight:700;letter-spacing:4px;margin-bottom:0">تكتيك المسرح</h1>
    <div class="gold-bar anim-fade-up stagger-3"></div>
    <div class="anim-fade-up stagger-4" style="font-size:36px;font-weight:900;letter-spacing:8px;color:var(--gold);margin-bottom:32px;font-family:Georgia,serif">DRAMYX</div>
    <div class="anim-fade-up stagger-5" style="font-size:16px;color:var(--text-light)">د. محمد الكشو &nbsp;—&nbsp; م. فارس النفزي</div>
  </div>
</div>
```

- [ ] **Step 2: Rebuild Slide 2 — The Question**

```html
<!-- ═══════ SLIDE 2 — السؤال ═══════ -->
<div class="slide slide-dark" id="slide-2">
  <div class="bg-overlay" style="background-image:url('../images/Kiss/anas argui - The Kiss - القبلة (of Tchekhov) , Directed by Mounir Argui [x7KCHIOzS7o - 1166x656 - 30m04s].png')"></div>
  <div class="slide-content" style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%">
    <h1 class="slide-title anim-spotlight" style="font-size:52px;line-height:1.6;max-width:800px">ماذا يبقى من العرض المسرحي...<br>بعد أن تُطفأ الأنوار؟</h1>
  </div>
</div>
```

- [ ] **Step 3: Rebuild Slide 3 — The Problem (light slide with elevated cards)**

```html
<!-- ═══════ SLIDE 3 — المشكلة ═══════ -->
<div class="slide slide-light" id="slide-3">
  <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;flex:1;width:100%">
    <h2 class="slide-title anim-fade-up stagger-1" style="text-align:center;margin-bottom:40px">المشكلة: بين الذاتية والضياع</h2>
    <div class="cards-row">
      <div class="elevated-card anim-fade-up stagger-2" style="flex:1;max-width:300px;text-align:right">
        <h3 style="font-family:'Amiri',serif;font-size:22px;color:var(--navy);margin-bottom:12px">نقد مسرحي ذاتي</h3>
        <p style="font-size:16px;line-height:1.8">يفتقر النقد المسرحي الحالي إلى معايير رقمية موحّدة وموضوعية، مما يؤدي إلى أحكام ذاتية تفتقر للدقة.</p>
      </div>
      <div class="elevated-card anim-fade-up stagger-3" style="flex:1;max-width:300px;text-align:right">
        <h3 style="font-family:'Amiri',serif;font-size:22px;color:var(--navy);margin-bottom:12px">ضياع الإرث الحركي</h3>
        <p style="font-size:16px;line-height:1.8">تفقد العروض المسرحية قيمتها التوثيقية بمجرد انتهائها، ويضيع معها الإرث الحركي والسينوغرافي الثمين.</p>
      </div>
      <div class="elevated-card anim-fade-up stagger-4" style="flex:1;max-width:300px;text-align:right">
        <h3 style="font-family:'Amiri',serif;font-size:22px;color:var(--navy);margin-bottom:12px">غياب أدوات المقارنة</h3>
        <p style="font-size:16px;line-height:1.8">لا توجد أدوات دقيقة لقياس مدى نجاح تحويل الأعمال الأدبية أو السينمائية إلى عروض مسرحية.</p>
      </div>
    </div>
  </div>
  <div class="slide-footer">كل هذا يؤكد الحاجة الماسة إلى "عقل رقمي" يوثق ويحلل العلامات المسرحية بموضوعية ودقة.</div>
</div>
```

- [ ] **Step 4: Rebuild Slide 4 — The Story**

```html
<!-- ═══════ SLIDE 4 — القصة ═══════ -->
<div class="slide slide-dark" id="slide-4">
  <div class="spotlight"></div>
  <div class="slide-content" style="width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <h2 class="slide-title anim-fade-up stagger-1" style="margin-bottom:8px">مخرج واحد. عرضان. تحوّل جذري.</h2>
    <div class="gold-bar anim-fade-up stagger-2" style="margin-bottom:40px"></div>
    <div class="split" style="max-width:1000px">
      <div class="split-half anim-slide-right stagger-3">
        <img src="../images/Kiss/anas argui - The Kiss - القبلة (of Tchekhov) , Directed by Mounir Argui [x7KCHIOzS7o - 1166x656 - 43m31s].png" alt="القبلة" style="max-height:35vh;border:2px solid var(--gold)">
        <h3 style="font-family:'Amiri',serif;font-size:28px;margin-top:16px;color:var(--gold)">القبلة</h3>
        <p style="color:var(--text-light);font-size:18px">تشيخوف — الفرد المنعزل</p>
      </div>
      <div class="split-half anim-slide-left stagger-4">
        <img src="../images/Blackout/8015c3a5-fc53-42fb-b4bb-6040a46c1c1d.jpg" alt="ما يراوش" style="max-height:35vh;border:2px solid var(--gold)">
        <h3 style="font-family:'Amiri',serif;font-size:28px;margin-top:16px;color:var(--gold)">ما يراوش</h3>
        <p style="color:var(--text-light);font-size:18px">ميترلينك — الجماعة التائهة</p>
      </div>
    </div>
    <div class="slide-footer" style="color:var(--text-light)">كيف نثبت هذا التحوّل بالأرقام؟</div>
  </div>
</div>
```

- [ ] **Step 5: Verify slides 1–4 in browser**

Navigate through slides 1–4. Check: spotlight glow on 1 and 4, background image on 2, elevated cards on 3, staggered entry animations on each slide.

- [ ] **Step 6: Commit**

```bash
git add pitch-deck.html
git commit -m "rebuild slides 1-4: cover, hook, problem, story with new design"
```

---

### Task 4: Slides 5–7 — Act 2 (The Reveal + New Slides)

Build the reveal section including the two new slides (How It Works and Methodology).

**Files:**
- Modify: `pitch-deck.html` — replace slide 5, add slides 6–7

- [ ] **Step 1: Rebuild Slide 5 — The Insight**

```html
<!-- ═══════ SLIDE 5 — الكشف ═══════ -->
<div class="slide slide-dark" id="slide-5">
  <div class="spotlight"></div>
  <div class="slide-content" style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%">
    <h1 class="slide-title anim-spotlight" style="font-size:50px;line-height:1.6;max-width:850px">ماذا لو كان بإمكان الآلة...<br>أن ترى ما يراه الناقد؟</h1>
    <div class="gold-bar anim-fade-up stagger-2"></div>
    <p class="anim-fade-up stagger-3" style="color:var(--text-light);font-size:20px;letter-spacing:4px;margin-top:16px">تقدير الوضعية &nbsp;•&nbsp; تحليل المسافات &nbsp;•&nbsp; سيمياء الإضاءة</p>
  </div>
</div>
```

- [ ] **Step 2: Create Slide 6 — How It Works (NEW)**

```html
<!-- ═══════ SLIDE 6 — كيف يعمل؟ ═══════ -->
<div class="slide slide-dark" id="slide-6">
  <div class="spotlight"></div>
  <div class="slide-content" style="width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <h2 class="slide-title anim-fade-up stagger-1" style="margin-bottom:40px">كيف يعمل؟ — ثلاث خطوات بسيطة</h2>
    <div style="display:flex;flex-direction:row-reverse;gap:30px;max-width:1000px;position:relative;align-items:stretch">
      <!-- Connecting line behind cards — draws on slide entry -->
      <div class="anim-draw-line" style="position:absolute;top:50%;right:15%;left:15%;height:2px;border-top:2px dashed var(--gold);opacity:0.3;z-index:0"></div>

      <div class="glass-card anim-fade-up stagger-2" style="flex:1;text-align:center;position:relative;z-index:1">
        <div style="font-size:48px;margin-bottom:8px">🎥</div>
        <div style="font-size:14px;color:var(--gold);margin-bottom:8px">①</div>
        <h3 style="font-family:'Amiri',serif;font-size:24px;margin-bottom:12px">نشاهد</h3>
        <p style="color:var(--text-light);font-size:16px;line-height:1.8">نسجّل العرض المسرحي بالكاميرا كما يراه المتفرج</p>
      </div>
      <div class="glass-card anim-fade-up stagger-3" style="flex:1;text-align:center;position:relative;z-index:1">
        <div style="font-size:48px;margin-bottom:8px">🔍</div>
        <div style="font-size:14px;color:var(--gold);margin-bottom:8px">②</div>
        <h3 style="font-family:'Amiri',serif;font-size:24px;margin-bottom:12px">نحلّل</h3>
        <p style="color:var(--text-light);font-size:16px;line-height:1.8">الآلة ترصد حركة الممثلين، المسافات بينهم، وتوزيعهم على الركح</p>
      </div>
      <div class="glass-card anim-fade-up stagger-4" style="flex:1;text-align:center;position:relative;z-index:1">
        <div style="font-size:48px;margin-bottom:8px">💡</div>
        <div style="font-size:14px;color:var(--gold);margin-bottom:8px">③</div>
        <h3 style="font-family:'Amiri',serif;font-size:24px;margin-bottom:12px">نكتشف</h3>
        <p style="color:var(--text-light);font-size:16px;line-height:1.8">نحصل على خرائط وأرقام تكشف ما لا تراه العين المجرّدة</p>
      </div>
    </div>
  </div>
</div>
```

- [ ] **Step 3: Create Slide 7 — Methodology (NEW)**

```html
<!-- ═══════ SLIDE 7 — المنهجية ═══════ -->
<div class="slide slide-light" id="slide-7">
  <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;flex:1;width:100%">
    <h2 class="slide-title anim-fade-up stagger-1" style="text-align:center;margin-bottom:40px">المنهجية: لماذا هاتان المسرحيتان؟</h2>
    <div style="display:flex;flex-direction:row-reverse;gap:40px;max-width:900px;width:100%">
      <div class="elevated-card anim-slide-right stagger-2" style="flex:1;text-align:right">
        <h3 style="font-family:'Amiri',serif;font-size:24px;color:var(--navy);margin-bottom:16px;text-align:center">الاختيار</h3>
        <ul style="list-style:none;font-size:17px;line-height:2.2">
          <li style="margin-bottom:8px"><span style="color:var(--gold);margin-left:8px">◆</span> نفس المخرج (منير العرقي) — لعزل متغيّر التطوّر الإخراجي</li>
          <li><span style="color:var(--gold);margin-left:8px">◆</span> نصّان مختلفان (تشيخوف / ميترلينك) — مقاربتان دراماتورجيتان متباينتان</li>
        </ul>
      </div>
      <div class="elevated-card anim-slide-left stagger-3" style="flex:1;text-align:right">
        <h3 style="font-family:'Amiri',serif;font-size:24px;color:var(--navy);margin-bottom:16px;text-align:center">القياس</h3>
        <ul style="list-style:none;font-size:17px;line-height:2.2">
          <li><span style="color:var(--gold);margin-left:8px">◆</span> وضعيات الأجساد</li>
          <li><span style="color:var(--gold);margin-left:8px">◆</span> المسافات بين الممثلين</li>
          <li><span style="color:var(--gold);margin-left:8px">◆</span> استغلال الفضاء الركحي</li>
          <li><span style="color:var(--gold);margin-left:8px">◆</span> كثافة الحركة</li>
          <li><span style="color:var(--gold);margin-left:8px">◆</span> الإضاءة</li>
        </ul>
      </div>
    </div>
  </div>
</div>
```

- [ ] **Step 4: Verify slides 5–7 in browser**

Navigate to slides 5–7. Check: spotlight reveal on 5, glass cards with emoji icons on 6, curtain-lift transition from 6→7, elevated two-column layout on 7.

- [ ] **Step 5: Commit**

```bash
git add pitch-deck.html
git commit -m "add slides 5-7: reveal, how-it-works, methodology"
```

---

### Task 5: Slides 8–11 — Act 3 (The Proof)

Rebuild the data slides with animated counters and improved layouts.

**Files:**
- Modify: `pitch-deck.html` — rebuild slides 8–11 (formerly slides 6–9)

- [ ] **Step 1: Rebuild Slide 8 — Space Engineering (with animated counter)**

```html
<!-- ═══════ SLIDE 8 — هندسة الفضاء ═══════ -->
<div class="slide slide-light" id="slide-8">
  <div style="display:flex;flex-direction:column;align-items:center;flex:1;width:100%">
    <h2 class="slide-title anim-fade-up stagger-1" style="text-align:center;margin-top:20px">هندسة الفضاء: من العزلة إلى الاكتظاظ</h2>
    <img src="Enhance_this_diagram_its_in_arabic_2k_delpmaspu.png" alt="هندسة الفضاء الركحي" class="slide-image anim-scale stagger-2" style="max-height:55vh">
  </div>
  <div class="slide-footer anim-fade-up stagger-3" style="display:flex;justify-content:center;gap:40px;font-size:20px;font-weight:700">
    <span>كثافة الحركة تضاعفت <span style="color:var(--gold);font-size:28px" data-counter="100" data-prefix="+" data-suffix="%">0%</span></span>
    <span>المساحة المستغلة ارتفعت <span style="color:var(--gold);font-size:28px" data-counter="112" data-prefix="+" data-suffix="%">0%</span></span>
  </div>
</div>
```

- [ ] **Step 2: Rebuild Slide 9 — Body & Proximity**

```html
<!-- ═══════ SLIDE 9 — الجسد والزمن ═══════ -->
<div class="slide slide-light" id="slide-9">
  <h2 class="slide-title anim-fade-up stagger-1" style="text-align:center;margin-top:20px">الجسد والزمن: من المسافة إلى الالتصاق</h2>
  <div class="split" style="flex:1;margin-top:20px">
    <div class="split-half anim-slide-right stagger-2">
      <img src="Enhance_image_in_arabic_bec4eb0ba2.jpeg" alt="مقارنة البروكسمية" style="max-height:55vh;max-width:100%;object-fit:contain">
    </div>
    <div class="split-half anim-slide-left stagger-3">
      <img src="E9d5f849faac42cf922499cf33fa360fjpg_4b9f6d5d04.jpeg" alt="تحليل الزمن والإيقاع" style="max-height:55vh;max-width:100%;object-fit:contain">
    </div>
  </div>
</div>
```

- [ ] **Step 3: Rebuild Slide 10 — Digital Dashboard**

```html
<!-- ═══════ SLIDE 10 — اللوحة الرقمية ═══════ -->
<div class="slide slide-light" id="slide-10">
  <div style="display:flex;flex-direction:column;align-items:center;flex:1;width:100%">
    <h2 class="slide-title anim-fade-up stagger-1" style="text-align:center;margin-top:20px">اللوحة الرقمية الشاملة: من الفردية المعزولة إلى التيه الجماعي</h2>
    <img src="Enhance_arabic_diagram_2345ea7c81.jpeg" alt="رادار الشخصية" class="slide-image anim-scale stagger-2" style="max-height:62vh">
  </div>
  <div class="slide-footer anim-fade-up stagger-3">من مسرح المرآة إلى مسرح الاشتباك</div>
</div>
```

- [ ] **Step 4: Rebuild Slide 11 — AI on Stage**

```html
<!-- ═══════ SLIDE 11 — الذكاء الاصطناعي ═══════ -->
<div class="slide slide-light" id="slide-11">
  <h2 class="slide-title anim-fade-up stagger-1" style="text-align:center;margin-top:20px">الذكاء الاصطناعي على خشبة المسرح</h2>
  <div class="split" style="flex:1;margin-top:20px">
    <div class="split-half anim-slide-right stagger-2">
      <div class="scan-overlay" style="display:inline-block">
        <img src="../results/with_distances/yolov8/baseline/Kiss/anas argui - The Kiss - القبلة (of Tchekhov) , Directed by Mounir Argui [x7KCHIOzS7o - 1166x656 - 15m42s].png" alt="تقدير الوضعية" style="max-height:55vh;max-width:100%;object-fit:contain;border-radius:8px;display:block">
      </div>
    </div>
    <div class="split-half anim-slide-left stagger-3">
      <img src="Make_diagram_in_arabic_3861df9675.jpeg" alt="توزيع المسافات" style="max-height:55vh;max-width:100%;object-fit:contain;border-radius:8px">
    </div>
  </div>
  <div class="slide-footer anim-fade-up stagger-4">تحليل آلي لحركة الممثلين والمسافات بين الأجساد</div>
</div>
```

- [ ] **Step 5: Verify slides 8–11 in browser**

Navigate to slides 8–11. Check: animated counters on slide 8 (numbers count from 0 to 100/112), split views with slide-in animations on 9 and 11, scale-in on 10.

- [ ] **Step 6: Commit**

```bash
git add pitch-deck.html
git commit -m "rebuild slides 8-11: data proof section with animated counters"
```

---

### Task 6: Slides 12–14 — Act 4 Part 1 (Platform, Use Cases, Roadmap)

Build the platform showcase and two new slides.

**Files:**
- Modify: `pitch-deck.html` — rebuild slide 12, add slides 13–14

- [ ] **Step 1: Rebuild Slide 12 — DRAMYX Platform**

```html
<!-- ═══════ SLIDE 12 — المنصة ═══════ -->
<div class="slide slide-dark" id="slide-12">
  <div class="spotlight"></div>
  <div class="slide-content" style="width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <h2 class="slide-title anim-fade-up stagger-1" style="margin-bottom:8px">تكتيك المسرح — DRAMYX</h2>
    <div class="gold-bar anim-fade-up stagger-2" style="margin-bottom:30px"></div>
    <div class="split" style="max-width:1100px;align-items:center">
      <div class="split-half anim-scale stagger-3" style="flex:1.2">
        <img src="a2296007-bfb6-4504-9ac3-05d46f2b5419.jpg" alt="اللوحة الرقمية الشاملة" style="max-height:50vh;max-width:100%;object-fit:contain;border-radius:8px;border:1px solid rgba(201,168,76,0.3)">
      </div>
      <div class="split-half anim-fade-up stagger-4" style="flex:0.8;text-align:right">
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

- [ ] **Step 2: Create Slide 13 — Use Cases (NEW)**

```html
<!-- ═══════ SLIDE 13 — حالات الاستخدام ═══════ -->
<div class="slide slide-dark" id="slide-13">
  <div class="spotlight"></div>
  <div class="slide-content" style="width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <h2 class="slide-title anim-fade-up stagger-1" style="margin-bottom:40px">من يستفيد من تكتيك المسرح؟</h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;max-width:800px;direction:rtl">
      <div class="glass-card anim-fade-up stagger-2" style="text-align:right">
        <div style="font-size:32px;margin-bottom:8px">🎭</div>
        <h3 style="font-family:'Amiri',serif;font-size:22px;margin-bottom:8px">المهرجانات</h3>
        <p style="color:var(--text-light);font-size:15px;line-height:1.8">أدوات تقييم موضوعية للجان التحكيم</p>
      </div>
      <div class="glass-card anim-fade-up stagger-3" style="text-align:right">
        <div style="font-size:32px;margin-bottom:8px">🎓</div>
        <h3 style="font-family:'Amiri',serif;font-size:22px;margin-bottom:8px">الجامعات</h3>
        <p style="color:var(--text-light);font-size:15px;line-height:1.8">أداة تعليمية لبرامج الدراسات المسرحية</p>
      </div>
      <div class="glass-card anim-fade-up stagger-4" style="text-align:right">
        <div style="font-size:32px;margin-bottom:8px">🎬</div>
        <h3 style="font-family:'Amiri',serif;font-size:22px;margin-bottom:8px">المخرجون</h3>
        <p style="color:var(--text-light);font-size:15px;line-height:1.8">تحليل ذاتي لاختياراتهم الإخراجية</p>
      </div>
      <div class="glass-card anim-fade-up stagger-5" style="text-align:right">
        <div style="font-size:32px;margin-bottom:8px">🏛️</div>
        <h3 style="font-family:'Amiri',serif;font-size:22px;margin-bottom:8px">الأرشيف الثقافي</h3>
        <p style="color:var(--text-light);font-size:15px;line-height:1.8">حفظ الإرث الأدائي رقمياً للأجيال القادمة</p>
      </div>
    </div>
  </div>
</div>
```

- [ ] **Step 3: Create Slide 14 — Roadmap (NEW)**

```html
<!-- ═══════ SLIDE 14 — خارطة الطريق ═══════ -->
<div class="slide slide-dark" id="slide-14">
  <div class="spotlight"></div>
  <div class="slide-content" style="width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center">
    <h2 class="slide-title anim-fade-up stagger-1" style="margin-bottom:50px">خارطة الطريق</h2>
    <div style="display:flex;flex-direction:row-reverse;gap:0;max-width:1000px;width:100%;align-items:flex-start;position:relative">
      <!-- Timeline line — draws on slide entry -->
      <div class="anim-draw-line" style="position:absolute;top:28px;right:10%;left:10%;height:3px;background:linear-gradient(to left,var(--gold),rgba(201,168,76,0.2));z-index:0"></div>

      <div class="anim-fade-up stagger-2" style="flex:1;text-align:center;position:relative;z-index:1">
        <div style="width:20px;height:20px;background:var(--gold);border-radius:50%;margin:18px auto 20px;box-shadow:0 0 15px rgba(201,168,76,0.4)"></div>
        <div class="glass-card" style="text-align:right;padding:20px">
          <h3 style="font-family:'Amiri',serif;font-size:20px;color:var(--gold);margin-bottom:8px">المرحلة الأولى — 2026</h3>
          <p style="color:var(--text-light);font-size:14px;line-height:1.8">نموذج بحثي أوّلي، تحليل مسرحيتين، نشر النتائج</p>
        </div>
      </div>
      <div class="anim-fade-up stagger-3" style="flex:1;text-align:center;position:relative;z-index:1">
        <div style="width:20px;height:20px;background:var(--gold);border-radius:50%;margin:18px auto 20px;box-shadow:0 0 15px rgba(201,168,76,0.4)"></div>
        <div class="glass-card" style="text-align:right;padding:20px">
          <h3 style="font-family:'Amiri',serif;font-size:20px;color:var(--gold);margin-bottom:8px">المرحلة الثانية — 2027</h3>
          <p style="color:var(--text-light);font-size:14px;line-height:1.8">منصة MVP، أكثر من 20 عرضاً، شراكات مع مهرجانات</p>
        </div>
      </div>
      <div class="anim-fade-up stagger-4" style="flex:1;text-align:center;position:relative;z-index:1">
        <div style="width:20px;height:20px;background:var(--gold);border-radius:50%;margin:18px auto 20px;box-shadow:0 0 15px rgba(201,168,76,0.4)"></div>
        <div class="glass-card" style="text-align:right;padding:20px">
          <h3 style="font-family:'Amiri',serif;font-size:20px;color:var(--gold);margin-bottom:8px">المرحلة الثالثة — +2028</h3>
          <p style="color:var(--text-light);font-size:14px;line-height:1.8">قاعدة بيانات عالمية، API للباحثين، دعم متعدد اللغات</p>
        </div>
      </div>
    </div>
  </div>
</div>
```

- [ ] **Step 4: Verify slides 12–14 in browser**

Navigate to slides 12–14. Check: platform slide split layout, use cases 2x2 grid with glass cards, roadmap timeline with gold nodes and glass cards.

- [ ] **Step 5: Commit**

```bash
git add pitch-deck.html
git commit -m "add slides 12-14: platform, use cases, roadmap"
```

---

### Task 7: Slides 15–17 — Act 4 Part 2 (Vision, Team, Closing)

Build the final three slides.

**Files:**
- Modify: `pitch-deck.html` — rebuild slides 15–17 (formerly 11–12)

- [ ] **Step 1: Rebuild Slide 15 — The Vision**

```html
<!-- ═══════ SLIDE 15 — الرؤية ═══════ -->
<div class="slide slide-light" id="slide-15">
  <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%">
    <h2 class="slide-title anim-fade-up stagger-1" style="text-align:center;margin-bottom:40px">الرؤية: المرجع العالمي المعتمد</h2>
    <div style="display:flex;gap:40px;flex-direction:row-reverse;max-width:900px;margin-bottom:40px">
      <div class="elevated-card anim-fade-up stagger-2" style="flex:1;text-align:center;padding:24px">
        <div style="font-size:36px;color:var(--gold);margin-bottom:12px">🏛️</div>
        <h3 style="font-family:'Amiri',serif;font-size:22px;color:var(--navy);margin-bottom:8px">رقمنة المسرح</h3>
        <p style="font-size:16px;line-height:1.8;color:#555">حفظ الإرث للأجيال القادمة</p>
      </div>
      <div class="elevated-card anim-fade-up stagger-3" style="flex:1;text-align:center;padding:24px">
        <div style="font-size:36px;color:var(--gold);margin-bottom:12px">📐</div>
        <h3 style="font-family:'Amiri',serif;font-size:22px;color:var(--navy);margin-bottom:8px">تطوير النقد</h3>
        <p style="font-size:16px;line-height:1.8;color:#555">معايير موضوعية وعلمية</p>
      </div>
      <div class="elevated-card anim-fade-up stagger-4" style="flex:1;text-align:center;padding:24px">
        <div style="font-size:36px;color:var(--gold);margin-bottom:12px">🌐</div>
        <h3 style="font-family:'Amiri',serif;font-size:22px;color:var(--navy);margin-bottom:8px">قاعدة بيانات عالمية</h3>
        <p style="font-size:16px;line-height:1.8;color:#555">أرشيف رقمي للأداء المسرحي</p>
      </div>
    </div>
  </div>
</div>
```

- [ ] **Step 2: Create Slide 16 — The Team (NEW)**

```html
<!-- ═══════ SLIDE 16 — الفريق ═══════ -->
<div class="slide slide-light" id="slide-16">
  <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%">
    <h2 class="slide-title anim-fade-up stagger-1" style="text-align:center;margin-bottom:40px">الفريق</h2>
    <div style="display:flex;flex-direction:row-reverse;gap:40px;max-width:800px;margin-bottom:40px">
      <div class="elevated-card anim-slide-right stagger-2" style="flex:1;text-align:center;padding:30px">
        <div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,var(--navy),var(--navy-mid));margin:0 auto 16px;display:flex;align-items:center;justify-content:center">
          <span style="font-size:32px;color:var(--gold)">د</span>
        </div>
        <h3 style="font-family:'Amiri',serif;font-size:22px;color:var(--navy);margin-bottom:8px">د. محمد الكشو</h3>
        <p style="font-size:14px;color:var(--gold);margin-bottom:12px">المشرف العلمي</p>
        <p style="font-size:15px;line-height:1.8;color:#555">مخرج مسرحي وباحث أكاديمي. خبرة في الإخراج والسيميولوجيا المسرحية.</p>
      </div>
      <div class="elevated-card anim-slide-left stagger-3" style="flex:1;text-align:center;padding:30px">
        <div style="width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,var(--navy),var(--navy-mid));margin:0 auto 16px;display:flex;align-items:center;justify-content:center">
          <span style="font-size:32px;color:var(--gold)">م</span>
        </div>
        <h3 style="font-family:'Amiri',serif;font-size:22px;color:var(--navy);margin-bottom:8px">م. فارس النفزي</h3>
        <p style="font-size:14px;color:var(--gold);margin-bottom:12px">المطوّر التقني</p>
        <p style="font-size:15px;line-height:1.8;color:#555">مهندس ذكاء اصطناعي، مسؤول عن تطوير المنصة التقنية وأنظمة التحليل الآلي.</p>
      </div>
    </div>
    <div class="anim-fade-up stagger-4" style="text-align:center">
      <div class="gold-bar"></div>
      <p style="font-size:18px;color:var(--navy);margin-top:16px"><span style="color:var(--gold);font-weight:700">مسرح المدينة بتونس</span></p>
    </div>
  </div>
</div>
```

- [ ] **Step 3: Rebuild Slide 17 — Closing**

```html
<!-- ═══════ SLIDE 17 — الختام ═══════ -->
<div class="slide slide-dark" id="slide-17">
  <div class="spotlight"></div>
  <div class="slide-content" style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%">
    <h1 class="slide-title anim-spotlight" style="font-size:52px;line-height:1.6">لنحوّل سحر المسرح<br>إلى علم باقٍ</h1>
    <div class="gold-bar anim-fade-up stagger-2" style="margin:24px auto"></div>
    <p class="anim-fade-up stagger-3" style="font-size:18px;color:var(--text-light);margin-top:16px">feresnefzi18@gmail.com</p>
    <div class="anim-fade-up stagger-4" style="margin-top:40px;font-size:12px;color:rgba(255,255,255,0.3);letter-spacing:4px">
      <span style="color:var(--gold);font-weight:700">DRAMYX</span> — © 2026
    </div>
  </div>
</div>
```

- [ ] **Step 4: Remove old slides 10–12 that are now replaced**

Ensure the file has exactly 17 slides (id `slide-1` through `slide-17`) with no leftover old slides. Update `TOTAL = 17` in JS and the `lightSlides` set to `new Set([3, 7, 8, 9, 10, 11, 15, 16])`.

- [ ] **Step 5: Full verification in browser**

Navigate through all 17 slides end-to-end. Verify:
- All slides render correctly with proper backgrounds (dark/light)
- Transitions match the spec (crossfade dark→dark, curtain-lift dark→light, horizontal light→light, fade-black light→dark)
- Animated counters on slide 8
- Navigation: arrow keys, PageDown/PageUp, Space/Backspace, Home/End
- Nav buttons appear on hover
- Slide counter updates correctly (1/17 through 17/17)
- Counter color adapts to slide background

- [ ] **Step 6: Commit**

```bash
git add pitch-deck.html
git commit -m "complete slides 15-17: vision, team, closing — full 17-slide deck"
```

---

### Task 8: Final Polish and Print Styles

Final pass for consistency, cleanup, and print/PDF export support.

**Files:**
- Modify: `pitch-deck.html`

- [ ] **Step 1: Verify all image paths exist**

Check that all referenced images exist at their paths. Run from the Presentation directory:

```bash
ls "../images/Kiss/anas argui - The Kiss"*.png 2>/dev/null | head -2
ls "../images/Blackout/8015c3a5"*.jpg 2>/dev/null | head -1
ls Enhance_this_diagram_its_in_arabic_2k_delpmaspu.png 2>/dev/null
ls Enhance_image_in_arabic_bec4eb0ba2.jpeg 2>/dev/null
ls E9d5f849faac42cf922499cf33fa360fjpg_4b9f6d5d04.jpeg 2>/dev/null
ls Enhance_arabic_diagram_2345ea7c81.jpeg 2>/dev/null
ls Make_diagram_in_arabic_3861df9675.jpeg 2>/dev/null
ls a2296007-bfb6-4504-9ac3-05d46f2b5419.jpg 2>/dev/null
ls "../results/with_distances/yolov8/baseline/Kiss/anas argui"*.png 2>/dev/null | head -1
```

Fix any missing paths.

- [ ] **Step 2: Verify print styles work**

The print CSS should show all slides stacked vertically. Open browser print preview (Ctrl+P) and verify all 17 slides appear, nav buttons are hidden, and counter is hidden.

- [ ] **Step 3: Final end-to-end walkthrough**

Navigate all 17 slides one more time. Check for:
- Any layout overflow or text clipping
- Animation timing feels natural
- Gold accents are consistent across all slides
- RTL text alignment is correct everywhere

- [ ] **Step 4: Commit final version**

```bash
git add pitch-deck.html
git commit -m "final polish: verify images, print styles, end-to-end consistency"
```
