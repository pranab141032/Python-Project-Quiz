import sqlite3

connection = sqlite3.connect("quiz.db")


cursor = connection.cursor()
cursor.execute("CREATE TABLE users (name TEXT, pass TEXT, player_type TEXT)")