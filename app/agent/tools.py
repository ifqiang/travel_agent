"""
LangChain 工具函数集
提供航班、酒店、旅游产品查询与预订功能
包含实时价格查询能力
"""
from langchain_core.tools import tool
from typing import Optional, List, Dict, Any
import json
import random
import aiohttp
from datetime import datetime
from ..db.connection import get_db


# ==================== 实时价格查询服务 ====================

class RealtimePriceService:
    """实时价格查询服务（模拟外部API调用）"""
    
    @staticmethod
    async def fetch_flight_realtime_price(flight_number: str, base_price: float) -> Dict[str, Any]:
        """
        查询航班实时价格（模拟调用外部机票API）
        实际项目中可对接携程、去哪儿等平台的API
        """
        # 模拟价格波动：基础价格 ±15% 的随机波动
        fluctuation = random.uniform(-0.15, 0.15)
        realtime_price = base_price * (1 + fluctuation)
        
        # 模拟动态因素
        factors = []
        if fluctuation > 0.05:
            factors.append("临近起飞价格上涨")
        elif fluctuation < -0.05:
            factors.append("优惠活动特价")
        
        # 模拟余票紧张程度影响
        urgency_level = random.choice(["宽松", "正常", "紧张"])
        if urgency_level == "紧张":
            realtime_price *= 1.1  # 票紧张时价格上涨10%
            factors.append("余票紧张价格上涨")
        
        return {
            "flight_number": flight_number,
            "base_price": base_price,
            "realtime_price": round(realtime_price, 2),
            "price_change": round(realtime_price - base_price, 2),
            "change_percent": round(fluctuation * 100, 2),
            "urgency": urgency_level,
            "factors": factors,
            "query_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_source": "实时报价系统"
        }
    
    @staticmethod
    async def fetch_hotel_realtime_price(hotel_name: str, base_price: float, check_in_date: str = None) -> Dict[str, Any]:
        """
        查询酒店实时价格（模拟调用外部酒店预订API）
        实际项目中可对接美团、携程等平台的API
        """
        # 模拟价格波动：基础价格 ±20% 的随机波动
        fluctuation = random.uniform(-0.20, 0.20)
        realtime_price = base_price * (1 + fluctuation)
        
        # 模拟日期因素（周末/节假日价格上涨）
        factors = []
        if check_in_date:
            try:
                date_obj = datetime.strptime(check_in_date, "%Y-%m-%d")
                if date_obj.weekday() >= 5:  # 周末
                    realtime_price *= 1.15
                    factors.append("周末价格上涨15%")
            except:
                pass
        
        if fluctuation > 0.1:
            factors.append("旺季价格上浮")
        elif fluctuation < -0.1:
            factors.append("限时促销优惠")
        
        # 模拟房型升级选项
        room_types = [
            {"type": "标准间", "price": realtime_price},
            {"type": "大床房", "price": realtime_price * 1.1},
            {"type": "豪华间", "price": realtime_price * 1.3},
        ]
        
        return {
            "hotel_name": hotel_name,
            "base_price": base_price,
            "realtime_price": round(realtime_price, 2),
            "price_change": round(realtime_price - base_price, 2),
            "change_percent": round((realtime_price / base_price - 1) * 100, 2),
            "factors": factors,
            "room_types": room_types,
            "query_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_source": "酒店实时报价系统"
        }
    
    @staticmethod
    async def fetch_product_realtime_price(product_name: str, base_price: float, travel_date: str = None) -> Dict[str, Any]:
        """
        查询旅游产品实时价格（模拟调用OTA平台API）
        实际项目中可对接各大旅行社API
        """
        # 模拟价格波动：基础价格 ±25% 的随机波动
        fluctuation = random.uniform(-0.25, 0.25)
        realtime_price = base_price * (1 + fluctuation)
        
        # 模拟季节因素
        factors = []
        if travel_date:
            try:
                date_obj = datetime.strptime(travel_date, "%Y-%m-%d")
                month = date_obj.month
                if month in [7, 8]:  # 暑期旺季
                    realtime_price *= 1.2
                    factors.append("暑期旺季价格上涨20%")
                elif month in [1, 2]:  # 春节旺季
                    realtime_price *= 1.3
                    factors.append("春节旺季价格上涨30%")
                elif month in [3, 4, 11]:  # 淡季
                    realtime_price *= 0.85
                    factors.append("淡季优惠15%")
            except:
                pass
        
        if fluctuation > 0.15:
            factors.append("热门时段价格上浮")
        elif fluctuation < -0.15:
            factors.append("早鸟优惠特价")
        
        # 模拟团购优惠
        group_discount = None
        if random.random() > 0.5:
            discount_rate = random.choice([0.9, 0.85, 0.8])
            group_discount = {
                "min_people": random.choice([2, 3, 4]),
                "discount_rate": discount_rate,
                "discount_price": round(realtime_price * discount_rate, 2)
            }
        
        return {
            "product_name": product_name,
            "base_price": base_price,
            "realtime_price": round(realtime_price, 2),
            "price_change": round(realtime_price - base_price, 2),
            "change_percent": round((realtime_price / base_price - 1) * 100, 2),
            "factors": factors,
            "group_discount": group_discount,
            "query_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_source": "旅游产品实时报价系统"
        }


