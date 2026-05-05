"""
Phase 2 Service Module: Presentation Pro
Handles video processing, emotion detection, and communication analysis
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
from dataclasses import dataclass, asdict, field
from abc import ABC, abstractmethod
from enum import Enum

class Emotion(str, Enum):
    """FER-2013 Emotion classes"""
    ANGRY = "Angry"
    DISGUST = "Disgust"
    FEAR = "Fear"
    HAPPY = "Happy"
    SAD = "Sad"
    SURPRISE = "Surprise"
    NEUTRAL = "Neutral"

@dataclass
class FrameEmotionPrediction:
    """Per-frame emotion prediction from CNN"""
    frame_idx: int
    timestamp: float
    emotion: Emotion
    confidence: float
    raw_scores: Dict[str, float]  # {emotion: score} for all classes

@dataclass
class VocalEnergyFrame:
    """Vocal energy sample (RMS/LSTM)"""
    frame_idx: int
    timestamp: float
    section: str  # "INTRODUCTION", "CORE_ARGUMENT", "CONCLUSION"
    rms_energy: float
    lstm_features: Optional[List[float]] = None

@dataclass
class CommunicationMetrics:
    """Communication quality metrics"""
    filter_words: Dict[str, int]  # {"um": 2, "uh": 1, "like": 4}
    pitch_variance_percent: float
    speaking_pace_wpm: float
    gesture_frequency: float
    vocal_energy_consistency: float

@dataclass
class Phase2Result:
    """Complete Phase 2 output"""
    emotion_predictions: List[FrameEmotionPrediction]
    communication_metrics: CommunicationMetrics
    dominant_emotion: Emotion
    confidence_score: float
    vocal_energy_dynamics: List[VocalEnergyFrame]
    insights: List[str]
    video_duration: float
    frame_count: int
    fps: int = 30
    
    def to_dict(self) -> Dict:
        return {
            "emotion_predictions": [asdict(p) for p in self.emotion_predictions],
            "communication_metrics": asdict(self.communication_metrics),
            "dominant_emotion": self.dominant_emotion.value,
            "confidence_score": self.confidence_score,
            "vocal_energy_dynamics": [asdict(v) for v in self.vocal_energy_dynamics],
            "insights": self.insights,
            "video_duration": self.video_duration,
            "frame_count": self.frame_count,
            "fps": self.fps
        }

class Phase2Backend(ABC):
    """Abstract base for Phase 2 backend implementations"""
    
    @abstractmethod
    def process_video(self, video_path: str) -> Phase2Result:
        """
        Main entry point for Phase 2 processing
        
        Args:
            video_path: Path to presentation video
            
        Returns:
            Phase2Result with all emotion predictions and metrics
        """
        pass
    
    @abstractmethod
    def extract_frames(self, video_path: str) -> Tuple[List[np.ndarray], float, int]:
        """Extract frames from video and return (frames, fps, duration)"""
        pass
    
    @abstractmethod
    def predict_emotions_cnn(self, frames: List[np.ndarray]) -> List[FrameEmotionPrediction]:
        """Run MobileNetV2 CNN on frames for emotion classification"""
        pass
    
    @abstractmethod
    def extract_audio_features(self, video_path: str) -> Dict:
        """Extract audio features: filter words, pitch, pace, vocal energy"""
        pass
    
    @abstractmethod
    def generate_insights(self, metrics: CommunicationMetrics, emotions: List[FrameEmotionPrediction]) -> List[str]:
        """Generate personalized insights and recommendations"""
        pass

class Phase2MockBackend(Phase2Backend):
    """Mock implementation for testing UI without CNN model"""
    
    EMOTIONS = [e.value for e in Emotion]
    
    def process_video(self, video_path: str) -> Phase2Result:
        """Process video and return mock results"""
        frames, fps, duration = self.extract_frames(video_path)
        emotions = self.predict_emotions_cnn(frames)
        audio_metrics = self.extract_audio_features(video_path)
        insights = self.generate_insights(audio_metrics, emotions)
        
        # Determine dominant emotion
        emotion_counts = {}
        for pred in emotions:
            emotion_counts[pred.emotion] = emotion_counts.get(pred.emotion, 0) + 1
        dominant = max(emotion_counts, key=emotion_counts.get)
        avg_confidence = np.mean([p.confidence for p in emotions])
        
        # Generate vocal energy dynamics
        vocal_energy = self._generate_vocal_energy(len(frames), fps, duration)
        
        return Phase2Result(
            emotion_predictions=emotions,
            communication_metrics=audio_metrics,
            dominant_emotion=dominant,
            confidence_score=avg_confidence,
            vocal_energy_dynamics=vocal_energy,
            insights=insights,
            video_duration=duration,
            frame_count=len(frames),
            fps=fps
        )
    
    def extract_frames(self, video_path: str) -> Tuple[List[np.ndarray], float, int]:
        """Mock: Simulate frame extraction"""
        fps = 30
        duration = 30  # 30 second video
        num_frames = int(fps * duration)
        
        # Mock frames as dummy arrays (normally would be actual video frames)
        frames = [np.random.rand(224, 224, 3) for _ in range(num_frames)]
        
        return frames, fps, duration
    
    def predict_emotions_cnn(self, frames: List[np.ndarray]) -> List[FrameEmotionPrediction]:
        """Mock: Simulate CNN predictions with temporal coherence"""
        predictions = []
        num_frames = len(frames)
        
        # Simulate smooth emotion transitions
        section_frames = num_frames // 3
        section_emotions = [Emotion.NEUTRAL, Emotion.HAPPY, Emotion.SURPRISE]
        
        for frame_idx, frame in enumerate(frames):
            section_idx = min(frame_idx // section_frames, 2)
            primary_emotion = section_emotions[section_idx]
            
            # Add some noise but keep coherence
            if np.random.rand() > 0.85:
                primary_emotion = Emotion(self.EMOTIONS[np.random.randint(0, 7)])
            
            timestamp = frame_idx / 30.0
            confidence = 0.6 + np.random.rand() * 0.4
            
            # Generate score distribution
            scores = {e: np.random.rand() for e in self.EMOTIONS}
            scores[primary_emotion.value] = confidence
            scores = {k: v / sum(scores.values()) for k, v in scores.items()}  # Normalize
            
            predictions.append(FrameEmotionPrediction(
                frame_idx=frame_idx,
                timestamp=timestamp,
                emotion=primary_emotion,
                confidence=confidence,
                raw_scores=scores
            ))
        
        return predictions
    
    def extract_audio_features(self, video_path: str) -> CommunicationMetrics:
        """Mock: Simulate audio feature extraction"""
        return CommunicationMetrics(
            filter_words={"um": 2, "uh": 1, "like": 4},
            pitch_variance_percent=15.0,
            speaking_pace_wpm=142,
            gesture_frequency=2.3,
            vocal_energy_consistency=0.72
        )
    
    def generate_insights(self, metrics: CommunicationMetrics, emotions: List[FrameEmotionPrediction]) -> List[str]:
        """Mock: Generate insights"""
        insights = []
        
        if metrics.pitch_variance_percent > 10:
            insights.append(
                f"Pitch Variance: Your pitch is {metrics.pitch_variance_percent:.1f}% flatter than expert benchmarks. "
                "Try emphasizing key idea points."
            )
        
        if abs(metrics.speaking_pace_wpm - 130) > 5:
            direction = "too fast" if metrics.speaking_pace_wpm > 130 else "too slow"
            insights.append(
                f"Pacing: Your current pace is {metrics.speaking_pace_wpm} wpm (target: 130). "
                f"You're speaking {direction}. Slow down after key data points."
            )
        
        filter_count = sum(metrics.filter_words.values())
        if filter_count > 2:
            insights.append(
                f"Filter Words: Detected {filter_count} filler words. "
                "Try pausing briefly instead of using 'um', 'uh', or 'like'."
            )
        
        if metrics.gesture_frequency < 1.5:
            insights.append(
                "Gestures: Consider using more hand gestures to emphasize key points. "
                "This helps maintain audience engagement."
            )
        
        return insights if insights else ["Great presentation! Keep up the excellent work."]
    
    def _generate_vocal_energy(self, num_frames: int, fps: int, duration: float) -> List[VocalEnergyFrame]:
        """Generate mock vocal energy dynamics with section coherence"""
        vocal_energy = []
        section_frames = num_frames // 3
        sections = ["INTRODUCTION", "CORE_ARGUMENT", "CONCLUSION"]
        
        for frame_idx in range(num_frames):
            section_idx = min(frame_idx // section_frames, 2)
            section = sections[section_idx]
            timestamp = frame_idx / fps
            
            # Higher energy in CORE_ARGUMENT
            base_energy = 0.4 if section == "INTRODUCTION" else (0.6 if section == "CORE_ARGUMENT" else 0.5)
            energy = base_energy + np.random.randn() * 0.1
            energy = np.clip(energy, 0.0, 1.0)
            
            vocal_energy.append(VocalEnergyFrame(
                frame_idx=frame_idx,
                timestamp=timestamp,
                section=section,
                rms_energy=energy
            ))
        
        return vocal_energy
