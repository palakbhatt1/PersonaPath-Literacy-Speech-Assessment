# PersonaPath UI - Setup & Deployment Guide

## 📋 What's Been Created

### ✅ Completed Components

```
✓ Gradio Dashboard App (app.py)
  ├─ Phase 1: Literacy Coach UI
  ├─ Phase 2: Presentation Pro UI
  ├─ Tab-based navigation
  └─ Real-time feedback & visualization

✓ Backend Service Architecture (services/)
  ├─ phase1_service.py (Abstract + Mock)
  ├─ phase2_service.py (Abstract + Mock)
  ├─ config.py (Modular backend injection)
  └─ __init__.py (Package exports)

✓ Mock Implementations
  ├─ Phase1MockBackend (test Phase 1 UI)
  ├─ Phase2MockBackend (test Phase 2 UI)
  └─ Data flow simulation

✓ Documentation
  ├─ UI_README.md (Integration guide)
  ├─ requirements.txt (Dependencies)
  └─ SETUP_GUIDE.md (This file)
```

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
cd "/Users/DL Project/PersonaPath-Literacy-Speech-Assessment-main"
pip install -r requirements.txt
```

### Step 2: Run the App

```bash
python app.py
```

### Step 3: Open in Browser

Navigate to: **http://localhost:7860**

---

## 🎯 Current State: Mock Mode

The app is currently running with **mock backends** that:

✅ **Display the correct UI** (matches your screenshot designs exactly)
✅ **Show realistic mock data** (simulates what real models would produce)
✅ **Allow testing UI interactions** without backend models
✅ **Ready for backend integration** (modular architecture)

### Mock Behavior

**Phase 1:**
- Simulates Wav2Vec output: "The elephant sat quietly by the river bank"
- Returns metrics: 45 WPM, 2 hesitations, 92% pronunciation score
- Generates sample feedback

**Phase 2:**
- Simulates frame extraction: 90 frames @ 30fps
- Generates emotion predictions: smooth temporal transitions
- Returns metrics: 78% confidence, filter words, pitch variance
- Generates insights based on simulated metrics

---

## 🔌 Integration: Next Steps

### Replace Mock with Real Models

#### For Phase 1 (Speech Recognition)

Edit **`services/phase1_service.py`**:

```python
class YourPhase1Backend(Phase1Backend):
    def extract_speech_to_text(self, audio_path: str) -> str:
        # TODO: Import your Wav2Vec model
        from transformers import pipeline
        pipe = pipeline("automatic-speech-recognition", 
                       model="facebook/wav2vec2-large")
        result = pipe(audio_path)
        return result["text"]
    
    # Implement other required methods...
```

Then update **`services/config.py`**:

```python
elif self.mode == BackendMode.PRODUCTION:
    from your_implementation import YourPhase1Backend, YourPhase2Backend
    self._phase1_backend = YourPhase1Backend()
    self._phase2_backend = YourPhase2Backend()
```

#### For Phase 2 (Emotion Detection)

Edit **`services/phase2_service.py`**:

```python
class YourPhase2Backend(Phase2Backend):
    def predict_emotions_cnn(self, frames: List[np.ndarray]) -> List[FrameEmotionPrediction]:
        # TODO: Load your MobileNetV2 model (from CNN_Emotion_Training.ipynb)
        import tensorflow as tf
        model = tf.keras.models.load_model("path/to/your/model.keras")
        
        predictions = []
        for idx, frame in enumerate(frames):
            # Preprocess frame
            input_frame = self._preprocess(frame)
            
            # Run inference
            output = model.predict(input_frame)
            emotion_idx = np.argmax(output)
            confidence = output[0][emotion_idx]
            
            # Create prediction object
            predictions.append(FrameEmotionPrediction(
                frame_idx=idx,
                timestamp=idx / 30.0,
                emotion=Emotion(self.EMOTIONS[emotion_idx]),
                confidence=float(confidence),
                raw_scores={e: float(s) for e, s in zip(self.EMOTIONS, output[0])}
            ))
        
        return predictions
    
    # Implement other required methods...
