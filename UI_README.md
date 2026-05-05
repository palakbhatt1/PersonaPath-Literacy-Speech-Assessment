# PersonaPath UI - Gradio Dashboard

Complete Gradio-based interface for PersonaPath Phases 1 & 2 with modular, backend-agnostic architecture.

## 🎯 Quick Start

### Installation

```bash
cd /path/to/PersonaPath-Literacy-Speech-Assessment-main

# Install Gradio and dependencies
pip install gradio numpy matplotlib

# Optional: Install audio/video processing
pip install librosa soundfile opencv-python
```

### Run the App

```bash
python app.py
```

Access dashboard at: **http://localhost:7860**

---

## 📊 Architecture Overview

### Data Flow

```
PHASE 1: Literacy Coach
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Audio File + Reference Text
    ↓
[Phase1Backend.extract_speech_to_text()] → Transcript
    ↓
[Phase1Backend.align_transcript()] → Word Alignments
    ↓
[Phase1Backend.extract_metrics()] → WPM, Hesitations, Pronunciation
    ↓
[Phase1Backend.generate_feedback()] → Personalized Feedback
    ↓
UI Display: Metrics, Alignment, Progress

PHASE 2: Presentation Pro
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Video File
    ↓
[Phase2Backend.extract_frames()] → Frame array
    ↓
[Phase2Backend.predict_emotions_cnn()] → Emotion predictions (per frame)
    ↓
[Phase2Backend.extract_audio_features()] → Filter words, pitch, pace
    ↓
[Phase2Backend.generate_insights()] → Recommendations
    ↓
UI Display: Emotions, Confidence, Metrics, Insights
```

---

## 🔧 Backend Integration

### Current Setup

The app uses **mock backends** for testing UI without models:
- `services/phase1_service.py` → `Phase1MockBackend`
- `services/phase2_service.py` → `Phase2MockBackend`

### Integration Steps

#### 1. **Replace Phase 1 Backend**

In `services/phase1_service.py`, implement `Phase1Backend`:

```python
from services.phase1_service import Phase1Backend, Phase1Result, WordAlignment

class YourPhase1Backend(Phase1Backend):
    def process_audio(self, audio_path: str, reference_passage: str) -> Phase1Result:
        # 1. Load audio
        audio_data = librosa.load(audio_path)
        
        # 2. Extract speech-to-text
        transcript = self.extract_speech_to_text(audio_path)
        
        # 3. Align with reference
        alignments = self.align_transcript(transcript, reference_passage)
        
        # 4. Extract metrics
        metrics = self.extract_metrics(audio_path, transcript)
        
        # 5. Generate feedback
        feedback = self.generate_feedback(metrics, alignments)
        
        return Phase1Result(
            transcript=transcript,
            words_per_minute=metrics["wpm"],
            hesitations=metrics["hesitations"],
            pronunciation_score=metrics["pronunciation_score"],
            word_alignments=alignments,
            feedback=feedback,
            session_progress=0.75,
            audio_duration=librosa.get_duration(filename=audio_path)
        )
    
    def extract_speech_to_text(self, audio_path: str) -> str:
        # Import Wav2Vec 2.0 from your implementation
        # return your_wav2vec_model(audio_path)
        pass
    
    def align_transcript(self, transcript: str, reference: str):
        # Implement alignment logic (Levenshtein, DTW, etc.)
        pass
    
    def extract_metrics(self, audio_path: str, transcript: str) -> Dict:
        # Calculate WPM, hesitations, pronunciation confidence
        pass
    
    def generate_feedback(self, metrics: Dict, alignments):
        # Create personalized feedback
        pass
```

#### 2. **Replace Phase 2 Backend**

In `services/phase2_service.py`, implement `Phase2Backend`:

