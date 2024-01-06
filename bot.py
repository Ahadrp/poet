#!/usr/bin/python3

from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError
import requests
import time
import os

def send_message(bot_token, channel_id, message):
    try:
        bot = Bot(token=bot_token)
        print("Sending message...")
        bot.send_message(chat_id=channel_id, text=message)
    except TelegramError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":

    load_dotenv()

    """
    url = "https://free-nba.p.rapidapi.com/players/237"

    headers = {
        "X-RapidAPI-Key": "eb12b991e4msh8390ec23a48d4f4p1054d1jsne0419ea7b577",
        "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    print(response.json())
    """


    # Set your bot token and channel ID
    bot_token = os.environ["TOKEN"]
    channel_id = os.environ["CHANNEL_ID"]

    while True:
        # Send the message
        send_message(bot_token, channel_id, "Hello")

        # Wait for one minute
        time.sleep(1)

