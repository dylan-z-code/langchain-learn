import os
from dotenv import load_dotenv
from typing import Optional

# 加载环境变量
load_dotenv()

class Config:
    """配置文件管理类"""

    # API配置
    ZHIPUAI_API_KEY = os.getenv("ZHIPUAI_API_KEY")

    # 模型配置
    MODEL_NAME = "glm-4"
    MODEL_TEMPERATURE = 0.7

    # Agent配置
    SYSTEM_PROMPT = """你是一个专业AI助手，可以访问网络搜索工具来获取最新信息。
当用户询问需要最新信息的问题时，你必须使用网络搜索工具来获取准确信息。
如果用户的问题涉及实时信息、新闻、天气、股价等需要最新数据的内容，请使用搜索工具。"""

    # 工具配置
    SEARCH_TOOL_NAME = "web_search"
    SEARCH_TOOL_DESCRIPTION = "使用 DuckDuckGo 进行网络搜索"

    @classmethod
    def validate_config(cls) -> bool:
        """验证配置是否完整"""
        if not cls.ZHIPUAI_API_KEY:
            print("错误：未找到ZHIPUAI_API_KEY环境变量")
            print("请在.env文件中设置ZHIPUAI_API_KEY=your_api_key")
            return False
        return True

    @classmethod
    def get_zhipuai_api_key(cls) -> str:
        """获取智谱API密钥"""
        return cls.ZHIPUAI_API_KEY