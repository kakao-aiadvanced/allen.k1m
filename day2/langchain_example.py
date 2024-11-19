'''
query -> Docs Retrieval -> Relevant Check -Yes-> Generate Answer -> Hallucination Check -No-> Generate Answer -> Hallucination Check -Yes-> Answer to User
                                          -No-> Generate Answer 'No'
'''
import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

parser = JsonOutputParser()


def load_docs(web_docs: list):
    loader = WebBaseLoader(
        web_path=web_docs,
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
    )
    return loader.load()


def split_docs(loaded_docs):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            " ",
            ".",
            ",",
            "\u200b",  # Zero-width space
            "\uff0c",  # Fullwidth comma
            "\u3001",  # Ideographic comma
            "\uff0e",  # Fullwidth full stop
            "\u3002",  # Ideographic full stop
            "",
        ],
    )
    return text_splitter.split_documents(loaded_docs)


def get_model():
    return ChatOpenAI(
        model="gpt-4o-mini"
    )


def get_embeddings():
    return OpenAIEmbeddings(
        model="text-embedding-3-small",
    )


def get_retriever(vs):
    return vs.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 6},
    )


def get_vectorstore(splits_docs, embeddings):
    return Chroma.from_documents(documents=splits_docs, embedding=embeddings)


def get_prompt():
    prompt = hub.pull("rlm/rag-prompt")
    return prompt


def relevance_prompt():
    return PromptTemplate(
        template=(
            "You are a system designed to evaluate the relevance of a retrieved document chunk to a user query.\n"
            "Assess if the retrieved chunk answers the user query directly or provides useful context for the query.\n"
            "Relevance is true/false \n"
            "Respond with a JSON object indicating relevance using the following format:\n"
            "{format_instructions}\n\n"
            "User Query: {query}\n\n"
            "Retrieved Chunk: {retrieved_chunk}"
        ),
        input_variables=["query", "retrieved_chunk"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )


def hallucination_prompt():
    return PromptTemplate(
        template=(
            "You are a system designed to evaluate whether the retrieved document chunk contains hallucinated or incorrect information.\n"
            "Compare the retrieved chunk to the user query and determine if it includes any hallucinated or factually incorrect information "
            "that is not grounded in the source text.\n\n"
            "Hallucination is true/false\n"
            "Respond with a JSON object indicating hallucination status using the following format:\n"
            "{format_instructions}\n\n"
            "User Query: {query}\n\n"
            "Retrieved Chunk: {retrieved_chunk}"
        ),
        input_variables=["query", "retrieved_chunk"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )


def make_relevance_chains():
    return relevance_prompt() | get_model() | parser


def make_hallucination_chains():
    return hallucination_prompt() | get_model() | parser


if __name__ == '__main__':
    urls = [
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
        "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    ]

    query = "what is the agent memory"

    docs = load_docs(urls)

    split_docs = split_docs(docs)

    embedding = get_embeddings()
    vectorstore = get_vectorstore(split_docs, embedding)

    retriever = get_retriever(vectorstore)

    retrieved_doc = retriever.invoke(query)

    relevance_chains = make_relevance_chains()

    relevance_result = relevance_chains.invoke(
        {"query": query, "retrieved_chunk": retrieved_doc[0].page_content}
    )
    if relevance_result['relevance']:
        # Generate Answer | Hallucination Check

        pass
    else:
        # Generate Answer 'No'
        pass
