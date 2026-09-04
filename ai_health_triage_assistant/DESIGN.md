---
name: AI Health Triage Assistant
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#3e484b'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#6f797b'
  outline-variant: '#bec8cb'
  surface-tint: '#006875'
  primary: '#005a65'
  on-primary: '#ffffff'
  primary-container: '#0d7482'
  on-primary-container: '#bbf4ff'
  inverse-primary: '#81d3e2'
  secondary: '#545f73'
  on-secondary: '#ffffff'
  secondary-container: '#d5e0f8'
  on-secondary-container: '#586377'
  tertiary: '#475456'
  on-tertiary: '#ffffff'
  tertiary-container: '#5f6c6e'
  on-tertiary-container: '#dfedef'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#9defff'
  primary-fixed-dim: '#81d3e2'
  on-primary-fixed: '#001f24'
  on-primary-fixed-variant: '#004e59'
  secondary-fixed: '#d8e3fb'
  secondary-fixed-dim: '#bcc7de'
  on-secondary-fixed: '#111c2d'
  on-secondary-fixed-variant: '#3c475a'
  tertiary-fixed: '#d7e5e7'
  tertiary-fixed-dim: '#bbc9cb'
  on-tertiary-fixed: '#111e1f'
  on-tertiary-fixed-variant: '#3c494b'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  headline-xl:
    fontFamily: plusJakartaSans
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: plusJakartaSans
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: plusJakartaSans
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.015em
  headline-lg-mobile:
    fontFamily: plusJakartaSans
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 30px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: plusJakartaSans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: plusJakartaSans
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: inter
    fontSize: 17px
    fontWeight: '400'
    lineHeight: 26px
    letterSpacing: -0.005em
  body-md:
    fontFamily: inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  body-sm:
    fontFamily: inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  label-lg:
    fontFamily: inter
    fontSize: 15px
    fontWeight: '600'
    lineHeight: 20px
  label-md:
    fontFamily: inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
  label-sm:
    fontFamily: inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  space-xxs: 0.25rem
  space-xs: 0.5rem
  space-sm: 0.75rem
  space-md: 1rem
  space-lg: 1.25rem
  space-xl: 1.5rem
  space-2xl: 2rem
  space-3xl: 3rem
  gutter-mobile: 1rem
  margin-mobile: 1.25rem
  gutter-tablet: 1.5rem
  margin-tablet: 2rem
  max-content-width: 30rem
---

## Brand & Style

The design system establishes an atmosphere of clinical authority merged with bedside empathy. Built for individuals navigating acute symptoms, chronic conditions, and urgent health concerns, the aesthetic reduces cognitive load and mitigates health-related anxiety.

### Personality & Emotional Tenets
- **Reassuring & Grounded:** Interventions feel steady, validated, and soothing rather than alarmist.
- **Clinical Precision:** High-contrast legibility, rigorous visual balance, and unambiguous hierarchies reflect diagnostic reliability.
- **Empathetic Simplicity:** Generous breathing room, accessible touch points, and conversational clarity comfort vulnerable patients.

### Design Movement: Modern Clinical Minimalist
The style synthesizes Swiss informational clarity with contemporary warm-slate minimalism. It rejects cold, sterile utilitarianism in favor of soft ambient depths, whisper-weight borders, and restorative teal and maritime palettes. Dynamic decorative flourishes are eliminated; visual impact relies purely on typography, deliberate spacing, and critical triage state indicators.

## Colors

The palette is engineered around calm restorative blues and clean slates, reserving high-chroma tones strictly for clinical triage stratification.

### Primary & Brand Palette
- **Primary Deep Teal (`#0D7482`):** Communicates clinical credibility and reassurance. Utilized for primary actions, active states, key interactive indicators, and brand anchoring.
- **Secondary Deep Slate (`#1E293B`):** Serves as high-contrast primary typography and foundational structural chrome.
- **Tertiary Soft Ice Teal (`#E6F4F6`):** Provides a soothing, low-stimulus tinted background for active selection states, callout cards, and highlighted triage messaging.
- **Neutral Slate (`#64748B`):** Delivers WCAG AAA-compliant secondary labels, metadata, and non-interactive borders.
- **Canvas App Background (`#F8FAFC`):** A warm, medical-grade paper off-white that reduces glare during night-time symptom logging.

### Reserved Triage Semantics
Semantic triage colors must never be used for casual decoration, generic illustrations, or marketing badges. They are strictly functional diagnostic markers:
- **Routine / Self-Care (Emerald):** `#059669` (Surface: `#ECFDF5`, Border: `#A7F3D0`). Signifies non-urgent outcomes, standard recovery metrics, and self-managed remedies.
- **Moderate / Consult Doctor (Amber):** `#D97706` (Surface: `#FFFBEB`, Border: `#FDE68A`). Identifies symptoms requiring clinical evaluation within 24–48 hours without immediate emergency escalation.
- **Urgent / Immediate Care (Crimson):** `#DC2626` (Surface: `#FEF2F2`, Border: `#FECACA`). Triggers clear emergency protocols, ED guidance, and crisis intervention pathways.

## Typography

The type system blends the human, welcoming geometry of Plus Jakarta Sans for structural headings with the utilitarian legibility of Inter for body prose, conversational agent dialogues, and dense clinical data.

