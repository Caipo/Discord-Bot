import discord
import BestGirl
from os import getenv


def main():
    # load_dotenv()
    TOKEN = getenv('DISCORD_TOKEN')
    client = discord.Client()

    @client.event
    async def on_message(message):

        await BestGirl.poll(message)
        # await Swift.swift(message, client)
    client.run(TOKEN)


if __name__ == "__main__":
    main()