# 全局价格服务实例
price_service = RealtimePriceService()


# ==================== 实时价格查询工具 ====================

@tool
async def get_flight_realtime_price(flight_number: str) -> str:
    """
    查询航班实时价格。
    在预订机票前，建议先调用此工具获取最新价格，因为机票价格会实时波动。
    
    Args:
        flight_number: 航班号
    
    Returns:
        实时价格信息，包含基础价格、实时价格、价格变动因素等
    """
    async with get_db() as db:
        cursor = await db.execute(
            "SELECT * FROM flights WHERE flight_number = ?",
            (flight_number,)
        )
        flight = await cursor.fetchone()
        
        if not flight:
            return f"❌ 航班 {flight_number} 不存在。"
        
        # 获取实时价格
        price_info = await price_service.fetch_flight_realtime_price(
            flight_number, flight['price']
        )
        
        result = f"💰 航班实时报价查询\n\n"
        result += f"✈️ 航班：{flight['flight_number']} ({flight['airline']})\n"
        result += f"🛫 航线：{flight['departure_city']} → {flight['arrival_city']}\n"
        result += f"🕐 起飞时间：{flight['departure_time']}\n\n"
        result += f"📊 价格信息：\n"
        result += f"  • 基础价格：¥{price_info['base_price']:.0f}\n"
        result += f"  • 实时价格：¥{price_info['realtime_price']:.0f}\n"
        
        if price_info['price_change'] > 0:
            result += f"  • 价格变动：↑ +¥{price_info['price_change']:.0f} ({price_info['change_percent']:+.1f}%)\n"
        elif price_info['price_change'] < 0:
            result += f"  • 价格变动：↓ -¥{abs(price_info['price_change']):.0f} ({price_info['change_percent']:.1f}%)\n"
        else:
            result += f"  • 价格变动：持平\n"
        
        result += f"  • 余票情况：{price_info['urgency']}\n"
        
        if price_info['factors']:
            result += f"\n📝 价格因素：{', '.join(price_info['factors'])}\n"
        
        result += f"\n⏰ 查询时间：{price_info['query_time']}\n"
        result += f"📡 数据来源：{price_info['data_source']}\n"
        
        result += f"\n💡 提示：机票价格实时波动，建议尽快预订锁定价格！"
        
        return result


@tool
async def get_hotel_realtime_price(hotel_name: str, check_in_date: Optional[str] = None) -> str:
    """
    查询酒店实时价格。
    在预订酒店前，建议先调用此工具获取最新价格，因为酒店价格会根据入住日期和房态实时调整。
    
    Args:
        hotel_name: 酒店名称
        check_in_date: 入住日期，格式 YYYY-MM-DD（可选，用于更精准报价）
    
    Returns:
        实时价格信息，包含基础价格、实时价格、房型选项等
    """
    async with get_db() as db:
        cursor = await db.execute(
            "SELECT * FROM hotels WHERE name = ?",
            (hotel_name,)
        )
        hotel = await cursor.fetchone()
        
        if not hotel:
            return f"❌ 酒店「{hotel_name}」不存在。"
        
        # 获取实时价格
        price_info = await price_service.fetch_hotel_realtime_price(
            hotel_name, hotel['price_per_night'], check_in_date
        )
        
        result = f"💰 酒店实时报价查询\n\n"
        result += f"🏨 酒店：{hotel['name']}\n"
        result += f"📍 地址：{hotel['city']} {hotel['address']}\n"
        result += f"⭐ 评分：{hotel['rating']:.1f}/5.0\n"
        result += f"🛎️ 设施：{hotel['amenities']}\n\n"
        
        if check_in_date:
            result += f"📅 入住日期：{check_in_date}\n\n"
        
        result += f"📊 价格信息：\n"
        result += f"  • 基础价格：¥{price_info['base_price']:.0f}/晚\n"
        result += f"  • 实时价格：¥{price_info['realtime_price']:.0f}/晚\n"
        
        if price_info['price_change'] > 0:
            result += f"  • 价格变动：↑ +¥{price_info['price_change']:.0f} ({price_info['change_percent']:+.1f}%)\n"
        elif price_info['price_change'] < 0:
            result += f"  • 价格变动：↓ -¥{abs(price_info['price_change']):.0f} ({price_info['change_percent']:.1f}%)\n"
        else:
            result += f"  • 价格变动：持平\n"
        
        if price_info['factors']:
            result += f"\n📝 价格因素：{', '.join(price_info['factors'])}\n"
        
        result += f"\n🛏️ 可选房型：\n"
        for room in price_info['room_types']:
            result += f"  • {room['type']}：¥{room['price']:.0f}/晚\n"
        
        result += f"\n⏰ 查询时间：{price_info['query_time']}\n"
        result += f"📡 数据来源：{price_info['data_source']}\n"
        
        result += f"\n💡 提示：酒店价格受入住日期影响，周末和节假日价格可能上浮！"
        
        return result


