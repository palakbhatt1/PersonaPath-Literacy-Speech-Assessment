# Frontend — PersonaPath

This document covers the frontend architecture, tech stack, and deployment plan for PersonaPath's user-facing interface.

## 1. Overview

The frontend is the "Cognitive Bridge" dual-persona UI: a friendly, encouraging experience for younger learners (Phase 1) and a data-dense analytical dashboard for advanced users (Phase 2). It does **not** run any ML models itself — it collects audio/video input, sends it to the backend API, and renders the returned scores, transcripts, and Claude-generated coaching feedback.

```
User (browser)
   │
   ▼
Frontend (Next.js, hosted on Vercel)
   │  fetch("/api/analyze", { audio/video })
   ▼
Backend API (FastAPI, hosted on Render / HF Spaces)
   │  runs Wav2Vec2 / MobileNetV2 / LSTM inference
   │  calls Anthropic API for coaching feedback
   ▼
Response: { scores, transcript, feedback, tags }
```

## 2. Current State

| Item | Status |
|---|---|
| `UI/`, `templates/` | Raw HTML/CSS ("Cognitive Bridge" design system) — `index.html`, `Phase1.html`, `Phase2.html` |
| `DESIGN.md` | Full design spec (typography, color tokens, layout rules) |
| Framework | None yet — static HTML/CSS only |
| Deployment | None yet |

## 3. Target Stack

- **Framework:** Next.js (App Router) — plays natively with Vercel, supports API routes if needed for lightweight proxying.
- **Styling:** Keep the existing design tokens from `DESIGN.md` (colors, `Lexend` / `Inter` / `Space Grotesk` fonts, border-radius scale) — port them into a Tailwind config or CSS variables rather than rewriting the visual language from scratch.
- **State/data fetching:** Native `fetch` to backend API; React state for local UI (recording state, phase toggle, results).
- **Media capture:** Browser `MediaRecorder` API for audio/video capture in-browser (avoids needing a native app).

## 4. Migration Plan: HTML → Next.js

1. **Scaffold** a Next.js app (`npx create-next-app@latest`).
2. **Port design tokens** from `DESIGN.md` into `globals.css` (CSS variables) or `tailwind.config.js`.
3. **Convert each HTML file to a route/component:**
   - `index.html` → `app/page.tsx` (landing / phase selector)
   - `Phase1.html` → `app/learn/page.tsx` (ages 5–10 experience, chat-bubble coaching UI)
   - `Phase2.html` → `app/analyze/page.tsx` (12-column analytical dashboard)
4. **Extract shared components:** navbar, "Claude's Coaching Corner" chat bubble, tech-tag pill, score gauge (Growth Green / Caution Red).
5. **Wire up media capture + upload:**
   - Record audio/video client-side with `MediaRecorder`.
   - POST to backend endpoint (e.g. `/api/analyze`) as `multipart/form-data`.
6. **Render results:** map backend JSON response into the Phase 1 / Phase 2 layouts (score gauges, transcript highlighting, tech tags, coaching feedback bubbles).
7. **Env vars:** store backend base URL as `NEXT_PUBLIC_API_URL` in Vercel project settings (never put the Anthropic API key in frontend code — that stays server-side in the backend).

## 5. Deployment (Vercel)

1. Push the Next.js app to GitHub (separate folder or repo, e.g. `personapath-frontend`).
2. Import the repo into Vercel (GitHub Student Pack unlocks Vercel Pro perks — not required for this to work, free tier is sufficient for a project this size).
3. Set environment variable:
   - `NEXT_PUBLIC_API_URL=https://<your-backend-url>`
4. Deploy — Vercel auto-builds on every push to `main`.
5. No GPU, no long-running processes, no FFmpeg needed on this side — it's pure static/SSR frontend, which is exactly what Vercel is built for.

## 6. Open Items

- [ ] Decide: Tailwind vs. plain CSS variables for porting `DESIGN.md` tokens.
- [ ] Decide: single repo (monorepo with backend) vs. two repos.
- [ ] Build the score-gauge and chat-bubble components as reusable pieces.
- [ ] Add loading/error states while waiting on backend inference (can take a few seconds on CPU).

## 7. Related Docs

- `DESIGN.md` — full "Cognitive Bridge" design system spec
- `backend.md` — FastAPI backend architecture and deployment (Render / Hugging Face Spaces)
