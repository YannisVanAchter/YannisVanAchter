import logging
import os

from dotenv import load_dotenv
import requests

# Constants
load_dotenv() 
GITHUB_USER = os.getenv("USER", None)
GITHUB_TOKEN = os.getenv("TOKEN", None)

if GITHUB_USER is None or GITHUB_TOKEN is None:
    message = "Please add your GitHub username and token to the .env file"
    if __name__ == "__main__":
        raise ImportError(message)
    message += " or as environment variables."
    message += "\n== Module requires USER and TOKEN to be set. ==\n"
    raise ImportError(message)

def _get(url):
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    return requests.get(url, headers=headers)

def has_contributed_to_repo(owner, repo) -> bool:
    logging.debug(f"Checking if {GITHUB_USER} has contributed to {owner}/{repo}")
    commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits?author={GITHUB_USER}"
    logging.debug(f"GET {commits_url}")
    response = _get(commits_url)
    logging.debug(response)
    if response.status_code == 200 and len(response.json()) > 0:
        return True
    else:
        logging.debug(f"{GITHUB_USER} has not contributed to {owner}/{repo}")
        logging.debug(response.json())
    return False

def get_possible_owners(repo) -> list:
    owners = []
    search_url = f"https://api.github.com/search/repositories?q={repo}"
    response = _get(search_url)
    if response.status_code == 200:
        for item in response.json()["items"]:
            if item["private"] is False:
                owners.append(item["owner"]["login"])
    return owners

def _tests():
    assert has_contributed_to_repo("YannisVanAchter", "YannisVanAchter"), "You have not contributed to my README repository"
    assert not has_contributed_to_repo("tiangolo", "fastapi"), "You have contributed to my README repository"
    assert "YannisVanAchter" in get_possible_owners("YannisVanAchter"), "You are not the owner of my README repository"

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    _tests()
