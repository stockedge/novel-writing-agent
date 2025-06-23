"""
感情価トラッキングシステム
物語の感情価をリアルタイムで追跡・分析
"""

import random
import re
from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass
class EmotionalEvent:
    """感情的イベントの記録"""

    position: int
    valence: float
    intensity: float
    event_type: str
    description: str


class EmotionalValenceTracker:
    """物語の感情価をリアルタイムで追跡・分析"""

    def __init__(self) -> None:
        self.valence_history: list[float] = []
        self.current_valence: float = 0.0
        self.emotional_events: list[EmotionalEvent] = []
        self.window_size: int = 5  # 移動平均の窓サイズ

        # 感情語彙データベース（拡張版）
        self.valence_vocabulary = {
            "positive": {
                "weak": {
                    "words": [
                        "希望",
                        "安堵",
                        "友情",
                        "微笑",
                        "暖かい",
                        "平和",
                        "穏やか",
                    ],
                    "weight": 0.3,
                },
                "moderate": {
                    "words": [
                        "勝利",
                        "再会",
                        "発見",
                        "成功",
                        "達成",
                        "幸福",
                        "満足",
                        "喜び",
                    ],
                    "weight": 0.6,
                },
                "strong": {
                    "words": [
                        "歓喜",
                        "奇跡",
                        "救済",
                        "愛の成就",
                        "至福",
                        "恍惚",
                        "栄光",
                        "解放",
                    ],
                    "weight": 1.0,
                },
            },
            "negative": {
                "weak": {
                    "words": ["不安", "疑念", "孤独", "寂しさ", "曇り", "不快", "困惑"],
                    "weight": -0.3,
                },
                "moderate": {
                    "words": [
                        "敗北",
                        "裏切り",
                        "喪失",
                        "悲しみ",
                        "怒り",
                        "失望",
                        "恐怖",
                    ],
                    "weight": -0.6,
                },
                "strong": {
                    "words": [
                        "絶望",
                        "死",
                        "破滅",
                        "全てを失う",
                        "地獄",
                        "阿鼻叫喚",
                        "破綻",
                        "滅亡",
                    ],
                    "weight": -1.0,
                },
            },
        }

        # 文脈修飾子（感情の強度を変更）
        self.context_modifiers = {
            "intensifiers": {
                "words": ["非常に", "とても", "極めて", "完全に", "絶対に", "まったく"],
                "multiplier": 1.5,
            },
            "diminishers": {
                "words": ["少し", "やや", "若干", "わずかに", "ほんの", "軽く"],
                "multiplier": 0.5,
            },
            "negators": {
                "words": ["ない", "ぬ", "ず", "まい", "決して", "全く"],
                "effect": "reverse",
            },
        }

    async def analyze_scene_valence(self, scene_text: str, scene_position: int = 0) -> float:
        """シーンの感情価を分析"""

        # テキストの前処理
        cleaned_text = self._preprocess_text(scene_text)

        # 基本的な感情価計算
        base_valence = self._calculate_base_valence(cleaned_text)

        # 文脈修飾子の適用
        modified_valence = self._apply_context_modifiers(cleaned_text, base_valence)

        # 物語位置による調整
        position_adjusted = self._adjust_for_narrative_position(modified_valence, scene_position)

        # 感情価履歴の更新
        self.valence_history.append(position_adjusted)
        self.current_valence = position_adjusted

        # 重要な感情的イベントの記録
        if abs(position_adjusted) > 0.7:
            event = EmotionalEvent(
                position=scene_position,
                valence=position_adjusted,
                intensity=abs(position_adjusted),
                event_type=(
                    "high_intensity" if abs(position_adjusted) > 0.8 else "moderate_intensity"
                ),
                description=self._describe_emotional_event(position_adjusted, cleaned_text),
            )
            self.emotional_events.append(event)

        return position_adjusted

    def _preprocess_text(self, text: str) -> str:
        """テキストの前処理"""

        # 句読点の正規化
        text = re.sub(r"[。！？\.\!\?]+", "。", text)

        # 余分な空白の除去
        text = re.sub(r"\s+", " ", text.strip())

        return text

    def _calculate_base_valence(self, text: str) -> float:
        """基本的な感情価を計算"""

        positive_score = 0.0
        negative_score = 0.0

        # ポジティブ語彙のスコア計算
        for _intensity_level, data in self.valence_vocabulary["positive"].items():
            weight = data["weight"]
            for word in data["words"]:
                count = text.count(word)
                positive_score += count * weight

        # ネガティブ語彙のスコア計算
        for _intensity_level, data in self.valence_vocabulary["negative"].items():
            weight = abs(data["weight"])  # 絶対値を取って計算
            for word in data["words"]:
                count = text.count(word)
                negative_score += count * weight

        # 正規化
        total_score = positive_score + negative_score
        if total_score > 0:
            valence = (positive_score - negative_score) / total_score
        else:
            valence = 0.0

        return max(-1.0, min(1.0, valence))

    def _apply_context_modifiers(self, text: str, base_valence: float) -> float:
        """文脈修飾子を適用"""

        modified_valence = base_valence

        # 強調語の検出
        intensifier_count = 0
        for word in self.context_modifiers["intensifiers"]["words"]:
            intensifier_count += text.count(word)

        if intensifier_count > 0:
            multiplier = self.context_modifiers["intensifiers"]["multiplier"]
            modified_valence *= min(2.0, 1.0 + intensifier_count * 0.2)

        # 減弱語の検出
        diminisher_count = 0
        for word in self.context_modifiers["diminishers"]["words"]:
            diminisher_count += text.count(word)

        if diminisher_count > 0:
            multiplier = self.context_modifiers["diminishers"]["multiplier"]
            modified_valence *= max(0.2, multiplier)

        # 否定語の検出
        negator_count = 0
        for word in self.context_modifiers["negators"]["words"]:
            negator_count += text.count(word)

        if negator_count % 2 == 1:  # 奇数回の否定
            modified_valence *= -0.8  # 完全な反転ではなく緩和

        return max(-1.0, min(1.0, modified_valence))

    def _adjust_for_narrative_position(self, valence: float, position: int) -> float:
        """物語位置による感情価の調整"""

        # 物語の三幕構造を考慮
        # 第一幕: 0-25%, 第二幕: 25-75%, 第三幕: 75-100%

        if position <= 3:  # 序盤
            # 序盤は感情の振れ幅を抑制
            return valence * 0.8
        elif position >= 10:  # 終盤
            # 終盤は感情の振れ幅を強調
            return valence * 1.2
        else:  # 中盤
            # 中盤はそのまま
            return valence

    def _describe_emotional_event(self, valence: float, text_sample: str) -> str:
        """感情的イベントの説明を生成"""

        if valence > 0.8:
            return f"強いポジティブな転換: {text_sample[:50]}..."
        elif valence > 0.5:
            return f"中程度のポジティブな展開: {text_sample[:50]}..."
        elif valence < -0.8:
            return f"強いネガティブな転換: {text_sample[:50]}..."
        elif valence < -0.5:
            return f"中程度のネガティブな展開: {text_sample[:50]}..."
        else:
            return f"中立的な展開: {text_sample[:50]}..."

    def calculate_reversal_impact(self, from_valence: float, to_valence: float) -> float:
        """転換の影響度を計算"""

        return abs(to_valence - from_valence)

    def get_optimal_next_reversal(
        self, current_valence: float, recent_reversals: list[float]
    ) -> dict[str, Any]:
        """次の最適な転換を提案"""

        # 最近の転換履歴を分析
        if len(recent_reversals) > 0:
            last_reversal_intensity = abs(recent_reversals[-1])
            avg_recent_intensity = np.mean([abs(r) for r in recent_reversals[-3:]])
        else:
            last_reversal_intensity = 0.0
            avg_recent_intensity = 0.0

        # 転換の頻度と強度のバランスを考慮
        if last_reversal_intensity > 0.8:
            # 大きな転換の後は小さめの変化を推奨
            suggested_intensity = random.uniform(0.4, 0.6)
        elif avg_recent_intensity < 0.5:
            # 最近の転換が弱い場合は強い転換を推奨
            suggested_intensity = random.uniform(0.8, 1.0)
        else:
            # 通常は中程度から強い転換
            suggested_intensity = random.uniform(0.6, 0.9)

        # 現在の感情価から逆方向への転換を推奨
        if current_valence > 0.3:
            suggested_direction = "negative"
            target_valence = current_valence - suggested_intensity
        elif current_valence < -0.3:
            suggested_direction = "positive"
            target_valence = current_valence + suggested_intensity
        else:
            # 中立付近では大きな転換をどちらかの方向へ
            suggested_direction = random.choice(["positive", "negative"])
            multiplier = 1 if suggested_direction == "positive" else -1
            target_valence = suggested_intensity * multiplier

        # 範囲内に収める
        target_valence = max(-1.0, min(1.0, target_valence))

        return {
            "suggested_direction": suggested_direction,
            "suggested_intensity": suggested_intensity,
            "target_valence": target_valence,
            "current_valence": current_valence,
            "reversal_type": self._suggest_reversal_type(current_valence, target_valence),
            "confidence": self._calculate_suggestion_confidence(recent_reversals),
        }

    def _suggest_reversal_type(self, current: float, target: float) -> str:
        """転換タイプを提案"""

        intensity = abs(target - current)

        if current > 0.5 and target < -0.5:
            return "classic_peripeteia"  # 栄光から転落
        elif current < -0.5 and target > 0.5:
            return "false_defeat"  # 絶望から救済
        elif intensity > 0.8:
            return "dramatic_reversal"  # 劇的転換
        else:
            return "gradual_shift"  # 漸進的変化

    def _calculate_suggestion_confidence(self, recent_reversals: list[float]) -> float:
        """提案の信頼度を計算"""

        if len(recent_reversals) < 3:
            return 0.5  # データ不足

        # 最近の転換のパターンを分析
        variance = np.var(recent_reversals)
        trend_consistency = self._analyze_trend_consistency(recent_reversals)

        # 適度な変動と一貫性があるほど信頼度が高い
        confidence = min(1.0, (variance * 2 + trend_consistency) / 2)

        return confidence

    def _analyze_trend_consistency(self, reversals: list[float]) -> float:
        """転換トレンドの一貫性を分析"""

        if len(reversals) < 2:
            return 0.5

        # 連続する転換の方向性を分析
        direction_changes = 0
        for i in range(1, len(reversals)):
            if (reversals[i] > 0) != (reversals[i - 1] > 0):
                direction_changes += 1

        # 適度な方向転換がある（単調でない）ほど良い
        optimal_changes = len(reversals) * 0.6
        consistency = 1.0 - abs(direction_changes - optimal_changes) / len(reversals)

        return max(0.0, min(1.0, consistency))

    def get_emotional_statistics(self) -> dict[str, Any]:
        """感情統計を取得"""

        if not self.valence_history:
            return {"error": "感情価履歴が空です"}

        history_array = np.array(self.valence_history)

        return {
            "mean_valence": float(np.mean(history_array)),
            "valence_variance": float(np.var(history_array)),
            "valence_std": float(np.std(history_array)),
            "min_valence": float(np.min(history_array)),
            "max_valence": float(np.max(history_array)),
            "range": float(np.max(history_array) - np.min(history_array)),
            "positive_ratio": float(np.sum(history_array > 0) / len(history_array)),
            "negative_ratio": float(np.sum(history_array < 0) / len(history_array)),
            "neutral_ratio": float(np.sum(history_array == 0) / len(history_array)),
            "emotional_events_count": len(self.emotional_events),
            "high_intensity_events": len([e for e in self.emotional_events if e.intensity > 0.8]),
        }

    def get_moving_average(self, window_size: int | None = None) -> list[float]:
        """移動平均を計算"""

        if window_size is None:
            window_size = self.window_size

        if len(self.valence_history) < window_size:
            return self.valence_history.copy()

        moving_avg = []
        for i in range(window_size - 1, len(self.valence_history)):
            window = self.valence_history[i - window_size + 1 : i + 1]
            moving_avg.append(sum(window) / window_size)

        return moving_avg
