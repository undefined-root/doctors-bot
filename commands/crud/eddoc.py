from time import time

from discord import Interaction, Embed, TextStyle
from discord.ui import TextInput

from common.classes.command import Command, CommandAction, CommandModal
from common.consts.error_messages import INVALID_VALUE_PROVIDED, ERROR_OCCURRED_WHILE, NO_ARGUMENTS_TO_UPDATE

from helpers.database import mysql
from helpers.response import get_success_response, get_error_response

class EdDocModal(CommandModal):
	title = "Edit doctor"
	_id: str

	_job = TextInput(
		label = "Job",
		style = TextStyle.short,
		placeholder = "Augenarzt ..."
	)

	_name = TextInput(
		label = "Name",
		style = TextStyle.short,
		placeholder = "Sarah ..."
	)

	_address = TextInput(
		label = "Address",
		style = TextStyle.short,
		placeholder = "Wernigerode Am Bahnhof 1 ..."
	)

	_number = TextInput(
		label = "Number",
		style = TextStyle.short,
		placeholder = "0123456789 ..."
	)

	def set_id(self, value: str) -> "EdDocModal":
		self._id = value
		return self

	async def on_submit(self, interaction: Interaction) -> None:
		await EdDocAction().run(interaction, self._id, self._job.value, self._name.value, self._address.value, self._number.value)

	async def show(self, interaction: Interaction) -> None:
		await super().show(interaction)

class EdDocAction(CommandAction):
	async def run(self, interaction: Interaction, id: str, job: str = None, name: str = None, address: str = None, number: str = None) -> None:
		def check_input() -> None:
			if not str.isdigit(id):
				raise ValueError(INVALID_VALUE_PROVIDED.format("`id`"))

			if not (job or name or address or number):
				raise ValueError(NO_ARGUMENTS_TO_UPDATE)

			if not (number.startswith("0") and str.isdigit(number)):
				raise ValueError(INVALID_VALUE_PROVIDED.format("`number`"))

		def edit_doctor_at_server() -> None:
			def get_query() -> str:
				query = "UPDATE DOCTORS SET "
				
				query += "TYPE = %(job)s, " if job else ""
				query += "NAME = %(name)s, " if name else ""
				query += "ADR = %(address)s, " if address else ""
				query += "NUM = %(number)s, " if number else ""

				return query[:-2] + " WHERE ID = %(id)s"

			def get_parameters() -> dict:
				parameters = { "id": int(id) }

				if job:
					parameters["job"] = job
				
				if name:
					parameters["name"] = name
				
				if address:
					parameters["address"] = address
				
				if number:
					parameters["number"] = number

				return parameters

			mysql.execute(get_query(), get_parameters())

		def get_response(start_time: float) -> Embed:
			return get_success_response(
				title = "Doctor edited",
				description = f"Doctor `{id}` edited at the server storage",
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
			edit_doctor_at_server()

		except Exception as exception:
			response = get_error_response(description = ERROR_OCCURRED_WHILE.format("editing doctor"), exception = exception)
			await interaction.response.send_message(embed = response)
			return

		await interaction.response.send_message(embed = get_response(start_time))

class EdDocCommand(Command):
	async def run(self, interaction: Interaction, id: str) -> None:
		await EdDocModal().set_id(id).show(interaction)