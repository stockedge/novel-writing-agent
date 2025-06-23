#!/usr/bin/env python3
"""
Groq API クイックテスト
Llama Guard 4 12B の動作確認
"""

import asyncio
import time
from langchain_groq import ChatGroq


async def test_groq_quick():
    """Groq API の簡単なテスト"""
    print("🚀 Groq API (DeepSeek R1 Distill Llama 70B) テスト開始...")
    
    try:
        # DeepSeek R1 Distill Llama 70B の初期化（推論特化創作用）
        llm = ChatGroq(model="deepseek-r1-distill-llama-70b", temperature=0.8)
        
        # 簡単なテストプロンプト
        test_prompt = """
        あなたは創作の専門家です。
        以下の設定で、短い物語の冒頭（100文字程度）を書いてください。
        
        設定:
        - 主人公: 魔法使いの少女
        - 場面: 森の中の小屋
        - 雰囲気: 神秘的で平和
        
        美しい文章でお願いします。
        """
        
        print("⚡ DeepSeek R1 Distill Llama 70B で生成中...")
        start_time = time.time()
        
        # 生成実行
        response = await llm.ainvoke(test_prompt)
        
        end_time = time.time()
        generation_time = end_time - start_time
        
        print(f"\n✅ 生成完了！ (処理時間: {generation_time:.2f}秒)")
        print("=" * 50)
        print("📖 生成された物語:")
        print("=" * 50)
        print(response.content)
        print("=" * 50)
        
        print(f"\n🎉 Groq API テスト成功！ ({generation_time:.2f}秒)")
        return True
        
    except Exception as e:
        print(f"\n❌ エラー: {str(e)}")
        return False


if __name__ == "__main__":
    asyncio.run(test_groq_quick()) 