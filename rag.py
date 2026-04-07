from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def load_multiple_pdfs(file_paths):
    all_docs = []

    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        for doc in documents:
            doc.metadata["source"] = file_path

        all_docs.extend(documents)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=100
    )

    docs = splitter.split_documents(all_docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    db = Chroma.from_documents(docs, embeddings)

    return db