"""
LangGraph Agent 编排
构建 ReAct 风格的对话 Agent
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from typing import AsyncGenerator, List, Optional
import json

from ..core.config import settings
from .tools import ALL_TOOLS
from .prompts import SYSTEM_PROMPT


class TravelAgent:
    """旅行助手 Agent"""
    
    def __init__(self):
        """初始化 Agent"""
        # 创建 LLM 实例
        self.llm = ChatOpenAI(
            model=settings.MODEL_NAME,
            api_key=settings.API_KEY,
            base_url=settings.API_BASE_URL,
            temperature=0.7,
            streaming=True,
        )
        
        # 绑定工具
        self.llm_with_tools = self.llm.bind_tools(ALL_TOOLS)
        
        # 内存检查点（用于保持对话历史）
        self.checkpointer = MemorySaver()
        
        # 创建 ReAct Agent（已编译好的图）
        self.app = create_react_agent(
            self.llm,
            ALL_TOOLS,
            state_modifier=SYSTEM_PROMPT,
            checkpointer=self.checkpointer,
        )
    
    async def chat(
        self,
        message: str,
        thread_id: str = "default",
        history: Optional[List[dict]] = None
    ) -> AsyncGenerator[str, None]:
        """
        与 Agent 对话（流式输出）
        
        Args:
            message: 用户消息
            thread_id: 会话 ID
            history: 历史消息列表
        
        Yields:
            流式输出的文本片段
        """
        # 构建消息
        messages = []
        if history:
            for msg in history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
        
        messages.append(HumanMessage(content=message))
        
        # 配置
        config = {"configurable": {"thread_id": thread_id}}
        
        # 流式调用 Agent
        full_response = ""
        async for event in self.app.astream_events(
            {"messages": messages},
            config=config,
            version="v2"
        ):
            kind = event["event"]
            
            # 工具调用开始
            if kind == "on_tool_start":
                tool_name = event["name"]
                tool_input = event["data"].get("input", {})
                yield f"\n🔧 正在调用工具: {tool_name}...\n"
            
            # 工具调用结束
            elif kind == "on_tool_end":
                tool_name = event["name"]
                yield f"✅ 工具 {tool_name} 执行完成\n\n"
            
            # LLM 生成 token
            elif kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    full_response += content
                    yield content
        
        # 如果没有流式输出，尝试获取完整响应
        if not full_response:
            result = await self.app.ainvoke(
                {"messages": messages},
                config=config
            )
            if result and "messages" in result:
                last_message = result["messages"][-1]
                if hasattr(last_message, "content"):
                    yield last_message.content
    
    async def chat_sync(
        self,
        message: str,
        thread_id: str = "default"
    ) -> str:
        """
        与 Agent 对话（同步返回完整结果）
        
        Args:
            message: 用户消息
            thread_id: 会话 ID
        
        Returns:
            完整的响应文本
        """
        config = {"configurable": {"thread_id": thread_id}}
        
        result = await self.app.ainvoke(
            {"messages": [HumanMessage(content=message)]},
            config=config
        )
        
        if result and "messages" in result:
            last_message = result["messages"][-1]
            if hasattr(last_message, "content"):
                return last_message.content
        
        return "抱歉，我暂时无法处理您的请求，请稍后再试。"


# 全局 Agent 实例
_agent_instance: Optional[TravelAgent] = None


def get_agent() -> TravelAgent:
    """获取 Agent 单例"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = TravelAgent()
    return _agent_instance