@tool
async def get_product_realtime_price(product_name: str, travel_date: Optional[str] = None) -> str:
    """
    查询旅游产品实时价格。
    在预订旅游产品前，建议先调用此工具获取最新价格，因为产品价格会根据季节和活动实时调整。
    
    Args:
        product_name: 产品名称
        travel_date: 出行日期，格式 YYYY-MM-DD（可选，用于更精准报价）
    
    Returns:
        实时价格信息，包含基础价格、实时价格、团购优惠等
    """
    async with get_db() as db:
        cursor = await db.execute(
            "SELECT * FROM products WHERE name = ?",
            (product_name,)
        )
        product = await cursor.fetchone()
        
        if not product:
            return f"❌ 旅游产品「{product_name}」不存在。"
        
        # 获取实时价格
        price_info = await price_service.fetch_product_realtime_price(
            product_name, product['price'], travel_date
        )
        
        result = f"💰 旅游产品实时报价查询\n\n"
        result += f"🎒 产品：{product['name']}\n"
        result += f"📍 目的地：{product['destination']}\n"
        result += f"⏱️ 时长：{product['duration_days']}天\n"
        result += f"📝 描述：{product['description']}\n"
        result += f"🎁 包含：{product['includes']}\n\n"
        
        if travel_date:
            result += f"📅 出行日期：{travel_date}\n\n"
        
        result += f"📊 价格信息：\n"
        result += f"  • 基础价格：¥{price_info['base_price']:.0f}\n"
        result += f"  • 实时价格：¥{price_info['realtime_price']:.0f}\n"
        
        if price_info['price_change'] > 0:
            result += f"  • 价格变动：↑ +¥{price_info['price_change']:.0f} ({price_info['change_percent']:+.1f}%)\n"
        elif price_info['price_change'] < 0:
            result += f"  • 价格变动：↓ -¥{abs(price_info['price_change']):.0f} ({price_info['change_percent']:.1f}%)\n"
        else:
            result += f"  • 价格变动：持平\n"
        
        if price_info['factors']:
            result += f"\n📝 价格因素：{', '.join(price_info['factors'])}\n"
        
        if price_info['group_discount']:
            discount = price_info['group_discount']
            result += f"\n👥 团购优惠：\n"
            result += f"  • {discount['min_people']}人及以上成团\n"
            result += f"  • 团购价：¥{discount['discount_price']:.0f}/人\n"
            result += f"  • 每人节省：¥{price_info['realtime_price'] - discount['discount_price']:.0f}\n"
        
        result += f"\n⏰ 查询时间：{price_info['query_time']}\n"
        result += f"📡 数据来源：{price_info['data_source']}\n"
        
        result += f"\n💡 提示：旅游产品价格受季节影响大，建议提前预订享受早鸟优惠！"
        
        return result


# ==================== 航班相关工具 ====================

@tool
async def search_flights(
    departure_city: Optional[str] = None,
    arrival_city: Optional[str] = None,
    date: Optional[str] = None
) -> str:
    """
    查询航班信息。
    
    Args:
        departure_city: 出发城市（可选）
        arrival_city: 到达城市（可选）
        date: 出发日期，格式 YYYY-MM-DD（可选）
    
    Returns:
        符合条件的航班列表
    """
    async with get_db() as db:
        query = "SELECT * FROM flights WHERE seats_available > 0"
        params = []
        
        if departure_city:
            query += " AND departure_city = ?"
            params.append(departure_city)
        if arrival_city:
            query += " AND arrival_city = ?"
            params.append(arrival_city)
        if date:
            query += " AND departure_time LIKE ?"
            params.append(f"{date}%")
        
        query += " ORDER BY price"
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        
        if not rows:
            return "未找到符合条件的航班。"
        
        result = "✈️ 航班查询结果：\n\n"
        for row in rows:
            result += f"【{row['flight_number']}】{row['airline']}\n"
            result += f"  航线：{row['departure_city']} → {row['arrival_city']}\n"
            result += f"  时间：{row['departure_time']} - {row['arrival_time']}\n"
            result += f"  价格：¥{row['price']:.0f} | 余票：{row['seats_available']}张\n\n"
        
        return result


