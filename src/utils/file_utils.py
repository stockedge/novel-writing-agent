"""
ファイル保存ユーティリティ
生成された物語とメタデータの保存
"""

import json
import os
from datetime import datetime
from typing import Any


async def save_optimized_novel(result: dict[str, Any], output_dir: str = "output") -> None:
    """最適化された小説を保存"""

    # 出力ディレクトリの作成
    os.makedirs(output_dir, exist_ok=True)

    title = result.get("title", "Untitled Novel")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # メイン原稿の保存
    manuscript = result.get("manuscript", {})
    manuscript_path = f"{output_dir}/novel_{timestamp}.txt"

    with open(manuscript_path, "w", encoding="utf-8") as f:
        f.write(f"『{title}』\n")
        f.write("=" * 60 + "\n\n")
        f.write("計算論的物語論統合型ハイファンタジー小説執筆システム v6.0 生成\n")
        f.write(f"生成日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n\n")

        # 各章の内容
        for chapter_key in sorted(manuscript.keys()):
            content = manuscript[chapter_key]
            f.write(content + "\n\n")
            f.write("-" * 60 + "\n\n")

    print(f"📖 小説原稿を保存: {manuscript_path}")

    # 世界設定資料の保存
    world_bible = result.get("world_bible", {})
    if world_bible:
        world_path = f"{output_dir}/world_bible_{timestamp}.json"
        with open(world_path, "w", encoding="utf-8") as f:
            json.dump(world_bible, f, ensure_ascii=False, indent=2)
        print(f"🌍 世界設定資料を保存: {world_path}")

    # メトリクスデータの保存
    metrics = result.get("narrative_metrics", {})
    if metrics:
        metrics_path = f"{output_dir}/metrics_{timestamp}.json"
        with open(metrics_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, ensure_ascii=False, indent=2)
        print(f"📊 メトリクスデータを保存: {metrics_path}")

    # 転換分析の保存
    reversal_analysis = result.get("reversal_analysis", {})
    if reversal_analysis:
        reversal_path = f"{output_dir}/reversal_analysis_{timestamp}.json"

        # シリアライゼーション用にデータを変換
        serializable_analysis = _make_serializable(reversal_analysis)

        with open(reversal_path, "w", encoding="utf-8") as f:
            json.dump(serializable_analysis, f, ensure_ascii=False, indent=2)
        print(f"🎭 転換分析を保存: {reversal_path}")

    # 統合レポートの保存
    await _save_integrated_report(result, f"{output_dir}/integrated_report_{timestamp}.md")

    print(f"✅ 全ファイルを '{output_dir}' に保存完了")


def _make_serializable(obj: Any, seen: set | None = None) -> Any:
    """オブジェクトをJSON serializable に変換（循環参照対応）"""

    if seen is None:
        seen = set()

    # 循環参照チェック
    obj_id = id(obj)
    if obj_id in seen:
        return f"<循環参照: {type(obj).__name__}>"

    # プリミティブ型の早期リターン
    if obj is None or isinstance(obj, str | int | float | bool):
        return obj

    # 処理済みマークを追加
    seen.add(obj_id)

    try:
        if hasattr(obj, "value") and hasattr(obj, "name"):
            # Enum
            return obj.value
        elif hasattr(obj, "__dict__"):
            # データクラスやカスタムオブジェクト
            result = {}
            for key, value in obj.__dict__.items():
                if not key.startswith("_"):  # プライベート属性をスキップ
                    result[key] = _make_serializable(value, seen)
            return result
        elif isinstance(obj, dict):
            return {key: _make_serializable(value, seen) for key, value in obj.items()}
        elif isinstance(obj, list | tuple):
            return [_make_serializable(item, seen) for item in obj]
        elif isinstance(obj, set):
            return [_make_serializable(item, seen) for item in obj]
        else:
            # その他の型は文字列表現
            return str(obj)
    finally:
        # 処理完了後にマークを削除
        seen.discard(obj_id)


