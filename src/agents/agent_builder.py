from langchain.agents import create_agent
from langchain_community.chat_models import ChatZhipuAI
from typing import List
from config.config import Config
from src.tools.search_tool import get_tools

class AgentBuilder:
    """Agent构建器"""

    def __init__(self):
        self.llm = None
        self.tools = None
        self.agent_graph = None

    def initialize_llm(self):
        """初始化语言模型"""
        self.llm = ChatZhipuAI(
            model=Config.MODEL_NAME,
            temperature=Config.MODEL_TEMPERATURE,
            zhipuai_api_key=Config.get_zhipuai_api_key()
        )
        return self.llm

    def initialize_tools(self):
        """初始化工具"""
        self.tools = get_tools()
        return self.tools

    def build_agent(self, debug: bool = False):
        """
        构建Agent

        Args:
            debug: 是否启用调试模式

        Returns:
            构建好的Agent graph
        """
        if not self.llm:
            self.initialize_llm()
        if not self.tools:
            self.initialize_tools()

        self.agent_graph = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=Config.SYSTEM_PROMPT,
            debug=debug
        )

        return self.agent_graph

    def get_agent(self):
        """获取已构建的Agent"""
        if not self.agent_graph:
            raise ValueError("Agent尚未构建，请先调用build_agent()")
        return self.agent_graph