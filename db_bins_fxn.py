# Postgres data for for LT storage
# change language, remove commits
#import the relevant libraries
import psycopg2

user = 'kkrxhdcnukwpky'
password = 'b00307276acd85718b22958bc86632f45018449551928445371c2e38c0d9b379'
host = 'ec2-44-205-41-76.compute-1.amazonaws.com'
port = '5432'
database = 'dciocdjj8v1tq5'

conn = psycopg2.connect(database=database, user=user, password=password, host = host, port = port)
c = conn.cursor()


conn.set_session(autocommit=True) # for errors

# Table
def create_bins_dates_tables():
    c.execute("CREATE TABLE IF NOT EXISTS bins_table(username TEXT, bin TEXT, bin_completion_date DATE, bin_status BOOL, CONSTRAINT user_bins_pk PRIMARY KEY (username, bin));") # removed date
    c.execute("PRAGMA foreign_keys = ON;")
    c.execute("CREATE TABLE IF NOT EXISTS bin_dates_table(bin_datestamp DATE, bin_level INTEGER, username TEXT, bin TEXT, FOREIGN KEY(username, bin) REFERENCES bins_table(username, bin) ON UPDATE CASCADE);")

    conn.commit()

# init for both at once
def add_bin(username, bin, bin_datestamp, bin_level, bin_completion_date, bin_status):
    c.execute("INSERT INTO bins_table(username, bin, bin_completion_date, bin_status) VALUES (%s,%s,%s,%s);", (username, bin, bin_completion_date, bin_status))
    c.execute("INSERT INTO bin_dates_table(bin_datestamp, bin_level, username, bin) VALUES (%s,%s,%s,%s);", (bin_datestamp, bin_level, username, bin))

    conn.commit()

def add_bin_dates(bin_datestamp, bin_level, username, bin):
    c.execute("INSERT INTO bin_dates_table(bin_datestamp, bin_level, username, bin) VALUES (%s,%s,%s,%s);", (bin_datestamp, bin_level, username, bin))

    conn.commit()


#def view_all_bins_data(username):
#    c.execute('SELECT bin, bin_date, bin_level, bin_completion_date, bin_status FROM bins_table WHERE username = "{}"'.format(username))
#    data = c.fetchall()
#    return data

#def view_unique_bins_date(username):
#    c.execute('SELECT DISTINCT note FROM note_table WHERE username = ?', (username,))
#    data = c.fetchall()
#    return data

def view_all_bins_details(username):
    c.execute("SELECT bin FROM bins_table WHERE username = %s;", (username)) # no need for DISTINCT
    data = c.fetchall()
    return data

#def view_all_bins_statuses(username):
#    c.execute('SELECT DISTINCT note_status FROM note_table WHERE username = ? AND is_task = True', (username,))
#    data = c.fetchall()
#    return data

# details for a given bin
def get_bin_details_data(bin, username):
    c.execute("SELECT bin, bin_completion_date, bin_status FROM bins_table WHERE bin  = %s AND username = %s;", (bin, username))
    data = c.fetchall()
    return data

# get all bins dates data
def get_all_bin_dates_data(username):
    c.execute("SELECT bin, bin_datestamp, bin_level FROM bin_dates_table WHERE username = %s;", (username))
    data = c.fetchall()
    return data

# get bins dates data for a specific bin
def get_bin_dates_data(bin, username):
    c.execute("SELECT bin_datestamp, bin_level, username, bin FROM bin_dates_table WHERE username = %s AND bin = %s;", (username, bin))
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
    c.execute("UPDATE bins_table SET bin = %s, bin_completion_date = %s, bin_status = %s WHERE username = %s and bin = %s;", (new_bin, new_bin_completion_date, new_bin_status, username, bin))
    data = c.fetchall()
    conn.commit()
    return data

# delete all bin_dates and bin_details
def delete_bins(username, bin):
    c.execute("DELETE FROM bin_dates_table WHERE bin = %s AND username = %s;", (bin, username))
    c.execute("DELETE FROM bins_table WHERE bin = %s AND username = %s;", (bin, username))
    conn.commit()

# Get ALL bins_table data 
def view_all_bins_table_data():
    c.execute("SELECT * FROM bins_table;")
    data = c.fetchall()
    return data

# Get ALL bin_dates_table data 
def view_all_bin_dates_table_data():
    c.execute("SELECT * FROM bin_dates_table;")
    data = c.fetchall()
    return data
