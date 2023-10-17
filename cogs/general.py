from discord import Interaction
from discord.ext.commands import Bot, Cog
from discord.app_commands import command

from commands.general.ping import PingCommand

class GeneralCog(Cog):
	_bot: Bot

	def __init__(self, bot: Bot) -> None:
		self._bot = bot

	@command(description = "Get bot latency")
	async def ping(self, interaction: Interaction) -> None:
		await PingCommand().run(interaction, self._bot)

async def setup(bot: Bot):
	await bot.add_cog(GeneralCog(bot))