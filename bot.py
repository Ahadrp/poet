#!/home/ahad/me_bot/bin/python3

from telegram.error import TelegramError
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot
import asyncio
import requests
import schedule
import logging
import time
import os

# Load the .env file
load_dotenv()

# Set your bot token and channel ID
bot_token = os.environ["TOKEN"]
channel_id = os.environ["CHANNEL_ID"]
interval_seconds = 3

logging.basicConfig(
    level=logging.INFO,  # Set the desired logging level
    format="%(asctime)s [%(levelname)s] %(message)s",  # Define the log message format
    datefmt="%Y-%m-%d %H:%M:%S"  # Define the date format
)

def process_resp(response: dict, key: str) -> str:
    """Return processed response
    """
    return response[key]


async def send_req() -> dict:
    """Return the response of request

    send req to api and get the response
    """

    logger.debug("CALL 'send_req'")

    response = ""

    url = "https://free-nba.p.rapidapi.com/players/237"

    headers = {
        "X-RapidAPI-Key": "eb12b991e4msh8390ec23a48d4f4p1054d1jsne0419ea7b577",
        "X-RapidAPI-Host": "free-nba.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        logger.info(f"Response '{response}'has been taken successfully!")
    except requests.exceptions.RequestException as e:
        logger.error(f"sending req failed because: '{e}'")
        return

    logger.debug("END 'send_req'")

    return response.json()


async def send_message_to_bot(bot_token, chat_id):
    """
    send req to api, get resp and send it to bot.
    """

    logger.debug("CALL send_message_to_bot")

    bot = Bot(token=bot_token)

    resp = await send_req()
    message = process_resp(resp, "last_name")

    try:
        await bot.send_message(chat_id=chat_id, text=message)
        logger.info(f"Message '{message}' has been send successfully")
    except TelegramError as e:
        logger.error(f"Error while sending message '{message}' because: {e}")

    logger.debug(f"END send_message_to_bot")


def send_request_and_response_at_specific_time(bot_token, chat_id, time_str):
    """Name of the method tells the story.
    """
    logger.info(f"call 'send_message_at_specific_time'")

    schedule.every().day.at(time_str).do(asyncio.run, send_message_to_bot(bot_token, chat_id))


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # Schedule sending request and response at specific times
    send_request_and_response_at_specific_time(bot_token, channel_id, "19:43")

    while True:
        schedule.run_pending()
        time.sleep(1)




