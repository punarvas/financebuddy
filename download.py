"""
download.py
Authors: Akash Mahajan and Faraz Gurramkonda
Date: 10/13/2024
"""

from splitwise import Splitwise
import pandas as pd
import json
from datetime import datetime, timedelta


def to_date(date):
    date = pd.to_datetime(date)
    day = date.day_name()
    date = date.strftime('%Y-%m-%d')
    return date, day


def get_exist(exp, fn):
    user_names = [e.getFirstName() for e in exp.getUsers()]
    if fn in user_names:
        return True, user_names.index(fn)
    return False, -1


def download_data():
    n_entries = 500
    print("Processing...")

    # Load authentication data
    with open("auth.json", "r") as file:
        auth = json.load(file)

    sObj = Splitwise(auth["consumer_key"], auth["consumer_secret"], api_key=auth["api_key"])
    expenses = sObj.getExpenses(offset=2, limit=n_entries)
    first_name = sObj.getCurrentUser().getFirstName()

    # Prepare data dictionary
    data = {"date": [], "day": [], "amount": [], "category": [], "description": []}

    # Define date filter for the last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)

    for e in expenses:
        me_exist, index = get_exist(e, first_name)
        if not me_exist:
            continue
        date, day = to_date(e.getDate())
        date_obj = pd.to_datetime(date)  # Convert date string back to datetime for comparison

        # Only include entries from the last 30 days
        if date_obj >= thirty_days_ago:
            amount = round(float(e.getUsers()[index].getOwedShare()))
            if amount == 0:
                continue
            category = e.getCategory().name
            desc = e.getDescription()
            data["date"].append(date)
            data["day"].append(day)
            data["amount"].append(amount)
            data["category"].append(category)
            data["description"].append(desc)

    # Create a DataFrame and save to CSV
    pd.DataFrame(data).to_csv("expenses.csv", index=False)
    print("Done")
