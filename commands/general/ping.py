from discord import Interaction
from discord.ext.commands import Bot

from common.classes.command import Command, CommandAction
from helpers.response import get_success_response

class PingAction(CommandAction):
	async def run(self, interaction: Interaction, bot: Bot) -> None:
		latency_ms = round(bot.latency * 1000)
		response = get_success_response(description = f"Bot latency is `{latency_ms}` ms.")

		await interaction.response.send_message(embed = response)

class PingCommand(Command):
	async def run(self, interaction: Interaction, bot: Bot) -> None:
		await PingAction().run(interaction, bot)