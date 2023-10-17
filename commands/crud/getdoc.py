from uuid import UUID, uuid4
from enum import Enum
from time import time

from discord import Interaction, Embed, SelectOption
from discord_typings import EmbedFieldData
from discord.ext.commands import Bot
from discord.ui import Select

from common.classes.command import Command, NonEphemeralCommand, CommandView, CommandAction
from common.classes.doctor import DoctorCallStateIds, DoctorCallStateNames, DoctorFields, DoctorsSerialized, DoctorCallState, Doctor, Doctors
from common.consts.error_messages import ERROR_OCCURRED_WHILE

from helpers.database import mysql
from helpers.interactions import wait_for_select
from helpers.response import get_default_response, get_error_response

class GetDocView(CommandView):
	FIELDS_SELECT_CUSTOM_ID = "FIELDS_SELECT"
	CALL_STATES_SELECT_CUSTOM_ID = "CALL_STATES"
	_message_id: int

	def __init__(self) -> None:
		super().__init__()
		
		self.add_item(Select(
			custom_id = self.FIELDS_SELECT_CUSTOM_ID,
			placeholder = "Fields ...",
			min_values = 1,
			max_values = len(DoctorFields),
			options = [SelectOption(label = a.value) for a in DoctorFields]
		))
		
		self.add_item(Select(
			custom_id = self.CALL_STATES_SELECT_CUSTOM_ID,
			placeholder = "States ...",
			min_values = 1,
			max_values = len(DoctorCallStateNames),
			options = [SelectOption(label = a.value) for a in DoctorCallStateNames]
		))

	def get_message_id(self) -> int:
		return self._message_id

	async def show(self, interaction: Interaction) -> None:
		await super().show(interaction)

class GetDocAction(CommandAction):
	_fields: list[DoctorFields] = []
	_callstates: list[DoctorCallState] = []
	_serialized_doctors: DoctorsSerialized

	def set_fields(self, value: list[DoctorFields]) -> None:
		self._fields = value
	
	def set_callstates(self, value: list[DoctorCallState]) -> None:
		self._callstates = value

	async def run(self, interaction: Interaction) -> None:
		def serialize_doctors_if_none() -> None:
			def fetch_doctors() -> Doctors:
				class RawDoctorsIndexes(Enum):
					UUID = 0
					ID = 1
					JOB = 2
					NAME = 3
					ADDRESS = 4
					NUMBER = 5
					CALL_STATE_ID = 6

				class RawDoctor: tuple[str, int, str, str, str, str, int]

				def fetch_raw_doctors() -> list[RawDoctor]:
					mysql.execute("SELECT UUID, ID, TYPE, NAME, ADR, NUM, CALL_STATE_ID FROM DOCTORS")
					return mysql.fetchall()

				return Doctors([Doctor(
					uuid = a[RawDoctorsIndexes.UUID.value],
					id = a[RawDoctorsIndexes.ID.value],
					job = a[RawDoctorsIndexes.JOB.value],
					name = a[RawDoctorsIndexes.NAME.value],
					address = a[RawDoctorsIndexes.ADDRESS.value],
					number = a[RawDoctorsIndexes.NUMBER.value],
					callstate = DoctorCallState(id = next(b for b in DoctorCallStateIds if b.value == a[RawDoctorsIndexes.CALL_STATE_ID.value]))
				) for a in fetch_raw_doctors()])

			if not hasattr(self, "_serialized_doctors"):
				self._serialized_doctors = fetch_doctors().serialize()

		def filter_doctors(doctors: Doctors) -> Doctors:
			if len(self._fields):
				doctors.hide_fields_except(self._fields)

			if len(self._callstates):
				doctors = doctors.get_doctors_with(self._callstates)

			return doctors

		def get_response(doctors: Doctors, start_time: float) -> Embed:
			if doctors:
				return get_default_response(
					title = "Doctors received",
					description = "Doctors list",
					fields = [EmbedFieldData(name = a.name, value = doctors.print_field(a)) for a in DoctorFields if not doctors.is_field_hidden(a)],
					fetch_time = time() - start_time
				)
			
			return get_default_response(
				title = "No doctors found",
				description = "Either no doctors exist or all doctors were filtered",
				fetch_time = time() - start_time
			)

		start_time = time()

		try:
			serialize_doctors_if_none()

		except Exception as exception:
			response = get_error_response(description = ERROR_OCCURRED_WHILE.format("getting doctors"), exception = exception)
			await interaction.response.edit_message(embed = response)
			return

		doctors = Doctors.deserialize(self._serialized_doctors)
		doctors = filter_doctors(doctors)
		await interaction.response.edit_message(embed = get_response(doctors, start_time))

class GetDocCommand(NonEphemeralCommand):
	_action: GetDocAction

	def __init__(self) -> None:
		super().__init__()
		self._action = GetDocAction()

	@classmethod
	def dispose(cls) -> None:
		super().dispose()
	
	async def run(self, interaction: Interaction, bot: Bot) -> None:
		async def delete_message(initial_interaction: Interaction, interaction: Interaction) -> None:
			if await initial_interaction.original_response():
				await initial_interaction.delete_original_response()
			else:
				await interaction.message.delete()

		def update_action_values(custom_id: str, values: list[str]) -> None:
			if custom_id == GetDocView.FIELDS_SELECT_CUSTOM_ID:
				self._action.set_fields([DoctorFields(a) for a in values])

			elif custom_id == GetDocView.CALL_STATES_SELECT_CUSTOM_ID:
				self._action.set_callstates([DoctorCallState(name = DoctorCallStateNames(a)) for a in values])

		initial_interaction = interaction
		await GetDocView().show(interaction)
		
		while(True):
			try:
				interaction = await wait_for_select(bot)
			
			except TimeoutError:
				await delete_message(initial_interaction, interaction)
				return

			if self._is_disposed():
				await delete_message(initial_interaction, interaction)
				return

			update_action_values(interaction.data["custom_id"], interaction.data["values"])
			await self._action.run(interaction)

	def _is_disposed(self) -> bool:
		return super().is_disposed()