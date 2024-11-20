from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from utils.llm import get_llm


def make_hallucination_grader(llm: ChatOpenAI):
    system = """You are a grader assessing whether
        an answer is grounded in / supported by a set of facts. Give a binary 'yes' or 'no' score to indicate
        whether the answer is grounded in / supported by a set of facts. Provide the binary score as a JSON with a
        single key 'score' and no preamble or explanation."""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "documents: {documents}\n\n answer: {generation} "),
        ]
    )
    hallucination_grader = prompt | llm | JsonOutputParser()
    return hallucination_grader


def hallucination_check(state):
    """
    hallucination check for the document and question
    """

    print("---HALLUCINATION CHECK---")
    question = state["question"]
    print(question)
    retrieved_docs = state["documents"]

    hallucination_checker = make_hallucination_grader(get_llm())

    answer = state["generation"]

    hallucination_score = hallucination_checker.invoke({"documents": retrieved_docs, "generation": answer})

    print("---HALLUCINATION CHECK RESULT---")
    print(hallucination_score)

    state["hallucination_result"] = hallucination_score["score"]

    return state
