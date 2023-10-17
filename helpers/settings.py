import os
from enum import Enum
import dotenv
import discord

class EnvironmentVariables(Enum):
	TOKEN = "TOKEN"
	GUILD = "GUILD"
	COMMANDS_CHANNEL_ID = "COMMANDS_CHANNEL_ID"
	DATABASE_HOST = "DATABASE_HOST"
	DATABASE_USER = "DATABASE_USER"
	DATABASE_PASSWORD = "DATABASE_PASSWORD"
	DATABASE_DATABASE = "DATABASE_DATABASE"

class Extensions(Enum):
	PYTHON_FILE = "py"

class Paths(Enum):
	COGS = "cogs"

dotenv.load_dotenv()

token = os.getenv(EnvironmentVariables.TOKEN.value)
guild_id = discord.Object(id = int(os.getenv(EnvironmentVariables.GUILD.value)))
commands_channel_id = os.getenv(EnvironmentVariables.COMMANDS_CHANNEL_ID.value)
database_host = os.getenv(EnvironmentVariables.DATABASE_HOST.value)
database_user = os.getenv(EnvironmentVariables.DATABASE_USER.value)
database_password = os.getenv(EnvironmentVariables.DATABASE_PASSWORD.value)
database_database = os.getenv(EnvironmentVariables.DATABASE_DATABASE.value)