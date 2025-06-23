"""
計算論的最適化ファンタジーエンジン
全コンポーネントを統合した最終実行エンジン
"""

from typing import Any, TypedDict

import numpy as np
from langchain_core.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field

from ..core.computational_narratology import ComputationalNarratologyEngine
from ..core.emotional_valence_tracker import EmotionalValenceTracker
from ..core.reversal_scene_generator import ReversalSceneGenerator
from ..core.semantic_pacing_controller import SemanticPacingController
from ..core.temporal_structure_designer import TemporalStructureDesigner


# --- Pydantic Models for Structured Output ---
class WorldFoundations(BaseModel):
    name: str = Field(description="物語の舞台となる世界や帝国の名前")
    magic_system: str = Field(description="物語の中心となるユニークな魔法体系")
    primary_races: list[str] = Field(description="主要な登場種族のリスト（3種族）")
    central_conflict: str = Field(description="物語の中心となる対立構造")

class CharacterProfile(BaseModel):
    role: str = Field(description="物語における役割 (e.g., protagonist, mentor, antagonist)")
    arc: str = Field(description="そのキャラクターが経験する変化や成長の物語")
    powers: list[str] = Field(description="持つ能力や特技のリスト")
    fatal_flaw: str | None = Field(description="キャラクターの致命的な欠点や弱点", default=None)
    hidden_agenda: str | None = Field(description="隠された目的や動機", default=None)

class PlotEvent(BaseModel):
    description: str = Field(description="そのイベントで何が起こるかの短い説明")
    type: str = Field(
        description="イベントの種類 (e.g., setup, inciting_incident, betrayal, climax, resolution)"
    )
    emotional_impact: float = Field(
        description="このイベントが読者に与える感情価の初期推定値 (-1.0から1.0)"
    )

class NovelFoundation(BaseModel):
    world: WorldFoundations
    characters: dict[str, CharacterProfile]
    basic_plot: list[PlotEvent] = Field(description="物語の骨子となる12個のイベントリスト")

# --- State Definition for LangGraph ---
class NovelGenerationState(TypedDict):
    """小説生成プロセスの状態を管理"""
    initial_concept: dict[str, Any]
    world: dict[str, Any]
    characters: dict[str, Any]
    basic_plot: dict[str, Any]
    optimized_plot: dict[str, Any]
    reversal_map: dict[str, Any]
    nonlinear_structure: dict[str, Any]
    manuscript: dict[str, str]
    narrative_metrics: dict[str, Any]
    final_result: dict[str, Any]


