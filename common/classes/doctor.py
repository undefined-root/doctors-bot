from enum import Enum
from collections import UserList
from typing import TypedDict

class DoctorCallStateIds(Enum):
	CALLED = 1
	NOT_CALLED = 2
	POSTPONED = 3

class DoctorCallStateNames(Enum):
	CALLED = "called"
	NOT_CALLED = "not called"
	POSTPONED = "postponed"

class DoctorFields(Enum):
	ID = "id"
	JOB = "job"
	NAME = "name"
	ADDRESS = "address"
	NUMBER = "number"
	CALL_STATE = "callstate"

class DoctorCallStateSerialized(TypedDict):
	id: int

class DoctorSerialized(TypedDict):
	uuid: str
	id: int
	job: str
	name: str
	address: str
	number: str
	callstate: DoctorCallStateSerialized

class DoctorsSerialized(TypedDict):
	doctors: list[DoctorSerialized]

class DoctorCallState:
	id: int
	name: str

	def __init__(self, id: DoctorCallStateIds = None, name: DoctorCallStateNames = None) -> None:
		if not id:
			self.name = name.value
			self.id = next(a.value for a in DoctorCallStateIds if a.name == name.name)
		
		elif not name:
			self.id = id.value
			self.name = next(a.value for a in DoctorCallStateNames if a.name == id.name)
	
	def serialize(self) -> DoctorCallStateSerialized:
		return {
			"id": self.id
		}

	@classmethod
	def deserialize(cls, serialized_object: DoctorCallStateSerialized) -> "DoctorCallState":
		return cls(id = DoctorCallStateIds(serialized_object["id"]))

class Doctor:
	uuid: str
	id: int
	job: str
	name: str
	address: str
	number: str
	callstate: DoctorCallState
	_hidden_fields: set[DoctorFields]

	def __init__(self, uuid: str, id: int, job: str, name: str, address: str, number: str, callstate: DoctorCallState) -> None:
		self.uuid = uuid
		self.id = id
		self.job = job
		self.name = name
		self.address = address
		self.number = number
		self.callstate = callstate
		self._hidden_fields = set()
	
	def serialize(self) -> DoctorSerialized:
		return {
			"uuid": self.uuid,
			"id": self.id,
			"job": self.job,
			"name": self.name,
			"address": self.address,
			"number": self.number,
			"callstate": self.callstate.serialize()
		}

	@classmethod
	def deserialize(cls, serialized_object: DoctorSerialized) -> "Doctor":
		return cls(
			uuid = serialized_object["uuid"],
			id = serialized_object["id"],
			job = serialized_object["job"],
			name = serialized_object["name"],
			address = serialized_object["address"],
			number = serialized_object["number"],
			callstate = DoctorCallState.deserialize(serialized_object["callstate"])
		)

	def is_field_hidden(self, field: DoctorFields) -> bool:
		return field in self._hidden_fields

	def hide_field(self, field: DoctorFields) -> None:
		self._hidden_fields.add(field)

class Doctors(UserList[Doctor]):
	def __init__(self, doctors: list[Doctor] = []) -> None:
		super().__init__(doctors)

	def serialize(self) -> DoctorsSerialized:
		return {
			"doctors": [doctor.serialize() for doctor in self]
		}

	@classmethod
	def deserialize(cls, serialized_object: DoctorsSerialized) -> "Doctors":
		return cls([Doctor.deserialize(doctor) for doctor in serialized_object["doctors"]])

	def is_field_hidden(self, field: DoctorFields) -> bool:
		return self[0].is_field_hidden(field)

	def get_doctors_with(self, callstates: list[DoctorCallState]) -> "Doctors":
		filtered_doctors = Doctors()

		for doctor in self:
			if doctor.callstate.id in [a.id for a in callstates]:
				filtered_doctors.append(doctor)

		return filtered_doctors

	def hide_field(self, field: DoctorFields) -> None:
		for doctor in self:
			doctor.hide_field(field)

	def hide_fields_except(self, fields: DoctorFields) -> None:
		for field_to_hide in set(DoctorFields) - set(fields):
			self.hide_field(field_to_hide)

	def print_field(self, field: DoctorFields) -> str:
		def get_field_values() -> list[str]:
			if field == DoctorFields.CALL_STATE:
				return [doctor.callstate.name for doctor in self]
		
			return [getattr(doctor, field.value) for doctor in self]
	
		text = ""
		i = 0

		for field_value in get_field_values():
			text += f"`{self[i].id}` {field_value}\n"
			i += 1
			
		return text