async def _save_integrated_report(result: dict[str, Any], report_path: str) -> None:
    """統合レポートをMarkdown形式で保存"""

    title = result.get("title", "Untitled Novel")
    metrics = result.get("narrative_metrics", {})
    metadata = result.get("generation_metadata", {})

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# 『{title}』生成レポート\n\n")

        f.write("## 概要\n\n")
        f.write(
            "計算論的物語論統合型ハイファンタジー小説執筆システム v6.0 により生成された作品の詳細分析レポートです。\n\n"
        )

        f.write(f"**生成日時**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n")
        f.write(f"**最終品質スコア**: {metadata.get('final_quality_score', 0):.2f}/1.0\n\n")

        # 物語構造メトリクス
        f.write("## 物語構造メトリクス\n\n")
        f.write("| 指標 | 値 | 目標値 | 評価 |\n")
        f.write("|------|----|---------|---------|\n")

        reversal_freq = metrics.get("reversal_frequency", 0)
        f.write(
            f"| 転換頻度 | {reversal_freq:.2f}回/章 | 2.5回/章 | {'✅' if reversal_freq >= 2.5 else '⚠️'} |\n"
        )

        reversal_intensity = metrics.get("average_reversal_intensity", 0)
        f.write(
            f"| 平均転換強度 | {reversal_intensity:.2f} | 0.8以上 | {'✅' if reversal_intensity >= 0.8 else '⚠️'} |\n"
        )

        emotional_variance = metrics.get("emotional_variance", 0)
        f.write(
            f"| 感情分散 | {emotional_variance:.2f} | 0.6以上 | {'✅' if emotional_variance >= 0.6 else '⚠️'} |\n"
        )

        semantic_distance = metrics.get("semantic_distance", 0)
        f.write(
            f"| 意味的距離 | {semantic_distance:.2f} | 0.7以上 | {'✅' if semantic_distance >= 0.7 else '⚠️'} |\n"
        )

        f.write("\n")

        # 使用された技法
        f.write("## 使用された計算論的技法\n\n")
        techniques = metadata.get("technique_summary", [])
        for technique in techniques:
            f.write(f"- {technique}\n")
        f.write("\n")

        # 品質評価
        success_score = metrics.get("success_score", 0)
        f.write("## 品質評価\n\n")

        if success_score >= 0.8:
            f.write("🏆 **優秀** - 計算論的に最適化された高品質な物語です\n\n")
            f.write("この作品は以下の点で優れています：\n")
            f.write("- 適切な頻度と強度での感情的転換\n")
            f.write("- 豊かな感情の起伏と多様性\n")
            f.write("- 高い意味的複雑性と読者エンゲージメント\n")
        elif success_score >= 0.6:
            f.write("✅ **良好** - 基準を満たした物語です\n\n")
            f.write("改善の余地がある分野：\n")
            if reversal_freq < 2.5:
                f.write("- 転換頻度の増加\n")
            if reversal_intensity < 0.8:
                f.write("- 転換強度の向上\n")
            if emotional_variance < 0.6:
                f.write("- 感情的多様性の拡充\n")
        else:
            f.write("⚠️ **改善可能** - さらなる最適化が推奨されます\n\n")
            f.write("重点的な改善が必要な分野：\n")
            f.write("- 物語構造の根本的な見直し\n")
            f.write("- 感情的転換の質と量の向上\n")
            f.write("- キャラクターアークの深化\n")

        f.write("\n")

        # 技術仕様
        f.write("## 技術仕様\n\n")
        f.write("### 計算論的物語論エンジン\n")
        f.write("- ナラティブ・リバーサル最適化アルゴリズム\n")
        f.write("- 感情価リアルタイムトラッキング\n")
        f.write("- 意味的距離最大化アルゴリズム\n\n")

        f.write("### 物語構造技法\n")
        f.write("- 非線形時間構造\n")
        f.write("- 複数視点の戦略的交錯\n")
        f.write("- 意味的ペーシング制御\n\n")

        f.write("### 品質保証システム\n")
        f.write("- 30,000作品分析データベース準拠\n")
        f.write("- リアルタイム成功確率計算\n")
        f.write("- 自動品質調整機能\n\n")

        # フッター
        f.write("---\n")
        f.write(
            "*このレポートは計算論的物語論統合型ハイファンタジー小説執筆システム v6.0 により自動生成されました*\n"
        )

    print(f"📋 統合レポートを保存: {report_path}")