@tool
async def book_flight(
    flight_number: str,
    passenger_name: str,
    passenger_phone: str,
    confirm_price: bool = False
) -> str:
    """
    预订航班机票。
    
    注意：机票价格实时波动，建议先调用 get_flight_realtime_price 查询最新价格。
    如果您已确认价格，请设置 confirm_price=True 完成预订。
    
    Args:
        flight_number: 航班号
        passenger_name: 乘客姓名
        passenger_phone: 乘客电话
        confirm_price: 是否确认价格并完成预订，默认False（仅查询实时价格）
    
    Returns:
        预订结果，包含订单号；或实时价格信息（当confirm_price=False时）
    """
    async with get_db() as db:
        # 查询航班
        cursor = await db.execute(
            "SELECT * FROM flights WHERE flight_number = ? AND seats_available > 0",
            (flight_number,)
        )
        flight = await cursor.fetchone()
        
        if not flight:
            return f"❌ 航班 {flight_number} 不存在或已无余票。"
        
        # 获取实时价格
        price_info = await price_service.fetch_flight_realtime_price(
            flight_number, flight['price']
        )
        realtime_price = price_info['realtime_price']
        
        # 如果未确认价格，返回实时价格信息供用户确认
        if not confirm_price:
            result = f"💰 机票实时报价\n\n"
            result += f"✈️ 航班：{flight['flight_number']} ({flight['airline']})\n"
            result += f"🛫 航线：{flight['departure_city']} → {flight['arrival_city']}\n"
            result += f"🕐 起飞时间：{flight['departure_time']}\n"
            result += f"🎫 余票：{flight['seats_available']}张\n\n"
            result += f"📊 价格详情：\n"
            result += f"  • 基础价格：¥{price_info['base_price']:.0f}\n"
            result += f"  • 实时价格：¥{realtime_price:.0f}\n"
            
            if price_info['price_change'] > 0:
                result += f"  • 价格变动：↑ +¥{price_info['price_change']:.0f}\n"
            elif price_info['price_change'] < 0:
                result += f"  • 价格变动：↓ -¥{abs(price_info['price_change']):.0f}\n"
            
            if price_info['factors']:
                result += f"  • 变动原因：{', '.join(price_info['factors'])}\n"
            
            result += f"\n⏰ 报价时间：{price_info['query_time']}\n\n"
            result += f"⚠️ 机票价格实时波动，以上价格仅供参考。\n"
            result += f"💡 如确认预订，请回复：确认预订航班 {flight_number}\n"
            result += f"   或调用时设置 confirm_price=True"
            return result
        
        # 用户已确认，执行预订（使用实时价格）
        user_info = json.dumps({
            "passenger_name": passenger_name,
            "passenger_phone": passenger_phone,
            "base_price": flight['price'],
            "realtime_price": realtime_price,
            "price_query_time": price_info['query_time']
        }, ensure_ascii=False)
        
        cursor = await db.execute(
            """INSERT INTO orders (order_type, item_id, item_name, user_info, total_price, status)
               VALUES ('flight', ?, ?, ?, ?, 'confirmed')""",
            (flight['id'], f"{flight['flight_number']} {flight['departure_city']}-{flight['arrival_city']}",
             user_info, realtime_price)
        )
        order_id = cursor.lastrowid
        
        # 更新余票
        await db.execute(
            "UPDATE flights SET seats_available = seats_available - 1 WHERE id = ?",
            (flight['id'],)
        )
        
        await db.commit()
        
        return f"""✅ 机票预订成功！

📋 订单号：{order_id}
✈️ 航班：{flight['flight_number']} ({flight['airline']})
🛫 航线：{flight['departure_city']} → {flight['arrival_city']}
🕐 起飞时间：{flight['departure_time']}
👤 乘客：{passenger_name}
💰 实时票价：¥{realtime_price:.0f}
📊 基础价格：¥{price_info['base_price']:.0f}
⏰ 锁价时间：{price_info['query_time']}

请妥善保管订单号，后续改签或退票需使用。"""


@tool
async def change_flight(
    order_id: int,
    new_flight_number: str
) -> str:
    """
    改签航班。
    
    Args:
        order_id: 原订单号
        new_flight_number: 新航班号
    
    Returns:
        改签结果
    """
    async with get_db() as db:
        # 查询原订单
        cursor = await db.execute(
            "SELECT * FROM orders WHERE id = ? AND order_type = 'flight' AND status != 'cancelled'",
            (order_id,)
        )
        order = await cursor.fetchone()
        
        if not order:
            return f"❌ 订单 {order_id} 不存在、不是机票订单或已取消。"
        
        # 查询新航班
        cursor = await db.execute(
            "SELECT * FROM flights WHERE flight_number = ? AND seats_available > 0",
            (new_flight_number,)
        )
        new_flight = await cursor.fetchone()
        
        if not new_flight:
            return f"❌ 新航班 {new_flight_number} 不存在或已无余票。"
        
        # 查询原航班
        cursor = await db.execute(
            "SELECT * FROM flights WHERE id = ?",
            (order['item_id'],)
        )
        old_flight = await cursor.fetchone()
        
        # 计算差价
        price_diff = new_flight['price'] - (old_flight['price'] if old_flight else 0)
        
        # 更新订单
        await db.execute(
            """UPDATE orders 
               SET item_id = ?, item_name = ?, total_price = ?, status = 'changed', updated_at = CURRENT_TIMESTAMP
               WHERE id = ?""",
            (new_flight['id'], f"{new_flight['flight_number']} {new_flight['departure_city']}-{new_flight['arrival_city']}",
             new_flight['price'], order_id)
        )
        
        # 更新余票
        await db.execute(
            "UPDATE flights SET seats_available = seats_available - 1 WHERE id = ?",
            (new_flight['id'],)
        )
        if old_flight:
            await db.execute(
                "UPDATE flights SET seats_available = seats_available + 1 WHERE id = ?",
                (old_flight['id'],)
            )
        
        await db.commit()
        
        diff_text = f"需补差价：¥{price_diff:.0f}" if price_diff > 0 else f"退还差价：¥{-price_diff:.0f}" if price_diff < 0 else "无需补差价"
        
        return f"""✅ 航班改签成功！

📋 订单号：{order_id}
✈️ 新航班：{new_flight['flight_number']} ({new_flight['airline']})
🛫 新航线：{new_flight['departure_city']} → {new_flight['arrival_city']}
🕐 起飞时间：{new_flight['departure_time']}
💰 {diff_text}

改签完成，请按时登机。"""