- **Headings (Plus Jakarta Sans):** Crafted with tight tracking and balanced weights (`600`, `700`) to present diagnosis summaries and symptom inquiries with warmth and authoritative clarity.
- **Body & Data (Inter):** Highly legible neutral grotesque with open apertures, distinct letterforms, and generous x-height. Preserves instant readability for patients experiencing fatigue, visual impairment, or elevated stress.
- **Hierarchy Rules:** Body text must strictly use `body-md` (15px) or `body-lg` (17px) on mobile viewports; critical diagnostic reading must never dip below 13px (`body-sm`).

## Layout & Spacing

The layout is grounded in a mobile-first fluid model bounded by an optimal ergonomic reading column (`max-content-width: 480px / 30rem`) on larger screens.

### Spatial Rhythm & Grid
- **Scale:** Base-8 grid unit system (`4px`, `8px`, `12px`, `16px`, `20px`, `24px`, `32px`, `48px`).
- **Mobile Hand Ergonomics:** Margins are set to `1.25rem` (20px) to provide edge clearance while maximizing card surface area. Interactive tappable touchpoints sit within comfortable one-handed thumbsweep ranges at the lower 40% of the screen.
- **Generous Breathing Space:** Symptom questions and response nodes must maintain at least `space-xl` (24px) vertical separation to prevent mis-taps during stressful intake procedures.

## Elevation & Depth

Visual hierarchy uses a hybrid strategy of **Tonal Layering** accompanied by **Subtle Ambient Shadows** and **Micro-Borders**. Heavy drop shadows and glass blurs are avoided to maintain clear contrast and medical-grade legibility.

### Surface Tiers
- **Base Canvas (Level 0):** `#F8FAFC`. The foundational backdrop for screen transitions and symptom questionnaires.
- **Card Surfaces (Level 1):** `#FFFFFF`. Resting surface for interactive inputs, diagnostic cards, and patient profiles. Bound by a crisp `1px` micro-border (`#E2E8F0`).
- **Active / Raised Elements (Level 2):** `#FFFFFF` paired with an ambient diffuse shadow:
  - `box-shadow: 0 4px 16px -2px rgba(15, 23, 42, 0.05), 0 2px 6px -1px rgba(15, 23, 42, 0.03);`
  - Utilized for bottom action sheets, active triage result highlights, and elevated sticky triage action bars.
- **Emergency Priority Layer (Level 3):** Reserved for urgent triage prompts and emergency call triggers:
  - `box-shadow: 0 10px 25px -3px rgba(220, 38, 38, 0.12), 0 4px 6px -2px rgba(220, 38, 38, 0.04);`

## Shapes

The design uses a roundedness level of `2` (Moderate/Friendly Curvature).

- **Standard Cards & Containers:** `1rem` (`rounded-lg` / 16px) creates an organic, accessible visual tone while preserving structural balance.
- **Modals & Bottom Drawers:** `1.5rem` (`rounded-xl` / 24px) top corner radii soften the interface when presenting diagnostic outcomes.
- **Form Inputs & Action Buttons:** `0.75rem` (`rounded-md` / 12px) provides clear, distinct tap boundaries.
- **Pills & Triage Badges:** Fully circular radii (`9999px`) reserved for classification tags, triage status chips, and step progression counters.

## Components

### Buttons
- **Primary Medical Action:** Solid `#0D7482` with crisp `#FFFFFF` text. Minimum height `52px` to guarantee accessible mobile touch targets. Smooth focus ring in `#0D7482` with a `2px` offset.
- **Secondary Clinical Action:** Surface `#E6F4F6` with `#0D7482` text. Used for alternative triage navigation, symptom re-evaluation, or non-critical secondary flows.
- **Urgent Care / 911 Direct Action:** High-urgency solid `#DC2626` background, bold white typography, equipped with an optional emergency phone icon.

### Cards & Assessment Modules
- White `#FFFFFF` foundation with `1px` border in `#E2E8F0`.
- **Triage Result Card:** Highlights urgency through a solid 4px left border matching the assigned triage semantic (Emerald, Amber, or Crimson), accompanied by a light semantic-tinted title pill (`11px`, all caps, tracking `0.04em`).

### Chips & Symptom Multi-Select
- Default State: `#FFFFFF` fill, `1px` border `#CBD5E1`, text `#475569`.
- Selected State: `#E6F4F6` background, `1.5px` border `#0D7482`, text `#0D7482` with a checked confirmation icon.
- Touch target minimum: `44px` height with `12px 16px` internal padding.

### Form Inputs & Health Scales
- Inputs feature clear, high-contrast labels above fields, backed by `#F8FAFC` inner surface and a `1px` border `#CBD5E1` transitioning to a `#0D7482` border with a subtle focus glow when active.
- **Severity Sliders:** 1–10 numerical pain/symptom scale with distinct visual color steps (0–3 Emerald, 4–6 Amber, 7–10 Crimson) and bold thumb controls designed for easy thumb drag.

### Lists & Symptom Timelines
- Separated with hairline borders (`#F1F5F9`), maintaining generous `16px` vertical internal padding to prevent mis-clicks when patients review past vitals and symptom logs.