import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import asyncio
import json

load_dotenv()

# DISCORD_TOKEN is in .env file
TOKEN = os.getenv("DISCORD_TOKEN")

# Check if token is loading
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

# storing user's pet data
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

# Added function that was missing
def update_pet(user_id, pet_info):
    pet_data[str(user_id)] = pet_info
    save_pet_data(pet_data)

pet_data = load_pet_data()

def get_pet(user_id):
    return pet_data.get(str(user_id))

# Adopting the pet
@bot.command()
async def adopt(ctx):
    uid = str(ctx.author.id)
    if uid in pet_data:
        await ctx.send("You already have a pet! Use `!pet` to interact with it.")
        return
    
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    await ctx.send("What would you like to name your pet?")
    try:
        name_msg = await bot.wait_for("message", check=check, timeout=120.0)
        pet_name = name_msg.content.strip()
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond. Your new pet is waiting!")
        return
    
    try:
        # retry loop in case invalid pet is chosen
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
            "name": pet_name,
            "type": pet_type,
            "hunger": 50,
            "happiness": 50,
            "paused": False
        }

        save_pet_data(pet_data)

        emoji = get_pet_emoji(pet_type)

        await ctx.send(f"You adopted {pet_name} the {pet_type} {emoji}! Use !pet to feed, play and look after them!")

        # adding help command in DMs
        try:
            help_embed = discord.Embed(
                title="🐾 Virtual Pet Bot Guide",
                description="Congratulations for adopting your virtual pet!",
                color=discord.Color.pink()
            )

            help_embed.add_field(name="'!pet'", value="Check on your pet's stats", inline=False)
            help_embed.add_field(name="'!feed'", value="Feed your pet", inline=False)
            help_embed.add_field(name="'!play'", value="Play with your pet", inline=False)
            #help_embed.add_field(name="'!namepet' (new name)", value="Change your pet's name", inline=False) #sort this later
            help_embed.add_field(name="!help", value="See this help guide again", inline=False)

            help_embed.set_footer(text="Have fun playing with your new pet! 🐾")

            await ctx.author.send(embed=help_embed)
        
        except discord.Forbidden:
            await ctx.send("I couldn't DM you the help guide. Please check your privacy settings.")

    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond.")

# pet status
@bot.command()
async def pet(ctx):
    pet = get_pet(ctx.author.id)
    if not pet:
        await ctx.send("You haven't adopted a pet yet. Start the adoption process using '!adopt'")
        return
    emoji = get_pet_emoji(pet["type"])
    await ctx.send(
        f"{emoji} {pet['name']} the {pet['type']}\n"
        f"Hunger: {pet['hunger']}/100\n"
        f"Happiness: {pet['happiness']}/100"
    )

# feeding pet
@bot.command()
async def feed(ctx):
    pet = get_pet(ctx.author.id)
    if not pet:
        await ctx.send("You haven't adopted a pet yet. Start the adoption process using !adopt")
        return
    
    pet["hunger"] = min(100, pet["hunger"] + 20)
    update_pet(ctx.author.id, pet)

    emoji = get_pet_emoji(pet["type"])
    await ctx.send(f"🍓 You fed {emoji} {pet['name']}! Hunger is now {pet['hunger']}/100")

# play with pet
@bot.command()
async def play(ctx):
    pet = get_pet(ctx.author.id)
    if not pet:
        await ctx.send("You haven't adopted a pet yet. Start the adoption process using !adopt")
        return
    
    pet["happiness"] = min(100, pet["happiness"] + 20)
    update_pet(ctx.author.id, pet)

    emoji = get_pet_emoji(pet["type"])
    await ctx.send(f"🧸 You played with {emoji} {pet['name']}! Happiness is now {pet['happiness']}/100")


#add pause later



bot.run(TOKEN)





