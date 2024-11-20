from langchain_openai import ChatOpenAI

_llm_instance = None


def get_llm():
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = ChatOpenAI(model="gpt-4o-mini")
    return _llm_instance
