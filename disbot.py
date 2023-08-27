from dotenv import load_dotenv
import discord
from discord.ext import commands
import os
from time import sleep
from llm import *
from gcal import *
import asyncio

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
prefix = "!"  # Change this to your preferred command prefix
bot = commands.Bot(command_prefix=prefix, intents = intents)

async def llm_wrapper(message):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, text2json, message)
    return result

async def make_calender_wrapper(message, me):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, gcal_main, message, me)
    return result

async def wrapper(query):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, long_wait, query)
    return result

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
        await message.channel.send(f"Processing '{message.content}' to make calender event!")
        task_1 = asyncio.create_task(llm_wrapper(message.content))
        response_1 = await task_1
        await message.channel.send(f"Here are the events info: {response_1}, now adding to google calender!")
        author = message.author.global_name
        if author == os.getenv("DISCORD_NAME_0") or author == os.getenv("DISCORD_NAME_1"):
            me = True 
        else: 
            me = False
        for event in response_1:
            tmp = event["Event_Name"]
            if me: 
                event["Event_Name"] = f"{os.getenv('NAME_0')}: {tmp}"
            else:
                event["Event_Name"] = f"{os.getenv('NAME_1')}: {tmp}"
            # pass cal_json to ical main
            task_2 = asyncio.create_task(make_calender_wrapper(event, me))
            response_2 = await task_2
            await message.channel.send(response_2)
        # task = asyncio.create_task(wrapper(message))
        # response = await task
        # await message.channel.send(f"Response: {response}")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


async def wrapper(a): 
    return long_wait(a)
    
    # await message.channel.send(f"Done Processing {message.content} to make calender event...")




async def make_calender(message): 
    sleep(5)
    print(f"Calender {{message}} made!")

# Replace 'YOUR_TOKEN' with your bot's token
bot.run(token)