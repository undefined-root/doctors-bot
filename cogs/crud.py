from discord import Interaction
from discord.ext.commands import Bot, Cog
from discord.app_commands import command

from commands.crud.getdoc import GetDocCommand
from commands.crud.addoc import AdDocCommand
from commands.crud.rmdoc import RmDocCommand
from commands.crud.eddoc import EdDocCommand

class CrudCog(Cog):
	_bot: Bot

	def __init__(self, bot: Bot):
		self._bot = bot

	@command(description = "Get doctors")
	async def getdoc(self, interaction: Interaction) -> None:
		GetDocCommand.dispose()
		await GetDocCommand().run(interaction, self._bot)

	@command(description = "Add doctor")
	async def addoc(self, interaction: Interaction) -> None:
		await AdDocCommand().run(interaction)

	@command(description = "Remove doctor")
	async def rmdoc(self, interaction: Interaction, id: str) -> None:
		await RmDocCommand().run(interaction, id)

	@command(description = "Edit doctor")
	async def eddoc(self, interaction: Interaction, id: str) -> None:
		await EdDocCommand().run(interaction, id)

async def setup(bot: Bot):
	await bot.add_cog(CrudCog(bot))