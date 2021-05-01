# bot.py
import os
import discord
import logging
from discord.ext import tasks


TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
delete_timer_seconds = 30
channels_to_clear = set()

@client.event
async def on_ready():
    logging.info(f'{client.user} has connected to Discord!')
    schedule_delete.start()


@client.event
async def on_message(message_event):
    if message_event.content == '/snap':
        await clear_channel(message_event.channel)
    if message_event.content == '/start':
        if message_event.channel not in channels_to_clear:
            channels_to_clear.add(message_event.channel)
            logging.info(f'Started delete timer on {message_event.channel.name} every {delete_timer_seconds}s.')
            await message_event.channel.send('Messages will be cleared periodically.')
        else:
            await message_event.channel.send(f'Timer already started for "#{message_event.channel.name}".')
    if message_event.content == '/stop':
        if message_event.channel not in channels_to_clear:
            await message_event.channel.send('This channel has not been flagged for periodic clearing.')
        else:
            channels_to_clear.remove(message_event.channel)
            await message_event.channel.send('Channel no longer set for periodic clearing.')
            logging.info(f'Stopped delete timer on {message_event.channel.name}.')


@tasks.loop(seconds=delete_timer_seconds)
async def schedule_delete():
    if len(channels_to_clear) > 0:
        for channel_to_clear in channels_to_clear:
            await clear_channel(channel_to_clear)

async def clear_channel(channel):
    messages = await channel.history(limit=300).flatten()
    if len(messages) > 0:
        logging.info(f'Deleting messages in {channel.name}.')
        for message in messages:
            await message.delete()
        logging.info(f'Deleted messages in {channel.name}.')

client.run(TOKEN)
