# Backend — PersonaPath

This document covers the backend architecture, model-serving plan, and hosting options for PersonaPath's inference API.

## 1. Overview

The backend is a Python API that:
1. Accepts an uploaded audio/video clip from the frontend.
2. Runs it through the three trained models (Wav2Vec 2.0, MobileNetV2, LSTM).
3. Computes pronunciation, confidence, and emotion metrics.
4. Sends those raw metrics to the Anthropic API to generate human-readable coaching feedback.
5. Returns a single JSON response to the frontend.

```
POST /api/analyze  (multipart/form-data: audio/video file)
   │
   ▼
1. Save/decode upload → temp file
2. Audio pipeline:
     Librosa → MFCC/delta/pitch/ZCR features → LSTM → confidence score
     Wav2Vec2 (transformers) → transcript → pronouncing + python-Levenshtein → mispronunciation flags
3. Video pipeline:
     OpenCV (Haar cascade) → face crops per frame → MobileNetV2 → emotion array
     FFmpeg → reassemble annotated video with original audio (if returning processed video)
4. Aggregate: { transcript, confidence_score, emotion_timeline, pronunciation_flags, wpm }
5. Anthropic API call: raw metrics → conversational coaching feedback text
6. Return JSON to frontend
```

## 2. Tech Stack

- **Framework:** FastAPI (async, auto-generated OpenAPI docs, easy to containerize)
- **Server:** Uvicorn (or Gunicorn+Uvicorn workers in production)
- **ML:** PyTorch + `transformers` (Wav2Vec2), TensorFlow/Keras (MobileNetV2, LSTM)
- **Audio:** Librosa
- **Video:** OpenCV, FFmpeg (system binary)
- **Linguistics:** `pronouncing`, `python-Levenshtein`
- **LLM feedback:** Anthropic API (`anthropic` Python SDK)
- **Packaging:** Docker (needed to reliably ship FFmpeg + heavy ML deps together)

## 3. Project Structure (target)

```
backend/
├── main.py                # FastAPI app, routes
├── models/
│   ├── wav2vec_infer.py   # Wav2Vec2 loading + transcript/pronunciation logic
│   ├── emotion_infer.py   # MobileNetV2 loading + frame-level emotion scoring
│   └── confidence_infer.py # LSTM loading + confidence scoring from audio features
├── pipeline/
│   ├── audio_features.py  # Librosa feature extraction
│   └── video_frames.py    # OpenCV frame extraction + face detection
├── feedback/
│   └── coach.py           # Builds prompt, calls Anthropic API, returns coaching text
├── weights/                # Saved model weights (.pt / .h5) — see §5 on size
├── requirements.txt
├── Dockerfile
└── .env.example            # ANTHROPIC_API_KEY, etc.
```

## 4. Key Endpoint

```python
# main.py (sketch)
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],
    allow_methods=["POST"],
)

@app.post("/api/analyze")
async def analyze(file: UploadFile):
    # 1. save temp file
    # 2. run audio + video pipelines
    # 3. call Anthropic for feedback
    # 4. return JSON
    ...
```

## 5. Model Weight Size — check this early

Before picking a host, check the on-disk size of your saved weights (`wav2vec2` checkpoints in particular can be 300MB–1GB+). This determines:
- Whether you can bake weights into the Docker image or need to download them at startup from Hugging Face Hub / cloud storage.
- Which free tiers are actually usable (some cap image size or disk).

```bash
du -sh backend/weights/*
```

## 6. CPU vs GPU

As discussed: **inference is far lighter than training.** For one request at a time:
- Wav2Vec2 (heaviest) — a few seconds on CPU for a short clip.
- MobileNetV2 — near-instant per frame, designed for lightweight/edge use.
- LSTM — trivial.

**Conclusion: CPU-only hosting is sufficient** for a demo/portfolio-scale deployment (low concurrent traffic). Revisit GPU only if you need many simultaneous users or sub-second responses.

## 7. Hosting Options (no GPU required)

| Option | Notes | Good for |
|---|---|---|
| **Render** | Docker support, free/student tier, persistent service, easy env vars | Simplest full control, recommended default |
| **Railway** | Similar to Render, Docker-based, student credits available | Alternative if Render free tier limits are hit |
| **Hugging Face Spaces** | Native fit since you already use HF `transformers`; Docker or Gradio/FastAPI SDK; free CPU tier, paid GPU tier available later | Best if you want a public ML demo page too |
| **Cloud VM (Azure/DigitalOcean via GitHub Student Pack credits)** | Full control, you manage everything (OS, FFmpeg, restarts) | Only if you outgrow the above or want infra experience |

**Recommendation:** Start with **Render** (Docker) or **Hugging Face Spaces** — both handle FFmpeg + heavy Python deps without extra config, and both have workable free tiers for this project's scale.

## 8. Dockerfile (sketch)

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg libsndfile1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 9. Environment Variables

- `ANTHROPIC_API_KEY` — set in the host's dashboard (Render/HF Spaces secrets), **never** committed or exposed to the frontend.
- `ALLOWED_ORIGIN` — your Vercel frontend URL, used in CORS config.

## 10. Open Items

- [ ] Confirm total weight size and decide bake-in vs. download-at-startup.
- [ ] Decide whether the backend returns a processed video (with overlays) or just JSON metrics — affects FFmpeg output handling and response size.
- [ ] Add request size limits / timeout handling for large video uploads.
- [ ] Write a `/health` endpoint for host uptime checks.

## 11. Related Docs

- `frontend.md` — Next.js frontend architecture and Vercel deployment
- `deployment.md` — end-to-end deployment steps tying both together
- `DESIGN.md` — UI design system spec
