# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2021 Avinal Kumar <avinal.xlvii@gmail.com>
#
# Distributed under the terms of MIT License
# The full license is in the file LICENSE, distributed with this software.

import datetime
import json
import os
import random
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import requests

## CONSTANTS 
# WAKA_KEY = "YOUR API KEY HERE FOR TESTS, PLEASE ADD TO SECRETS FOR PRODUCTION"
# ? Add your WakaTime API key to the Repository Secrets
# ? https://docs.github.com/en/actions/learn-github-actions/variables
WAKA_KEY = os.getenv("WAKATIME_API_KEY")


## Config
matplotlib.use("Agg")

if not os.path.exists("./colors.json"):
    print("error: colors.json not found")
    sys.exit(1)

with open("./colors.json") as json_file:
    color_data = json.load(json_file)


def this_week(dates: list) -> str:
    """Returns a week streak"""
    week_end = datetime.datetime.strptime(dates[4], "%Y-%m-%dT%H:%M:%SZ")
    week_start = datetime.datetime.strptime(dates[3], "%Y-%m-%dT%H:%M:%SZ")
    print("week header created")
    return f"From {week_start.strftime('%d %B, %Y')} to {week_end.strftime('%d %B, %Y')}: {dates[5]}"


def make_graph(data: list, name: str, figzie=(10, 5)):
    """Make progress graph from API graph
    
    Args:
    -----
        data (list): data from API= [name, time, percent, start_date, end_date, week_total]
        name (str): name of the graph
        figzie (tuple, optional): size of the figure
    
    Effects:
    --------
        Creates a graph and saves it as a SVG file
        
    Note:
    -----
        This function requires colors.json to be present in the root directory
    """
    fig, ax = plt.subplots(figsize=figzie)
    y_pos = np.arange(len(data[0]))
    bars = ax.barh(y_pos, data[2], height=0.9)
    ax.set_yticks(y_pos)
    ax.get_xaxis().set_ticks([])
    ax.set_yticklabels(data[0], color="#586069")
    ax.set_title(this_week(data), color="#586069")
    ax.invert_yaxis()
    plt.box(False)
    for i, bar in enumerate(bars):
        if data[0][i] in color_data:
            bar.set_color(color_data[data[0][i]]["color"])
        else:
            bar.set_color(
                "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
            )
        x_value = bar.get_width()
        y_values = bar.get_y() + bar.get_height() / 2
        plt.annotate(
            data[1][i],
            (x_value, y_values),
            xytext=(4, 0),
            textcoords="offset points",
            va="center",
            ha="left",
            color="#586069",
        )
    file_name = f"stat_{name}.svg"
    plt.savefig(f"{file_name}", bbox_inches="tight", transparent=True)
    print("new image generated:", file_name)


def get_stats() -> dict[str, list]:
    """Gets API data and returns markdown progress
    
    Return:
    -------
        dict: language and project data ready for graph with following structure
        {
            "langualge": [name, time, percent, start_date, end_date, week_total],
            "project": [name, time, percent, start_date, end_date, week_total],
        }
        
    Note:
    -----
        This function requires WakaTime API key to be set in the Repository Secrets
    """
    data = requests.get(
        f"https://wakatime.com/api/v1/users/current/stats/last_7_days?api_key={WAKA_KEY}"
    ).json()

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
        project_time.append(project["text"])
        project_name.append(project["name"])
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
