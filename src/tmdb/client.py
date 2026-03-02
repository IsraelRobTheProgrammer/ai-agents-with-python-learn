import requests
from django.conf import settings

# response = requests.get(url, headers=headers)


def get_headers():
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.TMDB_JWT_KEY}",
    }


def search_movie(query: str, page: int = 1, raw=False):
    url = "https://api.themoviedb.org/3/search/movie"
    headers = get_headers()
    params = {
        "query": query,
        "page": page,
        "include_adult": False,
        "language": "en-US",
    }

    response = requests.get(url, headers=headers, params=params)

    if raw:
        return response

    json_response = response.json()
    print(json_response)

    return json_response


def movie_detail(movie_id: int, page: int = 1, raw=False):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    headers = get_headers()
    params = {
        "movie_id": movie_id,
        "language": "en-US",
    }

    response = requests.get(url, headers=headers, params=params)

    if raw:
        return response

    json_response = response.json()
    print(json_response)

    return json_response
