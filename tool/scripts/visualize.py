import os
import sys
import datetime

import matplotlib.pyplot as plt
import pandas as pd

# arg1: preprocessed file filepath
# arg2: output folder path

today = datetime.date.today().strftime("%Y%m%d")
data_filename = today + "_data.csv"
diagram_filename = today + "_diagram.png"

plt.close("all")
output_path = os.path.normpath(sys.argv[2])

# split data into country files
data = pd.read_csv(sys.argv[1], index_col=["countriesAndTerritories", "date"])
grouped = data.groupby("countriesAndTerritories")

for name, group in grouped:
    country_path = os.path.join(output_path, name)
    if not os.path.isdir(country_path):
        os.mkdir(country_path)

    data_path = os.path.join(country_path, data_filename)
    group = group.reset_index().set_index("date").drop("countriesAndTerritories", axis=1)
    group.to_csv(data_path)

    fig, ax = plt.subplots()
    ax.set_ylabel("Cases")
    ax.set_xlabel("Date")
    ax_deaths, ax_gold = ax.twinx(), ax.twinx()
    ax_deaths.set_ylabel("Deaths")
    ax_gold.set_ylabel("Gold Price (in US-Dollar)")

    rspine = ax_gold.spines["right"]
    rspine.set_position(("axes", 1.25))
    ax_gold.set_frame_on(True)
    ax_gold.patch.set_visible(False)
    fig.subplots_adjust(right=0.75)
    fig.suptitle(name, y=1)
    lineCases = group["cases"].plot(ax=ax, use_index=True, label="Cases", style="r-", rot=60)
    lineDeaths = group["deaths"].plot(ax=ax_deaths, use_index=True, label="Deaths", style="k-")
    lineGold = group["price"].plot(ax=ax_gold, use_index=True, label="Gold Price", style="g-")

    ax.legend(loc='lower left', bbox_to_anchor=(0.0, 1.01), ncol=2, borderaxespad=0, frameon=False)
    ax_deaths.legend(loc='lower left', bbox_to_anchor=(0.5, 1.01), ncol=2, borderaxespad=0, frameon=False)
    ax_gold.legend(loc='lower left', bbox_to_anchor=(1.0, 1.01), ncol=2, borderaxespad=0, frameon=False)
    plt.savefig(os.path.join(country_path, diagram_filename), bbox_inches="tight")
    plt.close()

# delete preprocessed file
os.remove(sys.argv[1])
