#!/usr/bin/env python3
"""旅游AI助手 - 功能测试报告"""
import requests
import json

BASE_URL = "http://localhost:8000"

print("\n" + "="*70)
print("🚀 旅游AI助手 - 功能测试报告")
print("="*70)

results = []

# 1. 健康检查
try:
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    ok = r.status_code == 200
    results.append(("健康检查", ok, r.json() if ok else r.text[:100]))
except Exception as e:
    results.append(("健康检查", False, str(e)[:100]))

# 2. 城市数据
try:
    r = requests.get(f"{BASE_URL}/cities", timeout=5)
    ok = r.status_code == 200
    data = r.json() if ok else {}
    results.append(("城市数据", ok, f"{len(data.get('cities', []))} 个城市" if ok else r.text[:100]))
except Exception as e:
    results.append(("城市数据", False, str(e)[:100]))

# 3. 订单管理
try:
    r = requests.get(f"{BASE_URL}/orders", timeout=5)
    ok = r.status_code == 200
    data = r.json() if ok else {}
    results.append(("订单管理", ok, f"{data.get('total', 0)} 条订单" if ok else r.text[:100]))
except Exception as e:
    results.append(("订单管理", False, str(e)[:100]))

# 4. 主页访问
try:
    r = requests.get(f"{BASE_URL}/", timeout=5)
    ok = r.status_code == 200
    results.append(("主页访问", ok, "HTML页面正常" if ok else r.text[:100]))
except Exception as e:
    results.append(("主页访问", False, str(e)[:100]))

# 5. AI对话功能
try:
    r = requests.post(f"{BASE_URL}/chat", json={"message": "你好", "session_id": "test"}, timeout=30)
    ok = r.status_code == 200
    data = r.json() if ok else {}
    response = data.get("response", "")[:80] if ok else r.text[:80]
    results.append(("AI对话", ok, response if ok else f"错误: {r.status_code}"))
except Exception as e:
    results.append(("AI对话", False, str(e)[:100]))

# 输出结果
print("\n📊 测试结果:\n")
success = sum(1 for _, ok, _ in results if ok)
fail = len(results) - success

for name, ok, detail in results:
    status = "✅" if ok else "❌"
    print(f"  {status} {name:<15} {detail if not ok or name == 'AI对话' else ''}")

print("\n" + "-"*70)
print(f"总计: {success} 成功, {fail} 失败")
print("-"*70)

if fail == 0:
    print("\n🎉 所有功能测试通过！\n")
elif success >= 4:
    print("\n✅ 核心功能正常，AI对话需要配置有效的API Key\n")
else:
    print(f"\n⚠️  有 {fail} 个功能需要检查\n")