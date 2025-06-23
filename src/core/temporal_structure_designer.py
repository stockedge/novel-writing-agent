"""
時間構造設計システム
複雑な時間構造を設計・実装
"""

import random
from dataclasses import dataclass
from enum import Enum
from typing import Any


class TemporalTechnique(Enum):
    """時間操作技法"""

    IN_MEDIAS_RES = "in_medias_res"
    FRAME_NARRATIVE = "frame_narrative"
    PARALLEL_TIMELINES = "parallel_timelines"
    REVERSE_CHRONOLOGY = "reverse_chronology"
    TIME_LOOPS = "time_loops"
    PROPHETIC_VISIONS = "prophetic_visions"
    NESTED_FLASHBACKS = "nested_flashbacks"
    CONVERGENT_TIMELINES = "convergent_timelines"


@dataclass
class TemporalEvent:
    """時間的イベント"""

    content: str
    chronological_order: int
    narrative_order: int
    timeline_id: str
    event_type: str
    dependencies: list[str]
    reveals: list[str]


@dataclass
class Timeline:
    """時間軸"""

    timeline_id: str
    perspective: str
    events: list[TemporalEvent]
    time_range: tuple[int, int]
    intersection_points: list[int]


class TemporalStructureDesigner:
    """複雑な時間構造を設計"""

    def __init__(self) -> None:
        self.temporal_techniques = {
            TemporalTechnique.IN_MEDIAS_RES: {
                "description": "物語を中間から始める",
                "complexity": 0.3,
                "reader_engagement": 0.8,
                "suitable_for": ["action", "mystery", "thriller"],
            },
            TemporalTechnique.FRAME_NARRATIVE: {
                "description": "額縁物語（物語内物語）",
                "complexity": 0.5,
                "reader_engagement": 0.6,
                "suitable_for": ["epic", "historical", "philosophical"],
            },
            TemporalTechnique.PARALLEL_TIMELINES: {
                "description": "並行する時間軸",
                "complexity": 0.7,
                "reader_engagement": 0.9,
                "suitable_for": ["epic", "multi_character", "complex_plot"],
            },
            TemporalTechnique.REVERSE_CHRONOLOGY: {
                "description": "逆行する時系列",
                "complexity": 0.8,
                "reader_engagement": 0.7,
                "suitable_for": ["mystery", "tragedy", "revelation"],
            },
            TemporalTechnique.TIME_LOOPS: {
                "description": "時間のループ構造",
                "complexity": 0.9,
                "reader_engagement": 0.8,
                "suitable_for": ["fantasy", "philosophical", "character_study"],
            },
            TemporalTechnique.PROPHETIC_VISIONS: {
                "description": "予言的ビジョン",
                "complexity": 0.4,
                "reader_engagement": 0.7,
                "suitable_for": ["fantasy", "epic", "destiny"],
            },
            TemporalTechnique.NESTED_FLASHBACKS: {
                "description": "入れ子状のフラッシュバック",
                "complexity": 0.6,
                "reader_engagement": 0.6,
                "suitable_for": ["character_development", "mystery", "trauma"],
            },
            TemporalTechnique.CONVERGENT_TIMELINES: {
                "description": "収束する複数時間軸",
                "complexity": 0.8,
                "reader_engagement": 0.9,
                "suitable_for": ["epic", "climax", "resolution"],
            },
        }

        # 物語の各段階での推奨技法
        self.stage_recommendations = {
            "opening": [
                TemporalTechnique.IN_MEDIAS_RES,
                TemporalTechnique.PROPHETIC_VISIONS,
            ],
            "development": [
                TemporalTechnique.PARALLEL_TIMELINES,
                TemporalTechnique.NESTED_FLASHBACKS,
            ],
            "climax": [
                TemporalTechnique.CONVERGENT_TIMELINES,
                TemporalTechnique.TIME_LOOPS,
            ],
            "resolution": [
                TemporalTechnique.FRAME_NARRATIVE,
                TemporalTechnique.REVERSE_CHRONOLOGY,
            ],
        }

    async def create_temporal_complexity(self, linear_plot: dict[str, Any]) -> dict[str, Any]:
        """線形プロットを時間的に複雑化"""

        # プロットの分析
        plot_analysis = await self._analyze_linear_plot(linear_plot)

        # 最適な技法の組み合わせを選択
        selected_techniques = await self._select_optimal_techniques(plot_analysis)

        # 物語の開始点を決定
        starting_point = await self._determine_optimal_starting_point(
            linear_plot, selected_techniques
        )

        # 複数時間軸の設計
        timelines = await self._design_multiple_timelines(linear_plot, selected_techniques)

        # フラッシュバック構造の設計
        flashback_structure = await self._design_flashback_structure(linear_plot, timelines)

        # 予言的要素の配置
        prophetic_elements = await self._place_prophetic_elements(linear_plot, selected_techniques)

        # 時間軸の収束点を設計
        convergence_points = await self._design_convergence_points(timelines)

        # 読書経路の最適化
        reading_path = await self._optimize_reading_path(
            timelines, flashback_structure, prophetic_elements, convergence_points
        )

        return {
            "structure_type": [t.value for t in selected_techniques],
            "starting_point": starting_point,
            "timelines": timelines,
            "flashback_structure": flashback_structure,
            "prophetic_elements": prophetic_elements,
            "convergence_points": convergence_points,
            "reading_path": reading_path,
            "complexity_score": self._calculate_temporal_complexity_score(selected_techniques),
            "estimated_reader_engagement": self._estimate_reader_engagement(selected_techniques),
        }

    async def _analyze_linear_plot(self, linear_plot: dict[str, Any]) -> dict[str, Any]:
        """線形プロットを分析"""

        events = linear_plot.get("events", [])
        characters = linear_plot.get("characters", {})

        analysis = {
            "event_count": len(events),
            "character_count": len(characters),
            "plot_complexity": self._assess_plot_complexity(events),
            "emotional_intensity_curve": self._analyze_emotional_curve(events),
            "revelation_points": self._identify_revelation_points(events),
            "character_development_arcs": self._analyze_character_arcs(events, characters),
            "thematic_elements": self._extract_thematic_elements(events),
            "genre_indicators": self._identify_genre_indicators(linear_plot),
        }

        return analysis

    def _assess_plot_complexity(self, events: list[dict[str, Any]]) -> float:
        """プロットの複雑性を評価"""

        # イベントの種類の多様性
        event_types = {event.get("type", "unknown") for event in events}
        type_diversity = len(event_types) / 10.0  # 正規化

        # イベント間の依存関係
        dependencies = 0
        for event in events:
            dependencies += len(event.get("dependencies", []))

        dependency_complexity = min(1.0, dependencies / len(events))

        # 秘密と謎の数
        secrets = sum(1 for event in events if "secret" in event.get("tags", []))
        mystery_factor = min(1.0, secrets / max(1, len(events) * 0.3))

        return (type_diversity + dependency_complexity + mystery_factor) / 3.0

    def _analyze_emotional_curve(self, events: list[dict[str, Any]]) -> list[float]:
        """感情曲線を分析"""

        curve = []
        for event in events:
            emotional_value = event.get("emotional_impact", 0.0)
            curve.append(emotional_value)

        return curve

    def _identify_revelation_points(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """重要な啓示ポイントを特定"""

        revelations = []
        for i, event in enumerate(events):
            if (
                event.get("type") == "revelation"
                or "revelation" in event.get("tags", [])
                or event.get("importance", 0) > 0.7
            ):
                revelations.append(
                    {
                        "position": i,
                        "content": event.get("description", ""),
                        "impact": event.get("emotional_impact", 0.0),
                        "reveals": event.get("reveals", []),
                    }
                )

        return revelations

    def _analyze_character_arcs(
        self, events: list[dict[str, Any]], characters: dict[str, Any]
    ) -> dict[str, list[str]]:
        """キャラクターアークを分析"""

        arcs = {}
        for char_name in characters.keys():
            character_events = [e for e in events if char_name in e.get("characters", [])]
            arc_points = [e.get("description", "") for e in character_events]
            arcs[char_name] = arc_points

        return arcs

    def _extract_thematic_elements(self, events: list[dict[str, Any]]) -> list[str]:
        """テーマ要素を抽出"""

        themes = set()
        for event in events:
            themes.update(event.get("themes", []))

        return list(themes)

    def _identify_genre_indicators(self, linear_plot: dict[str, Any]) -> list[str]:
        """ジャンル指標を特定"""

        indicators = []

        # 設定やイベントからジャンルを推測
        if "magic" in str(linear_plot).lower():
            indicators.append("fantasy")
        if "war" in str(linear_plot).lower():
            indicators.append("epic")
        if "mystery" in str(linear_plot).lower():
            indicators.append("mystery")

        return indicators if indicators else ["general"]

    async def _select_optimal_techniques(
        self, plot_analysis: dict[str, Any]
    ) -> list[TemporalTechnique]:
        """最適な技法の組み合わせを選択"""

        selected_techniques = []

        complexity = plot_analysis["plot_complexity"]
        genre_indicators = plot_analysis["genre_indicators"]
        revelation_count = len(plot_analysis["revelation_points"])

        # 複雑性に基づく基本選択
        if complexity > 0.7:
            selected_techniques.append(TemporalTechnique.PARALLEL_TIMELINES)
            selected_techniques.append(TemporalTechnique.CONVERGENT_TIMELINES)
        elif complexity > 0.5:
            selected_techniques.append(TemporalTechnique.IN_MEDIAS_RES)
            selected_techniques.append(TemporalTechnique.NESTED_FLASHBACKS)
        else:
            selected_techniques.append(TemporalTechnique.IN_MEDIAS_RES)

        # ジャンルに基づく追加選択
        for genre in genre_indicators:
            if genre == "fantasy":
                if TemporalTechnique.PROPHETIC_VISIONS not in selected_techniques:
                    selected_techniques.append(TemporalTechnique.PROPHETIC_VISIONS)
            elif genre == "mystery":
                if TemporalTechnique.REVERSE_CHRONOLOGY not in selected_techniques:
                    selected_techniques.append(TemporalTechnique.REVERSE_CHRONOLOGY)

        # 啓示の数に基づく調整
        if revelation_count > 3:
            if TemporalTechnique.NESTED_FLASHBACKS not in selected_techniques:
                selected_techniques.append(TemporalTechnique.NESTED_FLASHBACKS)

        return selected_techniques[:3]  # 最大3つの技法

    async def _determine_optimal_starting_point(
        self, linear_plot: dict[str, Any], techniques: list[TemporalTechnique]
    ) -> dict[str, Any]:
        """最適な開始点を決定"""

        events = linear_plot.get("events", [])

        if TemporalTechnique.IN_MEDIAS_RES in techniques:
            # 中間点から開始
            mid_point = len(events) // 2
            dramatic_events = [
                i for i, e in enumerate(events) if e.get("emotional_impact", 0) > 0.5
            ]

            if dramatic_events:
                starting_index = min(dramatic_events, key=lambda x: abs(x - mid_point))
            else:
                starting_index = mid_point

            return {
                "technique": "in_medias_res",
                "starting_event_index": starting_index,
                "starting_event": (
                    events[starting_index] if starting_index < len(events) else events[0]
                ),
                "justification": "劇的な中間点からの開始で読者の関心を即座に引く",
            }

        elif TemporalTechnique.FRAME_NARRATIVE in techniques:
            # 枠物語として最後から開始
            return {
                "technique": "frame_narrative",
                "starting_event_index": len(events) - 1,
                "frame_narrator": "未来の語り手",
                "justification": "物語全体を回想として語る構造",
            }

        else:
            # 通常の開始
            return {
                "technique": "chronological",
                "starting_event_index": 0,
                "justification": "時系列順の自然な開始",
            }

    async def _design_multiple_timelines(
        self, linear_plot: dict[str, Any], techniques: list[TemporalTechnique]
    ) -> list[Timeline]:
        """複数時間軸を設計"""

        timelines = []
        events = linear_plot.get("events", [])
        characters = linear_plot.get("characters", {})

        # メイン時間軸
        main_timeline = Timeline(
            timeline_id="main",
            perspective="主人公",
            events=[self._convert_to_temporal_event(e, i, "main") for i, e in enumerate(events)],
            time_range=(0, len(events)),
            intersection_points=[],
        )
        timelines.append(main_timeline)

        # 並行時間軸の作成
        if TemporalTechnique.PARALLEL_TIMELINES in techniques:
            # 敵対者の時間軸
            antagonist_events = await self._create_antagonist_timeline(events, characters)
            antagonist_timeline = Timeline(
                timeline_id="antagonist",
                perspective="敵対者",
                events=antagonist_events,
                time_range=(0, len(events)),
                intersection_points=[len(events) // 3, 2 * len(events) // 3],
            )
            timelines.append(antagonist_timeline)

            # 支援者の時間軸
            if len(characters) > 2:
                supporter_events = await self._create_supporter_timeline(events, characters)
                supporter_timeline = Timeline(
                    timeline_id="supporter",
                    perspective="重要な支援者",
                    events=supporter_events,
                    time_range=(len(events) // 4, 3 * len(events) // 4),
                    intersection_points=[len(events) // 2],
                )
                timelines.append(supporter_timeline)

        return timelines

    def _convert_to_temporal_event(
        self, event: dict[str, Any], index: int, timeline_id: str
    ) -> TemporalEvent:
        """通常のイベントを時間的イベントに変換"""

        return TemporalEvent(
            content=event.get("description", ""),
            chronological_order=index,
            narrative_order=index,  # 後で調整
            timeline_id=timeline_id,
            event_type=event.get("type", "action"),
            dependencies=event.get("dependencies", []),
            reveals=event.get("reveals", []),
        )

    async def _create_antagonist_timeline(
        self, main_events: list[dict[str, Any]], characters: dict[str, Any]
    ) -> list[TemporalEvent]:
        """敵対者の時間軸を作成"""

        antagonist_events = []

        for i, main_event in enumerate(main_events):
            # 主人公の行動に対する敵対者の反応
            antagonist_event = TemporalEvent(
                content=f"敵対者の視点: {main_event.get('description', '')}への対応",
                chronological_order=i,
                narrative_order=i,
                timeline_id="antagonist",
                event_type="reaction",
                dependencies=[f"main_event_{i}"],
                reveals=[f"antagonist_motivation_{i}"],
            )
            antagonist_events.append(antagonist_event)

        # 独自の計画イベントを追加
        unique_events = [
            TemporalEvent(
                content="敵対者独自の計画の進行",
                chronological_order=len(main_events) // 3,
                narrative_order=len(main_events) // 3,
                timeline_id="antagonist",
                event_type="plot_advancement",
                dependencies=[],
                reveals=["hidden_agenda"],
            ),
            TemporalEvent(
                content="最終段階の準備",
                chronological_order=2 * len(main_events) // 3,
                narrative_order=2 * len(main_events) // 3,
                timeline_id="antagonist",
                event_type="preparation",
                dependencies=["hidden_agenda"],
                reveals=["final_plan"],
            ),
        ]

        antagonist_events.extend(unique_events)
        return antagonist_events

    async def _create_supporter_timeline(
        self, main_events: list[dict[str, Any]], characters: dict[str, Any]
    ) -> list[TemporalEvent]:
        """支援者の時間軸を作成"""

        supporter_events = []

        # 主人公への支援活動
        support_points = [
            len(main_events) // 4,
            len(main_events) // 2,
            3 * len(main_events) // 4,
        ]

        for i, point in enumerate(support_points):
            supporter_event = TemporalEvent(
                content=f"支援者の援助活動 {i + 1}",
                chronological_order=point,
                narrative_order=point,
                timeline_id="supporter",
                event_type="support",
                dependencies=[f"main_event_{point}"],
                reveals=[f"hidden_alliance_{i}"],
            )
            supporter_events.append(supporter_event)

        return supporter_events

    async def _design_flashback_structure(
        self, linear_plot: dict[str, Any], timelines: list[Timeline]
    ) -> dict[str, Any]:
        """フラッシュバック構造を設計"""

        events = linear_plot.get("events", [])
        revelation_points = self._identify_revelation_points(events)

        flashback_structure = {
            "primary_flashbacks": [],
            "nested_flashbacks": [],
            "flashback_triggers": [],
            "temporal_anchors": [],
        }

        # 主要なフラッシュバック
        for revelation in revelation_points:
            flashback = {
                "trigger_position": revelation["position"],
                "target_past_position": max(0, revelation["position"] - random.randint(3, 8)),
                "content_focus": revelation["reveals"],
                "emotional_purpose": "現在の状況への理解を深める",
                "duration": "medium",
                "perspective": "主人公の記憶",
            }
            flashback_structure["primary_flashbacks"].append(flashback)

        # 入れ子フラッシュバック
        if len(revelation_points) > 2:
            nested_flashback = {
                "outer_flashback": flashback_structure["primary_flashbacks"][0],
                "inner_flashback": {
                    "target_position": 0,
                    "content_focus": ["origin_story", "character_motivation"],
                    "emotional_purpose": "根本的な動機の説明",
                },
            }
            flashback_structure["nested_flashbacks"].append(nested_flashback)

        return flashback_structure

    async def _place_prophetic_elements(
        self, linear_plot: dict[str, Any], techniques: list[TemporalTechnique]
    ) -> list[dict[str, Any]]:
        """予言的要素を配置"""

        prophetic_elements = []

        if TemporalTechnique.PROPHETIC_VISIONS in techniques:
            events = linear_plot.get("events", [])

            # 序盤の予言
            early_prophecy = {
                "position": 1,
                "type": "prophetic_dream",
                "content": "主人公の運命についての暗示的なビジョン",
                "fulfillment_positions": [len(events) // 2, len(events) - 2],
                "ambiguity_level": 0.7,
                "symbolic_elements": ["光と闇の対比", "失われた王冠", "血に染まった剣"],
            }
            prophetic_elements.append(early_prophecy)

            # 中盤の啓示
            mid_prophecy = {
                "position": len(events) // 2,
                "type": "oracle_revelation",
                "content": "真の敵と最終的な犠牲についての予言",
                "fulfillment_positions": [len(events) - 1],
                "ambiguity_level": 0.5,
                "symbolic_elements": ["二つの道", "火の試練", "最後の選択"],
            }
            prophetic_elements.append(mid_prophecy)

        return prophetic_elements

    async def _design_convergence_points(self, timelines: list[Timeline]) -> list[dict[str, Any]]:
        """時間軸の収束点を設計"""

        convergence_points = []

        if len(timelines) > 1:
            # 中間収束点
            mid_convergence = {
                "position": "middle",
                "involved_timelines": [t.timeline_id for t in timelines],
                "convergence_type": "revelation_sharing",
                "narrative_impact": "複数の視点が一つの真実を明かす",
                "emotional_intensity": 0.7,
            }
            convergence_points.append(mid_convergence)

            # 最終収束点
            final_convergence = {
                "position": "climax",
                "involved_timelines": [t.timeline_id for t in timelines],
                "convergence_type": "unified_action",
                "narrative_impact": "全ての筋が一つのクライマックスに集約",
                "emotional_intensity": 0.9,
            }
            convergence_points.append(final_convergence)

        return convergence_points

    async def _optimize_reading_path(
        self,
        timelines: list[Timeline],
        flashback_structure: dict[str, Any],
        prophetic_elements: list[dict[str, Any]],
        convergence_points: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """読書経路を最適化"""

        reading_path = []

        # 基本的な章構成
        main_timeline = next((t for t in timelines if t.timeline_id == "main"), timelines[0])
        total_events = len(main_timeline.events)

        for i in range(0, total_events, 3):  # 3イベントごとに章を構成
            chapter = {
                "chapter_number": i // 3 + 1,
                "primary_timeline": "main",
                "events_range": (i, min(i + 3, total_events)),
                "perspective_shifts": [],
                "flashbacks": [],
                "prophetic_elements": [],
                "special_techniques": [],
            }

            # 視点の切り替え
            for timeline in timelines[1:]:  # メイン以外
                if i in timeline.intersection_points:
                    chapter["perspective_shifts"].append(
                        {
                            "shift_to": timeline.perspective,
                            "timeline_id": timeline.timeline_id,
                            "events": [e for e in timeline.events if e.chronological_order == i],
                        }
                    )

            # フラッシュバックの挿入
            for flashback in flashback_structure.get("primary_flashbacks", []):
                if flashback["trigger_position"] in range(i, min(i + 3, total_events)):
                    chapter["flashbacks"].append(flashback)

            # 予言的要素の挿入
            for prophecy in prophetic_elements:
                if prophecy["position"] in range(i, min(i + 3, total_events)):
                    chapter["prophetic_elements"].append(prophecy)

            reading_path.append(chapter)

        return reading_path

    def _calculate_temporal_complexity_score(self, techniques: list[TemporalTechnique]) -> float:
        """時間的複雑性スコアを計算"""

        total_complexity = sum(
            self.temporal_techniques[technique]["complexity"] for technique in techniques
        )

        # 技法の組み合わせボーナス
        combination_bonus = len(techniques) * 0.1

        return min(1.0, (total_complexity / len(techniques)) + combination_bonus)

    def _estimate_reader_engagement(self, techniques: list[TemporalTechnique]) -> float:
        """読者エンゲージメントを推定"""

        total_engagement = sum(
            self.temporal_techniques[technique]["reader_engagement"] for technique in techniques
        )

        return total_engagement / len(techniques) if techniques else 0.5
