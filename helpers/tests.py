import string
import random
from random import randint

def get_random_string() -> str:
	chars = string.ascii_letters + string.digits
	return "".join(random.choice(chars) for _ in range(randint(1, 9)))

def get_random_digits() -> str:
	return "".join(random.choice(string.digits) for _ in range(randint(1, 9)))