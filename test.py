import os
import traceback
from dotenv import load_dotenv
from langchain_community.chat_models import ChatZhipuAI
from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage

# 加载 .env 里的 API Key
load_dotenv()

# 1. 初始化智谱对话模型
llm = ChatZhipuAI(
    model="glm-4",          # 可选 glm-3-turbo, glm-4, glm-5
    temperature=0.7,
    zhipuai_api_key=os.getenv("ZHIPUAI_API_KEY"),  # 从环境变量读取
    # zhipuai_api_base="https://open.bigmodel.cn/api/paas/v4/"  # 国内默认地址
)

# 2. 定义工具 - 网络搜索
search_tool = DuckDuckGoSearchRun(name="web_search", description="使用 DuckDuckGo 进行网络搜索")

# 工具列表
tools = [search_tool]


# 4. 创建 agent graph
agent_graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""你是一个专业AI助手，可以访问网络搜索工具来获取最新信息。
当用户询问需要最新信息的问题时，你必须使用网络搜索工具来获取准确信息。
如果用户的问题涉及实时信息、新闻、天气、股价等需要最新数据的内容，请使用搜索工具。""",
    debug=True  # 显示详细执行过程
)

# 6. 交互式对话
print("开始与智谱AI对话（具备网络搜索能力），输入 'exit' 或 'quit' 退出")
print("注意：Agent可以访问网络搜索工具来获取最新信息。")

# 初始化消息列表
messages = []

while True:
    # 获取用户输入
    user_input = input("\n你：")

    # 检查退出条件
    if user_input.lower() in ["exit", "quit", "退出"]:
        print("对话结束")
        break

    # 添加用户消息
    messages.append(HumanMessage(content=user_input))

    # 使用 agent graph 处理输入
    try:
        # 创建输入
        inputs = {"messages": messages}

        # 执行 agent
        result = agent_graph.invoke(inputs)

        if result and result.get("messages"):
            # 获取完整的消息历史（包括工具调用）
            all_messages = result["messages"]

            # 找到最后一条AIMessage作为回复
            ai_reply = None
            for msg in reversed(all_messages):
                if msg.type == "ai":
                    ai_reply = msg.content
                    break

            # 更新消息历史为完整对话
            messages = all_messages

            if ai_reply:
                # 安全打印，处理编码问题
                try:
                    print(f"\nAI：{ai_reply}")
                except UnicodeEncodeError:
                    # 如果编码失败，尝试使用GBK编码替换无法编码的字符
                    safe_reply = ai_reply.encode('gbk', errors='replace').decode('gbk')
                    print(f"\nAI：{safe_reply}")
            else:
                print("\nAI：未收到有效回复")
        else:
            print("\nAI：未收到有效回复")

    except Exception as e:
        print(f"调用API时出错：{e}")
        traceback.print_exc()
        continue