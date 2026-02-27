from langgraph.prebuilt import create_react_agent

# from langchain_core.agents import create_a
from ai.llms import get_openai_model, get_required_model
from ai.tools import document_tools


def get_document_agent(model_required: dict[str, str], checkpointer=None):
    llm_model = get_required_model(model_required)
    openai_model = get_openai_model()

    agent = create_react_agent(
        model=llm_model,  # type: ignore
        tools=document_tools,
        prompt="You are a helpful assistant in managing a user's documents within this app",
        checkpointer=checkpointer,
    )

    return agent