# ==================== 酒店相关工具 ====================

@tool
async def search_hotels(
    city: Optional[str] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None
) -> str:
    """
    查询酒店信息。
    
    Args:
        city: 城市名称（可选）
        max_price: 最高价格/晚（可选）
        min_rating: 最低评分（可选）
    
    Returns:
        符合条件的酒店列表
    """
    async with get_db() as db:
        query = "SELECT * FROM hotels WHERE rooms_available > 0"
        params = []
        
        if city:
            query += " AND city = ?"
            params.append(city)
        if max_price:
            query += " AND price_per_night <= ?"
            params.append(max_price)
        if min_rating:
            query += " AND rating >= ?"
            params.append(min_rating)
        
        query += " ORDER BY rating DESC"
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        
        if not rows:
            return "未找到符合条件的酒店。"
        
        result = "🏨 酒店查询结果：\n\n"
        for row in rows:
            stars = "⭐" * int(row['rating'])
            result += f"【{row['name']}】{stars}\n"
            result += f"  地址：{row['city']} {row['address']}\n"
            result += f"  价格：¥{row['price_per_night']:.0f}/晚 | 空房：{row['rooms_available']}间\n"
            result += f"  设施：{row['amenities']}\n\n"
        
        return result


@tool
async def book_hotel(
    hotel_name: str,
    guest_name: str,
    guest_phone: str,
    check_in_date: str,
    nights: int = 1,
    room_type: str = "标准间",
    confirm_price: bool = False
) -> str:
    """
    预订酒店。
    
    注意：酒店价格根据入住日期和房态实时调整，建议先调用 get_hotel_realtime_price 查询最新价格。
    如果您已确认价格，请设置 confirm_price=True 完成预订。
    
    Args:
        hotel_name: 酒店名称
        guest_name: 入住人姓名
        guest_phone: 联系电话
        check_in_date: 入住日期，格式 YYYY-MM-DD
        nights: 入住晚数，默认1晚
        room_type: 房型，默认标准间（可选：大床房、豪华间）
        confirm_price: 是否确认价格并完成预订，默认False（仅查询实时价格）
    
    Returns:
        预订结果；或实时价格信息（当confirm_price=False时）
    """
    async with get_db() as db:
        # 查询酒店
        cursor = await db.execute(
            "SELECT * FROM hotels WHERE name = ? AND rooms_available > 0",
            (hotel_name,)
        )
        hotel = await cursor.fetchone()
        
        if not hotel:
            return f"❌ 酒店「{hotel_name}」不存在或已无空房。"
        
        # 获取实时价格
        price_info = await price_service.fetch_hotel_realtime_price(
            hotel_name, hotel['price_per_night'], check_in_date
        )
        
        # 根据房型计算价格
        room_price_multiplier = 1.0
        for room in price_info['room_types']:
            if room['type'] == room_type:
                room_price_multiplier = room['price'] / price_info['realtime_price']
                break
        
        realtime_price_per_night = price_info['realtime_price'] * room_price_multiplier
        total_price = realtime_price_per_night * nights
        
        # 如果未确认价格，返回实时价格信息供用户确认
        if not confirm_price:
            result = f"💰 酒店实时报价\n\n"
            result += f"🏨 酒店：{hotel['name']}\n"
            result += f"📍 地址：{hotel['city']} {hotel['address']}\n"
            result += f"⭐ 评分：{hotel['rating']:.1f}/5.0\n"
            result += f"🛎️ 设施：{hotel['amenities']}\n"
            result += f"🛌 空房：{hotel['rooms_available']}间\n\n"
            result += f"📅 入住日期：{check_in_date}，共{nights}晚\n\n"
            result += f"📊 价格详情：\n"
            result += f"  • 基础价格：¥{price_info['base_price']:.0f}/晚\n"
            result += f"  • 实时价格：¥{price_info['realtime_price']:.0f}/晚\n"
            
            if price_info['price_change'] > 0:
                result += f"  • 价格变动：↑ +¥{price_info['price_change']:.0f}/晚\n"
            elif price_info['price_change'] < 0:
                result += f"  • 价格变动：↓ -¥{abs(price_info['price_change']):.0f}/晚\n"
            
            if price_info['factors']:
                result += f"  • 变动原因：{', '.join(price_info['factors'])}\n"
            
            result += f"\n🛏️ 可选房型：\n"
            for room in price_info['room_types']:
                selected = "✓ " if room['type'] == room_type else "  "
                total = room['price'] * nights
                result += f"  {selected}• {room['type']}：¥{room['price']:.0f}/晚 (总价¥{total:.0f})\n"
            
            result += f"\n💵 预估总价：¥{total_price:.0f}\n"
            result += f"⏰ 报价时间：{price_info['query_time']}\n\n"
            result += f"⚠️ 酒店价格受入住日期影响，以上价格仅供参考。\n"
            result += f"💡 如确认预订，请回复：确认预订酒店 {hotel_name}\n"
            result += f"   或调用时设置 confirm_price=True"
            return result
        
        # 用户已确认，执行预订（使用实时价格）
        user_info = json.dumps({
            "guest_name": guest_name,
            "guest_phone": guest_phone,
            "check_in_date": check_in_date,
            "nights": nights,
            "room_type": room_type,
            "base_price_per_night": hotel['price_per_night'],
            "realtime_price_per_night": realtime_price_per_night,
            "price_query_time": price_info['query_time']
        }, ensure_ascii=False)
        
        cursor = await db.execute(
            """INSERT INTO orders (order_type, item_id, item_name, user_info, total_price, status)
               VALUES ('hotel', ?, ?, ?, ?, 'confirmed')""",
            (hotel['id'], hotel['name'], user_info, total_price)
        )
        order_id = cursor.lastrowid
        
        # 更新空房
        await db.execute(
            "UPDATE hotels SET rooms_available = rooms_available - 1 WHERE id = ?",
            (hotel['id'],)
        )
        
        await db.commit()
        
        return f"""✅ 酒店预订成功！

📋 订单号：{order_id}
🏨 酒店：{hotel['name']}
📍 地址：{hotel['city']} {hotel['address']}
🛏️ 房型：{room_type}
📅 入住：{check_in_date}，共{nights}晚
👤 入住人：{guest_name}
💰 实时房价：¥{realtime_price_per_night:.0f}/晚
💵 总价：¥{total_price:.0f}
📊 基础价格：¥{price_info['base_price']:.0f}/晚
⏰ 锁价时间：{price_info['query_time']}

请按时入住，祝您旅途愉快！"""


