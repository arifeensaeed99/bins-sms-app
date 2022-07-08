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
# ngine = create_engine(os.getenv('postgres://kkrxhdcnukwpky:b00307276acd85718b22958bc86632f45018449551928445371c2e38c0d9b379@ec2-44-205-41-76.compute-1.amazonaws.com:5432/dciocdjj8v1tq5'))
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
# c = conn.cursor()import sqlite3
# import psycopg

# DATABASE_URL = os.environ.get('postgresql-concave-71120')
# conn = psycopg.connect(DATABASE_URL) 
#  c = conn.cursor()

# Database

# c.execute('DROP TABLE bins_table')
# c.execute('DROP TABLE bin_dates_table')


# Table
def create_bins_dates_tables():
    c.execute('CREATE TABLE IF NOT EXISTS bins_table(username TEXT, bin TEXT, bin_completion_date DATE, bin_status BOOL, CONSTRAINT user_bins_pk PRIMARY KEY (username, bin))') # removed date
    c.execute('PRAGMA foreign_keys = ON')
    c.execute('CREATE TABLE IF NOT EXISTS bin_dates_table(bin_datestamp DATE, bin_level INTEGER, username TEXT, bin TEXT, FOREIGN KEY(username, bin) REFERENCES bins_table(username, bin) ON UPDATE CASCADE)')

    c.commit()

# init for both at once
def add_bin(username, bin, bin_datestamp, bin_level, bin_completion_date, bin_status):
    c.execute('INSERT INTO bins_table(username, bin, bin_completion_date, bin_status) VALUES (?,?,?,?)', (username, bin, bin_completion_date, bin_status))
    c.execute('INSERT INTO bin_dates_table(bin_datestamp, bin_level, username, bin) VALUES (?,?,?,?)', (bin_datestamp, bin_level, username, bin))
    
    c.commit()

def add_bin_dates(bin_datestamp, bin_level, username, bin):
    c.execute('INSERT INTO bin_dates_table(bin_datestamp, bin_level, username, bin) VALUES (?,?,?,?)', (bin_datestamp, bin_level, username, bin))
    c.commit()

#def view_all_bins_data(username):
#    c.execute('SELECT bin, bin_date, bin_level, bin_completion_date, bin_status FROM bins_table WHERE username = "{}"'.format(username))
#    data = c.fetchall()
#    return data

#def view_unique_bins_date(username):
#    c.execute('SELECT DISTINCT note FROM note_table WHERE username = ?', (username,))
#    data = c.fetchall()
#    return data

def view_all_bins_details(username):
    c.execute('SELECT bin FROM bins_table WHERE username = ?', (username,)) # no need for DISTINCT
    data = c.fetchall()
    return data

#def view_all_bins_statuses(username):
#    c.execute('SELECT DISTINCT note_status FROM note_table WHERE username = ? AND is_task = True', (username,))
#    data = c.fetchall()
#    return data

# details for a given bin
def get_bin_details_data(bin, username):
    c.execute('SELECT bin, bin_completion_date, bin_status FROM bins_table WHERE bin  = "{}" AND username = "{}"'.format(bin, username))
    data = c.fetchall()
    return data

# get all bins dates data
def get_all_bin_dates_data(username):
    c.execute('SELECT bin, bin_datestamp, bin_level FROM bin_dates_table WHERE username = "{}"'.format(username))
    data = c.fetchall()
    return data

# get bins dates data for a specific bin
def get_bin_dates_data(bin, username):
    c.execute('SELECT bin_datestamp, bin_level, username, bin FROM bin_dates_table WHERE username = "{}" AND bin = "{}"'.format(username, bin))
    data = c.fetchall()
    return data

#def get_status_task_notes(note_status, username):
#    c.execute('SELECT note, is_task, note_status, note_due_date, pred_category FROM note_table WHERE note_status  = "{}" AND username = "{}"'.format(note_status, username))
#    data = c.fetchall()
#    return data

#def get_note(note, username):
#    c.execute('SELECT note, is_task, note_status, note_due_date, pred_category FROM note_table WHERE note = ? AND username = ?', (note, username, ))
#    data = c.fetchall()
#    return data

# only changing bin name, completion date, status (Details)
def update_bin_details(new_bin, new_bin_completion_date, new_bin_status, username, bin):
    c.execute('UPDATE bins_table SET bin = ?, bin_completion_date = ?, bin_status = ? WHERE username = ? and bin = ?', (new_bin, new_bin_completion_date, new_bin_status, username, bin))
    c.commit()
    data = c.fetchall()
    return data



# delete all bin_dates and bin_details
def delete_bins(username, bin):
    c.execute('DELETE FROM bin_dates_table WHERE bin = ? AND username = ?', (bin, username))
    c.execute('DELETE FROM bins_table WHERE bin = ? AND username = ?', (bin, username))
    c.commit()

# Get ALL bins_table data 
def view_all_bins_table_data():
    c.execute('SELECT * FROM bins_table')
    data = c.fetchall()
    return data

# Get ALL bin_dates_table data 
def view_all_bin_dates_table_data():
    c.execute('SELECT * FROM bin_dates_table')
    data = c.fetchall()
    return data
