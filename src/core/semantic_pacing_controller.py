"""
意味的ペーシング制御システム
物語の意味的な速度と距離を制御
"""

import math
import random
from dataclasses import dataclass
from enum import Enum
from typing import Any

import numpy as np


class NarrativeSpeed(Enum):
    """物語速度の種類"""

    VERY_SLOW = "very_slow"
    SLOW = "slow"
    MODERATE = "moderate"
    FAST = "fast"
    VERY_FAST = "very_fast"


@dataclass
class SemanticPosition:
    """意味的位置"""

    physical: float
    emotional: float
    philosophical: float
    political: float
    spiritual: float
    mythological: float

    def distance_to(self, other: "SemanticPosition") -> float:
        """他の位置との距離を計算"""
        return math.sqrt(
            (self.physical - other.physical) ** 2
            + (self.emotional - other.emotional) ** 2
            + (self.philosophical - other.philosophical) ** 2
            + (self.political - other.political) ** 2
            + (self.spiritual - other.spiritual) ** 2
            + (self.mythological - other.mythological) ** 2
        )


@dataclass
class SemanticJourney:
    """意味的な旅程"""

    start_position: SemanticPosition
    end_position: SemanticPosition
    waypoints: list[SemanticPosition]
    total_distance: float
    journey_type: str


