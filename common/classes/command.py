from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from discord import Interaction
from discord.ui import View, Modal

class Command(ABC):
	@abstractmethod
	async def run(self) -> None:
		pass

class NonEphemeralCommand(Command, ABC):
	_instances: list[Command] = []
	_uuid: UUID

	@abstractmethod
	def __init__(self) -> None:
		self._uuid = uuid4()
		NonEphemeralCommand._instances.append(self)

	@classmethod
	@abstractmethod
	def dispose(cls) -> None:
		for instance in cls._instances:
			del instance

		cls._instances.clear()

	@abstractmethod
	def is_disposed(self) -> bool:
		return self._uuid not in [a._uuid for a in NonEphemeralCommand._instances]

	@abstractmethod
	async def run(self) -> None:
		pass

class CommandAction(ABC):
	@abstractmethod
	async def run(self, interaction: Interaction) -> None:
		pass

class CommandView(View, ABC):
	def __init__(self):
		super().__init__()

	@abstractmethod
	async def show(self, interaction: Interaction) -> None:
		await interaction.response.send_message(view = self)

class CommandModal(Modal):
	@abstractmethod
	async def on_submit(self) -> None:
		pass

	@abstractmethod
	async def show(self, interaction: Interaction) -> None:
		await interaction.response.send_modal(self)