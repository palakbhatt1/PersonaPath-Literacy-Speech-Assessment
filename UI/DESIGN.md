---
name: Cognitive Bridge
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
  on-surface-variant: '#444653'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#757684'
  outline-variant: '#c4c5d5'
  surface-tint: '#3755c3'
  primary: '#00288e'
  on-primary: '#ffffff'
  primary-container: '#1e40af'
  on-primary-container: '#a8b8ff'
  inverse-primary: '#b8c4ff'
  secondary: '#006c49'
  on-secondary: '#ffffff'
  secondary-container: '#6cf8bb'
  on-secondary-container: '#00714d'
  tertiary: '#70000c'
  on-tertiary: '#ffffff'
  tertiary-container: '#9b0015'
  on-tertiary-container: '#ffa39c'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dde1ff'
  primary-fixed-dim: '#b8c4ff'
  on-primary-fixed: '#001453'
  on-primary-fixed-variant: '#173bab'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffdad7'
  tertiary-fixed-dim: '#ffb3ad'
  on-tertiary-fixed: '#410004'
  on-tertiary-fixed-variant: '#930013'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-learning:
    fontFamily: Lexend
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.2'
  body-coaching:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  data-header:
    fontFamily: Lexend
    fontSize: 14px
    fontWeight: '600'
    lineHeight: '1.4'
    letterSpacing: 0.02em
  data-value:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: '1.4'
  tech-tag:
    fontFamily: Space Grotesk
    fontSize: 11px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 40px
  gutter: 20px
  container-max: 1280px
---

## Brand & Style

The design system is engineered to bridge the gap between developmental learning and high-fidelity data science. It caters to two primary user personas: the student (requiring encouragement and clarity) and the educator/analyst (requiring precision and insight).

The visual style is **Corporate Modern with a Soft Edge**. It leverages high-legibility layouts and professional color theory but softens the execution through generous radii and conversational patterns. The interface transitions from a supportive "Coaching" mode into a sophisticated "Analytical" mode without losing its core identity. It evokes trust, intellectual growth, and technological transparency.

## Colors

The palette is anchored by **Professional Blue**, providing a foundation of reliability and institutional quality. 

- **Primary (Professional Blue):** Used for navigation, primary actions, and branding.
- **Growth Green:** Reserved for "Correct" states, high-confidence AI scores, and positive progress.
- **Caution Red:** Denotes mispronunciations, low-confidence intervals, or "nervous" speech patterns.
- **Neutral Grey:** Used for skipped items, inactive states, and structural borders.
- **Background:** A high-legibility off-white (#F8FAFC) reduces eye strain during long analytical sessions while maintaining a clean, academic feel.

## Typography

This system utilizes a dual-font strategy to differentiate between intent and information density.

- **Lexend** is used for headlines and student-facing interfaces. Its design is specifically optimized for reading proficiency and provides a friendly, approachable character.
- **Inter** handles the bulk of body copy and data density, offering a neutral, systematic appearance for analytical dashboards.
- **Space Grotesk** is applied exclusively to "Tech Tags." Its monospaced-adjacent feel signals technical "under-the-hood" AI metadata (e.g., model versions).

**Phase 1 (Learning):** Focuses on larger scales (`display-learning`, `body-coaching`) to ensure accessibility for younger users.
**Phase 2 (Analysis):** Shifts to compact scales (`data-header`, `data-value`) to maximize information density in dashboards.

## Layout & Spacing

The system employs a **Fixed Grid** philosophy for analytical dashboards and a **Centered Fluid** model for coaching interfaces. 

- **Coaching Layout:** Large margins (xl) and centered content blocks to minimize distractions.
- **Analytical Layout:** A 12-column grid with 20px gutters. Information is grouped into modular cards that can span 3, 4, or 6 columns depending on the complexity of the visualization (e.g., a wide line graph vs. a narrow gauge).
- **Rhythm:** All spacing is based on a 4px baseline unit to ensure consistent alignment of "Tech Tags" and label elements within data rows.

## Elevation & Depth

Hierarchy is established using **Tonal Layers** and **Low-Contrast Outlines**. 

- **Surfaces:** The primary background is the lowest layer. Cards and "Coaching Bubbles" sit on a pure white surface.
- **Depth:** Instead of heavy shadows, this system uses subtle 1px borders in `Neutral Grey` (at 10-20% opacity) to define boundaries. 
- **Shadows:** For Phase 1 coaching bubbles, a soft, diffused "ambient" shadow (0px 4px 20px rgba(0,0,0,0.05)) is used to create a gentle "floating" effect, making the interface feel friendly and interactive.
- **Analytical Layers:** Phase 2 uses flat, inset backgrounds for data containers to suggest "wells" of information.

## Shapes

The shape language reflects the system's dual nature:
- **Phase 1 (Rounded):** Chat bubbles and primary buttons use the `rounded-xl` (1.5rem) setting to feel safe and soft.
- **Phase 2 (Structured):** Data cards and "Tech Tags" transition toward the base `rounded` (0.5rem) setting to maintain a professional, organized appearance suitable for high-density information.
- **Tech Tags:** These specific pill-shaped components always use a full radius (pill-shaped) regardless of the phase, distinguishing them as immutable metadata.

## Components

- **Buttons:** Primary buttons are "Professional Blue" with white text. In Phase 1, they are large and high-contrast. In Phase 2, they become smaller and more utilitarian.
- **Claude’s Coaching Corner (Chat Bubbles):** Large, rounded containers with a tail. They use the `primary_color` for the name label and `body-coaching` typography.
- **Tech Tags:** Small, pill-shaped labels with a light grey background and `tech-tag` monospace typography. They appear next to AI-generated insights to cite the model (e.g., "Wav2Vec 2.0").
- **Analytical Gauges:** Circular progress indicators using `Growth Green` for completion or accuracy percentages.
- **Data Cards:** White containers with a 1px soft border. They house line graphs (performance over time) and bar charts (frequency analysis).
- **Status Chips:** Small, solid-color indicators (Green, Red, or Grey) used in transcripts to highlight specific phonetic performance.