class SemanticPacingController:
    """物語の意味的な速度と距離を制御"""

    def __init__(self) -> None:
        self.semantic_domains = {
            "physical": {
                "concepts": ["戦闘", "旅", "探索", "逃走", "建築", "自然"],
                "range": (-1.0, 1.0),
                "weights": {"action": 0.8, "description": 0.6, "dialogue": 0.2},
            },
            "emotional": {
                "concepts": [
                    "愛",
                    "憎しみ",
                    "恐怖",
                    "希望",
                    "絶望",
                    "怒り",
                    "悲しみ",
                    "喜び",
                ],
                "range": (-1.0, 1.0),
                "weights": {"dialogue": 0.9, "internal": 0.8, "action": 0.4},
            },
            "philosophical": {
                "concepts": [
                    "正義",
                    "運命",
                    "自由意志",
                    "犠牲",
                    "真実",
                    "善悪",
                    "存在意義",
                ],
                "range": (-1.0, 1.0),
                "weights": {"internal": 0.9, "dialogue": 0.7, "symbolism": 0.8},
            },
            "political": {
                "concepts": ["権力", "統治", "反乱", "同盟", "陰謀", "外交", "戦争"],
                "range": (-1.0, 1.0),
                "weights": {"dialogue": 0.8, "action": 0.7, "description": 0.5},
            },
            "spiritual": {
                "concepts": ["信仰", "奇跡", "堕落", "贖罪", "神々", "祈り", "聖域"],
                "range": (-1.0, 1.0),
                "weights": {"symbolism": 0.9, "description": 0.7, "dialogue": 0.6},
            },
            "mythological": {
                "concepts": ["予言", "古代", "神々", "創造", "終末", "英雄", "怪物"],
                "range": (-1.0, 1.0),
                "weights": {"description": 0.8, "action": 0.7, "symbolism": 0.9},
            },
        }

        self.current_position = SemanticPosition(0, 0, 0, 0, 0, 0)
        self.trajectory_history: list[SemanticPosition] = []

        # 速度制御のパラメータ
        self.speed_parameters = {
            NarrativeSpeed.VERY_SLOW: {
                "description_ratio": 0.6,
                "internal_monologue_ratio": 0.3,
                "scene_detail_level": 0.9,
                "temporal_stretching": 2.0,
            },
            NarrativeSpeed.SLOW: {
                "description_ratio": 0.4,
                "internal_monologue_ratio": 0.2,
                "scene_detail_level": 0.7,
                "temporal_stretching": 1.5,
            },
            NarrativeSpeed.MODERATE: {
                "description_ratio": 0.3,
                "internal_monologue_ratio": 0.15,
                "scene_detail_level": 0.5,
                "temporal_stretching": 1.0,
            },
            NarrativeSpeed.FAST: {
                "description_ratio": 0.2,
                "internal_monologue_ratio": 0.1,
                "scene_detail_level": 0.3,
                "temporal_stretching": 0.7,
            },
            NarrativeSpeed.VERY_FAST: {
                "description_ratio": 0.1,
                "internal_monologue_ratio": 0.05,
                "scene_detail_level": 0.2,
                "temporal_stretching": 0.5,
            },
        }

    async def design_nonlinear_structure(self, plot: dict[str, Any]) -> dict[str, Any]:
        """非線形構造を設計"""

        # 基本的な時系列
        chronological_events = plot.get("events", [])

        # 各イベントの意味的位置を計算
        event_positions = []
        for event in chronological_events:
            position = await self._calculate_semantic_position(event)
            event_positions.append(
                {
                    "event": event,
                    "position": position,
                    "timestamp": event.get("timestamp", 0),
                }
            )

        # 意味的距離を最大化する再配列
        optimized_sequence = await self._optimize_semantic_journey(event_positions)

        # フラッシュバックとフラッシュフォワードの配置
        temporal_structure = await self._design_temporal_complexity(optimized_sequence)

        # 複数視点の交錯
        multi_pov_structure = await self._weave_perspectives(temporal_structure)

        # 意味的軌跡の計算
        semantic_trajectory = self._calculate_semantic_trajectory(multi_pov_structure)

        # ペーシングプロファイルの作成
        pacing_profile = await self._create_pacing_profile(multi_pov_structure)

        return {
            "structure": multi_pov_structure,
            "semantic_trajectory": semantic_trajectory,
            "pacing_profile": pacing_profile,
            "total_distance": semantic_trajectory["total_distance"],
            "complexity_score": self._calculate_complexity_score(multi_pov_structure),
            "reading_path": self._design_reading_path(multi_pov_structure),
        }

    async def _calculate_semantic_position(self, event: dict[str, Any]) -> SemanticPosition:
        """イベントの意味的位置を計算"""

        event_text = event.get("description", "")
        event_type = event.get("type", "action")

        positions = {}

        for domain, domain_info in self.semantic_domains.items():
            score = 0.0
            concept_count = 0

            # 各概念の出現頻度を計算
            for concept in domain_info["concepts"]:
                count = event_text.lower().count(concept.lower())
                if count > 0:
                    weight = domain_info["weights"].get(event_type, 0.5)
                    score += count * weight
                    concept_count += count

            # 正規化
            if concept_count > 0:
                normalized_score = min(1.0, score / concept_count)
                # 範囲内に収める
                min_val, max_val = domain_info["range"]
                positions[domain] = min_val + (normalized_score * (max_val - min_val))
            else:
                positions[domain] = 0.0

        return SemanticPosition(**positions)

    async def _optimize_semantic_journey(
        self, event_positions: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """意味的な旅を最適化"""

        if not event_positions:
            return []

        optimized_sequence = []
        remaining_events = event_positions.copy()

        # 最初のイベントを選択（通常は時系列順）
        current_event = min(remaining_events, key=lambda e: e["timestamp"])
        optimized_sequence.append(current_event)
        remaining_events.remove(current_event)

        current_position = current_event["position"]

        while remaining_events:
            # 次のイベントを選択（意味的距離を考慮）
            next_event = self._select_next_event(current_position, remaining_events)

            # 距離が大きすぎる場合は橋渡しイベントを作成
            distance = current_position.distance_to(next_event["position"])
            if distance > 0.7:
                bridge_event = await self._create_bridge_event(
                    current_position, next_event["position"]
                )
                if bridge_event:
                    optimized_sequence.append(bridge_event)

            optimized_sequence.append(next_event)
            remaining_events.remove(next_event)
            current_position = next_event["position"]

        return optimized_sequence

    def _select_next_event(
        self, current_position: SemanticPosition, candidates: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """次のイベントを選択"""

        # 意味的距離と時系列的制約を考慮
        best_event = None
        best_score = float("-inf")

        for event in candidates:
            event_position = event["position"]

            # 意味的距離スコア（適度な距離を好む）
            distance = current_position.distance_to(event_position)
            distance_score = self._calculate_distance_score(distance)

            # 時系列制約スコア
            temporal_score = self._calculate_temporal_score(event)

            # 総合スコア
            total_score = distance_score * 0.7 + temporal_score * 0.3

            if total_score > best_score:
                best_score = total_score
                best_event = event

        return best_event if best_event else candidates[0]

    def _calculate_distance_score(self, distance: float) -> float:
        """距離スコアを計算（適度な距離を好む）"""

        optimal_distance = 0.5
        deviation = abs(distance - optimal_distance)
        return max(0.0, 1.0 - deviation * 2)

    def _calculate_temporal_score(self, event: dict[str, Any]) -> float:
        """時系列スコアを計算"""

        # 時系列の制約があまり強くならないように調整
        return random.uniform(0.3, 0.7)

    async def _create_bridge_event(
        self, start_pos: SemanticPosition, end_pos: SemanticPosition
    ) -> dict[str, Any] | None:
        """橋渡しイベントを作成"""

        # 中間位置を計算
        mid_position = SemanticPosition(
            (start_pos.physical + end_pos.physical) / 2,
            (start_pos.emotional + end_pos.emotional) / 2,
            (start_pos.philosophical + end_pos.philosophical) / 2,
            (start_pos.political + end_pos.political) / 2,
            (start_pos.spiritual + end_pos.spiritual) / 2,
            (start_pos.mythological + end_pos.mythological) / 2,
        )

        # 橋渡しの種類を決定
        bridge_type = self._determine_bridge_type(start_pos, end_pos)

        bridge_event = {
            "event": {
                "type": "bridge",
                "description": f"意味的橋渡し: {bridge_type}",
                "timestamp": -1,  # 特別なタイムスタンプ
                "bridge_type": bridge_type,
            },
            "position": mid_position,
            "is_bridge": True,
        }

        return bridge_event

    def _determine_bridge_type(self, start_pos: SemanticPosition, end_pos: SemanticPosition) -> str:
        """橋渡しの種類を決定"""

        # 最も変化の大きい次元を特定
        changes = {
            "physical": abs(end_pos.physical - start_pos.physical),
            "emotional": abs(end_pos.emotional - start_pos.emotional),
            "philosophical": abs(end_pos.philosophical - start_pos.philosophical),
            "political": abs(end_pos.political - start_pos.political),
            "spiritual": abs(end_pos.spiritual - start_pos.spiritual),
            "mythological": abs(end_pos.mythological - start_pos.mythological),
        }

        max_change_domain = max(changes.keys(), key=lambda k: changes[k])

        bridge_types = {
            "physical": "環境の変化・移動",
            "emotional": "内面の変化・心境の推移",
            "philosophical": "価値観の変化・思索",
            "political": "権力関係の変化・状況の展開",
            "spiritual": "信念の変化・神秘的体験",
            "mythological": "過去の記憶・伝説の想起",
        }

        return bridge_types.get(max_change_domain, "状況の推移")

    async def _design_temporal_complexity(self, sequence: list[dict[str, Any]]) -> dict[str, Any]:
        """時間的複雑性を設計"""

        # フラッシュバックの配置
        flashbacks = await self._place_flashbacks(sequence)

        # フラッシュフォワードの配置
        flashforwards = await self._place_flashforwards(sequence)

        # 並行時間軸の設計
        parallel_timelines = await self._create_parallel_timelines(sequence)

        return {
            "main_sequence": sequence,
            "flashbacks": flashbacks,
            "flashforwards": flashforwards,
            "parallel_timelines": parallel_timelines,
            "temporal_complexity_score": self._calculate_temporal_complexity(
                flashbacks, flashforwards, parallel_timelines
            ),
        }

    async def _place_flashbacks(self, sequence: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """フラッシュバックを配置"""

        flashbacks = []

        for i, event in enumerate(sequence):
            # 特定の条件でフラッシュバックを配置
            if event["event"].get("type") == "revelation" or event["position"].emotional < -0.5:
                flashback = {
                    "position_in_sequence": i,
                    "target_past_event": f"過去の関連イベント_{i}",
                    "trigger": event["event"].get("description", ""),
                    "emotional_purpose": "現在の状況への理解を深める",
                }
                flashbacks.append(flashback)

        return flashbacks[:3]  # 最大3つまで

    async def _place_flashforwards(self, sequence: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """フラッシュフォワードを配置"""

        # フラッシュフォワードは控えめに使用
        flashforwards = []

        if len(sequence) > 5:
            mid_point = len(sequence) // 2
            flashforward = {
                "position_in_sequence": mid_point,
                "target_future_event": "最終決戦の予兆",
                "foreshadowing_purpose": "運命の必然性を示唆",
            }
            flashforwards.append(flashforward)

        return flashforwards

    async def _create_parallel_timelines(
        self, sequence: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        """並行時間軸を作成"""

        parallel_timelines = []

        # 主人公以外の視点からの並行展開
        timeline = {
            "perspective": "敵対者の視点",
            "events": [
                {"description": "主人公の行動への対応", "semantic_focus": "political"},
                {"description": "独自の計画の進行", "semantic_focus": "philosophical"},
            ],
            "intersection_points": [len(sequence) // 3, 2 * len(sequence) // 3],
        }
        parallel_timelines.append(timeline)

        return parallel_timelines

    def _calculate_temporal_complexity(
        self,
        flashbacks: list[dict[str, Any]],
        flashforwards: list[dict[str, Any]],
        parallel_timelines: list[dict[str, Any]],
    ) -> float:
        """時間的複雑性を計算"""

        complexity = 0.0
        complexity += len(flashbacks) * 0.3
        complexity += len(flashforwards) * 0.4
        complexity += len(parallel_timelines) * 0.5

        return min(1.0, complexity / 3.0)

    async def _weave_perspectives(self, temporal_structure: dict[str, Any]) -> dict[str, Any]:
        """複数視点を交錯させる"""

        main_sequence = temporal_structure["main_sequence"]
        parallel_timelines = temporal_structure["parallel_timelines"]

        woven_structure = {
            "chapters": [],
            "perspective_shifts": [],
            "convergence_points": [],
        }

        # 章ごとに視点を配置
        for i in range(0, len(main_sequence), 3):
            chapter_events = main_sequence[i : i + 3]

            # 主視点
            chapter = {
                "chapter_number": i // 3 + 1,
                "primary_perspective": "主人公",
                "events": chapter_events,
                "perspective_shifts": [],
            }

            # 視点の切り替え
            if parallel_timelines and (i // 3) % 2 == 1:
                chapter["perspective_shifts"].append(
                    {
                        "shift_to": parallel_timelines[0]["perspective"],
                        "events": parallel_timelines[0]["events"][:2],
                    }
                )

            woven_structure["chapters"].append(chapter)

        return woven_structure

    def _calculate_semantic_trajectory(self, structure: dict[str, Any]) -> dict[str, Any]:
        """意味的軌跡を計算"""

        chapters = structure.get("chapters", [])
        positions = []
        total_distance = 0.0

        prev_position = None

        for chapter in chapters:
            for event in chapter.get("events", []):
                position = event.get("position")
                if position:
                    positions.append(position)

                    if prev_position:
                        distance = prev_position.distance_to(position)
                        total_distance += distance

                    prev_position = position

        return {
            "positions": positions,
            "total_distance": total_distance,
            "average_step_distance": total_distance / max(1, len(positions) - 1),
            "semantic_coverage": self._calculate_semantic_coverage(positions),
        }

    def _calculate_semantic_coverage(self, positions: list[SemanticPosition]) -> dict[str, float]:
        """意味的カバレッジを計算"""

        if not positions:
            return {}

        coverage = {}

        for domain in [
            "physical",
            "emotional",
            "philosophical",
            "political",
            "spiritual",
            "mythological",
        ]:
            values = [getattr(pos, domain) for pos in positions]
            coverage[domain] = {
                "range": max(values) - min(values),
                "variance": float(np.var(values)),
                "coverage_ratio": (max(values) - min(values)) / 2.0,  # -1から1の範囲での割合
            }

        return coverage

    async def _create_pacing_profile(self, structure: dict[str, Any]) -> dict[int, NarrativeSpeed]:
        """ペーシングプロファイルを作成"""

        chapters = structure.get("chapters", [])
        pacing_profile = {}

        for i, chapter in enumerate(chapters):
            # 章の意味的密度を計算
            semantic_density = self._calculate_chapter_semantic_density(chapter)

            # 感情的強度を計算
            emotional_intensity = self._calculate_chapter_emotional_intensity(chapter)

            # ペーシングを決定
            if semantic_density > 0.7 or emotional_intensity > 0.8:
                speed = NarrativeSpeed.SLOW
            elif semantic_density > 0.5 or emotional_intensity > 0.6:
                speed = NarrativeSpeed.MODERATE
            else:
                speed = NarrativeSpeed.FAST

            pacing_profile[i + 1] = speed

        return pacing_profile

    def _calculate_chapter_semantic_density(self, chapter: dict[str, Any]) -> float:
        """章の意味的密度を計算"""

        events = chapter.get("events", [])
        if not events:
            return 0.0

        total_complexity = 0.0
        for event in events:
            position = event.get("position")
            if position:
                # 複数の次元にまたがるほど密度が高い
                non_zero_dimensions = sum(
                    1
                    for attr in [
                        "physical",
                        "emotional",
                        "philosophical",
                        "political",
                        "spiritual",
                        "mythological",
                    ]
                    if abs(getattr(position, attr)) > 0.3
                )
                total_complexity += non_zero_dimensions / 6.0

        return total_complexity / len(events)

    def _calculate_chapter_emotional_intensity(self, chapter: dict[str, Any]) -> float:
        """章の感情的強度を計算"""

        events = chapter.get("events", [])
        if not events:
            return 0.0

        max_emotional_value = 0.0
        for event in events:
            position = event.get("position")
            if position:
                emotional_magnitude = abs(position.emotional)
                max_emotional_value = max(max_emotional_value, emotional_magnitude)

        return max_emotional_value

    def _calculate_complexity_score(self, structure: dict[str, Any]) -> float:
        """構造の複雑性スコアを計算"""

        chapters = structure.get("chapters", [])

        # 視点の多様性
        perspectives = set()
        for chapter in chapters:
            perspectives.add(chapter.get("primary_perspective", ""))
            for shift in chapter.get("perspective_shifts", []):
                perspectives.add(shift.get("shift_to", ""))

        perspective_diversity = len(perspectives) / 5.0  # 最大5つの視点を想定

        # 時間的複雑性
        temporal_complexity = len([c for c in chapters if c.get("perspective_shifts")]) / len(
            chapters
        )

        # 意味的複雑性
        semantic_complexity = np.mean(
            [self._calculate_chapter_semantic_density(chapter) for chapter in chapters]
        )

        return (perspective_diversity + temporal_complexity + semantic_complexity) / 3.0

    def _design_reading_path(self, structure: dict[str, Any]) -> list[dict[str, Any]]:
        """読書経路を設計"""

        chapters = structure.get("chapters", [])
        reading_path = []

        for chapter in chapters:
            path_element = {
                "chapter": chapter["chapter_number"],
                "primary_focus": self._determine_chapter_focus(chapter),
                "reading_instructions": self._create_reading_instructions(chapter),
                "expected_duration": self._estimate_reading_duration(chapter),
            }
            reading_path.append(path_element)

        return reading_path

    def _determine_chapter_focus(self, chapter: dict[str, Any]) -> str:
        """章の焦点を決定"""

        events = chapter.get("events", [])
        if not events:
            return "transitional"

        # 最も強い意味的次元を特定
        domain_strengths = dict.fromkeys(
            ["physical", "emotional", "philosophical", "political", "spiritual", "mythological"],
            0.0,
        )

        for event in events:
            position = event.get("position")
            if position:
                for domain in domain_strengths:
                    domain_strengths[domain] += abs(getattr(position, domain))

        primary_domain = max(domain_strengths.keys(), key=lambda k: domain_strengths[k])

        focus_descriptions = {
            "physical": "行動とアドベンチャー",
            "emotional": "人間関係と感情の展開",
            "philosophical": "価値観と世界観の探求",
            "political": "権力と社会構造",
            "spiritual": "信仰と超自然的要素",
            "mythological": "伝説と古代の謎",
        }

        return focus_descriptions.get(primary_domain, "総合的展開")

    def _create_reading_instructions(self, chapter: dict[str, Any]) -> str:
        """読書指示を作成"""

        focus = self._determine_chapter_focus(chapter)
        has_perspective_shifts = bool(chapter.get("perspective_shifts"))

        if has_perspective_shifts:
            return f"複数視点での{focus}に注意深く読む"
        else:
            return f"{focus}を中心に物語の展開を追う"

    def _estimate_reading_duration(self, chapter: dict[str, Any]) -> str:
        """読書時間を推定"""

        events_count = len(chapter.get("events", []))
        complexity = self._calculate_chapter_semantic_density(chapter)

        if events_count > 4 or complexity > 0.7:
            return "長時間（じっくりと）"
        elif events_count > 2 or complexity > 0.4:
            return "中程度"
        else:
            return "短時間"

    async def control_narrative_speed(self, scene: str, target_speed: NarrativeSpeed) -> str:
        """物語の速度を制御"""

        parameters = self.speed_parameters[target_speed]

        if target_speed in [NarrativeSpeed.VERY_SLOW, NarrativeSpeed.SLOW]:
            return await self._slow_down_scene(scene, parameters)
        elif target_speed in [NarrativeSpeed.FAST, NarrativeSpeed.VERY_FAST]:
            return await self._speed_up_scene(scene, parameters)
        else:
            return scene  # 中程度はそのまま

    async def _slow_down_scene(self, scene: str, parameters: dict[str, float]) -> str:
        """シーンを遅くする"""

        modifications = ["\n【速度調整: 遅い物語速度】"]

        # 詳細な描写を追加
        if parameters["description_ratio"] > 0.4:
            modifications.extend(
                [
                    "- 五感を使った詳細な環境描写",
                    "- 登場人物の微細な表情と仕草",
                    "- 時間の流れを意識した描写",
                ]
            )

        # 内的独白を追加
        if parameters["internal_monologue_ratio"] > 0.2:
            modifications.extend(
                [
                    "- 登場人物の深い内面の探求",
                    "- 過去の記憶との対比",
                    "- 哲学的な思索の挿入",
                ]
            )

        # 象徴的要素を強化
        if parameters["scene_detail_level"] > 0.7:
            modifications.extend(
                ["- 象徴的な細部の強調", "- 隠喩的な表現の使用", "- 重層的な意味の構築"]
            )

        return scene + "\n".join(modifications)

    async def _speed_up_scene(self, scene: str, parameters: dict[str, float]) -> str:
        """シーンを速くする"""

        modifications = ["\n【速度調整: 速い物語速度】"]

        # 簡潔で動的な描写
        modifications.extend(
            [
                "- 行動中心の簡潔な描写",
                "- 短文とリズミカルな展開",
                "- 省略と暗示の活用",
                "- 時間の圧縮と焦点の絞り込み",
            ]
        )

        return scene + "\n".join(modifications)

    async def calculate_total_semantic_distance(self, manuscript: dict[str, str]) -> float:
        """
        原稿全体を分析し、意味的な総移動距離を計算する。

        Args:
            manuscript: 章ごとのテキストを格納した辞書。

        Returns:
            正規化された意味的総移動距離スコア (0.0 - 1.0)。
        """
        if not manuscript:
            return 0.0

        positions = []
        sorted_chapters = sorted(manuscript.keys())

        for chapter_key in sorted_chapters:
            chapter_text = manuscript[chapter_key]
            position = await self._calculate_semantic_position({"description": chapter_text})
            positions.append(position)

        total_distance = sum(
            positions[i].distance_to(positions[i + 1]) for i in range(len(positions) - 1)
        )

        # 正規化: 1章あたりの最大距離を約2.0と仮定して正規化する
        max_possible_distance = len(positions) * 2.0
        return min(1.0, total_distance / max(1.0, max_possible_distance))
