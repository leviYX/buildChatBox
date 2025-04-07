from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    file_path = "./test.pdf",
    # headers = None
    # password = None,
    mode = "single",
    pages_delimiter = "",
    # extract_images = True, # images_parser = RapidOCRBlobParser(),
)

docs = []
docs_lazy = loader.lazy_load()

for doc in docs_lazy:
    docs.append(doc)
print(docs[0].page_content[:1000])
print(docs[0].metadata)
