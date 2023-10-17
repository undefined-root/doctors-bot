import sys
import os
import re
import time

import discord
from discord import Intents
from discord.ext import commands

import helpers.settings as settings
from helpers.settings import Extensions, Paths

class Bot(commands.Bot):
	def __init__(self) -> None:
		super().__init__(command_prefix = ">", intents = Intents.all())
		self.run(settings.token)

	async def setup_hook(self) -> None:
		""" Loads cogs from cogs directory. """
		def get_filename_without_extension(filename: str) -> str:
			return f"cogs.{filename[:-len(Extensions.PYTHON_FILE.value)]}"

		for filename in os.listdir(Paths.COGS.value):
			if filename.endswith(Extensions.PYTHON_FILE.value):
				await self.load_extension(get_filename_without_extension(filename))

	async def on_ready(self) -> None:
		""" Synchronizes slash commands. And outputs bot stats to terminal. """
		self.tree.copy_global_to(guild = settings.guild_id)
		await self.tree.sync(guild = settings.guild_id)

		time_now = time.strftime("%Y-%m-%d %H:%M:%S")
		python_version = re.search(r"\d+\.\d+\.\d+", sys.version).group()
		prefix = f"\033[90m{time_now}\033[0m \033[94mINFO\033[0m     "

		print("\n========================= DOCTORS-BOT STARTED =========================")
		print(f"{prefix}\033[35mbot\033[0m                {self.user} (ID: {self.user.id})")
		print(f"{prefix}\033[35mdiscord.py version\033[0m {discord.__version__}")
		print(f"{prefix}\033[35mpython version\033[0m     {python_version}")