class ComputationallyOptimizedFantasyEngine:
    """計算論的物語論を統合したハイファンタジー執筆エンジン (LangGraph版)"""

    def __init__(self) -> None:
        # --- LLM and Core Components Initialization ---
        # Groq API を使用（超高速推論）
        # Qwen3-32B モデルを使用（多言語対応、高品質創作）
        self.llm = ChatGroq(model="qwen/qwen3-32b", temperature=0.8)
        self.components = {
            "narratology": ComputationalNarratologyEngine(),
            "valence_tracker": EmotionalValenceTracker(),
            "reversal_generator": ReversalSceneGenerator(llm=self.llm),
            "pacing_controller": SemanticPacingController(),
            "temporal_designer": TemporalStructureDesigner(),
        }

        # --- Graph Definition ---
        workflow = StateGraph(NovelGenerationState)
        workflow.add_node("create_foundation", self._create_foundation_node)
        workflow.add_node("optimize_plot_structure", self._optimize_plot_structure_node)
        workflow.add_node("design_reversal_map", self._design_reversal_map_node)
        workflow.add_node("create_nonlinear_structure", self._create_nonlinear_structure_node)
        workflow.add_node("write_manuscript", self._write_optimized_manuscript_node)
        workflow.add_node("verify_metrics", self._verify_success_metrics_node)
        workflow.add_node("finalize_novel", self._finalize_node)

        # --- Graph Flow ---
        workflow.set_entry_point("create_foundation")
        workflow.add_edge("create_foundation", "optimize_plot_structure")
        workflow.add_edge("optimize_plot_structure", "design_reversal_map")
        workflow.add_edge("design_reversal_map", "create_nonlinear_structure")
        workflow.add_edge("create_nonlinear_structure", "write_manuscript")
        workflow.add_edge("write_manuscript", "verify_metrics")
        workflow.add_edge("verify_metrics", "finalize_novel")
        workflow.add_edge("finalize_novel", END)

        self.graph = workflow.compile()

    # --- Node Implementations ---
    async def _create_foundation_node(self, state: NovelGenerationState) -> dict[str, Any]:
        """LLMを使用して物語の基礎（世界、キャラ、プロット）を動的に生成する"""
        print("1. 基礎世界構築中 (Gemini Pro)...")
        initial_concept = state["initial_concept"]

        parser = PydanticOutputParser(pydantic_object=NovelFoundation)

        prompt = f"""
        あなたは世界的に有名なファンタジー作家であり、独創的な世界観構築の専門家です。
        以下の初期コンセプトに基づき、壮大なファンタジー小説の土台となる「世界設定」「主要登場人物」「物語の基本プロット」を考案してください。

        ### 初期コンセプト
        - テーマ: {initial_concept.get("theme")}
        - 主人公: {initial_concept.get("protagonist", {}).get("name", "アルテミス・ヴェルダンディ")}
        - 物語のアーク: {initial_concept.get("protagonist", {}).get("arc", "傲慢な支配者から謙虚な求道者へ")}
        - 物語の核心となる転換: {initial_concept.get("core_reversals", [])}

        ### 指示
        - 主人公を含む、魅力的で対照的な3人の主要キャラクターを設計してください。
        - 物語の骨子となる、起承転結を意識した12個のイベントから成るプロットを作成してください。
        - 全ての要素は、与えられた初期コンセプトとテーマに沿った、一貫性のあるものにしてください。

        以下のJSONスキーマに従って、結果を厳密に出力してください。
        {parser.get_format_instructions()}
        """

        chain = self.llm | parser
        foundation = await chain.ainvoke(prompt)

        # Pydanticモデルを辞書に変換してstateに格納
        return {
            "world": foundation.world.dict(),
            "characters": {name: profile.dict() for name, profile in foundation.characters.items()},
            "basic_plot": {"events": [event.dict() for event in foundation.basic_plot]},
        }

    def _optimize_plot_structure_node(self, state: NovelGenerationState) -> dict[str, Any]:
        print("2. プロット構造を最適化中...")
        basic_plot = state["basic_plot"]

        events = basic_plot["events"]
        emotional_sequence = [e["emotional_impact"] for e in events]
        narratology_engine = self.components["narratology"]
        optimized_sequence = narratology_engine.optimize_reversal_sequence(  # type: ignore
            emotional_sequence
        )

        for event, reversal in zip(events, optimized_sequence, strict=False):
            event["optimized_emotional_impact"] = reversal.target_state
            event["reversal_info"] = {
                "type": reversal.type.value,
                "intensity": reversal.intensity,
                "function": reversal.narrative_function,
            }

        optimized_plot = {
            "events": events,
            "optimized_reversals": optimized_sequence,
            "emotional_profile": [r.target_state for r in optimized_sequence],
        }
        return {"optimized_plot": optimized_plot}

    def _design_reversal_map_node(self, state: NovelGenerationState) -> dict[str, Any]:
        print("3. 感情的転換点を設計中...")
        optimized_plot = state["optimized_plot"]
        reversals = optimized_plot["optimized_reversals"]

        reversal_map: dict[str, Any] = {"chapter_reversals": {}}
        for i, reversal in enumerate(reversals):
            chapter_num = (i // 3) + 1
            if f"chapter_{chapter_num}" not in reversal_map["chapter_reversals"]:
                reversal_map["chapter_reversals"][f"chapter_{chapter_num}"] = []

            reversal_info = {
                "reversal": reversal,
                "context": {
                    "current_situation": optimized_plot["events"][i]["description"],
                    "characters": list(state["characters"].keys()),
                    "location": "帝国各地",
                    "stakes": "個人から世界へ段階的拡大",
                },
            }
            reversal_map["chapter_reversals"][f"chapter_{chapter_num}"].append(reversal_info)

        return {"reversal_map": reversal_map}

    def _create_nonlinear_structure_node(self, state: NovelGenerationState) -> dict[str, Any]:
        print("4. 非線形物語構造を構築中...")
        # このデモでは簡略化し、章の数をプロットから決定する
        num_chapters = (len(state["optimized_plot"]["events"]) + 2) // 3
        return {
            "nonlinear_structure": {
                "reading_path": [{"chapter_number": i} for i in range(1, num_chapters + 1)]
            }
        }

    async def _write_optimized_manuscript_node(self, state: NovelGenerationState) -> dict[str, Any]:
        print("5. 最適化アルゴリズムで執筆中...")
        manuscript: dict[str, str] = {}
        for chapter_info in state["nonlinear_structure"]["reading_path"]:
            chapter_num = chapter_info["chapter_number"]
            print(f"  第{chapter_num}章を執筆中...")
            chapter_reversals = (
                state["reversal_map"].get("chapter_reversals", {}).get(f"chapter_{chapter_num}", [])
            )

            # Use LLM to generate chapter content
            reversal_functions = (
                [info["reversal"].narrative_function for info in chapter_reversals]
                if chapter_reversals
                else ["物語の進行"]
            )

            # 前の章のあらすじを安全に取得
            previous_summary = ""
            if manuscript:
                all_content = "...".join(list(manuscript.values()))
                previous_summary = f"前の章までの簡単なあらすじ: {all_content[-500:]}"
            else:
                previous_summary = "これは物語の最初の章です。"

            prompt = f"""
            あなたは世界的に有名なファンタジー作家です。以下の設定に基づき、壮大な物語の第{chapter_num}章を執筆してください。

            ### 世界観
            {state["world"]}

            ### 主要登場人物
            {state["characters"]}

            ### 物語全体のプロット概要
            {[event["description"] for event in state["optimized_plot"]["events"]]}

            ### この章で描くべきこと
            - {", ".join(reversal_functions)}
            - {previous_summary}

            ### 執筆指示
            - 具体的で、感情豊かで、読者を引き込むような文章でお願いします。
            - これは物語の重要な転換点です。劇的で記憶に残るシーンにしてください。
            - 章の終わりには、読者が次を読みたくなるような「引き」を作ってください。
            """
            response = await self.llm.ainvoke(prompt)
            manuscript[f"chapter_{chapter_num}"] = str(response.content)
        return {"manuscript": manuscript}

    async def _verify_success_metrics_node(self, state: NovelGenerationState) -> dict[str, Any]:
        """生成された原稿を分析し、成功指標を動的に検証する"""
        print("6. 成功指標を検証中 (動的分析)...")
        manuscript = state["manuscript"]
        if not manuscript:
            return {"narrative_metrics": {}}

        valence_tracker = self.components["valence_tracker"]
        pacing_controller = self.components["pacing_controller"]
        narratology_engine = self.components["narratology"]

        # 1. 感情価の分析
        all_valences = []
        for chapter_num, content in sorted(manuscript.items()):
            valence = await valence_tracker.analyze_scene_valence(  # type: ignore
                content, int(chapter_num.split("_")[1])
            )
            all_valences.append(valence)

        # 2. 転換指標の計算
        reversal_intensities = [
            abs(all_valences[i] - all_valences[i - 1]) for i in range(1, len(all_valences))
        ]
        significant_reversals = [intensity for intensity in reversal_intensities if intensity > 0.6]

        # 3. 意味的距離の計算
        semantic_distance = await pacing_controller.calculate_total_semantic_distance(manuscript)  # type: ignore

        # 4. メトリクスの集計
        metrics = {
            "reversal_frequency": len(significant_reversals) / max(1, len(manuscript)),
            "average_reversal_intensity": np.mean(significant_reversals)
            if significant_reversals
            else 0.0,
            "emotional_variance": np.var(all_valences) if all_valences else 0.0,
            "semantic_distance": semantic_distance,
            "narrative_speed": "slow",  # このデモでは固定
            "valence_history": all_valences,  # 可視化用
        }

        # 5. 最終的な成功スコアの計算
        metrics["success_score"] = narratology_engine.calculate_narrative_success_probability(  # type: ignore
            metrics
        )
        return {"narrative_metrics": metrics}

    def _finalize_node(self, state: NovelGenerationState) -> dict[str, Any]:
        print("7. 最終成果物を生成中...")
        title = "失われし皇帝の王冠 - ヴェルダンディア皇帝記"  # LLMで生成も可能
        final_result = {
            "title": title,
            "manuscript": state["manuscript"],
            "world_bible": {
                "world_setting": state["world"],
                "character_profiles": state["characters"],
            },
            "narrative_metrics": state["narrative_metrics"],
            "reversal_analysis": state["reversal_map"],
            "semantic_journey": state["nonlinear_structure"],
            "generation_metadata": {
                "final_quality_score": state["narrative_metrics"]["success_score"]
            },
        }
        return {"final_result": final_result}

    async def create_optimized_fantasy_novel(
        self, initial_concept: dict[str, Any]
    ) -> dict[str, Any]:
        """計算論的に最適化されたファンタジー小説を生成"""
        print("🔬 計算論的最適化プロセスを開始...")

        initial_state: NovelGenerationState = {"initial_concept": initial_concept}  # type: ignore
        final_state = await self.graph.ainvoke(initial_state)

        return final_state.get("final_result", {})  # type: ignore
