#!/home/ahad/me_bot/bin/python3

from telegram.error import TelegramError
from msql import Mysql
from datetime import datetime
from dotenv import load_dotenv
from poets import Poets
from telegram import Bot
import mysql.connector
import hashlib
import asyncio
import requests
import schedule
import random
import logging
import time
import os

# Load the .env file
load_dotenv()

# Set your bot token and channel ID
BOT_TOKEN = os.environ["TOKEN"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
VERSE_COUNT = '1'
poets_list = []
HOST = "127.0.0.1"
USER = "root"
PASSWORD = "1234"
DATABASE = "POETS"
TABLE = "Poems"

logging.basicConfig(
    level=logging.INFO,  # Set the desired logging level
    format="%(asctime)s [%(levelname)s] %(message)s",  # Define the log message format
    datefmt="%Y-%m-%d %H:%M:%S"  # Define the date format
)


def select_random_poet(Poets : Poets) -> int:
    """Return The int value of poet
    """
    global poets_list

    if len(poets_list) == 4:
        poets_list = []

    the_chosen_poet = 7
    while the_chosen_poet in poets_list:
        the_chosen_poet = random.choice((Poets.HAFEZ, Poets.SAADI, Poets.MOLAVI, Poets.KHAYAM))

    poets_list.append(the_chosen_poet)

    return the_chosen_poet


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

    url = f"https://c.ganjoor.net/beyt-json.php"

    """
    p is the int value of a poet.
    n is the count of verse we are requesting to take.
    """
    params = {"p": str(select_random_poet(Poets)), 'n': VERSE_COUNT}

    try:
        response = requests.get(url, params=params)
        logger.info(f"Response '{response}'has been taken successfully!")
    except requests.exceptions.RequestException as e:
        logger.error(f"sending req failed because: '{e}'")
        return

    logger.debug("END 'send_req'")

    return response.json()


async def make_message():
    resp = await send_req()

    poet_name = process_resp(resp, "poet")
    first_verse = process_resp(resp, "m1")
    second_verse = process_resp(resp, "m2")

    return f"{poet_name}:\n{first_verse}\n{second_verse}"


async def _send_message_to_bot():
    """
    send req to api, get resp and send it to bot.
    """
    message = ""

    logger.debug("CALL send_message_to_bot")

    bot = Bot(token=BOT_TOKEN)

    try:
        message = await make_message()
        while send_query(check_poem_exists, message)[0][0]:
            message = await make_message()
    except mysql.connector.Error as e:
        logger.error(f"couldn't hash data and store to database becaues: '{e}'")
        return


    try:
        send_query(hash_and_store, message)
    except mysql.connector.Error as e:
        logger.error(f"couldn't hash data and store to database becaues: '{e}'")
        return

    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=message)
        logger.info(f"Message '{message}' has been send successfully")
    except TelegramError as e:
        logger.error(f"Error while sending message '{message}' because: {e}")

    logger.debug(f"END send_message_to_bot")


def hash_md5(string):
    # Create an MD5 hash object
    md5_hash = hashlib.md5()

    # Convert the string to bytes and hash it
    md5_hash.update(string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    hashed_string = md5_hash.hexdigest()

    return hashed_string


def send_query(callback, T):
    msql = Mysql(HOST, USER, PASSWORD, DATABASE)
    return msql.handle_query(callback(T))


def hash_and_store(message: str) -> None:
    hashed_data = hash_md5(message)
    query = f"INSERT INTO `{TABLE}` VALUES ('{hashed_data}')"

    logger.info(f"sending query '{query}'")
    return query


def check_poem_exists(message: str):
    hashed_data = hash_md5(message)
    query = f"SELECT COUNT(*) FROM `{TABLE}` WHERE `poems_hash` = '{hashed_data}'"

    logger.info(f"sending query '{query}'")
    return query


def send_message_to_bot():
    """Wrepper, for being able to use async
    """
    asyncio.run(_send_message_to_bot())


def send_request_and_response_at_specific_time(time_str):
    """Name of the method tells the story.
    """
    logger.info(f"call 'send_message_at_specific_time'")

    schedule.every(3).seconds.do(send_message_to_bot)
    # schedule.every().day.at(time_str).do(asyncio.run, send_api_response_to_bot(BOT_TOKEN, chat_id, api_url))


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    # Schedule sending request and response at specific times
    send_request_and_response_at_specific_time("19:57")

    while True:
        schedule.run_pending()
        time.sleep(1)
