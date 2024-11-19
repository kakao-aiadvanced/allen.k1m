import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_docs():
    # Load, chunk and index the contents of the blog.
    loader = WebBaseLoader(
        web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
    )
    return loader.load()


def split_docs(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(docs)


def retrieve_from_vectorstore(splits):
    # Retrieve and generate using the relevant snippets of the blog.
    vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever()
    return retriever


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_prompt():
    return hub.pull("rlm/rag-prompt")


def example_v1():
    docs = load_docs()
    splits = split_docs(docs)
    retriever = retrieve_from_vectorstore(splits)

    prompt = get_prompt()
    llm = ChatOpenAI(model="gpt-4o-mini")

    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    retrieved_docs = rag_chain.invoke("What is Task Decomposition?")

    len(retrieved_docs)


if __name__ == '__main__':
    example_v1()