```python
from services.phase2_service import Phase2Backend, Phase2Result, FrameEmotionPrediction, Emotion

class YourPhase2Backend(Phase2Backend):
    def process_video(self, video_path: str) -> Phase2Result:
        # 1. Extract frames
        frames, fps, duration = self.extract_frames(video_path)
        
        # 2. Run CNN on frames
        emotions = self.predict_emotions_cnn(frames)
        
        # 3. Extract audio features
        audio_metrics = self.extract_audio_features(video_path)
        
        # 4. Generate insights
        insights = self.generate_insights(audio_metrics, emotions)
        
        # Determine dominant emotion
        emotion_counts = {}
        for pred in emotions:
            emotion_counts[pred.emotion] = emotion_counts.get(pred.emotion, 0) + 1
        dominant = max(emotion_counts, key=emotion_counts.get)
        
        return Phase2Result(
            emotion_predictions=emotions,
            communication_metrics=audio_metrics,
            dominant_emotion=dominant,
            confidence_score=np.mean([p.confidence for p in emotions]),
            vocal_energy_dynamics=vocal_energy,
            insights=insights,
            video_duration=duration,
            frame_count=len(frames),
            fps=fps
        )
    
    def extract_frames(self, video_path: str) -> Tuple[List[np.ndarray], float, int]:
        # Use OpenCV to extract video frames
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        # ... extract frames
        pass
    
    def predict_emotions_cnn(self, frames: List[np.ndarray]):
        # Load your MobileNetV2 model
        # Run inference on each frame
        # Return FrameEmotionPrediction objects
        pass
    
    def extract_audio_features(self, video_path: str) -> CommunicationMetrics:
        # Extract audio from video
        # Count filter words ("um", "uh", "like")
        # Calculate pitch variance, speaking pace, gesture frequency
        pass
    
    def generate_insights(self, metrics, emotions):
        # Create personalized recommendations
        pass
```

#### 3. **Update Configuration**

In `services/config.py`, replace mock backends:

```python
# Option A: Update config.py initialization
class ServiceConfig:
    def _initialize_backends(self):
        if self.mode == BackendMode.PRODUCTION:
            from your_module import YourPhase1Backend, YourPhase2Backend
            self._phase1_backend = YourPhase1Backend()
            self._phase2_backend = YourPhase2Backend()

# Option B: Override at runtime in app.py
if __name__ == "__main__":
    from services import get_config, BackendMode
    from your_module import YourPhase1Backend, YourPhase2Backend
    
    config = get_config()
    config.set_phase1_backend(YourPhase1Backend())
    config.set_phase2_backend(YourPhase2Backend())
    
    app = create_app()
    app.launch()
```

---

## 📁 Project Structure

```
PersonaPath-Literacy-Speech-Assessment-main/
├── app.py                              # Main Gradio app
├── services/
│   ├── __init__.py
│   ├── phase1_service.py              # Phase 1 backend interface + mock
│   ├── phase2_service.py              # Phase 2 backend interface + mock
│   └── config.py                      # Service configuration
├── CNN_Emotion_Training.ipynb          # Your Phase 2 model training
├── Test_Video_Emotion.ipynb           # Your Phase 2 test notebook
└── test/
    └── Test_emotion_vid1.mp4          # Test video
```

---

## 🎨 UI Components

### Phase 1: Literacy Coach

**Inputs:**
- Audio file (microphone recording or upload)
- Reference reading passage (editable text)

**Outputs:**
- 📊 Metrics: WPM, Hesitations count
- 👨‍🏫 Coaching feedback: Personalized message
- 📈 Progress: Daily session completion %
- 🔤 Word alignment: Color-coded correctness

**Key Components:**
- Audio recorder with waveform visualization
- Real-time metrics display
- Word-level alignment with confidence scores
- Coaching feedback panel

### Phase 2: Presentation Pro

**Inputs:**
- Video file (MP4 format)

**Outputs:**
- 😊 Confidence ring: Dominant emotion confidence %
- 🔤 Filter word counter: Um, Uh, Like counts
- 💡 Insights: AI-generated recommendations
- 📈 Metrics: Pitch variance, speaking pace (WPM)
- 🎵 Vocal energy dynamics: By section (Introduction, Core, Conclusion)
- 😊 Emotion timeline: Distribution over time

**Key Components:**
- Video player/uploader
- Real-time processing progress bar
- Multi-metric display
- Interactive charts for vocal energy and emotions
- Personalized insights panel

---

## 🔌 Service Interfaces

### Phase1Backend (Abstract)

