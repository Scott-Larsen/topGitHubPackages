"""
TIP: Don't forget to run: pip install requests!
A small Python program that uses the GitHub search API to list
the top projects by language, based on stars.
GitHub Search API documentation: https://developer.github.com/v3/search/
Additional parameters for searching repos can be found here:
https://help.github.com/en/articles/searching-for-repositories#search-by-number-of-stars
Note: The API will return results found before a timeout occurs,
so results may not be the same across requests, even with the same query.
Requests to this endpoint are rate limited to 10 requests per
minute per IP address.
"""

import requests
import json
import time
# from repos.models import GitHubRepo
from pprint import pprint

GITHUB_API_URL = "https://api.github.com/search/repositories"


class GitHubRecord:
    def __init__(self, name, language, num_stars):
        self.name = name
        self.language = language
        self.num_stars = num_stars
        # self.link = link

    def __repr__(self):
        return f"GitHubRecord{self.name} {self.language} {self.num_stars}"



# languages = ['Python', 'JavaScript', 'Rust']
# languages = ['Python', 'JavaScript', 'Rust', 'Go', 'Swift', 'CPlusPlus', 'TypeScript', 'Java', 'FSharp', 'CSharp', 'R', 'C']

languages = ['C']
# , 'Shell', 'C', 'Dart', 'PHP', 'Objective-C', 'Matlab', 'Ruby', 'VBA', 'Scala', 'Kotlin', 'VisualBasic', 'Perl', 'Lua', 'Julia', 'Haskell', 'Delphi']

def create_query(language, min_stars=1):
    return f"stars:>{min_stars} language:{language}"
    

def topReposByStars(language, sort="stars", order="desc"):
    # query = create_query(languages, min_stars)
    query = create_query(language)
    parameters = {"q": query, "sort": sort, "order": order}
    # print(parameters)
    response = requests.get(GITHUB_API_URL, params=parameters)

    if response.status_code != 200:
        raise GitHubApiException(response.status_code)

    response_json = response.json()
    
    # with open('python1.json', 'w') as f:
    #     json.dump(response_json, f)

    items = response_json["items"]
    # print(items[0])

    return items

    # return items
    # return [GitHubRecord(item["name"], item["language"], item["stargazers_count"]) for item in items]


if __name__ == "__main__":

    # javascript = None
    for lang in languages:
        # results = requests.get(f"https://api.github.com/search/repositories?q=stars:>1+language:{lang}&sort=stars&order=desc")
        results = topReposByStars(lang)

        print(results)

        # for result in results:
        #     language = result["language"]
        #     stars = result["stargazers_count"]
        #     name = result["name"]

            # print(f"-> {name} is a {language} repo with {stars} stars.")

        filename = 'json/' + lang.lower() + '.json'
        print(filename)

        with open(filename, 'w') as f:
            json.dump(results, f)

        time.sleep(10)