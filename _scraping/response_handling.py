import requests
from bs4 import BeautifulSoup


def get_response(site: str):
    """
    Get the parsed beautiful soup from a site link
    :param site: Site link as string
    :return: Parsed beautiful soup response
    """
    try:
        request = requests.get(site)
    except requests.exceptions.RequestException as e:
        raise RuntimeError("Request error for site " + site)

    if request.status_code != 200:
        raise RuntimeError("Status code error for site " + site)

    try:
        return BeautifulSoup(request.content, "html.parser")
    except Exception as e:
        raise RuntimeError("Parsing error for site " + site)
