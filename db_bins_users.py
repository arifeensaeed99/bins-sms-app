import sqlite3
conn = sqlite3.connect("users_bins_data.db") 
c = conn.cursor()

# Database
# c.execute('DROP TABLE users_bins_table')
    
# Table
def create_users_bins_table():
    c.execute('CREATE TABLE IF NOT EXISTS users_bins_table(username TEXT UNIQUE, password TEXT, email TEXT, phone TEXT UNIQUE, carrier TEXT)') # not null

def add_users_bins_data(username, password, email, phone, carrier):
    c.execute('INSERT INTO users_bins_table(username, password, email, phone, carrier) VALUES (?,?,?,?,?)', (username, password, email, phone, carrier))
    conn.commit()

def login_bins_user(username, password):
    c.execute('SELECT * FROM users_bins_table WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    return data

def view_all_bins_users():
    c.execute('SELECT * FROM users_bins_table')
    data = c.fetchall()
    return data


def update_bins_user_data(new_username, new_password, new_email, new_phone, new_carrier, username, password, email, phone, carrier):
    c.execute('UPDATE users_bins_table SET username = ?, password = ?, email = ?, phone = ?, carrier = ? WHERE username = ? and password = ? and email = ? and phone = ? and carrier = ?', (new_username, new_password, new_email, new_phone, new_carrier, username, password, email, phone, carrier))
    conn.commit()
    data = c.fetchall()
    return data