from time import time
from discord import Interaction, Embed, TextStyle
from discord.ui import TextInput

from common.classes.command import Command, CommandModal, CommandAction
from common.consts.error_messages import INVALID_VALUE_PROVIDED, ERROR_OCCURRED_WHILE

from helpers.database import mysql
from helpers.response import get_success_response, get_error_response

class AdDocModal(CommandModal):
	title = "Add doctor"

	_job = TextInput(
		label = "Job",
		style = TextStyle.short,
		placeholder = "Augenarzt ...",
		required = True
	)
	
	_name = TextInput(
		label = "Name",
		style = TextStyle.short,
		placeholder = "Sarah ...",
		required = True
	)

	_address = TextInput(
		label = "Address",
		style = TextStyle.short,
		placeholder = "Wernigerode Am Bahnhof 1 ...",
		required = True
	)
	
	_number = TextInput(
		label = "Number",
		style = TextStyle.short,
		placeholder = "0123456789 ...",
		required = True
	)

	async def on_submit(self, interaction: Interaction) -> None:
		await AdDocAction().run(interaction, self._job.value, self._name.value, self._address.value, self._number.value)

	async def show(self, interaction: Interaction) -> None:
		await super().show(interaction)

class AdDocAction(CommandAction):
	async def run(self, interaction: Interaction, job: str, name: str, address: str, number: str) -> None:
		def check_input() -> None:
			if not (number.startswith("0") and str.isdigit(number)):
				raise ValueError(INVALID_VALUE_PROVIDED.format("`number`"))

		def add_doctor_to_server() -> None:
			query = "INSERT INTO DOCTORS (TYPE, NAME, ADR, NUM) VALUES (%(job)s, %(name)s, %(address)s, %(number)s)"
			parameters = { "job": job, "name": name, "address": address, "number": number }

			mysql.execute(query, parameters)

		def get_response(start_time: float) -> Embed:
			return get_success_response(
				title =  "Doctor added",
				description = f"Doctor `{name}` was added to the server storage",
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
			add_doctor_to_server()

		except Exception as exception:
			response = get_error_response(description = ERROR_OCCURRED_WHILE.format("adding doctor"), exception = exception)
			await interaction.response.send_message(embed = response)
			return
		
		await interaction.response.send_message(embed = get_response(start_time))

class AdDocCommand(Command):
	def __init__(self) -> None:
		super().__init__()	

	async def run(self, interaction: Interaction) -> None:
		await AdDocModal().show(interaction)