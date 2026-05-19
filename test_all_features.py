#!/usr/bin/env python3
"""全功能测试脚本 - 验证旅游AI助手六大核心功能"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"


def test_chat(message, session_id="test_session"):
    """发送聊天消息并返回响应"""
    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": message, "session_id": session_id},
            timeout=60
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"HTTP {response.status_code}", "detail": response.text}
    except Exception as e:
        return {"error": str(e)}


def print_result(test_name, result):
    """打印测试结果"""
    print(f"\n{'=' * 60}")
    print(f"测试: {test_name}")
    print(f"{'=' * 60}")
    if "error" in result:
        print(f"❌ 失败: {result['error']}")
        if "detail" in result:
            print(f"详情: {result['detail'][:500]}")
    else:
        print(f"✅ 成功")
        response = result.get("response", "")
        if response:
            print(f"响应: {response[:800]}...")
        else:
            print(f"完整响应: {json.dumps(result, ensure_ascii=False, indent=2)[:800]}")


def main():
    print("\n" + "=" * 60)
    print("🚀 旅游AI助手 - 六大核心功能测试")
    print("=" * 60)

    results = {}

    # 测试1: 机票预订
    print("\n\n📍 测试1: 机票预订功能")
    results["机票预订"] = test_chat(
        "我想预订一张从北京到上海的机票，明天出发，经济舱",
        "test_flight_book"
    )
    print_result("机票预订", results["机票预订"])

    # 测试2: 机票改签
    print("\n\n📍 测试2: 机票改签功能")
    results["机票改签"] = test_chat(
        "我想改签机票，改成后天出发的航班",
        "test_flight_change"
    )
    print_result("机票改签", results["机票改签"])

    # 测试3: 酒店查询
    print("\n\n📍 测试3: 酒店查询功能")
    results["酒店查询"] = test_chat(
        "帮我查询上海的酒店，价格在300-500元之间，靠近外滩",
        "test_hotel"
    )
    print_result("酒店查询", results["酒店查询"])

    # 测试4: 订单管理
    print("\n\n📍 测试4: 订单管理功能")
    results["订单管理"] = test_chat(
        "查看我的所有订单",
        "test_orders"
    )
    print_result("订单管理", results["订单管理"])

    # 测试5: 旅游产品销售与预订
    print("\n\n📍 测试5: 旅游产品销售与预订")
    results["旅游产品"] = test_chat(
        "推荐一些热门的旅游产品，我想预订一个云南旅游套餐",
        "test_products"
    )
    print_result("旅游产品", results["旅游产品"])

    # 测试6: 智能推荐当地旅游方案
    print("\n\n📍 测试6: 智能推荐当地旅游方案")
    results["智能推荐"] = test_chat(
        "我要去杭州旅游3天，请帮我规划一个详细的行程方案",
        "test_recommend"
    )
    print_result("智能推荐", results["智能推荐"])

    # 汇总结果
    print("\n\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)

    success_count = 0
    fail_count = 0
    for name, result in results.items():
        if "error" not in result:
            print(f"✅ {name}: 成功")
            success_count += 1
        else:
            print(f"❌ {name}: 失败 - {result['error']}")
            fail_count += 1

    print(f"\n总计: {success_count} 成功, {fail_count} 失败")

    if fail_count == 0:
        print("\n🎉 所有功能测试通过！")
        return 0
    else:
        print(f"\n⚠️  有 {fail_count} 个功能测试失败")
        return 1


if __name__ == "__main__":
    exit(main())