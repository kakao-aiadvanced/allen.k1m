import os

from langchain_core.documents import Document
from tavily import TavilyClient


def _get_client():
    return TavilyClient(
        api_key=os.getenv("TRAVILY_TOKEN"),
    )


def web_search(state):
    """
    Web search based based on the question

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Appended web results to documents
    """

    print("---WEB SEARCH---")
    print(state)
    question = state["question"]
    documents = None
    if "documents" in state:
        documents = state["documents"]

    # Web search
    docs = _get_client().search(query=question)['results']

    web_results = "\n".join([d["content"] for d in docs])
    web_results = Document(page_content=web_results)
    if documents is not None:
        documents.append(web_results)
    else:
        documents = [web_results]
    return {"documents": documents, "question": question}
