import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio
import json

load_dotenv()

#DISCORD_TOKEN is in .env file

TOKEN = os.getenv("DISCORD_TOKEN")

#Check if token is loading

print(f"Token loaded: {'Success' if TOKEN else 'Failed'}")

intents = discord.Intents.default()

intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

#Hello World test

@bot.event

async def on_ready():
    print(f"{bot.user.name} is ready!")

#Using 'test' instaed of 'hello' so 'hello' isn't reused

@bot.command(name='test')

async def hello_world(ctx):
    await ctx.send('Hello, World!')

bot.run(TOKEN)

#Storing user's pet data

DATA_FILE = pet_data.json

def load_pet_data():
    if os.



