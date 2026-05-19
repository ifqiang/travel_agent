#!/usr/bin/env python3
"""最终功能测试 - 清晰输出测试结果"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

print("\n" + "="*70)
print("🚀 旅游AI助手 - 功能测试报告")
print("="*70)

results = []

# 1. 健康检查
try:
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    ok = r.status_code == 200
    results.append(("健康检查", ok, r.json() if ok else r.text))
except Exception as e:
    results.append(("健康检查", False, str(e)))

# 2. 城市列表
try:
    r = requests.get(f"{BASE_URL}/cities", timeout=5)
    ok = r.status_code == 200
    data = r.json() if ok else {}
    results.append(("城市数据", ok, f"{len(data.get('cities', []))} 个城市" if ok else r.text))
except Exception as e:
    results.append(("城市数据", False, str(e)))

# 3. 订单列表
try:
    r = requests.get(f"{BASE_URL}/orders", timeout=5)
    ok = r.status_code == 200
    data = r.json() if ok else {}
    results.append(("订单管理", ok, f"{data.get('total', 0)} 条订单" if ok else r.text))
except Exception as e:
    results.append(("订单管理", False, str(e)))

# 4. 主页访问
try:
    r = requests.get(f"{BASE_URL}/", timeout=5)
    ok = r.status_code == 200
    results.append(("前端页面", ok, "HTML页面正常" if ok else r.text[:100]))
except Exception as e:
    results.append(("前端页面", False, str(e)))

# 5. AI对话测试
try:
    r = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "你好", "session_id": "test"},
        timeout=30
    )
    ok = r.status_code == 200
    data = r.json() if ok else {}
    response = data.get("response", "")
    # 检查是否是配额错误
    if "配额" in response or "403" in response:
        results.append(("AI对话", False, "API配额已用尽"))
    else:
        results.append(("AI对话", ok, response[:50] + "..." if len(response) > 50 else response))
except Exception as e:
    results.append(("AI对话", False, str(e)))

# 输出结果
print("\n📊 测试结果:\n")
success = 0
fail = 0
for name, ok, detail in results:
    status = "✅" if ok else "❌"
    print(f"  {status} {name:<12} {detail if not ok else ''}")
    if ok:
        success += 1
    else:
        fail += 1

print("\n" + "-"*70)
print(f"总计: {success} 成功, {fail} 失败")
print("-"*70)

if fail == 0:
    print("\n🎉 所有功能测试通过！\n")
    sys.exit(0)
else:
    print(f"\n⚠️  有 {fail} 个功能需要检查\n")
    sys.exit(1)