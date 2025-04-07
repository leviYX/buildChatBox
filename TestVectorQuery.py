from langchain_ollama import OllamaEmbeddings
from langchain_elasticsearch import ElasticsearchStore



# 向量化
embed = OllamaEmbeddings(model="llama3.2:latest")

# 存储es
elastic_vector_search = ElasticsearchStore(
    es_url="http://localhost:9200",
    index_name="langchain_index",
    embedding=embed,
)


results = elastic_vector_search.similarity_search_with_score(
    query="白洁就睡去了",
    k=1,
)
for doc, score in results:
    print(f"* [SIM={score:3f}] {doc.page_content} [{doc.metadata}]")