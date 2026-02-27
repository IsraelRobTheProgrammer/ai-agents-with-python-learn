from document_manager.models import Document
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig


@tool
def list_documents(config: RunnableConfig):
    """
    Get a user's 5 recent doc(active) in a list
    """
    print(config)
    configurable = config.get("configurable", None) or config.get("metadata", None)
    user_id = configurable.get("user_id")

    if configurable == {}:
        raise Exception("Missing config data")

    limit = 5

    if user_id is None:
        raise Exception("Invalid request for user")

    doc_qs = Document.objects.filter(owner_id=user_id, active=True).order_by(
        "-created_at"
    )
    response_data = []

    for obj in doc_qs[:limit]:
        response_data.append(
            {
                "id": obj.id,
                "title": obj.title,
            }
        )

    return response_data


@tool
def get_document(doc_id: int, config: RunnableConfig):
    """
    Get the details of a document for the current user
    """
    configurable = config.get("configurable", None) or config.get("metadata", None)

    if configurable == {}:
        raise Exception("Missing config data")

    user_id = configurable.get("user_id")

    if user_id is None:
        raise Exception("Invalid request for user")

    try:
        doc_obj = Document.objects.get(id=doc_id, active=True, owner_id=user_id)
    except Document.DoesNotExist as e:
        print(e, "error from Doesn't exist")
        raise Exception("Document not found, try again")
    except Exception as e:
        print(e, "error from Generic request")
        raise Exception("Invalid request for a document detail, try again")

    print(doc_obj)
    response_data = {
        "id": doc_obj.id,
        "title": doc_obj.title,
    }

    return response_data


document_tools = [get_document, list_documents]
