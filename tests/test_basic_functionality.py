"""基本機能のテスト"""

import pytest

from src.core.computational_narratology import ComputationalNarratologyEngine
from src.core.emotional_valence_tracker import EmotionalValenceTracker
from src.core.semantic_pacing_controller import SemanticPacingController
from src.core.temporal_structure_designer import TemporalStructureDesigner


def test_computational_narratology_engine_init():
    """計算論的物語論エンジンの初期化テスト"""
    engine = ComputationalNarratologyEngine()
    assert engine is not None
    assert hasattr(engine, "narrative_principles")
    assert hasattr(engine, "success_patterns")


def test_emotional_valence_tracker_init():
    """感情価トラッカーの初期化テスト"""
    tracker = EmotionalValenceTracker()
    assert tracker is not None
    assert tracker.current_valence == 0.0
    assert len(tracker.valence_history) == 0


def test_semantic_pacing_controller_init():
    """意味的ペーシングコントローラーの初期化テスト"""
    controller = SemanticPacingController()
    assert controller is not None
    assert hasattr(controller, "semantic_domains")


def test_temporal_structure_designer_init():
    """時間構造デザイナーの初期化テスト"""
    designer = TemporalStructureDesigner()
    assert designer is not None
    assert hasattr(designer, "temporal_techniques")


@pytest.mark.asyncio
async def test_valence_analysis():
    """感情価分析の基本テスト"""
    tracker = EmotionalValenceTracker()

    # ポジティブなテキスト
    positive_text = "希望に満ちた美しい朝、勇者は勝利を確信していた。"
    valence = await tracker.analyze_scene_valence(positive_text)
    assert isinstance(valence, float)
    assert -1.0 <= valence <= 1.0

    # ネガティブなテキスト
    negative_text = "絶望的な状況で、すべてが失われたように思えた。"
    valence = await tracker.analyze_scene_valence(negative_text)
    assert isinstance(valence, float)
    assert -1.0 <= valence <= 1.0


def test_success_probability_calculation():
    """成功確率計算のテスト"""
    engine = ComputationalNarratologyEngine()

    metrics = {
        "reversal_frequency": 2.5,
        "average_reversal_intensity": 0.8,
        "emotional_variance": 0.6,
        "semantic_distance": 0.7,
    }

    probability = engine.calculate_narrative_success_probability(metrics)
    assert isinstance(probability, float)
    assert 0.0 <= probability <= 1.0


def test_reversal_sequence_optimization():
    """転換シーケンス最適化のテスト"""
    engine = ComputationalNarratologyEngine()

    base_sequence = [0.8, -0.3, 0.5, -0.7, 0.2]
    optimized = engine.optimize_reversal_sequence(base_sequence)

    assert len(optimized) == len(base_sequence)
    for reversal in optimized:
        assert hasattr(reversal, "type")
        assert hasattr(reversal, "intensity")
        assert hasattr(reversal, "target_state")
