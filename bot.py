#!/home/ahad/me_bot/bin/python3

from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError
import asyncio
import requests
import logging
import time
import os

logging.basicConfig(
    level=logging.INFO,  # Set the desired logging level
    format="%(asctime)s [%(levelname)s] %(message)s",  # Define the log message format
    datefmt="%Y-%m-%d %H:%M:%S"  # Define the date format
)

async def send_req() -> str:
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

    return response.json()


async def send_message(bot_token, chat_id, message):
    resp = ""
    bot = Bot(token=bot_token)

    try:
        await bot.send_message(chat_id=chat_id, text=message)
        logger.info(f"Message '{message}' has been send successfully")
    except TelegramError as e:
        logger.error(f"Error while sending message '{message}' because: {e}")

async def send_hello_periodically(bot_token, chat_id, interval_seconds):
    logger.info(f"call hello method peridically")

    while True:
        resp = await send_req()
        await send_message(bot_token, chat_id, resp)
        await asyncio.sleep(interval_seconds)

if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    load_dotenv()
    logger.info("env has been loaded")

    # Set your bot token and channel ID
    bot_token = os.environ["TOKEN"]
    channel_id = os.environ["CHANNEL_ID"]
    logger.info(f"token '{bot_token}' and channel id '{channel_id}' has been taken")
    interval_seconds = 3

    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_hello_periodically(bot_token, channel_id, interval_seconds))

