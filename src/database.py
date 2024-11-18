import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..//data")
DB_PATH = os.path.join(DB_DIR, "sistema.db")


def save_close_register(date, opening_value, closing_value, total_entries, total_exits, observations):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO close_registers (date, opening_value, closing_value, total_entries, total_exits, observations)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (date, opening_value, closing_value, total_entries, total_exits, observations))
    connection.commit()
    connection.close()