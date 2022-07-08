# Postgres data for for LT storage
# remove commits, change language for Postgres
#import the relevant libraries
import psycopg2

user = 'kkrxhdcnukwpky'
password = 'b00307276acd85718b22958bc86632f45018449551928445371c2e38c0d9b379'
host = 'ec2-44-205-41-76.compute-1.amazonaws.com'
port = '5432'
database = 'dciocdjj8v1tq5'

conn = psycopg2.connect(database=database, user=user, password=password, host = host, port = port)
c = conn.cursor()

# Table
def create_users_bins_table():
    c.execute('CREATE TABLE IF NOT EXISTS users_bins_table(username TEXT UNIQUE, password TEXT, email TEXT, phone TEXT UNIQUE, carrier TEXT, timezone TEXT)') # not null

def add_users_bins_data(username, password, email, phone, carrier, timezone):
    c.execute('INSERT INTO users_bins_table(username, password, email, phone, carrier, timezone) VALUES ({},{}, {}, {}, {}, {})'.format(username, password, email, phone, carrier, timezone))

def login_bins_user(username, password):
    c.execute('SELECT * FROM users_bins_table WHERE username = {} AND password = {}'.format(username, password))
    data = c.fetchall()
    return data

def view_all_bins_users():
    c.execute('SELECT * FROM users_bins_table')
    data = c.fetchall()
    return data


def update_bins_user_data(new_username, new_password, new_email, new_phone, new_carrier, new_timezone, username, password, email, phone, carrier, timezone):
    c.execute('UPDATE users_bins_table SET username = {}, password = {}, email = {}, phone = {}, carrier = {}, timezone = {} WHERE username = {} and password = {} and email = {} and phone = {} and carrier = {} and timezone = {}'.format(new_username, new_password, new_email, new_phone, new_carrier, new_timezone, username, password, email, phone, carrier, timezone))
    data = c.fetchall()
    return data