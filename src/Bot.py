# bot.py
import os
import discord
from discord.ext import tasks
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message_event):
    if message_event.content == '/snap':
        await schedule_delete(message_event.channel)
    if message_event.content == '/starttimer':
        schedule_delete.start(message_event.channel)
    if message_event.content == '/endtimer':
        schedule_delete.stop(message_event.channel)


@tasks.loop(seconds=30)
async def schedule_delete(channel):
    messages = await channel.history(limit=300).flatten()
    for message in messages:
        await message.delete()

client.run(TOKEN)
