from typing import Optional

from document_manager.models import Document
from django.db.models import Q

from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig


@tool
def search_query_documents(query: str, config: RunnableConfig, limit: int = 5):
    """
    Search the most recent LIMIT documents for the current user
    Args:
        - query : string to perform search across title or content of documents
        - limit : number of results returned
    """
    configurable = config.get("configurable", None) or config.get("metadata", None)
    user_id = configurable.get("user_id")  # type: ignore

    if configurable == {}:
        raise Exception("Missing config data")

    if user_id is None:
        raise Exception("Invalid request for user")

    default_lookups = {
        "owner_id": user_id,
        "active": True,
    }
    doc_qs = (
        Document.objects.filter(**default_lookups)
        .filter(Q(title__icontains=query) | Q(content__icontains=query))
        .order_by("-created_at")
    )
    response_data = []

    for obj in doc_qs[:limit]:
        response_data.append(
            {
                "id": obj.id,  # type: ignore
                "title": obj.title,
            }
        )

    return response_data


@tool
def list_documents(config: RunnableConfig, limit: int = 5):
    """
    Lists the most recent LIMIT document for the user
    Args:
        - limit : number of results returned
    """
    configurable = config.get("configurable", None) or config.get("metadata", None)
    user_id = configurable.get("user_id")  # type: ignore

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
                "id": obj.id,  # type: ignore
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

    user_id = configurable.get("user_id")  # type: ignore

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
        "id": doc_obj.id,  # type: ignore
        "title": doc_obj.title,
        "content": doc_obj.content,
        "created_at": doc_obj.created_at,
    }

    return response_data


@tool
def create_document(title: str, content: str, config: RunnableConfig):
    """
    Create a new document for the user provided.
    Args:
        - title : string max character of 120
        - content : long form text in many paragraphs or pages
    """
    configurable = config.get("configurable", None) or config.get("metadata", None)

    if configurable == {}:
        raise Exception("Missing config data")

    user_id = configurable.get("user_id")  # type: ignore

    if user_id is None:
        raise Exception("Invalid request for user")

    try:
        doc_obj = Document.objects.create(
            title=title,
            content=content,
            owner_id=user_id,
        )
    except Exception as e:
        print(e, "error from Generic request")
        raise Exception("Invalid request for a document detail, try again")

    print(doc_obj)
    response_data = {
        "id": doc_obj.id,  # type: ignore
        "title": doc_obj.title,
        "content": doc_obj.content,
        "created_at": doc_obj.created_at,
    }

    return response_data


@tool
def delete_document(doc_id: int, config: RunnableConfig):
    """
    Delete the document for the current user using the document_id
    Args:
        - doc_id : id of document to be deleted
    """
    configurable = config.get("configurable", None) or config.get("metadata", None)

    if configurable == {}:
        raise Exception("Missing config data")

    user_id = configurable.get("user_id")  # type: ignore

    if user_id is None:
        raise Exception("Invalid request for user")

    try:
        doc_obj = Document.objects.get(id=doc_id, active=True, owner_id=user_id)
        doc_obj.delete()
    except Document.DoesNotExist as e:
        print(e, "error from Doesn't exist")
        raise Exception("Document not found, try again")
    except Exception as e:
        print(e, "error from Generic request")
        raise Exception("Invalid request for a document detail, try again")

    response_data = {"message": f"Document with {doc_id} has been succesffully deleted"}

    return response_data


@tool
def update_document(
    doc_id: int, title: Optional[str], content: Optional[str], config: RunnableConfig
):
    """
    Update a document for the user using the doc_id and related arguments.
    Args:
        - doc_id : id of document to be updated (required)
        - title : string max character of 120 (optional)
        - content : long form text in many paragraphs or pages (optional)
    """

    configurable = config.get("configurable", None) or config.get("metadata", None)

    if configurable == {}:
        raise Exception("Missing config data")

    user_id = configurable.get("user_id")  # type: ignore

    if user_id is None:
        raise Exception("Invalid request for user")

    try:
        doc_obj = Document.objects.get(id=doc_id, owner_id=user_id)
        if title is not None:
            doc_obj.title = title

        if content is not None:
            doc_obj.content = content

        if title or content:
            doc_obj.save()

    except Exception as e:
        print(e, "error from Generic request")
        raise Exception("Invalid request for a document detail, try again")

    print(doc_obj)
    response_data = {
        "id": doc_obj.id,  # type: ignore
        "title": doc_obj.title,
        "content": doc_obj.content,
        "created_at": doc_obj.created_at,
    }

    return response_data


document_tools = [
    get_document,
    list_documents,
    create_document,
    delete_document,
    update_document,
]
