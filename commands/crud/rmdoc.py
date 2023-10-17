from time import time
from discord import Interaction, Embed

from common.classes.command import Command, CommandAction
from common.consts.error_messages import INVALID_VALUE_PROVIDED

from helpers.database import mysql
from helpers.response import get_success_response, get_error_response

class RmDocAction(CommandAction):
	async def run(self, interaction: Interaction, id: str) -> None:
		def check_input() -> None:
			if not str.isdigit(id):
				raise ValueError(INVALID_VALUE_PROVIDED.format("`id`"))

		def remove_doc_from_server() -> None:
			query = "DELETE FROM DOCTORS WHERE ID = %(id)s"
			parameters = { "id": int(id) }

			mysql.execute(query, parameters)

		def get_response(start_time: float) -> Embed:
			return get_success_response(
				title = "Doctor removed",
				description = f"Doctor `{id}` was either removed or not found",
				fetch_time = time() - start_time
			)

		start_time = time()

		try:
			check_input()

		except ValueError as exception:
			response = get_error_response(description = str(exception))
			await interaction.response.send_message(embed = response)
			return

		try:
			remove_doc_from_server()

		except Exception as exception:
			response = get_error_response(description = "Error occurred while removing doctor", exception = exception)
			await interaction.response.send_message(embed = response)
			return

		await interaction.response.send_message(embed = get_response(start_time))

class RmDocCommand(Command):
	async def run(self, interaction: Interaction, id: str) -> None:
		await RmDocAction().run(interaction, id)