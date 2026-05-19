"""
订单管理路由
提供订单查询、取消等接口
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
import aiosqlite

from ..db.connection import get_db

router = APIRouter(prefix="/orders", tags=["orders"])


class OrderType(str, Enum):
    """订单类型枚举"""
    flight = "flight"
    hotel = "hotel"
    product = "product"


class OrderStatus(str, Enum):
    """订单状态枚举"""
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    changed = "changed"


class OrderResponse(BaseModel):
    """订单响应模型"""
    id: int
    order_type: str
    item_name: str
    total_price: float
    status: str
    created_at: str
    updated_at: Optional[str] = None


class OrderListResponse(BaseModel):
    """订单列表响应"""
    total: int
    orders: List[OrderResponse]


class CancelResponse(BaseModel):
    """取消订单响应"""
    success: bool
    message: str
    order_id: int


@router.get("", response_model=OrderListResponse)
async def list_orders(
    order_type: Optional[OrderType] = Query(None, description="订单类型筛选"),
    status: Optional[OrderStatus] = Query(None, description="订单状态筛选"),
    limit: int = Query(20, ge=1, le=100, description="返回数量限制"),
    offset: int = Query(0, ge=0, description="偏移量")
):
    """
    查询订单列表
    
    Args:
        order_type: 订单类型筛选（flight/hotel/product）
        status: 订单状态筛选（pending/confirmed/cancelled/changed）
        limit: 返回数量限制
        offset: 偏移量（分页）
    
    Returns:
        订单列表
    """
    async with get_db() as db:
        # 构建查询
        count_query = "SELECT COUNT(*) as total FROM orders WHERE 1=1"
        data_query = "SELECT * FROM orders WHERE 1=1"
        params = []
        
        if order_type:
            count_query += " AND order_type = ?"
            data_query += " AND order_type = ?"
            params.append(order_type.value)
        
        if status:
            count_query += " AND status = ?"
            data_query += " AND status = ?"
            params.append(status.value)
        
        # 获取总数
        cursor = await db.execute(count_query, params)
        total = (await cursor.fetchone())["total"]
        
        # 获取数据
        data_query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor = await db.execute(data_query, params)
        rows = await cursor.fetchall()
        
        orders = [
            OrderResponse(
                id=row["id"],
                order_type=row["order_type"],
                item_name=row["item_name"],
                total_price=row["total_price"],
                status=row["status"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )
            for row in rows
        ]
        
        return OrderListResponse(total=total, orders=orders)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int):
    """
    获取订单详情
    
    Args:
        order_id: 订单号
    
    Returns:
        订单详情
    """
    async with get_db() as db:
        cursor = await db.execute(
            "SELECT * FROM orders WHERE id = ?",
            (order_id,)
        )
        row = await cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"订单 {order_id} 不存在")
        
        return OrderResponse(
            id=row["id"],
            order_type=row["order_type"],
            item_name=row["item_name"],
            total_price=row["total_price"],
            status=row["status"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )


@router.post("/{order_id}/cancel", response_model=CancelResponse)
async def cancel_order(order_id: int):
    """
    取消订单
    
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
            raise HTTPException(
                status_code=400,
                detail=f"订单 {order_id} 不存在或已取消"
            )
        
        # 更新订单状态
        await db.execute(
            "UPDATE orders SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (order_id,)
        )
        
        # 恢复库存
        if order["order_type"] == "flight":
            await db.execute(
                "UPDATE flights SET seats_available = seats_available + 1 WHERE id = ?",
                (order["item_id"],)
            )
        elif order["order_type"] == "hotel":
            await db.execute(
                "UPDATE hotels SET rooms_available = rooms_available + 1 WHERE id = ?",
                (order["item_id"],)
            )
        
        await db.commit()
        
        return CancelResponse(
            success=True,
            message=f"订单 {order_id} 已成功取消，退款 ¥{order['total_price']:.0f}",
            order_id=order_id
        )


@router.get("/stats/summary")
async def get_order_stats():
    """
    获取订单统计摘要
    
    Returns:
        各类型订单数量和金额统计
    """
    async with get_db() as db:
        # 按类型统计
        cursor = await db.execute("""
            SELECT 
                order_type,
                COUNT(*) as count,
                SUM(total_price) as total_amount
            FROM orders
            WHERE status != 'cancelled'
            GROUP BY order_type
        """)
        type_stats = await cursor.fetchall()
        
        # 按状态统计
        cursor = await db.execute("""
            SELECT 
                status,
                COUNT(*) as count
            FROM orders
            GROUP BY status
        """)
        status_stats = await cursor.fetchall()
        
        return {
            "by_type": {
                row["order_type"]: {
                    "count": row["count"],
                    "total_amount": row["total_amount"] or 0
                }
                for row in type_stats
            },
            "by_status": {
                row["status"]: row["count"]
                for row in status_stats
            }
        }