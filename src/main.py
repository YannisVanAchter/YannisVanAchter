# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021 Avinal Kumar <avinal.xlvii@gmail.com>
#
# Distributed under the terms of MIT License
# The full license is in the file LICENSE, distributed with this software.
import os
import sys

import dotenv
import requests

from graph import make_graph
from github import get_possible_owners, has_contributed_to_repo

## CONSTANTS 
dotenv.load_dotenv()
# WAKA_KEY = "YOUR API KEY HERE FOR TESTS, PLEASE ADD TO SECRETS FOR PRODUCTION"
# ? Add your WakaTime API key to the Repository Secrets
# ? https://docs.github.com/en/actions/learn-github-actions/variables
WAKA_KEY = os.getenv("WAKATIME_API_KEY", None)

if WAKA_KEY is None:
    print("error: please add your WakaTime API key to the Repository Secrets")
    sys.exit(1)

def get_stats() -> dict[str, list]:
    data = requests.get(f"https://wakatime.com/api/v1/users/current/stats/last_7_days?api_key={WAKA_KEY}").json()
    try:
        project_data = data["data"]["projects"]
        lang_data = data["data"]["languages"]
        start_date = data["data"]["start"]
        end_date = data["data"]["end"]
        week_total = data["data"]["human_readable_total_including_other_language"]
    except KeyError:
        print("error: please add your WakaTime API key to the Repository Secrets")
        sys.exit(1)

    language_name = []
    language_time = []
    language_percent = []

    for lang in lang_data:
        language_name.append(lang["name"])
        language_time.append(lang["text"])
        language_percent.append(lang["percent"])
    
    project_name = []
    project_time = []
    project_percent = []
    
    for project in project_data:
        find = False
        for owner in get_possible_owners(project["name"]):
            print(owner, project["name"], sep="/")
            if has_contributed_to_repo(owner, project["name"]):
                project_name.append(owner + "/" + project["name"])
                find = True
                break
        
        if not find:
            project_name.append("Private Repository")
        project_time.append(project["text"])
        project_percent.append(project["percent"])
    
    data_list = {
        "lang": [language_name, language_time, language_percent, start_date, end_date, week_total],
        "project": [project_name, project_time, project_percent, start_date, end_date, week_total],
    }
    print("coding data collected")
    return data_list

if __name__ == "__main__":
    waka_stat = get_stats()
    make_graph(waka_stat.get("lang"), "language")
    make_graph(waka_stat.get("project"), "project", (10, 2))
    print("python script run successful")