async def export_for_publication(
    result: dict[str, Any], format_type: str = "epub", output_dir: str = "output"
) -> None:
    """出版用フォーマットでエクスポート"""

    os.makedirs(output_dir, exist_ok=True)

    title = result.get("title", "Untitled Novel")
    manuscript = result.get("manuscript", {})
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if format_type.lower() == "epub":
        await _export_epub(title, manuscript, f"{output_dir}/novel_{timestamp}.epub")
    elif format_type.lower() == "pdf":
        await _export_pdf(title, manuscript, f"{output_dir}/novel_{timestamp}.pdf")
    elif format_type.lower() == "html":
        await _export_html(title, manuscript, f"{output_dir}/novel_{timestamp}.html")
    else:
        print(f"⚠️ 未対応のフォーマット: {format_type}")


async def _export_epub(title: str, manuscript: dict[str, str], output_path: str) -> None:
    """EPUB形式でエクスポート（簡略版）"""

    # 実際の実装では ebooklib などのライブラリを使用
    print(f"📚 EPUB形式でのエクスポートは将来のバージョンで実装予定: {output_path}")


async def _export_pdf(title: str, manuscript: dict[str, str], output_path: str) -> None:
    """PDF形式でエクスポート（簡略版）"""

    # 実際の実装では reportlab などのライブラリを使用
    print(f"📄 PDF形式でのエクスポートは将来のバージョンで実装予定: {output_path}")


async def _export_html(title: str, manuscript: dict[str, str], output_path: str) -> None:
    """HTML形式でエクスポート"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(
            f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: '游明朝', 'YuMincho', serif; line-height: 1.8; margin: 40px; }}
        h1 {{ text-align: center; color: #2c3e50; border-bottom: 3px solid #3498db; }}
        h2 {{ color: #34495e; margin-top: 40px; }}
        .chapter {{ margin-bottom: 60px; padding: 20px; background-color: #f8f9fa; }}
        .metadata {{ font-size: 0.9em; color: #666; text-align: center; margin-bottom: 40px; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="metadata">
        計算論的物語論統合型ハイファンタジー小説執筆システム v6.0 生成<br>
        生成日時: {datetime.now().strftime("%Y年%m月%d日")}
    </div>
"""
        )

        for chapter_key in sorted(manuscript.keys()):
            content = manuscript[chapter_key]
            # 簡単なHTML変換
            html_content = content.replace("\n", "<br>\n")
            f.write(f'    <div class="chapter">\n        {html_content}\n    </div>\n')

        f.write("</body>\n</html>")

    print(f"🌐 HTML形式でエクスポート: {output_path}")


async def create_backup(result: dict[str, Any], backup_dir: str = "backups") -> None:
    """バックアップを作成"""

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{backup_dir}/backup_{timestamp}"

    os.makedirs(backup_path, exist_ok=True)

    # 完全なデータをJSONで保存
    backup_data = {
        "timestamp": timestamp,
        "system_version": "6.0.0",
        "result": _make_serializable(result),
    }

    with open(f"{backup_path}/complete_data.json", "w", encoding="utf-8") as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)

    print(f"💾 バックアップを作成: {backup_path}")


async def load_from_backup(backup_path: str) -> dict[str, Any]:
    """バックアップから読み込み"""

    try:
        with open(f"{backup_path}/complete_data.json", encoding="utf-8") as f:
            backup_data = json.load(f)

        print(f"📂 バックアップから読み込み: {backup_path}")
        return backup_data.get("result", {})

    except FileNotFoundError:
        print(f"❌ バックアップファイルが見つかりません: {backup_path}")
        return {}
    except json.JSONDecodeError:
        print(f"❌ バックアップファイルが破損しています: {backup_path}")
        return {}
