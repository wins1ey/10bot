import os

import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

from logger import log

log("Bot Starting...")

load_dotenv(find_dotenv())
discord_token = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix = '/', intents = intents)

@bot.event
async def on_ready():
    log(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.command(name = "10man")
async def start_10man(ctx):
    message = await ctx.send("React with :thumbsup: to join 10man.")
    log(f"{ctx.author.name} has started a 10man.")

    def check(reaction, user):
        return user != bot.user and str(reaction.emoji) == "👍"

    registered_users = []
    
    while len(registered_users) < 10:

        # Add user to the 10man by reacting to the bot's message.
        reaction, user = await bot.wait_for("reaction_add", check = check)
        if user not in registered_users:
            registered_users.append(user)
            await user.send("You have been registered for the 10man.")
            log(f"{user.name} has registered by reacting.")

        # Remove user
        async def reaction_remove(reaction, user):
            if str(reaction.emoji) == "👍" and user in registered_users:
                registered_users.remove(user)
                await user.send("You have been removed from the 10man.")
                log(f"{user.name} has removed their react and as been dropped.")

        bot.add_listener(reaction_remove, "on_reaction_remove")

    message = await ctx.send("Starting 10man.")
    log("Loop exited!")
        
bot.run(discord_token)