```python
class Phase1Backend(ABC):
    @abstractmethod
    def process_audio(audio_path, reference_passage) -> Phase1Result
    
    @abstractmethod
    def extract_speech_to_text(audio_path) -> str
    
    @abstractmethod
    def align_transcript(transcript, reference) -> List[WordAlignment]
    
    @abstractmethod
    def extract_metrics(audio_path, transcript) -> Dict
    
    @abstractmethod
    def generate_feedback(metrics, alignments) -> str
```

### Phase2Backend (Abstract)

```python
class Phase2Backend(ABC):
    @abstractmethod
    def process_video(video_path) -> Phase2Result
    
    @abstractmethod
    def extract_frames(video_path) -> Tuple[List[np.ndarray], float, int]
    
    @abstractmethod
    def predict_emotions_cnn(frames) -> List[FrameEmotionPrediction]
    
    @abstractmethod
    def extract_audio_features(video_path) -> CommunicationMetrics
    
    @abstractmethod
    def generate_insights(metrics, emotions) -> List[str]
```

---

## 📊 Data Models

### Phase 1 Output

```python
@dataclass
class Phase1Result:
    transcript: str                          # Speech-to-text output
    words_per_minute: float                  # Speaking rate
    hesitations: int                         # Count of filler pauses
    pronunciation_score: float               # 0-1 confidence
    word_alignments: List[WordAlignment]     # Per-word analysis
    feedback: str                            # Coaching message
    session_progress: float                  # 0-1 completion %
    audio_duration: float                    # Seconds
```

### Phase 2 Output

```python
@dataclass
class Phase2Result:
    emotion_predictions: List[FrameEmotionPrediction]
    communication_metrics: CommunicationMetrics
    dominant_emotion: Emotion
    confidence_score: float
    vocal_energy_dynamics: List[VocalEnergyFrame]
    insights: List[str]
    video_duration: float
    frame_count: int
    fps: int = 30
```

---

## 🚀 Advanced: Custom Modifications

### Add New Metrics to Phase 1

1. Update `Phase1Result` dataclass
2. Implement metric extraction in `extract_metrics()`
3. Update UI display in `build_phase1_interface()`
4. Add visualization in `create_*_plot()` functions

### Add New Metrics to Phase 2

1. Update `CommunicationMetrics` dataclass
2. Implement extraction in `extract_audio_features()`
3. Add to insights generation in `generate_insights()`
4. Update UI in `build_phase2_interface()`

### Custom Report Generation

Create `reports/` module:

```python
# reports/phase1_report.py
def generate_phase1_report(result: Phase1Result) -> str:
    # Create PDF/HTML report with metrics and recommendations
    pass

# reports/phase2_report.py
def generate_phase2_report(result: Phase2Result) -> str:
    # Create PDF/HTML report with emotion analysis and insights
    pass
```

---

## 🐛 Troubleshooting

### Common Issues

**Problem:** "Phase X backend not initialized"
- **Solution:** Check `services/config.py` initialization. Ensure backends are properly set.

**Problem:** Audio not processing
- **Solution:** Verify audio file format (WAV, MP3, OGG supported). Check microphone permissions.

**Problem:** Video analysis takes too long
- **Solution:** Reduce frame extraction rate or implement batch processing in `predict_emotions_cnn()`.

**Problem:** Out of memory with large video
- **Solution:** Implement streaming frame processing instead of loading all frames at once.

---

## 📝 Testing

Run mock demo:

```bash
python app.py
# Then:
# 1. Go to Phase 1, upload test audio
# 2. Go to Phase 2, upload test video
# 3. Check metrics/outputs match expected mock values
```

---

## 🔗 Integration Checklist

- [ ] Replace `Phase1MockBackend` with actual STT model
- [ ] Replace `Phase2MockBackend` with actual CNN model
- [ ] Test Phase 1 audio processing
- [ ] Test Phase 2 video processing
- [ ] Add report generation
- [ ] Deploy to production server
- [ ] Set up user authentication (optional)
- [ ] Add database for result storage (optional)

---

## 📚 References

- **Gradio Docs:** https://gradio.app/docs/
- **Wav2Vec 2.0:** https://huggingface.co/models?other=wav2vec2
- **MobileNetV2:** https://keras.io/api/applications/mobilenet/
- **FER-2013 Dataset:** https://www.kaggle.com/deadskull7/fer2013

---

**Questions?** Check `services/phase1_service.py` and `services/phase2_service.py` for detailed docstrings and expected signatures.
