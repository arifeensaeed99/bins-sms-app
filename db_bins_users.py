# Postgres data migration for LT storage
# postgresql-concave-71120

#import the relevant sql library 
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

import psycopg2

user = 'kkrxhdcnukwpky'
password = 'b00307276acd85718b22958bc86632f45018449551928445371c2e38c0d9b379'
host = 'ec2-44-205-41-76.compute-1.amazonaws.com'
port = '5432'
database = 'dciocdjj8v1tq5'

conn = psycopg2.connect(database=database, user=user, password=password, host = host, port = port)
c = conn.cursor()

# link to your database
#engine = create_engine(os.getenv(['postgresql-concave-71120']))
# db = scoped_session(sessionmaker(bind = engine))
# attach the data frame (df) to the database with a name of the 
# table; the name can be whatever you like

# users = pd.DataFrame(view_all_bins_users(), columns = ['username', 'password', 'email', 'phone', 'carrier', 'timezone'])

# bins = pd.DataFrame(view_all_bins_table_data(), columns = ['username', 'bin', 'bin_completion_date', 'bin_status'])
# bins_dates = pd.DataFrame(view_all_bin_dates_table_data(), columns = ['bin_datestamp', 'bin_level', 'username', 'bin'])

# users.to_sql('users_bins_table', con = engine, if_exists='append')

# bins.to_sql('bins_table', con = engine, if_exists='append')
# bins_dates.to_sql('bin_dates_table', con = engine, if_exists='append')
# run a quick test // add to
# print(engine.execute(“SELECT * FROM phil_nlp”).fetchone())    

# db.commit()

import sqlite3
# import psycopg

# DATABASE_URL = os.environ.get('postgresql-concave-71120')
# conn = psycopg.connect(DATABASE_URL) 
# c = conn.cursor()

# Database
# c.execute('DROP TABLE users_bins_table')

    
# Table
def create_users_bins_table():
    c.execute('CREATE TABLE IF NOT EXISTS users_bins_table(username TEXT UNIQUE, password TEXT, email TEXT, phone TEXT UNIQUE, carrier TEXT, timezone TEXT)') # not null

    c.commit()

def add_users_bins_data(username, password, email, phone, carrier, timezone):
    c.execute('INSERT INTO users_bins_table(username, password, email, phone, carrier, timezone) VALUES (?,?,?,?,?, ?)', (username, password, email, phone, carrier, timezone))
    c.commit()

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
    c.commit()
    data = c.fetchall()
    return data