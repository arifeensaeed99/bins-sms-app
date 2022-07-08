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

conn.setAutoCommit(True) # for errors

# Table
def create_users_bins_table():
    c.execute("CREATE TABLE IF NOT EXISTS users_bins_table(username TEXT UNIQUE, password TEXT, email TEXT, phone TEXT UNIQUE, carrier TEXT, timezone TEXT);") # not null
    
    conn.commit()

def add_users_bins_data(username, password, email, phone, carrier, timezone):
    c.execute("INSERT INTO users_bins_table(username, password, email, phone, carrier, timezone) VALUES (%s,%s, %s, %s, %s, %s);",(username, password, email, phone, carrier, timezone))
    
    conn.commit()

def login_bins_user(username, password):
    c.execute("SELECT * FROM users_bins_table WHERE username = %s AND password = %s;", (username, password))
    data = c.fetchall()
    return data

def view_all_bins_users():
    c.execute("SELECT * FROM users_bins_table;")
    data = c.fetchall()
    return data

def update_bins_user_data(new_username, new_password, new_email, new_phone, new_carrier, new_timezone, username, password, email, phone, carrier, timezone):
    c.execute("UPDATE users_bins_table SET username = %s, password = %s, email = %s, phone = %s, carrier = %s, timezone = %s WHERE username = %s and password = %s and email = %s and phone = %s and carrier = %s and timezone = %s;", (new_username, new_password, new_email, new_phone, new_carrier, new_timezone, username, password, email, phone, carrier, timezone))
    
    conn.commit()

def end_bins_users_session():
    c.close()

    conn.close()

    
    