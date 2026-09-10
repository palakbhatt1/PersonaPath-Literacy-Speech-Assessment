# Deployment — PersonaPath

End-to-end deployment guide tying the frontend (Vercel) and backend (Render/HF Spaces) together, including GitHub Student Developer Pack notes.

## 1. Deployment Architecture

```
GitHub repo(s)
   │
   ├── frontend/  ──push──▶  Vercel  ──▶  https://personapath.vercel.app
   │
   └── backend/   ──push──▶  Render / HF Spaces  ──▶  https://personapath-api.onrender.com
```

Two independently deployed services, connected by one environment variable (`NEXT_PUBLIC_API_URL` on the frontend) and one CORS setting (`ALLOWED_ORIGIN` on the backend).

## 2. Repo Structure Decision

Pick one:

**Option A — Monorepo (simpler to manage)**
```
PersonaPath/
├── frontend/   (Next.js)
├── backend/    (FastAPI)
├── models/
├── data/
└── docs/
```
Both Vercel and Render/HF Spaces support pointing at a subfolder of a monorepo as the build root.

**Option B — Two repos**
`personapath-frontend` and `personapath-backend`. Cleaner separation, slightly more overhead syncing changes.

Recommendation: **Option A** for a project this size — one repo, subfolder deploys.

## 3. Step-by-Step

### 3.1 Backend first (so you have a URL to point the frontend at)

1. Finish porting model inference code into `backend/` per `backend.md`.
2. Push to GitHub.
3. Create a new **Render** Web Service (or HF Space):
   - Connect the GitHub repo.
   - Set root directory to `backend/` (if monorepo).
   - Runtime: Docker (uses your `Dockerfile`).
   - Add env var `ANTHROPIC_API_KEY`.
   - Add env var `ALLOWED_ORIGIN` (fill in after step 3.2, or use `*` temporarily for testing).
4. Deploy. Confirm `/health` (or `/docs` — FastAPI auto-generates Swagger UI) responds.
5. Note the live URL, e.g. `https://personapath-api.onrender.com`.

### 3.2 Frontend

1. Finish porting `UI/` HTML into Next.js per `frontend.md`.
2. Push to GitHub (same repo, `frontend/` subfolder, or separate repo).
3. Go to vercel.com → **New Project** → import the GitHub repo.
   - If monorepo: set "Root Directory" to `frontend/` in project settings.
4. Add environment variable:
   - `NEXT_PUBLIC_API_URL=https://personapath-api.onrender.com`
5. Deploy.
6. Go back to Render and set `ALLOWED_ORIGIN` to your real Vercel URL (e.g. `https://personapath.vercel.app`) instead of `*`.
7. Redeploy backend so CORS picks up the change.

### 3.3 Verify end-to-end

1. Open the Vercel URL.
2. Record/upload a sample clip through the UI.
3. Confirm it reaches the backend, runs inference, and the coaching feedback renders correctly.
4. Check Render/HF Spaces logs if anything fails (most common issues: CORS origin mismatch, missing env var, upload size limits).

## 4. GitHub Student Developer Pack — what it actually gets you here

- **Vercel:** The Student Pack has historically included Vercel perks. Offers change over time, so check the current listing at education.github.com/pack before assuming a specific tier. Not required for this project to work — Vercel's free (Hobby) tier is enough for a portfolio-scale Next.js frontend.
- **Cloud credits (Azure/DigitalOcean, etc.):** Useful if you outgrow Render/HF free tiers, or want a VM for full control. Not needed for the initial deployment.
- **No GPU perk is required** — as established, inference runs fine on CPU for this project's scale.

## 5. Cost/Limits Sanity Check

| Service | Free tier limits to watch |
|---|---|
| Vercel Hobby | Fine for a Next.js frontend; watch serverless function execution time if you add API routes there |
| Render free web service | Spins down after inactivity (cold start delay on first request after idle) — expect a slower first analysis after idle periods |
| Hugging Face Spaces free CPU | Similar cold-start behavior; good alternative if Render's sleep behavior is annoying |

## 6. Post-Deployment Checklist

- [ ] Backend `/docs` (Swagger) loads and shows `/api/analyze`.
- [ ] Frontend successfully calls backend and renders results for a real sample.
- [ ] `ANTHROPIC_API_KEY` is set only on the backend, never in frontend code or `NEXT_PUBLIC_*` vars.
- [ ] CORS restricted to your real Vercel domain (not `*`) before calling this "done."
- [ ] Add a short demo write-up / GIF to the repo README pointing at the live URLs.

## 7. Related Docs

- `frontend.md` — Next.js + Vercel details
- `backend.md` — FastAPI + model serving + Render/HF Spaces details
- `DESIGN.md` — UI design system spec
