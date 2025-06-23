"""
転換シーン自動生成システム
感情的転換を含むシーンを自動生成
"""

import random
from dataclasses import dataclass
from enum import Enum
from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel


class SceneType(Enum):
    """シーンタイプ"""

    DIALOGUE_HEAVY = "dialogue_heavy"
    ACTION_SEQUENCE = "action_sequence"
    INTERNAL_MONOLOGUE = "internal_monologue"
    DESCRIPTIVE_SCENE = "descriptive_scene"
    REVELATION_SCENE = "revelation_scene"


@dataclass
class SceneTemplate:
    """シーンテンプレート"""

    setup: str
    turning_point: str
    aftermath: str
    emotional_beats: list[str]
    required_elements: list[str]


class ReversalSceneGenerator:
    """感情的転換を含むシーンを自動生成"""

    def __init__(self, llm: BaseChatModel | None = None):
        self.scene_templates = {
            "classic_peripeteia": SceneTemplate(
                setup="勝利の祝宴、権力の頂点、栄光の瞬間",
                turning_point="隠された真実の発覚、致命的な過ちの露見、信頼する者の裏切り",
                aftermath="全ての崩壊、失墜、孤立無援",
                emotional_beats=["高揚", "困惑", "理解", "絶望", "受容"],
                required_elements=[
                    "権力の象徴",
                    "信頼関係",
                    "隠された真実",
                    "破滅の予兆",
                ],
            ),
            "false_defeat": SceneTemplate(
                setup="絶望的な包囲、最後の抵抗、全てが失われた状況",
                turning_point="予期せぬ援軍、隠された力の覚醒、奇跡的な発見",
                aftermath="形勢逆転、新たな希望、力の再編",
                emotional_beats=["絶望", "諦め", "微かな光", "驚愕", "歓喜"],
                required_elements=[
                    "圧倒的劣勢",
                    "隠された同盟者",
                    "力の源",
                    "逆転の契機",
                ],
            ),
            "betrayal_cascade": SceneTemplate(
                setup="信頼関係の確認、絆の深まり、安心感",
                turning_point="第一の裏切り、さらなる背信、連鎖的な崩壊",
                aftermath="完全な孤立、信頼の喪失、世界観の転覆",
                emotional_beats=["信頼", "疑念", "衝撃", "怒り", "虚無"],
                required_elements=[
                    "重要な人間関係",
                    "秘密の動機",
                    "連鎖反応",
                    "最後の砦",
                ],
            ),
            "pyrrhic_victory": SceneTemplate(
                setup="最終決戦、勝利への道筋、目標の達成",
                turning_point="勝利の代償の発覚、失ったものの大きさ、空虚な達成",
                aftermath="勝利の空しさ、代償への直面、新たな責任",
                emotional_beats=["決意", "奮闘", "勝利", "代償の理解", "空虚"],
                required_elements=["重大な目標", "犠牲", "勝利の瞬間", "代償の重さ"],
            ),
            "recognition_scene": SceneTemplate(
                setup="謎の状況、断片的な情報、混乱した現実",
                turning_point="真実の開示、認識の転換、現実の再構築",
                aftermath="新たな理解、世界観の変化、使命の明確化",
                emotional_beats=["困惑", "探求", "発見", "驚愕", "受容"],
                required_elements=["隠された真実", "証拠", "証人", "転換点"],
            ),
        }

        # 感情的転換の技法
        self.reversal_techniques = {
            "dramatic_irony": "読者は知っているが登場人物は知らない情報の活用",
            "misdirection": "読者の注意を別の場所に向けて真実を隠す",
            "red_herring": "偽の手がかりで読者を誤導",
            "revelation": "隠されていた重要な情報の開示",
            "role_reversal": "敵と味方、強者と弱者の立場の逆転",
            "temporal_shift": "時間の非線形性を活用した驚き",
        }

        # ハイファンタジー特有の要素
        self.fantasy_elements = {
            "magic_system": ["古代魔法", "禁じられた呪文", "魔法の代償", "魔力の源"],
            "mythical_beings": ["ドラゴン", "不死者", "精霊", "古き神々"],
            "artifacts": ["伝説の剣", "禁断の書", "預言の石", "封印の鍵"],
            "prophecies": ["古い予言", "神託", "運命の糸", "星の導き"],
            "realms": ["異次元", "精霊界", "死者の国", "時の狭間"],
        }

        self.llm = llm

    async def generate_reversal_scene(
        self, context: dict[str, Any], reversal_spec: dict[str, Any]
    ) -> str:
        """指定された転換を含むシーンを生成"""

        # テンプレートの選択
        template = self._select_scene_template(reversal_spec["reversal_type"])

        # ファンタジー要素の選択
        fantasy_elements = self._select_fantasy_elements(context, reversal_spec)

        # シーンの詳細設計
        scene_design = await self._design_scene_structure(
            template, context, reversal_spec, fantasy_elements
        )

        # 実際のシーン生成
        scene_text = await self._generate_scene_text(scene_design)

        # 感情的転換の強度チェック
        if not await self._verify_reversal_intensity(scene_text, reversal_spec):
            scene_text = await self._intensify_reversal(scene_text, reversal_spec)

        return scene_text

    def _select_scene_template(self, reversal_type: str) -> SceneTemplate:
        """転換タイプに応じたテンプレートを選択"""

        return self.scene_templates.get(reversal_type, self.scene_templates["classic_peripeteia"])

    def _select_fantasy_elements(
        self, context: dict[str, Any], reversal_spec: dict[str, Any]
    ) -> dict[str, list[str]]:
        """シーンに適したファンタジー要素を選択"""

        selected_elements = {}

        # 転換の強度に応じて要素の数を決定
        intensity = reversal_spec.get("intensity", 0.5)
        num_elements = 2 if intensity > 0.8 else 1

        for category, elements in self.fantasy_elements.items():
            selected_elements[category] = random.sample(elements, min(num_elements, len(elements)))

        return selected_elements

    async def _design_scene_structure(
        self,
        template: SceneTemplate,
        context: dict[str, Any],
        reversal_spec: dict[str, Any],
        fantasy_elements: dict[str, list[str]],
    ) -> dict[str, Any]:
        """シーンの詳細構造を設計"""

        return {
            "template": template,
            "context": context,
            "reversal_spec": reversal_spec,
            "fantasy_elements": fantasy_elements,
            "scene_beats": self._create_scene_beats(template, reversal_spec),
            "character_arcs": self._design_character_arcs(context, reversal_spec),
            "setting_details": self._design_setting(context, fantasy_elements),
            "dialogue_prompts": self._create_dialogue_prompts(template, context),
            "sensory_details": self._design_sensory_elements(reversal_spec),
        }

    def _create_scene_beats(
        self, template: SceneTemplate, reversal_spec: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """シーンビートを作成"""

        beats = []
        emotional_arc = reversal_spec.get("emotional_arc", template.emotional_beats)

        for i, (beat_emotion, template_beat) in enumerate(
            zip(emotional_arc, template.emotional_beats, strict=False)
        ):
            beat = {
                "sequence": i + 1,
                "emotion": template_beat,
                "target_valence": (beat_emotion if isinstance(beat_emotion, float) else 0.0),
                "narrative_function": self._determine_beat_function(i, len(emotional_arc)),
                "techniques": self._select_techniques_for_beat(i, reversal_spec),
            }
            beats.append(beat)

        return beats

    def _determine_beat_function(self, position: int, total_beats: int) -> str:
        """ビートの物語的機能を決定"""

        if position == 0:
            return "状況設定・感情的基盤の確立"
        elif position < total_beats // 2:
            return "緊張の構築・転換への準備"
        elif position == total_beats // 2:
            return "転換点・クライマックス"
        elif position < total_beats - 1:
            return "余波の展開・新状況の理解"
        else:
            return "新しい平衡・次への準備"

    def _select_techniques_for_beat(
        self, position: int, reversal_spec: dict[str, Any]
    ) -> list[str]:
        """ビートに適した技法を選択"""

        reversal_type = reversal_spec.get("reversal_type", "classic_peripeteia")
        techniques = []

        if position == 0:  # 設定ビート
            techniques.append("dramatic_irony")
        elif position == len(reversal_spec.get("emotional_arc", [])) // 2:  # 転換点
            if reversal_type == "classic_peripeteia":
                techniques.extend(["revelation", "role_reversal"])
            elif reversal_type == "false_defeat":
                techniques.extend(["misdirection", "revelation"])
            elif reversal_type == "betrayal_cascade":
                techniques.extend(["revelation", "dramatic_irony"])

        return techniques

    def _design_character_arcs(
        self, context: dict[str, Any], reversal_spec: dict[str, Any]
    ) -> dict[str, dict[str, str]]:
        """キャラクターアークを設計"""

        characters = context.get("characters", [])
        arcs = {}

        # charactersがリストの場合の処理
        if isinstance(characters, list):
            for char_name in characters:
                char_info = {"role": "supporter", "current_emotion": "中立"}
                arcs[char_name] = {
                    "initial_state": char_info.get("current_emotion", "中立"),
                    "arc_type": self._determine_character_arc_type(char_info, reversal_spec),
                    "final_state": self._calculate_final_emotional_state(char_info, reversal_spec),
                    "key_moments": self._identify_character_key_moments(char_info, reversal_spec),
                }
        # charactersが辞書の場合の処理
        elif isinstance(characters, dict):
            for char_name, char_info in characters.items():
                arcs[char_name] = {
                    "initial_state": char_info.get("current_emotion", "中立"),
                    "arc_type": self._determine_character_arc_type(char_info, reversal_spec),
                    "final_state": self._calculate_final_emotional_state(char_info, reversal_spec),
                    "key_moments": self._identify_character_key_moments(char_info, reversal_spec),
                }

        return arcs

    def _determine_character_arc_type(
        self, char_info: dict[str, Any], reversal_spec: dict[str, Any]
    ) -> str:
        """キャラクターのアークタイプを決定"""

        role = char_info.get("role", "supporter")
        reversal_type = reversal_spec.get("reversal_type", "classic_peripeteia")

        if role == "protagonist":
            if reversal_type == "classic_peripeteia":
                return "英雄の転落"
            elif reversal_type == "false_defeat":
                return "絶望からの復活"
            elif reversal_type == "recognition_scene":
                return "真実への覚醒"
        elif role == "antagonist":
            return "敵の一時的勝利" if reversal_type == "classic_peripeteia" else "敵の敗北"
        else:
            return "立場の変化"

    def _calculate_final_emotional_state(
        self, char_info: dict[str, Any], reversal_spec: dict[str, Any]
    ) -> str:
        """最終感情状態を計算"""

        target_valence = reversal_spec.get("target_state", 0.0)

        if target_valence > 0.5:
            return "希望・決意"
        elif target_valence < -0.5:
            return "絶望・怒り"
        else:
            return "混乱・探求"

    def _identify_character_key_moments(
        self, char_info: dict[str, Any], reversal_spec: dict[str, Any]
    ) -> list[str]:
        """キャラクターの重要な瞬間を特定"""

        moments = []
        reversal_type = reversal_spec.get("reversal_type", "classic_peripeteia")

        if reversal_type == "betrayal_cascade":
            moments.extend(["裏切りの発覚", "信頼の崩壊", "孤立の受容"])
        elif reversal_type == "false_defeat":
            moments.extend(["最後の抵抗", "援軍の到着", "希望の復活"])
        elif reversal_type == "recognition_scene":
            moments.extend(["疑問の浮上", "証拠の発見", "真実の受容"])

        return moments

    def _design_setting(
        self, context: dict[str, Any], fantasy_elements: dict[str, list[str]]
    ) -> dict[str, str]:
        """設定の詳細を設計"""

        setting = {
            "location": context.get("location", "王宮の大広間"),
            "atmosphere": self._determine_atmosphere(context),
            "magical_elements": ", ".join(fantasy_elements.get("magic_system", [])),
            "symbolic_objects": ", ".join(fantasy_elements.get("artifacts", [])),
            "environmental_mood": self._create_environmental_mood(context),
        }

        return setting

    def _determine_atmosphere(self, context: dict[str, Any]) -> str:
        """雰囲気を決定"""

        time_of_day = context.get("time", "夜")
        weather = context.get("weather", "嵐")

        atmospheres = {
            ("朝", "晴れ"): "希望に満ちた明るさ",
            ("夜", "嵐"): "不吉な予感と緊張",
            ("夕暮れ", "曇り"): "憂鬱で不安定",
            ("深夜", "霧"): "神秘的で不気味",
        }

        return atmospheres.get((time_of_day, weather), "緊張感のある静寂")

    def _create_environmental_mood(self, context: dict[str, Any]) -> str:
        """環境的ムードを作成"""

        mood_elements = [
            "風の音が不吉な予感を運ぶ",
            "影が長く伸びて真実を隠す",
            "光と闇が入り混じり運命を暗示する",
            "古い建物が過去の罪を証言する",
        ]

        return random.choice(mood_elements)

    def _create_dialogue_prompts(
        self, template: SceneTemplate, context: dict[str, Any]
    ) -> list[str]:
        """対話プロンプトを作成"""

        prompts = []
        characters = context.get("characters", [])

        # charactersがリストの場合
        if isinstance(characters, list):
            char_names = characters
        # charactersが辞書の場合
        elif isinstance(characters, dict):
            char_names = list(characters.keys())
        else:
            char_names = []

        for char_name in char_names:
            prompts.extend(
                [
                    f"{char_name}の内心の動揺を表現する独白",
                    f"{char_name}が真実に直面する瞬間の言葉",
                    f"{char_name}の価値観が揺らぐ瞬間の表現",
                ]
            )

        return prompts

    def _design_sensory_elements(self, reversal_spec: dict[str, Any]) -> dict[str, list[str]]:
        """感覚的詳細を設計"""

        intensity = reversal_spec.get("intensity", 0.5)

        details = {
            "visual": ["血の色が変わる瞬間", "光が急に陰る", "表情が凍りつく"],
            "auditory": [
                "静寂が雷鳴のように響く",
                "心臓の鼓動が異常に大きく聞こえる",
                "遠くで鐘が不吉に鳴る",
            ],
            "tactile": [
                "冷たい汗が背中を流れる",
                "手が震えて制御できない",
                "足の力が抜ける",
            ],
        }

        # 強度に応じて詳細の数を調整
        if intensity > 0.8:
            return details
        else:
            return {k: v[:2] for k, v in details.items()}

    async def _generate_scene_text(self, scene_design: dict[str, Any]) -> str:
        """実際のシーンテキストを生成"""

        # この部分は実際にはLLMを使用する
        # ここでは構造化されたテンプレートを使用

        template = scene_design["template"]

        scene_parts = []

        # 設定部分
        scene_parts.append(f"【設定】{template.setup}")
        scene_parts.append(f"場所: {scene_design['setting_details']['location']}")
        scene_parts.append(f"雰囲気: {scene_design['setting_details']['atmosphere']}")

        # 転換点部分
        scene_parts.append(f"\n【転換点】{template.turning_point}")

        # 余波部分
        scene_parts.append(f"\n【余波】{template.aftermath}")

        # キャラクターの反応
        for char_name, arc in scene_design["character_arcs"].items():
            scene_parts.append(
                f"\n{char_name}の変化: {arc['initial_state']} → {arc['final_state']}"
            )

        # 感覚的詳細
        sensory = scene_design["sensory_details"]
        scene_parts.append("\n【感覚的詳細】")
        scene_parts.append(f"視覚: {', '.join(sensory['visual'][:2])}")
        scene_parts.append(f"聴覚: {', '.join(sensory['auditory'][:2])}")

        return "\n".join(scene_parts)

    async def _verify_reversal_intensity(
        self, scene_text: str, reversal_spec: dict[str, Any]
    ) -> bool:
        """転換の強度を検証"""

        target_intensity = reversal_spec.get("intensity", 0.8)

        # 簡単な強度測定（実際にはより sophisticated な分析を行う）
        intensity_indicators = [
            "絶望",
            "衝撃",
            "驚愕",
            "裏切り",
            "破滅",
            "奇跡",
            "救済",
            "真実",
        ]

        intensity_score = sum(scene_text.count(indicator) for indicator in intensity_indicators)
        estimated_intensity = min(1.0, intensity_score * 0.2)

        return estimated_intensity >= target_intensity * 0.8

    async def _intensify_reversal(self, scene_text: str, reversal_spec: dict[str, Any]) -> str:
        """転換を強化"""

        # 感情的要素を強化
        intensified_elements = [
            "\n【強化された感情的要素】",
            "- 登場人物の内心の動揺をより詳細に描写",
            "- 物理的な反応（震え、冷汗、脱力）を追加",
            "- 環境の変化（風、光、音）で心理状態を反映",
            "- 過去の記憶や予感との対比を強調",
        ]

        return scene_text + "\n".join(intensified_elements)
