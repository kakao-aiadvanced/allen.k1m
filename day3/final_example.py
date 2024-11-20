from langgraph.constants import END
from langgraph.graph import StateGraph

from edges.hallucination import hallucination_check
from edges.relevance import relevance_check
from nodes.answer import answer
from nodes.generation import generate
from nodes.retrieve import retrieve
from nodes.web_search import web_search
from state.graph_state import GraphState

if __name__ == '__main__':
    # query
    query = "agent memory"

    workflow = StateGraph(GraphState)

    # Define the nodes
    workflow.add_node("retrieve", retrieve)  # retrieve docs
    workflow.add_node("answer", answer)  # answer to user
    workflow.add_node("generate", generate)  # generate answer
    workflow.add_node("websearch", web_search)  # search the web
    workflow.add_node("relevance_check", relevance_check)  # Relevance check
    workflow.add_node("hallucination_check", hallucination_check)  # Hallucination check
    # workflow.add_node("failed", lambda state: print("Failed: hallucination"))  # Failed state

    # Define the edges
    workflow.add_edge("retrieve", "relevance_check")  # retrieve → relevance_check

    workflow.add_conditional_edges(
        "relevance_check",
        relevance_check,
        {
            "yes": "generate",  # If relevant, go to generate
            "no": "websearch",  # If not relevant, go to web_search
        }
    )
    workflow.add_edge("websearch", "relevance_check")  # web_search → relevance_check

    workflow.add_edge("generate", "hallucination_check")  # generate → hallucination_check

    workflow.add_conditional_edges(
        "hallucination_check",
        hallucination_check,
        {
            "yes": "answer",
            "no": "generate",
            "end": END
        }
    )
    # Set the entry point
    workflow.set_entry_point("retrieve")

    # Compile
    app = workflow.compile()

    # Test
    inputs = {"question": query}
    for output in app.stream(inputs):
        for key, value in output.items():
            print(f"Finished running: {key}:")
            # print(value["generation"])
