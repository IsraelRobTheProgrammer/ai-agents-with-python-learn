from langgraph_supervisor import create_supervisor

from agents import get_document_agent, get_movie_discovery_agent, get_required_model


def get_supervisor(model_required: dict[str, str], checkpointer=None):
    llm = get_required_model(model_required)

    movie_discovery_agent = get_movie_discovery_agent()
    doc_agent = get_document_agent()

    supervisor = create_supervisor(
        agents=[movie_discovery_agent, doc_agent],
        model=llm,  # type: ignore
        prompt=(
            "You manage a document management assistant and movie discovery assistant. Assign to work them"
        ),
    ).compile(checkpointer=checkpointer)

    return supervisor
