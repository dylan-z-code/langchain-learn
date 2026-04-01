from langchain_community.tools import DuckDuckGoSearchRun
from typing import List
from config.config import Config

def create_search_tool():
    """
    创建网络搜索工具

    Returns:
        DuckDuckGoSearchRun: 搜索工具实例
    """
    return DuckDuckGoSearchRun(
        name=Config.SEARCH_TOOL_NAME,
        description=Config.SEARCH_TOOL_DESCRIPTION
    )

def get_tools() -> List:
    """
    获取所有可用工具列表

    Returns:
        List: 工具列表
    """
    return [create_search_tool()]