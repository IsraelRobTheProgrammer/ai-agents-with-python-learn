from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from typing import Optional, Union
from langchain_google_genai import ChatGoogleGenerativeAI

# from langchain_core.agents import create_a
from ai.llms import get_required_model
from ai.tools import document_tools, movie_tools

llm_type = Union[ChatGoogleGenerativeAI, ChatOpenAI]


def get_document_agent(
    model_required: Optional[dict[str, str]] = None,
    checkpointer=None,
):

    llm_chosen = get_required_model(model_required)  # type: ignore

    agent = create_react_agent(
        model=llm_chosen,
        tools=document_tools,
        prompt="You are a helpful assistant in managing a user's documents within this app",
        checkpointer=checkpointer,
        name="document-assistant-agent",
    )

    return agent


def get_movie_discovery_agent(
    model_required: Optional[dict[str, str]] = None,
    checkpointer=None,
):

    llm_chosen = get_required_model(model_required)  # type: ignore

    agent = create_react_agent(
        model=llm_chosen,
        tools=movie_tools,
        prompt="You are a helpful assistant in finding information about movies",
        checkpointer=checkpointer,
        name="movie-discovery-assistant-agent",
    )

    return agent


# from langgraph.prebuilt import create_react_agent
# from langchain_openai import ChatOpenAI
# from typing import Optional, Union
# from langchain_google_genai import ChatGoogleGenerativeAI

# # from langchain_core.agents import create_a
# from ai.llms import get_required_model
# from ai.tools import document_tools, movie_tools

# llm_type = Union[ChatGoogleGenerativeAI, ChatOpenAI]


# def get_document_agent(
#     model_required: Optional[dict[str, str]] = None,
#     llm: Optional[llm_type] = None,
#     checkpointer=None,
# ):
#     if not model_required or not llm:
#         raise Exception("Either one of llm or model_required parameter is needed")

#     llm_chosen = get_required_model(model_required) if model_required else llm

#     agent = create_react_agent(
#         model=llm_chosen,
#         tools=document_tools,
#         prompt="You are a helpful assistant in managing a user's documents within this app",
#         checkpointer=checkpointer,
#         name="document-assistant-agent",
#     )

#     return agent


# def get_movie_discovery_agent(
#     model_required: Optional[dict[str, str]] = None,
#     llm: Optional[llm_type] = None,
#     checkpointer=None,
# ):
#     if not model_required or not llm:
#         raise Exception("Either one of llm or model_required parameter is needed")

#     llm_chosen = get_required_model(model_required) if model_required else llm

#     agent = create_react_agent(
#         model=llm_chosen,
#         tools=movie_tools,
#         prompt="You are a helpful assistant in finding information about movies",
#         checkpointer=checkpointer,
#         name="movie-discovery-assistant-agent",
#     )

#     return agent
