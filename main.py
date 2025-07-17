import discord
from discord.ext import commands
import random
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

last_word = None
last_player = None
game_active = False
scores = {}

starter_words = [
    "auto", "torba", "kafa", "more",
