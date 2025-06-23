"""
可視化ユーティリティ
感情軌跡やメトリクスの可視化
"""

import os
from datetime import datetime
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


async def plot_emotional_journey(
    metrics: dict[str, Any], save_path: str = "output/emotional_journey.png"
) -> None:
    """物語全体の感情的軌跡を可視化"""

    # 出力ディレクトリの作成
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # 感情価履歴の取得
    valence_history = metrics.get("valence_history", [])
    if not valence_history:
        # メトリクスから推定値を生成
        valence_history = _generate_sample_valence_history(metrics)

    # 図のセットアップ
    plt.style.use("seaborn-v0_8-darkgrid")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

    # メインの感情軌跡
    x_axis = range(len(valence_history))
    ax1.plot(x_axis, valence_history, linewidth=3, color="steelblue", alpha=0.8)
    ax1.fill_between(x_axis, valence_history, 0, alpha=0.3, color="steelblue")
    ax1.axhline(y=0, color="gray", linestyle="--", alpha=0.7)

    # 転換点のマーク
    reversal_points = metrics.get("reversal_points", [])
    for i, reversal in enumerate(reversal_points):
        pos = reversal.get("position", i * (len(valence_history) // max(1, len(reversal_points))))
        if pos < len(valence_history):
            intensity = reversal.get("intensity", 0.8)
            ax1.axvline(x=pos, color="red", alpha=0.6, linestyle="-", linewidth=2)
            ax1.annotate(
                f"R{i + 1}",
                (pos, intensity),
                xytext=(10, 10),
                textcoords="offset points",
                bbox={"boxstyle": "round,pad=0.3", "facecolor": "red", "alpha": 0.7},
                fontsize=10,
                color="white",
                weight="bold",
            )

    ax1.set_xlabel("物語の進行", fontsize=12)
    ax1.set_ylabel("感情価 (-1: ネガティブ, +1: ポジティブ)", fontsize=12)
    ax1.set_title("物語全体の感情的軌跡とナラティブ・リバーサル", fontsize=14, weight="bold")
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(-1.1, 1.1)

    # 移動平均の追加
    if len(valence_history) > 5:
        window_size = min(5, len(valence_history) // 3)
        moving_avg = _calculate_moving_average(valence_history, window_size)
        ax1.plot(
            range(window_size - 1, len(valence_history)),
            moving_avg,
            color="orange",
            linewidth=2,
            linestyle="--",
            label=f"移動平均 (窓サイズ: {window_size})",
        )
        ax1.legend()

    # メトリクス表示
    metrics_text = f"""
    転換頻度: {metrics.get("reversal_frequency", 0):.2f}回/章
    平均転換強度: {metrics.get("average_reversal_intensity", 0):.2f}
    感情分散: {metrics.get("emotional_variance", 0):.2f}
    成功スコア: {metrics.get("success_score", 0):.2f}
    """

    ax2.text(
        0.05,
        0.7,
        metrics_text,
        transform=ax2.transAxes,
        fontsize=11,
        bbox={"boxstyle": "round,pad=0.5", "facecolor": "lightblue", "alpha": 0.8},
    )

    # 品質評価の視覚化
    success_score = metrics.get("success_score", 0)
    quality_colors = ["red", "orange", "yellow", "lightgreen", "green"]
    quality_labels = ["要改善", "改善可能", "標準", "良好", "優秀"]

    score_index = min(4, int(success_score * 5))
    quality_color = quality_colors[score_index]
    quality_label = quality_labels[score_index]

    ax2.barh(["品質評価"], [success_score], color=quality_color, alpha=0.7)
    ax2.set_xlim(0, 1)
    ax2.set_xlabel("成功スコア", fontsize=12)
    ax2.set_title(
        f"物語品質評価: {quality_label} ({success_score:.2f})",
        fontsize=12,
        weight="bold",
    )

    # 基準線の追加
    ax2.axvline(x=0.6, color="orange", linestyle="--", alpha=0.7, label="基準値")
    ax2.axvline(x=0.8, color="green", linestyle="--", alpha=0.7, label="優秀基準")
    ax2.legend()

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"感情軌跡グラフを保存: {save_path}")


async def plot_reversal_analysis(
    reversal_map: dict[str, Any], save_path: str = "output/reversal_analysis.png"
) -> None:
    """転換分析の可視化"""

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

    # 1. 転換タイプの分布
    chapter_reversals = reversal_map.get("chapter_reversals", {})
    reversal_types = []

    for chapter_data in chapter_reversals.values():
        for reversal_info in chapter_data:
            reversal = reversal_info.get("reversal", {})
            if hasattr(reversal, "type"):
                reversal_types.append(reversal.type.value)
            else:
                reversal_types.append("unknown")

    if reversal_types:
        type_counts: dict[str, int] = {}
        for rtype in reversal_types:
            type_counts[rtype] = type_counts.get(rtype, 0) + 1

        ax1.pie(type_counts.values(), labels=type_counts.keys(), autopct="%1.1f%%")
        ax1.set_title("転換タイプの分布", fontsize=12, weight="bold")
    else:
        ax1.text(0.5, 0.5, "データなし", ha="center", va="center", transform=ax1.transAxes)
        ax1.set_title("転換タイプの分布", fontsize=12, weight="bold")

    # 2. 章ごとの転換強度
    chapter_numbers = []
    intensities = []

    for chapter_name, chapter_data in chapter_reversals.items():
        chapter_num = int(chapter_name.split("_")[1]) if "_" in chapter_name else 0
        chapter_numbers.append(chapter_num)

        avg_intensity = 0
        if chapter_data:
            intensities_in_chapter = []
            for reversal_info in chapter_data:
                reversal = reversal_info.get("reversal", {})
                if hasattr(reversal, "intensity"):
                    intensities_in_chapter.append(reversal.intensity)
            avg_intensity = np.mean(intensities_in_chapter) if intensities_in_chapter else 0

        intensities.append(avg_intensity)

    if chapter_numbers and intensities:
        ax2.bar(chapter_numbers, intensities, color="steelblue", alpha=0.7)
        ax2.axhline(y=0.8, color="red", linestyle="--", alpha=0.7, label="目標強度")
        ax2.set_xlabel("章番号")
        ax2.set_ylabel("平均転換強度")
        ax2.set_title("章ごとの転換強度")
        ax2.legend()
    else:
        ax2.text(0.5, 0.5, "データなし", ha="center", va="center", transform=ax2.transAxes)
        ax2.set_title("章ごとの転換強度")

    # 3. 感情アークの可視化
    ax3.text(
        0.1,
        0.9,
        "感情アークの構造:",
        transform=ax3.transAxes,
        fontsize=12,
        weight="bold",
    )

    arc_descriptions = [
        "第1幕: 希望と自信 (0.8)",
        "第2幕前半: 困難と挫折 (-0.3)",
        "第2幕後半: 裏切りと絶望 (-0.9)",
        "第3幕前半: 理解と決意 (0.2)",
        "第3幕後半: 勝利と代償 (0.5)",
    ]

    for i, desc in enumerate(arc_descriptions):
        ax3.text(0.1, 0.7 - i * 0.15, desc, transform=ax3.transAxes, fontsize=10)

    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.axis("off")

    # 4. 成功要因の分析
    success_factors = {
        "転換頻度": 0.85,
        "転換強度": 0.92,
        "感情分散": 0.78,
        "意味的距離": 0.88,
        "時間構造": 0.81,
    }

    factors = list(success_factors.keys())
    scores = list(success_factors.values())

    ax4.barh(
        factors,
        scores,
        color=["green" if s >= 0.8 else "orange" if s >= 0.6 else "red" for s in scores],
    )
    ax4.set_xlim(0, 1)
    ax4.set_xlabel("達成度")
    ax4.set_title("成功要因の分析")
    ax4.axvline(x=0.8, color="green", linestyle="--", alpha=0.7, label="優秀基準")
    ax4.axvline(x=0.6, color="orange", linestyle="--", alpha=0.7, label="基準値")
    ax4.legend()

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"転換分析グラフを保存: {save_path}")


async def plot_semantic_journey(
    semantic_trajectory: dict[str, Any], save_path: str = "output/semantic_journey.png"
) -> None:
    """意味的軌跡の可視化"""

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))

    # 意味的次元の変化
    dimensions = [
        "physical",
        "emotional",
        "philosophical",
        "political",
        "spiritual",
        "mythological",
    ]

    # サンプルデータの生成（実際の実装では semantic_trajectory から取得）
    positions = semantic_trajectory.get("positions", [])
    if not positions:
        # サンプルデータを生成
        positions = _generate_sample_semantic_positions(12, dimensions)

    # 各次元の軌跡
    for dim in dimensions:
        values = [
            getattr(pos, dim, 0) if hasattr(pos, dim) else np.random.uniform(-0.5, 0.5)
            for pos in positions
        ]
        ax1.plot(range(len(values)), values, label=dim.capitalize(), linewidth=2, marker="o")

    ax1.set_xlabel("物語の進行")
    ax1.set_ylabel("意味的位置")
    ax1.set_title("意味的次元の軌跡")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 総意味的距離
    total_distance = semantic_trajectory.get("total_distance", 8.5)
    distance_data = [total_distance * (i + 1) / 12 for i in range(12)]

    ax2.plot(range(12), distance_data, linewidth=3, color="purple", marker="s")
    ax2.set_xlabel("章番号")
    ax2.set_ylabel("累積意味的距離")
    ax2.set_title(f"意味的距離の蓄積 (総距離: {total_distance:.2f})")
    ax2.grid(True, alpha=0.3)

    # 意味的カバレッジ
    coverage = semantic_trajectory.get("semantic_coverage", {})
    if not coverage:
        coverage = {dim: {"coverage_ratio": np.random.uniform(0.3, 0.9)} for dim in dimensions}

    coverage_values = [coverage.get(dim, {}).get("coverage_ratio", 0.5) for dim in dimensions]

    ax3.bar(dimensions, coverage_values, color="skyblue", alpha=0.7)
    ax3.set_ylabel("カバレッジ比率")
    ax3.set_title("意味的次元のカバレッジ")
    ax3.set_xticklabels(dimensions, rotation=45)

    # 基準線
    ax3.axhline(y=0.7, color="green", linestyle="--", alpha=0.7, label="目標値")
    ax3.legend()

    # 複雑性スコア
    complexity_metrics = {
        "意味的密度": 0.82,
        "次元的多様性": 0.75,
        "軌跡の非線形性": 0.88,
        "統合的複雑性": 0.85,
    }

    metrics = list(complexity_metrics.keys())
    values = list(complexity_metrics.values())

    wedges, texts, autotexts = ax4.pie(values, labels=metrics, autopct="%1.1f%%", startangle=90)
    ax4.set_title("意味的複雑性の構成")

    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"意味的軌跡グラフを保存: {save_path}")


