import sqlite3
conn = sqlite3.connect("data.db")
c = conn.cursor()


# Database

# c.execute('DROP TABLE bins_table')
# c.execute('DROP TABLE bin_dates_table')


# Table
def create_bins_dates_tables():
    c.execute('CREATE TABLE IF NOT EXISTS bins_table(username TEXT, bin TEXT, bin_completion_date DATE, bin_status BOOL, CONSTRAINT user_bins_pk PRIMARY KEY (username, bin))') # removed date
    c.execute('PRAGMA foreign_keys = ON')
    c.execute('CREATE TABLE IF NOT EXISTS bin_dates_table(bin_datestamp DATE, bin_level INTEGER, username TEXT, bin TEXT, FOREIGN KEY(username, bin) REFERENCES bins_table(username, bin) ON UPDATE CASCADE)')

# init for both at once
def add_bin(username, bin, bin_datestamp, bin_level, bin_completion_date, bin_status):
    c.execute('INSERT INTO bins_table(username, bin, bin_completion_date, bin_status) VALUES (?,?,?,?)', (username, bin, bin_completion_date, bin_status))
    c.execute('INSERT INTO bin_dates_table(bin_datestamp, bin_level, username, bin) VALUES (?,?,?,?)', (bin_datestamp, bin_level, username, bin))
    
    conn.commit()

def add_bin_dates(bin_datestamp, bin_level, username, bin):
    c.execute('INSERT INTO bin_dates_table(bin_datestamp, bin_level, username, bin) VALUES (?,?,?,?)', (bin_datestamp, bin_level, username, bin))
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
    conn.commit()
    data = c.fetchall()
    return data



# delete all bin_dates and bin_details
def delete_bins(username, bin):
    c.execute('DELETE FROM bin_dates_table WHERE bin = ? AND username = ?', (bin, username))
    c.execute('DELETE FROM bins_table WHERE bin = ? AND username = ?', (bin, username))
    conn.commit()

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
