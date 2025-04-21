from langchain_elasticsearch import ElasticsearchStore
from langchain_ollama import OllamaEmbeddings


def create_elastic_store():
    embed = OllamaEmbeddings(model="llama3.2:latest")
    return ElasticsearchStore(
        es_url="http://localhost:9200",
        index_name="langchain_index",
        embedding=embed,
)


class RetrieverUtils:
    @staticmethod
    def create_elasticsearch_Store(search_type,k):
        return create_elastic_store().as_retriever(
            search_type=search_type,
            search_kwargs={"k": k}
        )

