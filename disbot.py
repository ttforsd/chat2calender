from dotenv import load_dotenv
import discord
from discord.ext import commands
import os
from time import sleep

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
prefix = "!"  # Change this to your preferred command prefix
bot = commands.Bot(command_prefix=prefix, intents = intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages sent by the bot itself

    if message.content.startswith(prefix):
        # Handle commands here if you want
        await bot.process_commands(message)
    else:
        print(message)
        await message.channel.send(f"Processing {message.content} to make calender event...")
        await msg2json(message)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

async def msg2json(message): 
    l = [] 
    msg = message.content
    for i in range(len(msg)): 
        l.append(msg)
    print(l)
    sleep(5)
    await message.channel.send(f"Done Processing {message.content} to make calender event...")
    return msg


# Replace 'YOUR_TOKEN' with your bot's token
bot.run(token)