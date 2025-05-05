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

#Using 'test' instead of 'hello' so 'hello' isn't reused (if i use it again)

@bot.command(name='test')

async def hello_world(ctx):
    await ctx.send('Hello, World!')

#Here for testing
#bot.run(TOKEN)

DATA_FILE = pet_data.json

PET_EMOJIS = {
    "dog": "🐶",
    "cat": "🐱",
    "rabbit": "🐰",
    "parrot": "🦜",
    "snake": "🐍",
    "monkey": "🐒",
    "penguin": "🐧",
    "panda": "🐼",
    "hamster": "🐹",
    "raccoon": "🦝",
    "cow": "🐮",
    "seal": "🦭",
    "dinosaur": "🦖",
    "unicorn": "🦄",
    "default": "🐾"
}

#storing user's pet data (check later to see if this works)

def load_pet_data():
    if os.path.exists(DATA_FILE):
      with open(DATA_FILE, "r") as f:
          return json(f)
    
    else:
        return {}
    
def save_pet_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_pet_emoji(pet_type):
    return PET_EMOJIS.get(pet_type.lower(), PET_EMOJIS["default"])

pet_data = load_pet_data

def get_pet(user_id):
    return pet_data.get(str(user_id))

#Adopting the pet

@bot.command()
async def adopt(ctx):
    uid = str(ctx.author.id)
    if uid in pet_data:
        await ctx.send("You already have a pet! Use `!pet` to interact with it.")
        return
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
#maybe add random name generator or something similar if user can't decide name

    await ctx.send("What would you like to name your pet?")
    try:
        name_msg = await bot.wait_for("message", check=check, timeout=60.0)
        pet_name = name.msg.content.strip()