```

---

## 📊 Data Flow (How It Works)

### Phase 1 Flow

```
User Input: Audio + Passage
         ↓
    app.py (UI)
         ↓
handle_phase1_process()
         ↓
CONFIG.phase1_backend.process_audio()
         ↓
┌─────────────────────────────────────┐
│ Phase1Backend Abstract Class        │
├─────────────────────────────────────┤
│ • extract_speech_to_text()          │
│ • align_transcript()                │
│ • extract_metrics()                 │
│ • generate_feedback()               │
└─────────────────────────────────────┘
         ↓
    Phase1Result
         ↓
    Display Outputs:
    • Transcript
    • Word alignments
    • WPM, hesitations
    • Feedback
    • Progress %
```

### Phase 2 Flow

```
User Input: Video
         ↓
    app.py (UI)
         ↓
handle_phase2_process()
         ↓
CONFIG.phase2_backend.process_video()
         ↓
┌─────────────────────────────────────┐
│ Phase2Backend Abstract Class        │
├─────────────────────────────────────┤
│ • extract_frames()                  │
│ • predict_emotions_cnn() [CNN]      │
│ • extract_audio_features()          │
│ • generate_insights()               │
└─────────────────────────────────────┘
         ↓
    Phase2Result
         ↓
    Display Outputs:
    • Emotion predictions
    • Confidence score
    • Filter word counts
    • Speaking metrics
    • Insights
    • Vocal energy chart
    • Emotion timeline
```

---

## 📁 File Structure

```
PersonaPath-Literacy-Speech-Assessment-main/
├── app.py                              [MAIN APP - Start here]
├── requirements.txt                    [Dependencies]
├── UI_README.md                        [Integration guide]
├── SETUP_GUIDE.md                      [This file]
│
├── services/                           [Backend service layer]
│   ├── __init__.py
│   ├── phase1_service.py              [Phase 1 interface + mock]
│   ├── phase2_service.py              [Phase 2 interface + mock]
│   └── config.py                      [Service configuration]
│
├── CNN_Emotion_Training.ipynb          [Your Phase 2 model training]
├── Test_Video_Emotion.ipynb           [Your Phase 2 test notebook]
└── test/
    └── Test_emotion_vid1.mp4          [Test video file]
```

---

## 🧪 Testing the Mock Implementation

### Test Phase 1

1. Open app at http://localhost:7860
2. Go to **Phase 1: Literacy Coach** tab
3. Click on audio input and either:
   - Record a sentence (doesn't matter what you say - it uses mock data)
   - Or upload any audio file
4. Click **🚀 Process Audio & Generate Feedback**
5. Should see:
   - Transcript: "The elephant sat quietly by the river bank"
   - WPM: 45
   - Hesitations: 2
   - Word alignment with color coding
   - Feedback message

### Test Phase 2

1. Go to **Phase 2: Presentation Pro** tab
2. Upload any video file (or create dummy file with 30 seconds)
3. Click **🚀 Analyze Presentation**
4. Should see:
   - Confidence: "Happy: 78%"
   - Filter words: Um=2, Uh=1, Like=4
   - Pitch Variance: 15%
   - Speaking Pace: 142 WPM
   - Vocal Energy chart
   - Emotion distribution chart
   - Insights

---

## 🔄 Switching Between Backend Modes

### Option 1: Via Code (Edit `app.py`)

```python
# Line 20-21, change:
CONFIG = get_config(BackendMode.MOCK)  # Current: mock demo
# To:
CONFIG = get_config(BackendMode.PRODUCTION)  # Switch to production
```

### Option 2: Programmatic (Advanced)

```python
from services import get_config, BackendMode
from your_models import YourPhase1Backend, YourPhase2Backend

config = get_config()
config.set_phase1_backend(YourPhase1Backend())
config.set_phase2_backend(YourPhase2Backend())
```

---

## ⚙️ Configuration

### Environment Variables (Optional)

Create `.env` file:

```env
GRADIO_SERVER_PORT=7860
GRADIO_SERVER_NAME=0.0.0.0
MODEL_CACHE_DIR=/path/to/models
```

Load in `app.py`:

```python
from dotenv import load_dotenv
import os

