#SET UP SHIT
import os, discord, requests, face_recognition, cv2, os, random, ffmpeg, asyncio
from dotenv import load_dotenv
from discord.ext import commands
from os import listdir
from os.path import isfile, join

from elosports.elo import Elo
import time
import random
import mysql.connector
import Swift
import BestGirl



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_message(message):
    global client
    
    await BestGirl.poll(message)
    #await Swift.swift(message, client)


client.run(TOKEN)

