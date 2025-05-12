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

# debugging

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready!")

# testing, testing, is this thing on?

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

# added Cog for later

#class PetCog(commands.Cog):
    #def __init__(self, bot):
        #self.bot = bot
        #self.bot.loop.create_task(self.pet_check_loop())

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
        name_msg = await bot.wait_for("message", check=check, timeout=120.0)
        pet_name = name_msg.content.strip()
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Your new pet is waiting!")
        return
    
    try:
        #retry loop incase invalid pet is chosen
        valid_pet = False
        max_attempts = 3
        attempts = 0

        while not valid_pet and attempts < max_attempts:
            await ctx.send("What type of pet would you like to adopt? Choose one of these options:\n" + ", ".join(PET_EMOJIS.keys() - {"default"}))
            type_msg = await bot.wait_for("message", check=check, timeout=120.0)
            pet_type = type_msg.content.strip().lower()

            if pet_type in PET_EMOJIS and pet_type != "default":
                valid_pet = True
            else:
                attempts += 1
                if attempts >= max_attempts:
                    await ctx.send(f"You tried too many times. Try using a dog instead! {PET_EMOJIS['dog']}")
                    pet_type = "dog"
                    valid_pet = True
                else:
                    valid_options = ", ".join([f"{pet} {PET_EMOJIS[pet]}" for pet in PET_EMOJIS if pet != "default"])
                    await ctx.send(f"That's not a valid pet type. Please choose a pet from these options:\n{valid_options}")

        pet_data[uid] = {
            "Name": pet_name,
            "Type": pet_type,
            "Hunger": 50,
            "Happiness": 50,
            "Paused": False
        }

        save_pet_data(pet_data)

        emoji = get_pet_emoji(pet_type)

        await ctx.send(f"You adopted {pet_name} the {pet_type} {emoji}! Use !pet to feed, play and look after them!")

        #adding help command in DMs

        try:
            help_embed = discord.Embed(
                title="🐾 Virtual Pet Bot Guide",
                description="Congratulations for adopting your virtual pet!",
                color=discord.Color.pink()
            )

            help_embed.add_field(name="'!pet'", value="Check on your pet's stats", inline=False)
            help_embed.add_field(name="'!feed'", value="Feed your pet", inline=False)
            help_embed.add_field(name="'!play'", value="Play with your pet", inline=False)
            help_embed.add_field(name="'!namepet' (new name)", value="Change your pet's name", inline=False)
            help_embed.add_field(name="!help", value="See this help guide again", inline=False)

            help_embed.set_footer(text="Have fun playing with your new pet! 🐾")

            await ctx.author.send(embed=help_embed)
        
        except discord.Forbidden:
            await ctx.send("I couldn't DM you the help guide. Please check your privacy settings.")

    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Pet adoption cancelled.")

bot.run(TOKEN)





