import csv
import os

#function

"""
load test data from login_data csv from testdata directory.
"""
def load_csv_data():
    data = []
    csv_path = os.path.join(os.path.dirname(__file__), "..", "testdata", "login_data.csv")
    csv_path = os.path.abspath(csv_path)
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append((row["username"], row["password"]))
    return data

"""
return the expected results according to the username and password.
"""
def determine_expected_message(username, password):
    if username == "tomsmith" and password == "SuperSecretPassword!":
        return "You logged into a secure area!"
    elif username != "tomsmith":
        return "Your username is invalid!"
    else:
        return "Your password is invalid!"