# ==================== 旅游产品相关工具 ====================

@tool
async def search_products(
    destination: Optional[str] = None,
    max_price: Optional[float] = None
) -> str:
    """
    查询旅游产品。
    
    Args:
        destination: 目的地（可选）
        max_price: 最高价格（可选）
    
    Returns:
        符合条件的旅游产品列表
    """
    async with get_db() as db:
        query = "SELECT * FROM products WHERE available = 1"
        params = []
        
        if destination:
            query += " AND destination = ?"
            params.append(destination)
        if max_price:
            query += " AND price <= ?"
            params.append(max_price)
        
        query += " ORDER BY price"
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        
        if not rows:
            return "未找到符合条件的旅游产品。"
        
        result = "🎒 旅游产品查询结果：\n\n"
        for row in rows:
            result += f"【{row['name']}】\n"
            result += f"  目的地：{row['destination']} | 时长：{row['duration_days']}天\n"
            result += f"  描述：{row['description']}\n"
            result += f"  价格：¥{row['price']:.0f}\n"
            result += f"  包含：{row['includes']}\n\n"
        
        return result


@tool
async def book_product(
    product_name: str,
    traveler_name: str,
    traveler_phone: str,
    travel_date: str,
    people_count: int = 1,
    confirm_price: bool = False
) -> str:
    """
    预订旅游产品。
    
    注意：旅游产品价格根据季节和活动实时调整，建议先调用 get_product_realtime_price 查询最新价格。
    如果您已确认价格，请设置 confirm_price=True 完成预订。
    
    Args:
        product_name: 产品名称
        traveler_name: 出行人姓名
        traveler_phone: 联系电话
        travel_date: 出行日期，格式 YYYY-MM-DD
        people_count: 出行人数，默认1人
        confirm_price: 是否确认价格并完成预订，默认False（仅查询实时价格）
    
    Returns:
        预订结果；或实时价格信息（当confirm_price=False时）
    """
    async with get_db() as db:
        # 查询产品
        cursor = await db.execute(
            "SELECT * FROM products WHERE name = ? AND available = 1",
            (product_name,)
        )
        product = await cursor.fetchone()
        
        if not product:
            return f"❌ 旅游产品「{product_name}」不存在或已下架。"
        
        # 获取实时价格
        price_info = await price_service.fetch_product_realtime_price(
            product_name, product['price'], travel_date
        )
        
        realtime_price = price_info['realtime_price']
        
        # 检查是否满足团购条件
        group_price = realtime_price
        group_applied = False
        if price_info['group_discount'] and people_count >= price_info['group_discount']['min_people']:
            group_price = price_info['group_discount']['discount_price']
            group_applied = True
        
        final_price_per_person = group_price
        total_price = final_price_per_person * people_count
        
        # 如果未确认价格，返回实时价格信息供用户确认
        if not confirm_price:
            result = f"💰 旅游产品实时报价\n\n"
            result += f"🎒 产品：{product['name']}\n"
            result += f"📍 目的地：{product['destination']}\n"
            result += f"⏱️ 时长：{product['duration_days']}天\n"
            result += f"📝 描述：{product['description']}\n"
            result += f"🎁 包含：{product['includes']}\n\n"
            result += f"📅 出行日期：{travel_date}\n"
            result += f"👥 出行人数：{people_count}人\n\n"
            result += f"📊 价格详情：\n"
            result += f"  • 基础价格：¥{price_info['base_price']:.0f}/人\n"
            result += f"  • 实时价格：¥{realtime_price:.0f}/人\n"
            
            if price_info['price_change'] > 0:
                result += f"  • 价格变动：↑ +¥{price_info['price_change']:.0f}/人\n"
            elif price_info['price_change'] < 0:
                result += f"  • 价格变动：↓ -¥{abs(price_info['price_change']):.0f}/人\n"
            
            if price_info['factors']:
                result += f"  • 变动原因：{', '.join(price_info['factors'])}\n"
            
            if price_info['group_discount']:
                discount = price_info['group_discount']
                result += f"\n👥 团购优惠：\n"
                result += f"  • {discount['min_people']}人及以上成团可享团购价\n"
                result += f"  • 团购价：¥{discount['discount_price']:.0f}/人\n"
                if group_applied:
                    result += f"  • ✓ 已满足团购条件，已应用团购价！\n"
                else:
                    result += f"  • 当前{people_count}人，还需{discount['min_people'] - people_count}人可享团购价\n"
            
            result += f"\n💵 单价：¥{final_price_per_person:.0f}/人\n"
            result += f"💵 总价：¥{total_price:.0f} ({people_count}人)\n"
            result += f"⏰ 报价时间：{price_info['query_time']}\n\n"
            result += f"⚠️ 旅游产品价格受季节影响，以上价格仅供参考。\n"
            result += f"💡 如确认预订，请回复：确认预订产品 {product_name}\n"
            result += f"   或调用时设置 confirm_price=True"
            return result
        
        # 用户已确认，执行预订（使用实时价格）
        user_info = json.dumps({
            "traveler_name": traveler_name,
            "traveler_phone": traveler_phone,
            "travel_date": travel_date,
            "people_count": people_count,
            "base_price": product['price'],
            "realtime_price": realtime_price,
            "final_price_per_person": final_price_per_person,
            "group_applied": group_applied,
            "price_query_time": price_info['query_time']
        }, ensure_ascii=False)
        
        cursor = await db.execute(
            """INSERT INTO orders (order_type, item_id, item_name, user_info, total_price, status)
               VALUES ('product', ?, ?, ?, ?, 'confirmed')""",
            (product['id'], product['name'], user_info, total_price)
        )
        order_id = cursor.lastrowid
        
        await db.commit()
        
        group_info = ""
        if group_applied:
            group_info = f"\n👥 团购优惠：已应用团购价，每人节省¥{realtime_price - final_price_per_person:.0f}"
        
        return f"""✅ 旅游产品预订成功！

📋 订单号：{order_id}
🎒 产品：{product['name']}
📍 目的地：{product['destination']}
📅 出行日期：{travel_date}
⏱️ 时长：{product['duration_days']}天
👤 出行人：{traveler_name}
👥 人数：{people_count}人
💰 实时价格：¥{final_price_per_person:.0f}/人
💵 总价：¥{total_price:.0f}
📊 基础价格：¥{price_info['base_price']:.0f}/人
⏰ 锁价时间：{price_info['query_time']}{group_info}
🎁 包含：{product['includes']}

祝您旅途愉快！"""


