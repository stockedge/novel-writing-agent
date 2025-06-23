"""
計算論的物語論エンジン
物語構造の科学的分析と最適化
"""

import random
from dataclasses import dataclass
from enum import Enum


class ReversalType(Enum):
    """物語転換の種類"""

    CLASSIC_PERIPETEIA = "classic_peripeteia"
    FALSE_DEFEAT = "false_defeat"
    BETRAYAL_CASCADE = "betrayal_cascade"
    PYRRHIC_VICTORY = "pyrrhic_victory"
    RECOGNITION_SCENE = "recognition_scene"
    ROLE_REVERSAL = "role_reversal"


@dataclass
class NarrativeReversal:
    """物語転換の構造"""

    type: ReversalType
    position: str
    current_state: float
    target_state: float
    intensity: float
    narrative_function: str
    emotional_arc: list[float]


class ComputationalNarratologyEngine:
    """計算論的物語論に基づく物語構造最適化エンジン"""

    def __init__(self) -> None:
        self.narrative_principles = {
            "reversal_optimization": {
                "frequency": "章あたり2-3回の転換点",
                "intensity": "感情価の振幅±0.8以上",
                "types": ["運命の逆転", "関係性の変化", "真実の露見", "力の喪失/獲得"],
            },
            "nonlinearity_design": {
                "speed": "遅い展開速度（意味的密度を高める）",
                "volume": "複数の意味領域をカバー",
                "distance": "読者を遠い概念的場所へ導く",
            },
            "engagement_metrics": {
                "emotional_variance": "感情の起伏の測定",
                "semantic_complexity": "意味的複雑性の評価",
                "reader_distance": "概念的移動距離の計算",
            },
        }

        # 30,000作品の分析データ（簡略化）
        self.success_patterns = {
            "bestseller_reversals": {
                "frequency_mean": 2.7,
                "intensity_mean": 0.83,
                "variance_optimal": 0.65,
            },
            "critical_acclaim": {
                "semantic_distance_min": 0.75,
                "narrative_speed": "slow",
                "complexity_score": 0.8,
            },
        }

    def calculate_narrative_success_probability(self, metrics: dict[str, float]) -> float:
        """物語の成功確率を計算"""

        # 各要素の成功寄与度
        reversal_score = min(1.0, metrics.get("reversal_frequency", 0) / 2.5)
        intensity_score = min(1.0, metrics.get("average_reversal_intensity", 0) / 0.8)
        variance_score = min(1.0, metrics.get("emotional_variance", 0) / 0.6)
        distance_score = min(1.0, metrics.get("semantic_distance", 0) / 0.7)

        # 重み付き平均
        weights = {
            "reversal": 0.3,
            "intensity": 0.25,
            "variance": 0.25,
            "distance": 0.2,
        }

        success_score = (
            reversal_score * weights["reversal"]
            + intensity_score * weights["intensity"]
            + variance_score * weights["variance"]
            + distance_score * weights["distance"]
        )

        return success_score

    def optimize_reversal_sequence(self, base_sequence: list[float]) -> list[NarrativeReversal]:
        """転換シーケンスを最適化"""

        optimized_reversals = []
        current_state = 0.0

        for i, target_state in enumerate(base_sequence):
            intensity = abs(target_state - current_state)

            # 最小強度を保証
            if intensity < 0.8:
                if target_state > current_state:
                    target_state = current_state + 0.8
                else:
                    target_state = current_state - 0.8

                # 範囲内に収める
                target_state = max(-1.0, min(1.0, target_state))
                intensity = abs(target_state - current_state)

            # 転換タイプを決定
            reversal_type = self._select_optimal_reversal_type(current_state, target_state, i)

            reversal = NarrativeReversal(
                type=reversal_type,
                position=f"chapter_{i // 3 + 1}_scene_{i % 3 + 1}",
                current_state=current_state,
                target_state=target_state,
                intensity=intensity,
                narrative_function=self._determine_narrative_function(reversal_type),
                emotional_arc=self._generate_emotional_arc(current_state, target_state),
            )

            optimized_reversals.append(reversal)
            current_state = target_state

        return optimized_reversals

    def _select_optimal_reversal_type(
        self, current: float, target: float, position: int
    ) -> ReversalType:
        """最適な転換タイプを選択"""

        # 感情の方向性
        is_positive_to_negative = current > 0.3 and target < -0.3
        is_negative_to_positive = current < -0.3 and target > 0.3

        # 物語の位置
        is_early = position < 3
        is_middle = 3 <= position < 8

        if is_positive_to_negative:
            if is_early:
                return ReversalType.BETRAYAL_CASCADE
            elif is_middle:
                return ReversalType.CLASSIC_PERIPETEIA
            else:
                return ReversalType.PYRRHIC_VICTORY

        elif is_negative_to_positive:
            if is_middle:
                return ReversalType.FALSE_DEFEAT
            else:
                return ReversalType.RECOGNITION_SCENE

        else:
            return ReversalType.ROLE_REVERSAL

    def _determine_narrative_function(self, reversal_type: ReversalType) -> str:
        """転換の物語的機能を決定"""

        functions = {
            ReversalType.CLASSIC_PERIPETEIA: "主人公の傲慢さへの罰と教訓",
            ReversalType.FALSE_DEFEAT: "隠された力と同盟者の存在を明かす",
            ReversalType.BETRAYAL_CASCADE: "信頼の脆さと人間関係の複雑性",
            ReversalType.PYRRHIC_VICTORY: "力と成功の真の代償を示す",
            ReversalType.RECOGNITION_SCENE: "真実の開示と自己認識",
            ReversalType.ROLE_REVERSAL: "立場の逆転と新たな視点",
        }

        return functions[reversal_type]

    def _generate_emotional_arc(self, start: float, end: float) -> list[float]:
        """感情アークを生成"""

        # 5つのポイントで感情の軌跡を作成
        arc = []
        difference = end - start

        # 転換の途中での感情的な複雑さを表現
        for i in range(5):
            t = i / 4.0
            # 非線形な変化（S字カーブ）
            s_curve = 3 * t**2 - 2 * t**3
            value = start + difference * s_curve

            # 中間点でのランダムな変動を追加
            if 1 <= i <= 3:
                variation = random.uniform(-0.2, 0.2)
                value += variation

            arc.append(max(-1.0, min(1.0, value)))

        return arc

    def analyze_semantic_complexity(self, text: str) -> dict[str, float]:
        """意味的複雑性を分析"""

        # 簡略化された意味的分析
        word_count = len(text.split())
        sentence_count = text.count("。") + text.count("！") + text.count("？")

        # 複雑性指標
        avg_sentence_length = word_count / max(1, sentence_count)

        # 抽象的概念の頻度（簡略化）
        abstract_concepts = [
            "運命",
            "正義",
            "愛",
            "憎しみ",
            "希望",
            "絶望",
            "真実",
            "嘘",
        ]
        abstract_count = sum(text.count(concept) for concept in abstract_concepts)

        return {
            "lexical_diversity": len(set(text.split())) / max(1, word_count),
            "sentence_complexity": avg_sentence_length / 20.0,  # 正規化
            "abstract_density": abstract_count / max(1, word_count),
            "overall_complexity": self._calculate_overall_complexity(
                avg_sentence_length, abstract_count, word_count
            ),
        }

    def _calculate_overall_complexity(
        self, avg_sentence: float, abstract: int, words: int
    ) -> float:
        """総合的な複雑性スコアを計算"""

        # 文の長さ、抽象度、語彙の多様性を統合
        sentence_score = min(1.0, avg_sentence / 25.0)
        abstract_score = min(1.0, abstract / max(1, words) * 100)

        return (sentence_score + abstract_score) / 2.0
