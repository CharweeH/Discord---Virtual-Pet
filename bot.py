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

DATA_FILE = "pet_data.json"

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
      with open(DATA_FILE, 'r') as user_data:
          return json.load(user_data)
    
    else:
        return {}
    
def save_pet_data(data):
    with open(DATA_FILE, 'w') as user_data:
        json.dump(data, user_data, indent=4)

def get_pet_emoji(pet_type):
    return PET_EMOJIS.get(pet_type.lower(), PET_EMOJIS["default"])

pet_data = load_pet_data()

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
        pet_name = name_msg.content.strip()
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Your new pet is waiting!")
        return
    
    await ctx.send("What type of pet would you like to adopt? Choose one of these options:\n" + ", ".join(PET_EMOJIS.keys() - {"default"}))
    try:
        #retry loop incase invalid pet is chosen
        valid_pet = False
        max_attempts = 3
        attempts = 0

        while not valid_pet and attempts < max_attempts:
            type_msg = await bot.wait.for("message", check=check, timeout=60.0)
            pet_type = type_msg.content.strip().lower()

            if pet_type in PET_EMOJIS and pet_type != "default":
                valid_pet = True
            else:
                attempts += 1
                if attempts >= max_attempts:
                    await ctx.send(f"You tried too many times. Try using a dog instead! {PET_EMOJIS["dog"]}")
                    pet_type = "dog"
                    valid_pet = True
                else:
                    valid_options = ", ".join([f"{pet} {PET_EMOJIS[pet]}" for pet in PET_EMOJIS if pet != "default"])
                    await ctx.send(f"That's not a valid pet type. Please choose a pet from these options:\n{valid_options}")

#fix issues tomorrow and add pet_data



bot.run(TOKEN)



