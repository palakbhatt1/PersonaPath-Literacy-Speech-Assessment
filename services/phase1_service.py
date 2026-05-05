"""
Phase 1 Service Module: Literacy Coach
Handles audio processing, speech-to-text, alignment, and metrics extraction
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod

@dataclass
class WordAlignment:
    """Word-level alignment result"""
    word: str
    correct: bool
    confidence: float
    start_time: float
    end_time: float

@dataclass
class Phase1Result:
    """Complete Phase 1 output"""
    transcript: str
    words_per_minute: float
    hesitations: int
    pronunciation_score: float
    word_alignments: List[WordAlignment]
    feedback: str
    session_progress: float
    audio_duration: float
    
    def to_dict(self) -> Dict:
        return {
            "transcript": self.transcript,
            "words_per_minute": self.words_per_minute,
            "hesitations": self.hesitations,
            "pronunciation_score": self.pronunciation_score,
            "word_alignments": [asdict(w) for w in self.word_alignments],
            "feedback": self.feedback,
            "session_progress": self.session_progress,
            "audio_duration": self.audio_duration
        }

class Phase1Backend(ABC):
    """Abstract base for Phase 1 backend implementations"""
    
    @abstractmethod
    def process_audio(self, audio_path: str, reference_passage: str) -> Phase1Result:
        """
        Main entry point for Phase 1 processing
        
        Args:
            audio_path: Path to audio file
            reference_passage: Text passage to align against
            
        Returns:
            Phase1Result with all metrics and feedback
        """
        pass
    
    @abstractmethod
    def extract_speech_to_text(self, audio_path: str) -> str:
        """Extract transcript from audio using Wav2Vec 2.0 or similar"""
        pass
    
    @abstractmethod
    def align_transcript(self, transcript: str, reference: str) -> List[WordAlignment]:
        """Align transcript words with reference passage"""
        pass
    
    @abstractmethod
    def extract_metrics(self, audio_path: str, transcript: str) -> Dict:
        """Extract WPM, hesitations, pronunciation score"""
        pass
    
    @abstractmethod
    def generate_feedback(self, metrics: Dict, alignments: List[WordAlignment]) -> str:
        """Generate personalized feedback based on metrics and alignments"""
        pass

class Phase1MockBackend(Phase1Backend):
    """Mock implementation for testing UI without backend"""
    
    def process_audio(self, audio_path: str, reference_passage: str) -> Phase1Result:
        """Process audio and return mock results"""
        transcript = self.extract_speech_to_text(audio_path)
        alignments = self.align_transcript(transcript, reference_passage)
        metrics = self.extract_metrics(audio_path, transcript)
        feedback = self.generate_feedback(metrics, alignments)
        
        return Phase1Result(
            transcript=transcript,
            words_per_minute=metrics["wpm"],
            hesitations=metrics["hesitations"],
            pronunciation_score=metrics["pronunciation_score"],
            word_alignments=alignments,
            feedback=feedback,
            session_progress=0.75,
            audio_duration=metrics["duration"]
        )
    
    def extract_speech_to_text(self, audio_path: str) -> str:
        """Mock: Return reference text (replace with Wav2Vec model)"""
        return "The elephant sat quietly by the river bank"
    
    def align_transcript(self, transcript: str, reference: str) -> List[WordAlignment]:
        """Mock: Simple word alignment"""
        words = transcript.split()
        alignments = []
        for i, word in enumerate(words):
            alignments.append(WordAlignment(
                word=word,
                correct=True,
                confidence=0.85 + np.random.rand() * 0.15,
                start_time=i * 0.5,
                end_time=(i + 1) * 0.5
            ))
        return alignments
    
    def extract_metrics(self, audio_path: str, transcript: str) -> Dict:
        """Mock: Calculate metrics"""
        # Simulate metrics
        words = transcript.split()
        wpm = 45  # 45 words per minute
        hesitations = 2
        
        return {
            "wpm": wpm,
            "hesitations": hesitations,
            "pronunciation_score": 0.92,
            "duration": 60.0  # seconds
        }
    
    def generate_feedback(self, metrics: Dict, alignments: List[WordAlignment]) -> str:
        """Mock: Generate feedback"""
        wpm = metrics["wpm"]
        hesitations = metrics["hesitations"]
        
        feedback_parts = []
        if wpm > 40:
            feedback_parts.append("Great pace!")
        if hesitations <= 2:
            feedback_parts.append("Excellent fluency!")
        
        # Find words that might need work
        problem_words = [a.word for a in alignments if a.confidence < 0.85]
        if problem_words:
            feedback_parts.append(f"Let's practice: {', '.join(problem_words[:2])}")
        
        return " ".join(feedback_parts) or "Keep practicing!"
