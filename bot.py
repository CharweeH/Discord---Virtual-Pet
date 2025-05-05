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

DATA_FILE = pet_data.json

PET_EMOJIS = {
    "dog" = "🐶",
    "cat" = "🐱",
    "rabbit" = "🐰",
    "parrot" = "🦜",
    "snake" = "🐍",
    "monkey" = "🐒",
    "penguin" = "🐧".
    "panda" = "🐼",
    "hamster" = "🐹",
    "raccoon" = "🦝",
    "cow" = "🐮",
    "seal" = "🦭",
    "dinosaur" = "🦖",
    "unicorn" = "🦄",
    "default" = "🐾"
}

#Storing user's pet data

def load_pet_data():
    if os.path.exists(DATA_FILE)
      with open(DATA_FILE, "r") as f:
          return.json(f)
    
    else:
        return {}
    
def save_pet_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_pet_emoji(pet_type):
    return PET_EMOJIS.get(pet_type.lower(), PET_EMOJIS["default"])






