"""
コアコンポーネント
"""

from .computational_narratology import (
    ComputationalNarratologyEngine,
    NarrativeReversal,
    ReversalType,
)
from .emotional_valence_tracker import EmotionalEvent, EmotionalValenceTracker
from .reversal_scene_generator import ReversalSceneGenerator, SceneType
from .semantic_pacing_controller import (
    NarrativeSpeed,
    SemanticPacingController,
    SemanticPosition,
)
from .temporal_structure_designer import (
    TemporalEvent,
    TemporalStructureDesigner,
    TemporalTechnique,
)

__all__ = [
    "ComputationalNarratologyEngine",
    "NarrativeReversal",
    "ReversalType",
    "EmotionalValenceTracker",
    "EmotionalEvent",
    "ReversalSceneGenerator",
    "SceneType",
    "SemanticPacingController",
    "SemanticPosition",
    "NarrativeSpeed",
    "TemporalStructureDesigner",
    "TemporalTechnique",
    "TemporalEvent",
]
