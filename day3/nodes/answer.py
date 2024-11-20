def answer(state):
    """
    Answer the question

    Args:
        state (dict): The current graph state

    Returns:
        str: The answer to the question
    """

    print("---ANSWER---")
    question = state["question"]
    generation = state["generation"]

    print(generation)
    return generation
