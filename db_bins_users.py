import sqlite3
import psycopg2
import os

DATABASE_URL = os.environ.get('postgresql-concave-71120')
conn = psycopg2.connect(DATABASE_URL) 
c = conn.cursor()

# Database
# c.execute('DROP TABLE users_bins_table')

    
# Table
def create_users_bins_table():
    c.execute('CREATE TABLE IF NOT EXISTS users_bins_table(username TEXT UNIQUE, password TEXT, email TEXT, phone TEXT UNIQUE, carrier TEXT, timezone TEXT)') # not null

def add_users_bins_data(username, password, email, phone, carrier, timezone):
    c.execute('INSERT INTO users_bins_table(username, password, email, phone, carrier, timezone) VALUES (?,?,?,?,?, ?)', (username, password, email, phone, carrier, timezone))
    conn.commit()

def login_bins_user(username, password):
    c.execute('SELECT * FROM users_bins_table WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    return data

def view_all_bins_users():
    c.execute('SELECT * FROM users_bins_table')
    data = c.fetchall()
    return data


def update_bins_user_data(new_username, new_password, new_email, new_phone, new_carrier, new_timezone, username, password, email, phone, carrier, timezone):
    c.execute('UPDATE users_bins_table SET username = ?, password = ?, email = ?, phone = ?, carrier = ?, timezone = ? WHERE username = ? and password = ? and email = ? and phone = ? and carrier = ? and timezone = ?', (new_username, new_password, new_email, new_phone, new_carrier, new_timezone, username, password, email, phone, carrier, timezone))
    conn.commit()
    data = c.fetchall()
    return data