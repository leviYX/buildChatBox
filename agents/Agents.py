from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent,AgentType
from dotenv import load_dotenv

llm = ChatOllama(base_url = "http://127.0.0.1:11434",model = "huihui_ai/deepseek-r1-abliterated:14b",temperature = 0.5,num_predict = 10000)
load = load_dotenv("./.env")

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
@tool
def add(a: int, b: int) -> int:
    "Add two numbers and return a result."
    return int(a) + int(b)

@tool
def subtract(a: int, b: int) -> int:
    """Subtract two numbers and return a result."""
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return a result."""
    return a * b

@tool
def divide(a: int, b: int) -> int:
    """Divide two numbers and return a result."""
    return int(a / b)

tools = [wikipedia,add,subtract,multiply,divide]
map_of_tools = {tool.name:tool for tool in tools}

# 构建一个agent，传入llm和tools。并且指定agent类型是AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION，这样可以给我们的tool传参
# verbose表示详细输出处理过程
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

prompt_template = ChatPromptTemplate([
    ("system", "你是一个数学专家并且还是一个篮球体育专家"),
    ("user", "1 + 2等于多少?"),
    ("user", "科比是谁?"),
    ("user", "请把答案给我用json的格式返回。")

])
query = 'Whats is the sum of 1 and  2 .  Who is kobe?'
resp = agent.run(prompt_template)
print(resp)











