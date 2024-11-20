from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from utils.llm import get_llm


def _make_prompt(system: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "question: {question}\n\n document: {document} "),
        ]
    )


def make_relevance_checker(llm: ChatOpenAI):
    system = """You are a grader assessing relevance
        of a retrieved document to a user question. If the document contains keywords related to the user question,
        grade it as relevant. It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
        Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question. \n
        Provide the binary score as a JSON with a single key 'score' and no premable or explanation.
        """
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "question: {question}\n\n document: {document} "),
        ]
    )

    retrieval_grader = prompt | llm | JsonOutputParser()
    return retrieval_grader


def relevance_check(state):
    """
    relevance check for the document and question
    """

    print("---RELEVANCE CHECK---")
    question = state["question"]
    print(question)
    retrieved_docs = state["documents"]

    relevance_checker = make_relevance_checker(get_llm())
    doc_for_relevance_check = retrieved_docs[0].page_content
    relevance_result = relevance_checker.invoke({"question": question, "document": doc_for_relevance_check})

    print("---RELEVANCE CHECK RESULT---")
    print(relevance_result)
    state["relevance_result"] = relevance_result["score"]
    return state
