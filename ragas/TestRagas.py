from ragas import SingleTurnSample
from ragas.metrics import AspectCritic
from langchain_ollama import ChatOllama
from ragas.llms import LangchainLLMWrapper

test_data = {
    "user_input": "summarise given text\nThe company reported an 8% rise in Q3 2024, driven by strong performance in the Asian market. Sales in this region have significantly contributed to the overall growth. Analysts attribute this success to strategic marketing and product localization. The positive trend in the Asian market is expected to continue into the next quarter.",
    "response": "The company experienced an 8% increase in Q3 2024, largely due to effective marketing strategies and product adaptation, with expectations of continued growth in the coming quarter.",
}
llm = ChatOllama(base_url = "http://127.0.0.1:11434",model = "llama3.2:latest",temperature = 0.5,num_predict = 10000)
evaluator_llm = LangchainLLMWrapper(llm)

metric = AspectCritic(name="summary_accuracy",llm=llm, definition="Verify if the summary is accurate.")

def call_async_func():
   metric.single_turn_ascore(SingleTurnSample(**test_data))

call_async_func()