import discord
import best_girl
from os import getenv
from dotenv import load_dotenv


def main():
    load_dotenv()
    TOKEN = getenv('DISCORD_TOKEN')
    client = discord.Client()

    @client.event
    async def on_message(message):

        await best_girl.poll(message)
        # await Swift.swift(message, client)
    client.run(TOKEN)


if __name__ == "__main__":
    main()
