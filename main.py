import os
import random
import signal

import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

from logger import log

log("Starting bot")

try:
    load_dotenv(find_dotenv())
    discord_token = os.environ.get("DISCORD_TOKEN")
    log("Discord token loaded")
except Exception as e:
    log(f"Error loading Discord token: {e}")
    exit(1)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

registered_users = []


@bot.event
async def on_ready():
    log(f"Logged in as {bot.user} (ID: {bot.user.id})")


class ButtonJoin(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Join", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        name = interaction.user.name
        if user not in registered_users:
            log(f"{name} joined the 10man")
            registered_users.append(user)
            message = "10man\n\n"
            for users in registered_users:
                message = message + users.name + "\n"
            self.value = True
            if len(registered_users) == 10:
                self.stop()
                log("10man populated")
                captains = get_captains()
                message = message + f"\nCaptains: {captains[0]} and {captains[1]}"
                await interaction.response.edit_message(content=message, view=None)
            else:
                await interaction.response.edit_message(content=message)
        else:
            log(f"{name} tried to join more than once")
            await interaction.response.send_message("You tried to join more than once.", ephemeral=True)

    @discord.ui.button(label="Leave", style=discord.ButtonStyle.red)
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user
        name = interaction.user.name
        if user in registered_users:
            log(f"{name} left the 10man")
            registered_users.remove(user)
            message = "10man\n\n"
            for users in registered_users:
                message = message + users.name + "\n"
            await interaction.response.edit_message(content=message)
            self.value = True
        else:
            log(f"{name} tried to leave a 10man they did not join")
            await interaction.response.send_message("You are not in this 10man.", ephemeral=True)


@bot.command(name="10man")
async def start_10man(ctx):
    registered_users.clear()
    await ctx.send("10man", view=ButtonJoin())
    log(f"{ctx.author.name} has started a 10man")


def get_captains():

    # Select 2 random captains.
    captain1 = random.choice(registered_users)
    registered_users.remove(captain1)
    captain2 = random.choice(registered_users)
    registered_users.remove(captain2)

    captains = []
    captains.append(captain1)
    captains.append(captain2)

    log(f"Selected captains: {captain1} and {captain2}")
    return captains


def signal_handler(sig, frame):
    log("Received Ctrl+C, closing bot")
    exit(1)


signal.signal(signal.SIGINT, signal_handler)

try:
    log("Running bot")
    bot.run(discord_token)
except Exception as e:
    log(f"Error connecting to Discord: {e}")
    exit(1)
