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

## Config
matplotlib.use("Agg")

if not os.path.exists("./img") or not os.path.isdir("./img"):
    os.makedirs("./img")

if not os.path.exists("./colors.json"):
    print("error: colors.json not found")
    sys.exit(1)

with open("./colors.json") as json_file:
    color_data = json.load(json_file)

def this_week(dates: list) -> str:
    week_end = datetime.datetime.strptime(dates[4], "%Y-%m-%dT%H:%M:%SZ")
    week_start = datetime.datetime.strptime(dates[3], "%Y-%m-%dT%H:%M:%SZ")
    return f"From {week_start.strftime('%d %B, %Y')} to {week_end.strftime('%d %B, %Y')}: {dates[5]}"

def make_graph(data: list, name: str, figzie=(10, 5)):
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
            bar.set_color("#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)]))
        x_value = bar.get_width()
        y_values = bar.get_y() + bar.get_height() / 2
        plt.annotate(data[1][i], (x_value, y_values), xytext=(4, 0), textcoords="offset points", va="center", ha="left", color="#586069")
    file_name = f"./img/stat_{name}.svg"
    plt.savefig(file_name, bbox_inches="tight", transparent=True)
    print("new image generated:", file_name)

if __name__ == "__main__":
    make_graph([["Python", "JavaScript", "HTML", "CSS", "Shell"], ["2 hrs 30 mins", "1 hr 30 mins", "1 hr 15 mins", "1 hr", "30 mins"], [30, 20, 15, 10, 5], "2021-09-01T00:00:00Z", "2021-09-08T00:00:00Z", "6 hrs 45 mins"], "test")