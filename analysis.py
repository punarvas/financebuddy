"""
analysis.py
Authors: Akash Mahajan
Date: 10/13/2024
"""

import pandas as pd
import re
import json


def proc_keyword(kw):
    # Define a set of common stopwords
    stopwords = {"and", "or", "if", "else", "not", "the", "is", "in", "at", "on", "a", "an", "to", "of", "for"}
    keyw = kw
    if not keyw.isalpha() or kw in stopwords:
        return None
    if keyw != "":
        keyw = keyw.lower()
        keyw = re.sub(r'\W+', '', keyw)
        keyw = keyw.strip()
    return keyw


def join(x):
    return " ".join(x)


def split(x):
    return str(x).lower().split(" ")


def list_to_str(key):
    return f"[{key[0]}, {key[1]}]"


def analyze():
    df = pd.read_csv("expenses.csv")
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(by="date", ascending=False).reset_index(drop=True)
    analysis_results = {}
    analysis_results["total_spent"] = str(df.amount.sum())
    analysis_results["minimum_spent"] = str(df.amount.min())
    analysis_results["maximum_spent"] = str(df.amount.max())
    analysis_results["number_of_entries_day"] = df.day.value_counts().astype(str).to_dict()
    analysis_results["category_wise_expenses"] = \
        df[["category", "amount"]].groupby("category").sum().astype(str).to_dict()["amount"]
    analysis_results["category_wise_min_expenses"] = \
        df[["category", "amount"]].groupby("category").min().astype(str).to_dict()["amount"]
    analysis_results["category_wise_max_expenses"] = \
        df[["category", "amount"]].groupby("category").max().astype(str).to_dict()["amount"]
    # Use a set comprehension to filter out empty strings, numeric values, and stopwords
    analysis_results["keywords"] = list(
        set(proc_keyword(s) for s in " ".join(df.description.values).split(" ") if proc_keyword(s)))
    analysis_results["day_wise_total_expenses"] = df[["day", "amount"]].groupby(by="day").sum().astype(str).to_dict()[
        "amount"]
    analysis_results["day_wise_min_expenses"] = df[["day", "amount"]].groupby(by="day").min().astype(str).to_dict()[
        "amount"]
    analysis_results["day_wise_max_expenses"] = df[["day", "amount"]].groupby(by="day").max().astype(str).to_dict()[
        "amount"]
    analysis_results["category_payment_on_what_days"] = df[["category", "day"]].groupby('category')['day'].apply(
        list).to_dict()
    analysis_results["category_wise_day_wise_expenses"] = \
        df[["category", "day", "amount"]].groupby(['category', 'day']).sum().astype(str).to_dict()["amount"]
    res = df[["category", "day", "amount"]].groupby(['category', 'day']).sum().apply(list).astype(str).to_dict()[
        "amount"]
    res = {list_to_str(key): value for key, value in res.items()}
    analysis_results["category_wise_day_wise_expenses"] = res
    analysis_results["day_expenses_description_keywords"] = df[["day", "description"]].groupby("day").agg({
        "description": join
    })["description"].apply(split).to_dict()

    with open("analysis_results.json", "w") as file:
        json.dump(analysis_results, file, indent=4)
