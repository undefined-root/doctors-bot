from datetime import datetime

import discord
from discord import Embed
from discord_typings import EmbedFieldData

def get_default_response(title: str = None, description: str = None, fields: list[EmbedFieldData] = [], fetch_time: float = None) -> Embed:
	fetch_time = round(fetch_time, 3) if fetch_time else 0
	time_now = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
	footer_text = f"Operation succeeded ({fetch_time} s) • {time_now}"

	response = Embed(
		title = title,
		description = description,
		color = discord.Color.orange()
	)
	response.set_footer(text = footer_text)

	for field in fields:
		response.add_field(name = field["name"], value = field["value"])
	
	return response

def get_success_response(title: str = "", description: str = "", fetch_time: float = 0) -> Embed:
	fetch_time = round(fetch_time, 3)
	time_now = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
	footer_text = f"Operation succeeded ({fetch_time} s) • {time_now}"

	response = Embed(
		title = title,
		description = description,
		color = discord.Color.green()
	)
	response.set_footer(text = footer_text)
	return response

def get_error_response(title: str = "", description: str = "", exception: Exception = "") -> Embed:
	time_now = datetime.today().strftime("%d-%m-%Y %H:%M:%S")
	footer_text = f"Operation failed • {time_now}"
	
	response = Embed(
		title = title,
		description = f"{description}```{str(exception)}```",
		color = discord.Color.red()
	)
	response.set_footer(text = footer_text)
	return response