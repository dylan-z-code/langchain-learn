import traceback
from langchain_core.messages import HumanMessage
from typing import List, Dict, Any

class ConversationHandler:
    """对话处理器"""

    def __init__(self):
        self.messages = []

    def add_user_message(self, content: str):
        """添加用户消息"""
        self.messages.append(HumanMessage(content=content))

    def get_messages(self) -> List:
        """获取所有消息"""
        return self.messages

    def update_messages(self, new_messages: List):
        """更新消息历史"""
        self.messages = new_messages

    def get_ai_reply(self, agent_result: Dict[str, Any]) -> str:
        """
        从Agent结果中提取AI回复

        Args:
            agent_result: Agent执行结果

        Returns:
            str: AI回复内容，如果未找到返回None
        """
        if not agent_result or not agent_result.get("messages"):
            return None

        all_messages = agent_result["messages"]

        # 找到最后一条AIMessage
        for msg in reversed(all_messages):
            if msg.type == "ai":
                return msg.content

        return None

    def safe_print(self, text: str, prefix: str = "AI") -> str:
        """
        安全打印文本，处理编码问题

        Args:
            text: 要打印的文本
            prefix: 前缀

        Returns:
            str: 安全处理后的文本
        """
        try:
            output = f"\n{prefix}：{text}"
            print(output)
            return text
        except UnicodeEncodeError:
            # 如果编码失败，尝试使用GBK编码替换无法编码的字符
            safe_text = text.encode('gbk', errors='replace').decode('gbk')
            output = f"\n{prefix}：{safe_text}"
            print(output)
            return safe_text

    def handle_exception(self, e: Exception):
        """处理异常"""
        print(f"调用API时出错：{e}")
        traceback.print_exc()