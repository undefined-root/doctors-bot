import random
from random import randint

from common.classes.doctor import DoctorCallStateIds, DoctorCallStateNames, DoctorFields, DoctorCallState, Doctor, Doctors
from helpers.tests import get_random_string, get_random_digits

#region Randomize

def get_random_field() -> DoctorFields:
	return random.choice(list(DoctorFields))

def get_random_fields() -> list[DoctorFields]:
	fields = [get_random_field() for _ in range(len(DoctorFields))]
	unique_fields: list[DoctorFields] = []

	for field in fields:
		if field.value not in [a.value for a in unique_fields]:
			unique_fields.append(field)

	return unique_fields

def get_random_callstate_id() -> DoctorCallStateIds:
	return random.choice(list(DoctorCallStateIds))

def get_random_callstate_name() -> DoctorCallStateNames:
	return random.choice(list(DoctorCallStateNames))

def get_random_callstate() -> DoctorCallState:
	return DoctorCallState(id = get_random_callstate_id())

def get_random_callstates() -> list[DoctorCallState]:
	callstates = [get_random_callstate() for _ in range(len(DoctorCallStateIds))]
	unique_callstates: list[DoctorCallState] = []

	for callstate in callstates:
		if callstate.id not in [a.id for a in unique_callstates]:
			unique_callstates.append(callstate)
	
	return unique_callstates

def get_random_doctor() -> Doctor:
	return Doctor(
		uuid = get_random_string(),
		id = randint(0, 99),
		job = get_random_string(),
		name = get_random_string(),
		address = get_random_string(),
		number = get_random_digits(),
		callstate = get_random_callstate()
	)

def get_random_doctors() -> Doctors:
	return Doctors([get_random_doctor() for _ in range(randint(1, 9))])

#endregion

#region Compare

def compare_callstate(callstate1: DoctorCallState, callstate2: DoctorCallState) -> bool:
	return [callstate1.id, callstate1.name] == [callstate2.id, callstate2.name]

def compare_doctor(doctor1: Doctor, doctor2: Doctor) -> bool:
	list1 = [doctor1.uuid, doctor1.id, doctor1.job, doctor1.name, doctor1.address, doctor1.number]
	list2 = [doctor2.uuid, doctor2.id, doctor2.job, doctor2.name, doctor2.address, doctor2.number]
	
	return list1 == list2 and compare_callstate(doctor1, doctor2)

def compare_doctors(doctors1: Doctors, doctors2: Doctors) -> bool:
	if len(doctors1) != len(doctors2):
		return False

	for i in range(len(doctors1)):
		if not compare_doctor(doctors1[i], doctors2[i]):
			return False
	
	return True

#endregion

#region Test initialization

def test_callstate_init() -> None:
	random_callstate_id = get_random_callstate_id()
	random_callstate_name = next(a for a in DoctorCallStateNames if a.name == random_callstate_id.name)

	callstate1 = DoctorCallState(id = random_callstate_id)
	callstate2 = DoctorCallState(name = random_callstate_name)

	assert callstate1.id == callstate2.id == random_callstate_id.value
	assert callstate2.name == callstate2.name == random_callstate_name.value

def test_doctor_init() -> None:
	doctor1 = get_random_doctor()
	doctor2 = Doctor(doctor1.uuid, doctor1.id, doctor1.job, doctor1.name, doctor1.address, doctor1.number, doctor1.callstate)

	assert compare_doctor(doctor1, doctor2)

def test_doctors_init() -> None:
	random_doctor = get_random_doctor()

	doctors1 = Doctors()
	doctors1.append(random_doctor)

	doctors2 = Doctors([random_doctor])
	assert compare_doctors(doctors1, doctors2)

#endregion

#region Test Doctor

def test_doctor_fields() -> None:
	doctor = get_random_doctor()

	assert doctor.is_field_hidden(DoctorFields.JOB) == False
	doctor.hide_field(DoctorFields.JOB)
	assert doctor.is_field_hidden(DoctorFields.JOB) == True

#endregion

#region Test Doctors

def test_doctors_fields() -> None:
	doctors = get_random_doctors()

	assert len(doctors.print_field(DoctorFields.NUMBER))
	assert doctors.is_field_hidden(DoctorFields.JOB) == False

	doctors.hide_field(DoctorFields.JOB)
	assert doctors.is_field_hidden(DoctorFields.JOB) == True

def test_doctors_hide_fields_except() -> None:
	random_fields = get_random_fields()
	doctors1 = get_random_doctors()
	doctors2 = Doctors.deserialize(doctors1.serialize())

	for field_to_hide in set(DoctorFields) - set(random_fields):
		doctors2.hide_field(field_to_hide)

	doctors1.hide_fields_except(random_fields)
	
	for field in DoctorFields:
		assert doctors1.is_field_hidden(field) == doctors2.is_field_hidden(field)

def test_doctors_hide_doctors_without() -> None:
	callstates = get_random_callstates()
	doctors1 = get_random_doctors()
	doctors2 = Doctors()

	for doctor1 in doctors1:
		if doctor1.callstate.id in [a.id for a in callstates]:
			doctors2.append(doctor1)

	doctors1 = doctors1.get_doctors_with(callstates)
	assert compare_doctors(doctors1, doctors2)

#endregion

#region Test serialization

def test_callstate_serialize() -> None:
	callstate1 = get_random_callstate()
	callstate2 = DoctorCallState.deserialize(callstate1.serialize())

	assert compare_callstate(callstate1, callstate2)

def test_doctor_serialize() -> None:
	doctor1 = get_random_doctor()
	doctor2 = Doctor.deserialize(doctor1.serialize())

	assert compare_doctor(doctor1, doctor2)

def test_doctors_serialize() -> None:
	doctors1 = get_random_doctors()
	doctors2 = Doctors.deserialize(doctors1.serialize())

	assert compare_doctors(doctors1, doctors2)

#endregion