import datetime
import math
import sys

import pandas as pd


# arg1: COVID-19 dataset filepath
# arg2: gold price dataset filepath
# arg3: start date (yyyy-mm-dd; inclusive)
# arg4: end date (yyyy-mm-dd; inclusive)


# parse gold price csv file and fill weekend gaps with last available data
def preprocess_gold_prices(csv_file_gold, start_date, end_date):
    data = pd.read_csv(csv_file_gold, sep=";", thousands=".", decimal=",", header=0, usecols=["Datum", "Schlusskurs"],
                       index_col="Datum").sort_index()
    data.index.names = ["date"]
    data.columns = ["price"]
    data.index = pd.to_datetime(data.index)
    data["price"] = data["price"].astype(float)
    # filter by start and end dates
    data = data.loc[(data.index >= start_date) & (data.index <= end_date)]

    # fill weekend gaps with last available data
    daterange = pd.date_range(start_date, end_date, freq="D").to_frame(name="date").set_index("date")
    data = daterange.merge(data, on="date", how="outer")
    last = float("NaN")
    for index, row in data.iterrows():
        if math.isnan(row["price"]):
            row["price"] = last
        last = row["price"]
    return data


# parse COVID data
def preprocess_covid_data(csv_file_covid, start_date, end_date):
    data = pd.read_csv(csv_file_covid, sep=",", header=0)
    data["date"] = data.apply(
        lambda row: datetime.datetime.strftime(datetime.datetime(row.year, row.month, row.day), "%Y-%m-%d"), axis=1)
    data["date"] = pd.to_datetime(data["date"])
    data = data[["countriesAndTerritories", "date", "cases", "deaths"]].set_index(
        ["countriesAndTerritories", "date"]).sort_index()
    data["cases"] = data["cases"].astype(int)
    data["deaths"] = data["deaths"].astype(int)

    # accumulate cases and deaths
    data["cases"] = data["cases"].groupby(by=["countriesAndTerritories"]).cumsum()
    data["deaths"] = data["deaths"].groupby(by=["countriesAndTerritories"]).cumsum()

    # filter by start and end dates
    data = data.loc[
        (data.index.get_level_values("date") >= start_date) & (data.index.get_level_values("date") <= end_date)]
    # ignore data with zero cases
    data = data.loc[data["cases"] != 0]
    return data


def merge_data(covid_data, gold_data):
    return covid_data.reset_index().merge(gold_data, on="date", how="outer").set_index(
        ["countriesAndTerritories", "date"]).sort_index()


if __name__ == "__main__":
    start_date = datetime.datetime.strptime(sys.argv[3], "%Y-%m-%d")
    end_date = datetime.datetime.strptime(sys.argv[4], "%Y-%m-%d")

    gold_data = preprocess_gold_prices(sys.argv[2], start_date, end_date)
    covid_data = preprocess_covid_data(sys.argv[1], start_date, end_date)

    preprocessed = merge_data(covid_data, gold_data)
    preprocessed.to_csv("preprocessed.csv")