# ==================== 订单管理工具 ====================

@tool
async def list_orders(
    order_type: Optional[str] = None,
    status: Optional[str] = None
) -> str:
    """
    查询订单列表。
    
    Args:
        order_type: 订单类型：flight/hotel/product（可选）
        status: 订单状态：pending/confirmed/cancelled/changed（可选）
    
    Returns:
        订单列表
    """
    async with get_db() as db:
        query = "SELECT * FROM orders WHERE 1=1"
        params = []
        
        if order_type:
            query += " AND order_type = ?"
            params.append(order_type)
        if status:
            query += " AND status = ?"
            params.append(status)
        
        query += " ORDER BY created_at DESC"
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        
        if not rows:
            return "暂无订单记录。"
        
        type_icons = {"flight": "✈️", "hotel": "🏨", "product": "🎒"}
        status_text = {"pending": "待确认", "confirmed": "已确认", "cancelled": "已取消", "changed": "已改签"}
        
        result = "📋 订单列表：\n\n"
        for row in rows:
            icon = type_icons.get(row['order_type'], '📦')
            st = status_text.get(row['status'], row['status'])
            result += f"{icon} 订单号：{row['id']} | {st}\n"
            result += f"   项目：{row['item_name']}\n"
            result += f"   金额：¥{row['total_price']:.0f}\n"
            result += f"   时间：{row['created_at']}\n\n"
        
        return result


