"""
PersonaPath Service Configuration
Defines backend implementations and integration points
"""

from enum import Enum
from typing import Union
from .phase1_service import Phase1Backend, Phase1MockBackend
from .phase2_service import Phase2Backend, Phase2MockBackend

class BackendMode(str, Enum):
    """Backend configuration modes"""
    MOCK = "mock"  # Mock implementations for UI testing
    NOTEBOOK = "notebook"  # Integration with existing notebooks
    PRODUCTION = "production"  # Full model pipeline

class ServiceConfig:
    """Centralized service configuration"""
    
    def __init__(self, mode: BackendMode = BackendMode.MOCK):
        self.mode = mode
        self._phase1_backend: Union[Phase1Backend, None] = None
        self._phase2_backend: Union[Phase2Backend, None] = None
        self._initialize_backends()
    
    def _initialize_backends(self):
        """Initialize backends based on configured mode"""
        if self.mode == BackendMode.MOCK:
            self._phase1_backend = Phase1MockBackend()
            self._phase2_backend = Phase2MockBackend()
        
        elif self.mode == BackendMode.NOTEBOOK:
            # TODO: Import actual notebook implementations
            # from notebooks.cnn_emotion_training import CNNEmotionModel
            # from notebooks.phase1_stts import SpeechToTextModel
            self._phase1_backend = Phase1MockBackend()  # Placeholder
            self._phase2_backend = Phase2MockBackend()  # Placeholder
        
        elif self.mode == BackendMode.PRODUCTION:
            # TODO: Initialize production models
            self._phase1_backend = Phase1MockBackend()  # Placeholder
            self._phase2_backend = Phase2MockBackend()  # Placeholder
    
    @property
    def phase1_backend(self) -> Phase1Backend:
        """Get Phase 1 backend"""
        if self._phase1_backend is None:
            raise RuntimeError("Phase 1 backend not initialized")
        return self._phase1_backend
    
    @property
    def phase2_backend(self) -> Phase2Backend:
        """Get Phase 2 backend"""
        if self._phase2_backend is None:
            raise RuntimeError("Phase 2 backend not initialized")
        return self._phase2_backend
    
    def set_phase1_backend(self, backend: Phase1Backend):
        """Replace Phase 1 backend at runtime"""
        self._phase1_backend = backend
    
    def set_phase2_backend(self, backend: Phase2Backend):
        """Replace Phase 2 backend at runtime"""
        self._phase2_backend = backend

# Global configuration instance
_service_config: Union[ServiceConfig, None] = None

def get_config(mode: BackendMode = BackendMode.MOCK) -> ServiceConfig:
    """Get or create global service configuration"""
    global _service_config
    if _service_config is None:
        _service_config = ServiceConfig(mode)
    return _service_config

def set_config(config: ServiceConfig):
    """Replace global service configuration"""
    global _service_config
    _service_config = config
