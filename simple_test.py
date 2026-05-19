#!/usr/bin/env python3
"""简化版功能测试"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_chat(message, session_id="test"):
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": message, "session_id": session_id},
            timeout=60
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

print("\n" + "="*60)
print("🚀 旅游AI助手 - 功能测试")
print("="*60)

tests = [
    ("机票预订", "我想预订一张从北京到上海的机票，明天出发，经济舱", "t1"),
    ("机票改签", "我想改签机票，改成后天出发的航班", "t2"),
    ("酒店查询", "帮我查询上海的酒店，价格在300-500元之间", "t3"),
    ("订单管理", "查看我的所有订单", "t4"),
    ("旅游产品", "推荐一些热门的旅游产品", "t5"),
    ("智能推荐", "我要去杭州旅游3天，请帮我规划行程", "t6"),
]

results = []
for name, msg, sid in tests:
    print(f"\n📍 测试: {name}...")
    result = test_chat(msg, sid)
    if "error" in result:
        print(f"   ❌ 失败: {result['error']}")
        results.append((name, False, result['error']))
    else:
        resp = result.get("response", "")[:200]
        print(f"   ✅ 成功: {resp}...")
        results.append((name, True, resp))

print("\n" + "="*60)
print("📊 测试汇总")
print("="*60)
success = sum(1 for _, ok, _ in results if ok)
fail = len(results) - success
for name, ok, detail in results:
    status = "✅" if ok else "❌"
    print(f"{status} {name}")

print(f"\n总计: {success} 成功, {fail} 失败")
if fail == 0:
    print("\n🎉 所有功能测试通过！")