load_dotenv()
port = int(os.getenv("GRADIO_SERVER_PORT", 7860))
```

---

## 📊 UI Components Map

### Phase 1 Layout

```
┌─────────────────────────────────────────────────────┐
│                  PersonaPath                        │
│              [Phase 1] [Phase 2]                    │
├──────────────────────┬──────────────────────────────┤
│                      │                              │
│  Reading Passage     │  Coaching Corner             │
│  [Text Area]         │  [Feedback Message]          │
│                      │                              │
│  Recording           │  Metrics                     │
│  [Audio Input]       │  [WPM] [Hesitations]        │
│                      │                              │
│  Waveform            │  Progress                    │
│  [Chart]             │  [Slider]                    │
│                      │                              │
│                      │  Word Alignment              │
│                      │  [Colored Words]             │
│                      │                              │
│  [Process Button]                                   │
└──────────────────────┴──────────────────────────────┘
```

### Phase 2 Layout

```
┌─────────────────────────────────────────────────────┐
│                  PersonaPath                        │
│              [Phase 1] [Phase 2]                    │
├──────────────────────┬──────────────────────────────┤
│                      │                              │
│  Video Player        │  ● ACTIVE SESSION            │
│  [Video Input]       │                              │
│                      │  Confidence                  │
│  Analysis Progress   │  [Ring/Value]                │
│  [Progress Bar]      │                              │
│                      │  Filter Words                │
│  Vocal Energy        │  [Um][Uh][Like]              │
│  [Bar Chart]         │                              │
│                      │  Insights                    │
│  Emotion Timeline    │  [Text Area]                 │
│  [Distribution]      │                              │
│                      │  Metrics                     │
│                      │  [Pitch][Pace]               │
│                      │                              │
│  [Process Button]                                   │
└──────────────────────┴──────────────────────────────┘
```

---

## 🐛 Debugging

### Enable Debug Logging

In `app.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Print Intermediate Results

```python
def handle_phase1_process(audio_file, passage_text):
    print(f"Audio file: {audio_file}")
    print(f"Passage: {passage_text}")
    result = CONFIG.phase1_backend.process_audio(audio_file, passage_text)
    print(f"Result: {result.to_dict()}")  # Print full result
    # ... rest of function
```

---

## 📈 Performance Optimization

### For Large Videos

Modify `Phase2Backend.extract_frames()`:

```python
def extract_frames(self, video_path, skip_frames=2):
    # Skip every 2nd frame to reduce memory
    # This trades resolution for speed
    pass
```

### Batch Processing

```python
def predict_emotions_cnn(self, frames, batch_size=32):
    # Process 32 frames at once instead of one-by-one
    predictions = []
    for i in range(0, len(frames), batch_size):
        batch = frames[i:i+batch_size]
        # ... batch inference
    return predictions
```

---

## 🚀 Deployment

### Local Demo

```bash
python app.py
```

### Share Publicly (Gradio)

```python
app.launch(share=True)  # Generates public URL
```

### Docker (Optional)

```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

```bash
docker build -t personapath-ui .
docker run -p 7860:7860 personapath-ui
```

---

## ❓ FAQ

**Q: Why separate services from UI?**
A: Clean architecture. You can test UI without models, swap backends easily, and scale independently.

**Q: Can I modify the UI?**
A: Yes! All UI components are in `build_phase1_interface()` and `build_phase2_interface()` functions.

**Q: How do I add new metrics?**
A: Update dataclasses in `services/phase*_service.py`, then add UI display in `build_phase*_interface()`.

**Q: Can I integrate with my notebook?**
A: Yes! Convert notebook functions to inherit from `Phase1Backend` or `Phase2Backend`, then register in config.

---

## 📞 Support

- Check `UI_README.md` for detailed integration docs
- Review service interfaces in `services/phase1_service.py` and `services/phase2_service.py`
- Examine mock implementations for example data formats

---

**Ready to build? Start with:** `python app.py` 🚀
