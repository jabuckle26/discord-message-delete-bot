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

command_list = {'snap': '/snap', 'start': '/start', 'stop': '/stop'}


@client.event
async def on_ready():
    logging.info(f'{client.user} has connected to Discord!')
    schedule_delete.start()


@client.event
async def on_message(message_event):
    if is_bot_tagged(message_event.content):
        logging.info('Bot was tagged.')
        await message_event.channel.send("Don't @ me...Get back to work!")

    if is_bot_command(message_event.content):
        await determine_bot_command(message_event)


@tasks.loop(seconds=delete_timer_seconds)
async def schedule_delete():
    if len(channels_to_clear) > 0:
        for channel_to_clear in channels_to_clear:
            await clear_channel(channel_to_clear)


async def determine_bot_command(message_event):
    if message_event.content == command_list['snap']:
        await clear_channel(message_event.channel)
    elif message_event.content == command_list['start']:
        await handle_start_command(message_event)
    elif message_event.content == command_list['stop']:
        await handle_stop_command(message_event)


async def clear_channel(channel):
    messages = await channel.history(limit=300).flatten()
    if len(messages) > 0:
        logging.info(f'Deleting messages in {channel.name}.')
        for message in messages:
            await message.delete()
        logging.info(f'Deleted messages in {channel.name}.')


async def handle_start_command(message_event):
    if message_event.channel not in channels_to_clear:
        channels_to_clear.add(message_event.channel)
        logging.info(f'Started delete timer on {message_event.channel.name} every {delete_timer_seconds}s.')
        await message_event.channel.send('Messages will be cleared periodically.')
    else:
        await message_event.channel.send(f'Timer already started for "#{message_event.channel.name}".')


async def handle_stop_command(message_event):
    if message_event.channel not in channels_to_clear:
        await message_event.channel.send('This channel has not been flagged for periodic clearing.')
    else:
        channels_to_clear.remove(message_event.channel)
        await message_event.channel.send('Channel no longer set for periodic clearing.')
        logging.info(f'Stopped delete timer on {message_event.channel.name}.')


def is_bot_tagged(message_text):
    return str(client.user.id) in message_text


def is_bot_command(message_text):
    return message_text in list(command_list.values())


client.run(TOKEN)
