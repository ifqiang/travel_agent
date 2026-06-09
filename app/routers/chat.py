"""
聊天路由
提供与 AI Agent 对话的接口
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import json
import re

from ..agent.graph import get_agent
from ..db.connection import get_db

router = APIRouter(prefix="/chat", tags=["chat"])


def is_quota_error(error: Exception) -> bool:
    """检查是否为配额不足错误"""
    error_str = str(error).lower()
    patterns = [
        "insufficient_user_quota",
        "quota is not enough",
        "user quota",
        "403",
        "rate limit",
        "exceeded",
    ]
    return any(pattern in error_str for pattern in patterns)


def get_quota_error_message() -> str:
    """获取配额不足的友好提示"""
    return "⚠️ API 调用配额已用尽，暂时无法继续对话。\n\n可能的原因：\n• API Key 的免费额度已用完\n• 请求频率超限\n\n建议：\n• 稍后再试\n• 检查 API Key 配额状态\n• 联系管理员充值或更换 API Key"


class ChatRequest(BaseModel):
    """聊天请求"""
    message: str
    thread_id: Optional[str] = "default"
    session_id: Optional[str] = None  # 会话ID，用于对话历史存储
    history: Optional[List[dict]] = None


class ChatResponse(BaseModel):
    """聊天响应"""
    response: str


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    与 AI Agent 对话（同步返回）

    Args:
        request: 聊天请求

    Returns:
        完整的响应
    """
    try:
        agent = get_agent()
        response = await agent.chat_sync(
            message=request.message,
            thread_id=request.thread_id or "default"
        )
        return ChatResponse(response=response)
    except Exception as e:
        # 检查是否为配额不足错误
        if is_quota_error(e):
            return ChatResponse(response=get_quota_error_message())
        raise HTTPException(status_code=500, detail=str(e))


async def save_message(session_id: str, role: str, content: str) -> None:
    """保存对话消息到数据库"""
    async with get_db() as db:
        await db.execute(
            "INSERT INTO conversations (session_id, role, content) VALUES (?, ?, ?)",
            (session_id, role, content)
        )
        await db.commit()


async def get_conversation_history(session_id: str, limit: int = 50) -> List[dict]:
    """获取对话历史"""
    async with get_db() as db:
        cursor = await db.execute(
            """
            SELECT role, content, created_at 
            FROM conversations 
            WHERE session_id = ? 
            ORDER BY created_at ASC 
            LIMIT ?
            """,
            (session_id, limit)
        )
        rows = await cursor.fetchall()
        return [{"role": row["role"], "content": row["content"]} for row in rows]


@router.get("/history/{session_id}")
async def get_history(session_id: str, limit: int = 50):
    """
    获取指定会话的对话历史

    Args:
        session_id: 会话ID
        limit: 返回消息数量限制

    Returns:
        对话历史列表
    """
    history = await get_conversation_history(session_id, limit)
    return {"session_id": session_id, "history": history, "count": len(history)}


@router.get("/sessions")
async def get_all_sessions():
    """
    获取所有会话列表

    Returns:
        会话列表，包含每个会话的ID、最后一条消息和消息数量
    """
    async with get_db() as db:
        cursor = await db.execute("""
            SELECT session_id, content, created_at
            FROM conversations
            WHERE role = 'user'
            ORDER BY created_at DESC
        """)
        rows = await cursor.fetchall()
        
        sessions = {}
        for row in rows:
            session_id = row["session_id"]
            if session_id not in sessions:
                sessions[session_id] = {
                    "session_id": session_id,
                    "last_message": row["content"],
                    "created_at": row["created_at"]
                }
        
        for session_id in sessions:
            cursor = await db.execute(
                "SELECT COUNT(*) as count FROM conversations WHERE session_id = ?",
                (session_id,)
            )
            count = (await cursor.fetchone())["count"]
            sessions[session_id]["message_count"] = count
        
        return {"sessions": list(sessions.values()), "total": len(sessions)}


@router.delete("/history")
async def clear_all_history():
    """
    清空所有会话历史

    Returns:
        操作结果
    """
    async with get_db() as db:
        await db.execute("DELETE FROM conversations")
        await db.commit()
    return {"success": True, "message": "所有会话历史已清空"}


@router.delete("/history/{session_id}")
async def clear_history(session_id: str):
    """
    清空指定会话的对话历史

    Args:
        session_id: 会话ID

    Returns:
        操作结果
    """
    async with get_db() as db:
        await db.execute(
            "DELETE FROM conversations WHERE session_id = ?",
            (session_id,)
        )
        await db.commit()
    return {"success": True, "message": f"会话 {session_id} 的历史已清空"}


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    与 AI Agent 对话（流式返回 SSE）

    Args:
        request: 聊天请求

    Returns:
        SSE 流式响应
    """
    async def generate():
        session_id = request.session_id or request.thread_id or "default"
        full_response = ""

        try:
            # 保存用户消息
            if request.session_id:
                await save_message(session_id, "user", request.message)

            # 获取历史对话作为上下文
            db_history = []
            if request.session_id:
                db_history = await get_conversation_history(session_id, limit=20)

            agent = get_agent()
            async for chunk in agent.chat(
                message=request.message,
                thread_id=request.thread_id or "default",
                history=request.history or db_history
            ):
                full_response += chunk
                # SSE 格式
                yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"

            # 保存AI响应
            if request.session_id and full_response:
                await save_message(session_id, "assistant", full_response)

            # 发送结束标记
            yield f"data: {json.dumps({'done': True}, ensure_ascii=False)}\n\n"
        except Exception as e:
            # 检查是否为配额不足错误
            if is_quota_error(e):
                error_msg = get_quota_error_message()
                yield f"data: {json.dumps({'content': error_msg}, ensure_ascii=False)}\n\n"
                if request.session_id:
                    await save_message(session_id, "assistant", error_msg)
                yield f"data: {json.dumps({'done': True}, ensure_ascii=False)}\n\n"
            else:
                yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )