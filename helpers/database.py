import mysql.connector
from helpers.settings import database_host, database_user, database_password, database_database

_database = mysql.connector.connect(
	host = database_host,
	user = database_user,
	password = database_password,
	database = database_database
)
_database.autocommit = True

mysql = _database.cursor()