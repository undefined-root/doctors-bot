from discord import Interaction, InteractionType
from discord.ext.commands import Bot

async def wait_for_select(bot: Bot) -> Interaction:
	def check_select(interaction: Interaction):
		return interaction.type == InteractionType.component

	return await bot.wait_for("interaction", check = check_select, timeout = 60)