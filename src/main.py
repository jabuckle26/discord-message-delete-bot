import os
import discord
import logging
from src.Bot.Bot import Bot

TOKEN = os.getenv('DISCORD_TOKEN')
print(f'token is {TOKEN}')
bot_client = discord.Client()
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
delete_timer_seconds = 30
channels_to_clear = set()

command_list = {'snap': '/snap', 'start': '/start', 'stop': '/stop'}

bot = Bot(bot_client)

bot.start(TOKEN)
