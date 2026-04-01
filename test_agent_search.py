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

# 3. 创建 agent graph
agent_graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""你是一个专业AI助手，可以访问网络搜索工具来获取最新信息。
当用户询问需要最新信息的问题时，你必须使用网络搜索工具来获取准确信息。
如果用户的问题涉及实时信息、新闻、天气、股价等需要最新数据的内容，请使用搜索工具。""",
    debug=False  # 显示详细执行过程
)

# 测试搜索功能
print("测试Agent搜索功能...")
print("=" * 50)

# 测试问题列表
test_questions = [
    "今天北京天气怎么样？",
    "最新的科技新闻有哪些？",
    "谁是现在的美国总统？",
    "hello"
]

for question in test_questions:
    print(f"\n测试问题：{question}")
    print("-" * 30)

    # 创建消息
    messages = [HumanMessage(content=question)]
    inputs = {"messages": messages}

    try:
        # 执行 agent
        result = agent_graph.invoke(inputs)

        if result and result.get("messages"):
            # 获取所有消息
            all_messages = result["messages"]

            # 打印消息类型和内容
            print(f"收到 {len(all_messages)} 条消息：")
            for i, msg in enumerate(all_messages):
                try:
                    preview = msg.content[:100] if msg.content else ""
                    print(f"  消息{i+1}: 类型={msg.type}, 内容={preview}...")
                except UnicodeEncodeError:
                    # 如果编码失败，打印repr版本
                    print(f"  消息{i+1}: 类型={msg.type}, 内容={repr(msg.content[:100])}...")

            # 找到最后一条AIMessage
            ai_reply = None
            for msg in reversed(all_messages):
                if msg.type == "ai":
                    ai_reply = msg.content
                    break

            if ai_reply:
                print(f"\nAI回复：{ai_reply}")
            else:
                print("\n未找到AI回复")
        else:
            print("未收到有效结果")

    except Exception as e:
        print(f"调用API时出错：{e}")
        traceback.print_exc()

    print("=" * 50)