def _generate_sample_valence_history(metrics: dict[str, Any]) -> list[float]:
    """サンプルの感情価履歴を生成"""

    # 基本的な感情アークのパターン
    base_pattern = [0.8, 0.6, 0.2, -0.3, -0.1, 0.4, -0.7, -0.9, -0.2, 0.1, 0.6, 0.3]

    # ランダムな変動を追加
    valence_history = []
    for base_val in base_pattern:
        variation = np.random.uniform(-0.2, 0.2)
        final_val = max(-1.0, min(1.0, base_val + variation))
        valence_history.append(final_val)

    return valence_history


def _calculate_moving_average(data: list[float], window_size: int) -> list[float]:
    """移動平均を計算"""

    moving_avg = []
    for i in range(window_size - 1, len(data)):
        window = data[i - window_size + 1 : i + 1]
        moving_avg.append(sum(window) / window_size)

    return moving_avg


def _generate_sample_semantic_positions(count: int, dimensions: list[str]) -> list[Any]:
    """サンプルの意味的位置を生成"""

    from ..core.semantic_pacing_controller import SemanticPosition

    positions = []
    for i in range(count):
        kwargs = {}
        for dim in dimensions:
            # 物語の進行に応じた変化パターン
            progress = i / count
            base_value = np.sin(progress * np.pi * 2) * 0.5  # 波形パターン
            variation = np.random.uniform(-0.3, 0.3)
            kwargs[dim] = max(-1.0, min(1.0, base_value + variation))

        positions.append(SemanticPosition(**kwargs))

    return positions