@tool
async def cancel_order(order_id: int) -> str:
    """
    取消订单。
    
    Args:
        order_id: 订单号
    
    Returns:
        取消结果
    """
    async with get_db() as db:
        # 查询订单
        cursor = await db.execute(
            "SELECT * FROM orders WHERE id = ? AND status != 'cancelled'",
            (order_id,)
        )
        order = await cursor.fetchone()
        
        if not order:
            return f"❌ 订单 {order_id} 不存在或已取消。"
        
        # 更新订单状态
        await db.execute(
            "UPDATE orders SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (order_id,)
        )
        
        # 恢复库存
        if order['order_type'] == 'flight':
            await db.execute(
                "UPDATE flights SET seats_available = seats_available + 1 WHERE id = ?",
                (order['item_id'],)
            )
        elif order['order_type'] == 'hotel':
            await db.execute(
                "UPDATE hotels SET rooms_available = rooms_available + 1 WHERE id = ?",
                (order['item_id'],)
            )
        
        await db.commit()
        
        return f"""✅ 订单已取消！

📋 订单号：{order_id}
📦 项目：{order['item_name']}
💰 已退款：¥{order['total_price']:.0f}

取消成功，欢迎再次预订。"""


# ==================== 智能推荐工具 ====================

@tool
async def recommend_travel_plan(
    destination: str,
    budget: float,
    days: int = 3
) -> str:
    """
    根据目的地和预算智能推荐旅游方案。
    
    Args:
        destination: 目的地城市
        budget: 预算金额
        days: 计划天数，默认3天
    
    Returns:
        推荐的旅游方案
    """
    async with get_db() as db:
        # 查询目的地的航班
        cursor = await db.execute(
            "SELECT * FROM flights WHERE arrival_city = ? AND seats_available > 0 ORDER BY price LIMIT 2",
            (destination,)
        )
        flights = await cursor.fetchall()
        
        # 查询目的地的酒店
        cursor = await db.execute(
            "SELECT * FROM hotels WHERE city = ? AND rooms_available > 0 ORDER BY rating DESC LIMIT 2",
            (destination,)
        )
        hotels = await cursor.fetchall()
        
        # 查询目的地的旅游产品
        cursor = await db.execute(
            "SELECT * FROM products WHERE destination = ? AND available = 1 ORDER BY price LIMIT 3",
            (destination,)
        )
        products = await cursor.fetchall()
        
        result = f"🎯 {destination} {days}天旅游方案推荐\n"
        result += f"💰 您的预算：¥{budget:.0f}\n\n"
        
        total_cost = 0
        
        # 推荐航班
        if flights:
            flight = flights[0]
            result += f"✈️ 推荐航班：{flight['flight_number']} ({flight['airline']})\n"
            result += f"   价格：¥{flight['price']:.0f}\n\n"
            total_cost += flight['price']
        else:
            result += "✈️ 暂无航班推荐\n\n"
        
        # 推荐酒店
        if hotels:
            hotel = hotels[0]
            hotel_cost = hotel['price_per_night'] * days
            result += f"🏨 推荐酒店：{hotel['name']}\n"
            result += f"   价格：¥{hotel['price_per_night']:.0f}/晚 × {days}晚 = ¥{hotel_cost:.0f}\n\n"
            total_cost += hotel_cost
        else:
            result += "🏨 暂无酒店推荐\n\n"
        
        # 推荐旅游产品
        if products:
            result += "🎒 推荐旅游产品：\n"
            for p in products:
                if total_cost + p['price'] <= budget:
                    result += f"   • {p['name']} - ¥{p['price']:.0f}\n"
                    total_cost += p['price']
        else:
            result += "🎒 暂无旅游产品推荐\n"
        
        result += f"\n💵 预估总花费：¥{total_cost:.0f}\n"
        
        if total_cost <= budget:
            result += f"✅ 在预算范围内，还剩余 ¥{budget - total_cost:.0f}\n\n"
            result += "如需预订，请告诉我：\n"
            result += "1. 您的姓名和联系电话\n"
            result += "2. 出行日期\n"
            result += "我将为您一键预订所有项目！"
        else:
            result += f"⚠️ 超出预算 ¥{total_cost - budget:.0f}，建议调整方案或增加预算。"
        
        return result


# 导出所有工具
ALL_TOOLS = [
    # 实时价格查询工具
    get_flight_realtime_price,
    get_hotel_realtime_price,
    get_product_realtime_price,
    # 航班相关工具
    search_flights,
    book_flight,
    change_flight,
    # 酒店相关工具
    search_hotels,
    book_hotel,
    # 旅游产品相关工具
    search_products,
    book_product,
    # 订单管理工具
    list_orders,
    cancel_order,
    # 智能推荐工具
    recommend_travel_plan,
]