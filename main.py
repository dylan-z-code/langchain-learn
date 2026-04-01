#!/usr/bin/env python
"""
主应用入口
具备网络搜索能力的智谱AI对话Agent
"""

import sys
from config.config import Config
from src.agents.agent_builder import AgentBuilder
from src.utils.conversation_handler import ConversationHandler

def main():
    """主函数"""
    # 验证配置
    if not Config.validate_config():
        sys.exit(1)

    print("开始与智谱AI对话（具备网络搜索能力），输入 'exit' 或 'quit' 退出")
    print("注意：Agent可以访问网络搜索工具来获取最新信息。")

    # 初始化组件
    agent_builder = AgentBuilder()
    conversation_handler = ConversationHandler()

    try:
        # 构建Agent
        agent_graph = agent_builder.build_agent(debug=False)
    except Exception as e:
        print(f"初始化Agent失败：{e}")
        sys.exit(1)

    # 主对话循环
    while True:
        try:
            # 获取用户输入
            user_input = input("\n你：")

            # 检查退出条件
            if user_input.lower() in ["exit", "quit", "退出"]:
                print("对话结束")
                break

            # 添加用户消息
            conversation_handler.add_user_message(user_input)

            # 准备输入
            inputs = {"messages": conversation_handler.get_messages()}

            # 执行Agent
            result = agent_graph.invoke(inputs)

            # 处理结果
            ai_reply = conversation_handler.get_ai_reply(result)

            if ai_reply:
                # 安全打印回复
                conversation_handler.safe_print(ai_reply, "AI")

                # 更新消息历史
                if result and result.get("messages"):
                    conversation_handler.update_messages(result["messages"])
            else:
                print("\nAI：未收到有效回复")

        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
            break
        except Exception as e:
            conversation_handler.handle_exception(e)

if __name__ == "__main__":
    main()