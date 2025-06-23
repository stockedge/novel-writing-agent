#!/usr/bin/env python3
"""
計算論的物語論統合型ハイファンタジー小説執筆システム v6.0
メインエントリーポイント
"""

import asyncio
from datetime import datetime

from src.engines.computational_fantasy_engine import (
    ComputationallyOptimizedFantasyEngine,
)
from src.utils.file_utils import save_optimized_novel
from src.utils.visualization import plot_emotional_journey


async def main():
    """メイン実行関数"""

    print("=" * 60)
    print("計算論的物語論統合型ハイファンタジー小説執筆システム v6.0")
    print("=" * 60)

    # エンジン初期化
    print("\n🔬 計算論的物語エンジンを初期化中...")
    engine = ComputationallyOptimizedFantasyEngine()

    # 初期コンセプトの設定
    initial_concept = {
        "theme": "権力の頂点からの転落と贖罪への道",
        "protagonist": {
            "name": "アルテミス・ヴェルダンディ",
            "role": "堕ちた皇帝",
            "arc": "傲慢な支配者から謙虚な求道者への変貌",
        },
        "core_reversals": [
            "信頼する者全ての裏切り",
            "最大の敵が唯一の味方に",
            "勝利が最大の敗北に",
            "死が新たな生の始まりに",
        ],
        "semantic_journey": {
            "start": "王宮の栄華と権力の陶酔",
            "middle": "孤独の深淵と絶望の極み",
            "end": "精神的悟りと真の自由",
            "distance": "maximum",
        },
        "nonlinear_elements": [
            "過去の罪が徐々に明かされる",
            "複数の時間軸での因果応報",
            "予言と現実の複雑な交錯",
            "死者の証言による真実の開示",
        ],
        "target_metrics": {
            "reversal_frequency": 2.8,
            "reversal_intensity": 0.85,
            "semantic_distance": 0.9,
            "emotional_variance": 0.75,
        },
    }

    print("\n📊 初期コンセプトの分析中...")
    print(f"テーマ: {initial_concept['theme']}")
    print(f"主人公: {initial_concept['protagonist']['name']}")
    print(f"目標転換頻度: {initial_concept['target_metrics']['reversal_frequency']}回/章")

    # 物語生成実行
    print("\n🚀 計算論的最適化による物語生成を開始...")
    start_time = datetime.now()

    try:
        result = await engine.create_optimized_fantasy_novel(initial_concept)

        end_time = datetime.now()
        generation_time = (end_time - start_time).total_seconds()

        # 結果の表示
        print("\n" + "=" * 60)
        print("🎉 生成完了！")
        print("=" * 60)
        print(f"題名: 『{result['title']}』")
        print(f"生成時間: {generation_time:.2f}秒")

        # 物語構造の分析結果
        metrics = result["narrative_metrics"]
        print("\n📈 物語構造の分析結果:")
        print(f"  転換頻度: {metrics['reversal_frequency']:.2f}回/章 (目標: 2.5回)")
        print(f"  平均転換強度: {metrics['average_reversal_intensity']:.2f} (目標: 0.8以上)")
        print(f"  意味的距離: {metrics['semantic_distance']:.2f} (目標: 0.7以上)")
        print(f"  物語速度: {metrics['narrative_speed']}")
        print(f"  感情分散: {metrics['emotional_variance']:.2f} (目標: 0.6以上)")
        print(f"  総合成功スコア: {metrics['success_score']:.2f}/1.0")

        # 品質評価
        if metrics["success_score"] >= 0.8:
            print("\n🏆 優秀 - 計算論的に最適化された高品質な物語です")
        elif metrics["success_score"] >= 0.6:
            print("\n✅ 良好 - 基準を満たした物語です")
        else:
            print("\n⚠️  改善可能 - さらなる最適化が推奨されます")

        # 感情軌跡の可視化
        print("\n📊 感情軌跡を可視化中...")
        await plot_emotional_journey(result["narrative_metrics"])

        # ファイル出力
        print("\n💾 結果をファイルに保存中...")
        await save_optimized_novel(result)

        print("\n✨ 全て完了しました！生成された物語をお楽しみください。")

        return result

    except Exception as e:
        print(f"\n❌ エラーが発生しました: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


if __name__ == "__main__":
    asyncio.run(main())
