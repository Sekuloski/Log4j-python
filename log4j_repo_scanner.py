import json
import requests
from github import Github


def run_query(uri, query, status_code, headers):
    request = requests.post(uri, json={'query': query}, headers=headers)
    if request.status_code == status_code:
        return request.json()
    else:
        raise Exception(f"Unexpected status code returned: {request.status_code}")


def search_repo(token, repo_user, repository_name, p_name):
    g = Github(token)
    user = g.get_user(repo_user)
    user_repository = user.get_repo(repository_name)

    contents = user_repository.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(user_repository.get_contents(file_content.path))
        else:
            if 'log4j' in str(file_content.decoded_content):
                print(repo_user + "/" + repository_name + " - " + p_name)
                return


if __name__ == '__main__':
    githubQuery = open("query.txt", 'r').read()

    githubURI = 'https://api.github.com/graphql'

    githubToken = open("PATH TO GITHUB ACCESS TOKEN", "r").read()  # <-- CHANGE THIS

    githubHeaders = {"Authorization": "Bearer " + githubToken, "Accept": "application/vnd.github.hawkgirl-preview+json"}

    with open('query_results.json', 'w', encoding='utf-8') as file:
        json.dump(run_query(githubURI, githubQuery, 200, githubHeaders), file, ensure_ascii=False, indent=4)

    with open('query_results.json') as file:
        data = json.load(file)
        edges = data['data']['repository']['dependencyGraphManifests']['edges']
        for dependency_file in range(len(edges)):
            repo = edges[dependency_file]['node']['dependencies']['nodes']
            for dependency in repo:
                if dependency['repository'] is None:
                    continue
                elif dependency['repository']['isPrivate'] == 'true':
                    continue
                else:
                    package_name = dependency['packageName']
                    strings = dependency['repository']['nameWithOwner'].split('/')
                    username = strings[0]
                    repository = strings[1]
                    search_repo(githubToken, username, repository, package_name)
