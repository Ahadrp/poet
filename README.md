# Telegram Poem Bot

This project, is a Telegram bot written in Python designed to send poems to a Telegram channel at specified intervals. 

## Features

- Sends requests to a server to fetch a poem from a random poet.
- Customizable interval for sending requests.
- Users can define the list of poets from which poems are fetched.
- Option to store poem retrieval data in a MySQL database (optional).
- Alternative option to disable database storage by modifying a `.env` file.
- Requires the bot to be added as an admin to the Telegram channel.

## Setup

1. Clone the repository to your local machine.
2. Install the necessary Python dependencies.
3. Set up a MySQL server if you choose to use the database option.
4. Create a `.env` file and set the following variables:
   - `DATABASE_ENABLED`: Set to `1` to enable database storage, or `0` to disable it.
   - `CHANNEL_ID`: Specify the ID of the Telegram channel where the bot will send poems.
5. Modify the list of poets in the `.py` file as desired.
6. Add the bot as an admin to your Telegram channel.
7. Run the bot using `python bot.py`.

## Configuration

- `DATABASE_ENABLED`: Set to `1` to enable database storage, or `0` to disable it.
- `CHANNEL_ID`: Specify the ID of the Telegram channel where the bot will send poems.

## Usage

1. Start the bot by running `bot.py`.
2. Interact with the bot on Telegram.
3. Specify the interval for poem requests.
4. Enjoy the poems sent by the bot to your Telegram channel.

## Database (Optional)

If you choose to use a MySQL database for storing poem retrieval data, ensure that you have set up the database and configured the connection details in the code.

## Contributors

- [Ahad Rahimipour](https://github.com/ahadrahimipour) - Author

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.