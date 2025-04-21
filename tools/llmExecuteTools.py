from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

llm = ChatOllama(base_url = "http://127.0.0.1:11434",model = "llama3.2:latest",temperature = 0.5,num_predict = 10000)

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

tools = [wikipedia,add,subtract,multiply,divide]
map_of_tools = {tool.name:tool for tool in tools}

# 初始问题
query = "In which year did Messi win the World Cup championship？"
message = [HumanMessage(query)]

# 构建绑定tools的模型对象，把tools都传进去
llm_bind_tools = llm.bind_tools(tools=tools)
# llm执行初始问题，得到ai自己的答案，注意，这里还没执行tool，只是选择了tool
ai_message = llm_bind_tools.invoke(message)

# 初始问题也就是人的问题，然后把ai的答案拼起来，此时得到了两个信息
message.append(ai_message)

# 遍历ai的执行结果，取出他选择的tool
for tool_call in ai_message.tool_calls:
    # 统一小写
    tool_name = tool_call['name'].lower()
    # 从map映射取出对应的tool
    execute_tool = map_of_tools[tool_name]
    # 执行tool，并且把tool_call传入，其实这个tool_call是个map结构，正是参数
    print(tool_call)
    tool_invoke = execute_tool.invoke(tool_call)
    message.append(tool_invoke)

print(message)
# 把人的问题，ai的结果，以及tool都整合到一个message里面，让tool大模型去执行，最后就是最终结果了。
final_output = llm_bind_tools.invoke(message)
print(final_output)