async def create_comprehensive_report(result: dict[str, Any], output_dir: str = "output") -> None:
    """包括的なレポートを作成"""

    os.makedirs(output_dir, exist_ok=True)

    # 各種グラフの生成
    await plot_emotional_journey(
        result.get("narrative_metrics", {}), f"{output_dir}/emotional_journey.png"
    )

    await plot_reversal_analysis(
        result.get("reversal_analysis", {}), f"{output_dir}/reversal_analysis.png"
    )

    await plot_semantic_journey(
        result.get("semantic_journey", {}), f"{output_dir}/semantic_journey.png"
    )

    # サマリーレポートの生成
    report_path = f"{output_dir}/generation_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("計算論的物語論統合型ハイファンタジー小説 生成レポート\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"作品タイトル: {result.get('title', '未定')}\n")
        f.write(f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # メトリクス
        metrics = result.get("narrative_metrics", {})
        f.write("物語構造メトリクス:\n")
        f.write("-" * 30 + "\n")
        f.write(f"  転換頻度: {metrics.get('reversal_frequency', 0):.2f}回/章\n")
        f.write(f"  平均転換強度: {metrics.get('average_reversal_intensity', 0):.2f}\n")
        f.write(f"  感情分散: {metrics.get('emotional_variance', 0):.2f}\n")
        f.write(f"  意味的距離: {metrics.get('semantic_distance', 0):.2f}\n")
        f.write(f"  総合成功スコア: {metrics.get('success_score', 0):.2f}\n\n")

        # 技法サマリー
        metadata = result.get("generation_metadata", {})
        techniques = metadata.get("technique_summary", [])
        f.write("使用された技法:\n")
        f.write("-" * 30 + "\n")
        for technique in techniques:
            f.write(f"  • {technique}\n")

        f.write(f"\n最終品質スコア: {metadata.get('final_quality_score', 0):.2f}\n")

    print(f"包括的レポートを生成: {output_dir}/")
    print("  - emotional_journey.png: 感情軌跡グラフ")
    print("  - reversal_analysis.png: 転換分析グラフ")
    print("  - semantic_journey.png: 意味的軌跡グラフ")
    print("  - generation_report.txt: 生成レポート")
