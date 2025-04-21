from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

@tool
def add(a: int, b: int) -> int:
    """Add two numbers and return a result."""
    return a - b

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

# 此时每一个@tool函数就成为了一个tool，我们就可以像上面的wikipedia一样直接invoke或者run。
# print(multiply.invoke({"a": 1, "b": 2}))

# 构建一个map，py的语法糖好用
tools = [wikipedia,add,subtract,multiply,divide]
map_of_tools = {tool.name:tool for tool in tools}
#print(map_of_tools)


llm = ChatOllama(
    base_url = "http://127.0.0.1:11434",
    model = "llama3.2:latest",
    temperature = 0.5,
    num_predict = 10000
)

# 构建绑定tools的模型对象，把tools都传进去
llm_bind_tools = llm.bind_tools(tools=tools)
# 执行问题
resp = llm_bind_tools.invoke("1+1 = ？")
print(resp)