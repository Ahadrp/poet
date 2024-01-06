#!/usr/bin/python3

from dotenv import load_dotenv
import requests
import os

if __name__ == "__main__":

    load_dotenv()

    url = "https://free-nba.p.rapidapi.com/players/237"

    headers = {
        "X-RapidAPI-Key": "eb12b991e4msh8390ec23a48d4f4p1054d1jsne0419ea7b577",
        "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    # print(response.json())

    print(os.environ["TOKEN"])

