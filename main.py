import os

import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
discord_token = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix = '/', intents = intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.command(name = "10man")
async def start_10man(ctx):
    message = await ctx.send("React with :thumbsup: to join 10man.")
    @bot.event
    async def on_reaction_add(reaction, user):
        await ctx.send("Registered " + user.name + " for the 10man.")

bot.run(discord_token)