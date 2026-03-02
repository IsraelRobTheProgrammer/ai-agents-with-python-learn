from tmdb import client as tmdb_client


from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig


@tool
def search_movies(query: str, config: RunnableConfig, limit: int = 5):
    """
    Search the most recent LIMIT movies from The Movie DB with a max of 25
    Args:
        - query : string to perform a movie search
        - limit : number of results returned
    """

    configurable = config.get("configurable", None) or config.get("metadata", None)
    user_id = configurable.get("user_id") # type: ignore

    if configurable == {}:
        raise Exception("Missing config data")

    if user_id is None:
        raise Exception("Invalid request for user")

    print(f"Searching with user: {user_id}")

    try:
        response = tmdb_client.search_movie(query)
        results = response.get("results") # type: ignore
        total_results = response.get("total_results") # type: ignore

        if total_results == 0:
            return []

        if limit > 25:
            limit = 25

        return {"api_results": results[:limit], "total": total_results}

    except Exception as e:
        print(e, "error from search_movies")
        raise e


@tool
def get_movie_detail(movie_id: int, config: RunnableConfig):
    """
    Movie detail from The Movie DB using the movie_id
    Args:
        - movie_id : Get more details about the movie
    """

    configurable = config.get("configurable", None) or config.get("metadata", None)
    user_id = configurable.get("user_id")  # type: ignore

    if configurable == {}:
        raise Exception("Missing config data")

    if user_id is None:
        raise Exception("Invalid request for user")

    print(f"Searching with user: {user_id}")

    try:
        response = tmdb_client.movie_detail(movie_id)

        return response

    except Exception as e:
        print(e, "error from search_movies")
        raise e


movie_tools = [search_movies, get_movie_detail]
