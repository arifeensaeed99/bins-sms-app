from operator import contains
from re import S
from select import select
import smtplib
from email.message import EmailMessage # Used as text message, add email?
import streamlit as st
import pandas as pd
import datetime
import hashlib
import time
import random
import plotly.express as px
from time import gmtime, strftime, localtime # 

import requests

from dateutil import tz

from db_bins_fxn import *
from db_bins_users import *

def text_alert(subject, body, num, carrier):
    msg = EmailMessage()
    msg['subject'] = subject
    msg.set_content(body)
    msg['to'] = to_carrier_text_formatter(num, carrier)

    user = "bins.sms.app@gmail.com" # Actual Gmail account (Bot)
    msg['from'] = 'Bins SMS App' # replace to be = user?

    pwd = "xixwajdiwsylryap" 

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, pwd)
    server.send_message(msg)
    server.quit()

def to_carrier_text_formatter(number, carrier):
    if carrier == "AT&T":
        return str(number) + "@txt.att.net"
    elif carrier == "Boost Mobile":
        return str(number) + "@sms.myboostmobile.com"
    elif carrier == "Cricket Wireless":
        return str(number) + "@mms.cricketwireless.net"
    elif carrier == "Google Project Fi":
        return str(number) + "@mmg.fi.google.com"
    elif carrier == "Republic Wireless":
        return str(number) + "@text.republicwireless.com"
    elif carrier == "Sprint":
        return str(number) + "@messaging.sprintpcs.com"
    elif carrier == "Straight Talk":
        return str(number) + "@vtext.com"
    elif carrier == "T-Mobile":
        return str(number) + "@tmomail.net"
    elif carrier == "Ting":
        return str(number) + "@message.ting.com"
    elif carrier == "U.S. Cellular":
        return str(number) + "@email.uscc.net"
    elif carrier == "Verizon":
        return str(number) + "@vtext.com"
    elif carrier == "Virgin Mobile":
        return str(number) + "@vmobl.com"

def email_provider_verifier(email):
    for line in open('all_email_provider_domains.txt', 'r').readlines(): # replaced with generic
        if line[:-1] in email:
            return True
            break
        else:
            continue
    return False

def is_uni_email(email):

    # Start traversing the string
    for i in range(len(email)):
 
        if (email[i] == '@'):
            break
 
    domain = email[i+1: len(email)]

    # print(domain)

    # Send a request to Universities HipoLabs for a domain search, use Get Request and Len of Json (yigitguler)
    uni_email = requests.get("http://universities.hipolabs.com/search?domain=" + str(domain))

    # print(uni_email.json())

    if len(uni_email.json()):
        #print('Data is here')
        return True
    else:
        #print('No data here')
        return False

# identity verification
def generate_hashes(password):
        return hashlib.sha256(str.encode(password)).hexdigest()

def verify_hashes(password, hashed_text):
        if generate_hashes(password) == hashed_text:
                return hashed_text
        else:
                return False

def main():
    # Postgres data migration at init for LT storage
    # postgresql-concave-71120

    #import the relevant sql library 
    from sqlalchemy import create_engine
    # link to your database
    engine = create_engine('postgresql-concave-71120', echo = False)
    # attach the data frame (df) to the database with a name of the 
    # table; the name can be whatever you like
    
    users = pd.DataFrame(view_all_bins_users(), columns = ['username', 'password', 'email', 'phone', 'carrier', 'timezone'])

    bins = pd.DataFrame(view_all_bins_table_data(), columns = ['username', 'bin', 'bin_completion_date', 'bin_status'])
    bins_dates = pd.DataFrame(view_all_bin_dates_table_data(), columns = ['bin_datestamp', 'bin_level', 'username', 'bin'])

    users.to_sql('users_bins_table', con = engine, if_exists='append')

    bins.to_sql('bins_table', con = engine, if_exists='append')
    bins_dates.to_sql('bin_dates_table', con = engine, if_exists='append')
    # run a quick test // add to
    # print(engine.execute(“SELECT * FROM phil_nlp”).fetchone())   
    
    
    # Title
    st.title('📊 Bins SMS App')

    # Menu
    menu = ['About', 'Login', 'Create Account', 'Edit Account']
    submenu = ['Report Current Levels', 'See Trends', 'Add Bin', 'Edit Bin Details', 'Delete Bin']
    choice = st.sidebar.selectbox('Menu', menu)

    if choice == 'About':
        st.subheader('About')
        
        # Descriptions
        st.write('This application exists to monitor your Levels and Bins _(defined below)_ daily and over time, and sends you a text message with a Report each time you log-in.')
        st.write("")

        st.latex(" Merriam-Webster:")
        st.write("")
        st.latex("**bin**")
        st.markdown("**bin** _noun_ \ 'bin \ plural **bins**")
        st.write("Definition of _bin_: a box, frame, crib, or enclosed place used for storage")
        st.write("")
        st.write('_In this application, a Bin is a goal, a task, or a means of motivation -- anything you are working on as you journey through life_')
        
        st.write("")

        st.latex("**level**")
        st.write("**level** _noun_ lev·​el \ ˈle-vəl \ plural **levels**")
        st.write("Definition of _level_: a measurement of the difference of altitude of two points...")
        st.write("")
        st.write('_In addition, a Level is an emotion towards how a Bin is going, measured on a scale of 0 to 100, usually with respect to the current moment_')

        st.write("")
        st.write("_______________")
        st.write("")
        st.write("Bearing these definitions in mind, please log in from the left, or, if this is your first time, sign up by providing key information, such as a username, email and **a phone number***.")
        st.caption("_*Please note that the app currently only works for US numbers_")

    elif choice == 'Login':
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type = 'password')
        log_in = st.sidebar.checkbox('Login/Logout')
        
        if log_in:
                create_users_bins_table()
                hashed_password = generate_hashes(password)
                result = login_bins_user(username, verify_hashes(password, hashed_password))
                
                # Initializing Session State
                if 'current_user' not in st.session_state:
                        st.session_state['current_user'] = ''

                if result:                                   
                        
                        create_bins_dates_tables()

                        # Time Zone conversion
                        user_tz = result[0][5]
                        from_zone = tz.gettz('UTC')
                        to_zone = tz.gettz(user_tz)

                        # Dates (UTC Heroku -> user timezone) throughout app session
                        year = datetime.date.today().strftime("%Y")
                        year = year.replace(tz_info=from_zone)
                        year = year.astime(to_zone)

                        month = datetime.date.today().strftime("%B")
                        month = month.replace(tz_info=from_zone)
                        month = month.astime(to_zone)

                        day = datetime.date.today().strftime("%d")
                        day = day.replace(tz_info=from_zone)
                        day = day.astime(to_zone)

                        weekday = datetime.date.today().strftime("%A")
                        weekday = weekday.replace(tz_info=from_zone)
                        weekday = weekday.astime(to_zone)

                        ending = ''
                        if int(day) < 10:
                            day = day[1]
                        if day == '1' or day == '21' or day == '31':
                            ending = "st"
                        elif day == '2' or day == '22':
                            ending = "nd"
                        elif day == '3' or day == '23':
                            ending = "rd"
                        else:
                            ending = "th"

                        st.info("_**{}, {} {}{}, {}**_".format(weekday, month, day, ending, year)) # UTC to local time
                        
                        if username != st.session_state['current_user']: # first login
                                
                                # get averages of most recent 3 Levels per Bin

                                res = get_all_bin_dates_data(username)

                                bins_df = pd.DataFrame(res, columns = ['Bin', 'Datestamp', 'Level'])

                                bins_df = bins_df.sort_values(['Datestamp'], ascending = False) # sort descending by date

                                # st.dataframe(bins_df)

                                top_bins_df = bins_df.groupby(['Bin']).head(3) # group by most recent 3 records per Bin

                                # st.dataframe(top_bins_df)

                                bins_avgs = top_bins_df.groupby(['Bin']).mean() # avgs of most recent 3 Levels per Bin

                                # st.dataframe(bins_avgs)

                                body = ""

                                for row in bins_avgs.itertuples():
                                    if round(row[1], 1) >= 80:
                                        body += str(row[0]) + ": " + str(round(row[1])) + ', so 📉' + "\n"
                                    elif round(row[1], 1) <= 40:
                                        body += str(row[0]) + ": " + str(round(row[1])) + ', so 📈' + "\n"
                                    else:
                                        body += str(row[0]) + ": " + str(round(row[1])) + "\n"

                                # st.write(body)

                                
                        
                                st.session_state['current_user'] = username
                                
                                st.success('Welcome, {}!'.format(username))

                                with st.empty():
                                        # ensure correct timing
                                        timer = 5
                                        st.info('Sending Bins Average Levels Report text message to ' + str(result[0][3]) + '...')
                                        
                                        # Time Zone conversion here for closeness to true time
                                        utc = strftime("%m/%d/%Y at %I:%M:%S %p", localtime()) # UTC in Heroku
                                        utc = utc.replace(tzinfo = from_zone)
                                        user_time = utc.astimezone(to_zone)

                                        text_alert('📊 Latest Bins 3 Levels Report for ' + str(result[0][0]) + ",  " + str(user_time)  +  ":", body, result[0][3], result[0][4])
                                        
                                        while True:
                                            time.sleep(1)
                                            timer -= 1

                                            if timer == 0:
                                                st.empty()
                                                st.success('Text sent!')
                                                break            
                                
                                st.write('NOTE: An average of the **most recent 3** Levels per Bin is used in the report text!')
                                st.write('Additionally, if you recently logged in and out, give some time for the text to deliver, or log out and log in.')
                                st.info('**If you just logged in for the first time ever, you need at least one Level in one Bin for the text message to be useful.**')
                                st.write(" ")
                                st.info("**Begin by selecting the activity Add Bin to add your first Bin if this is your first time ever logging in.**")


                        if st.session_state['current_user'] == username:

                                activity = st.selectbox('Please select from the activities below:', submenu)
                                
                                # Create database
                                create_bins_dates_tables()

                                # Activity
                                
                                if activity == 'Report Current Levels':
                                    st.text("")
                                    st.subheader('Report Current Levels for all your Bins')
                                    
                                    res = view_all_bins_details(username)
                                    
                                    # Emojis 
                                    emojis = ["😀", "😃","😄", "😁", "😆", "😅", "😂", "🤣 ", "😇", "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚", "😋", "😛", "😝", "😜", "🤪", "🤨", "🧐", "🤓", "😎", "🤩", "🥳", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "😣", "😖", "😫", "😩", "🥺", "😢", "😭", "😤", "😠", "😡", "🤬", "🤯", "😳", "🥵", "🥶", "😱", "😨", "😰", "😥", "😓", "🤗", "🤔", "🤭", "🤫", "🤥", "😶", "😐", "😑", "😬", "🙄", "😯", "😦", "😧", "😮", "😲", "🥱", "😴", "🤤", "😪", "😵", "🤐", "🥴", "🤢", "🤮", "🤧", "😷", "🤒", "🤕", "🤑", "🤠", "😈", "👿", "👹", "👺", "🤡", "💩", "👻", "💀", "☠️", "👽", "👾","🤖", "🎃", "😺", "😸", "😹", "😻", "😼", "😽", "🙀", "😿", "😾"]
                                    
                                    st.warning("_**{}'s**_".format(weekday) + " be like: " + str(random.choice(emojis)))

                                    st.write("_Try to do this **at least once a day** to accurately monitor your Levels over time._")

                                    for b in res:
                                        b = b[0]
                                        st.latex(b)
                                        bin_level = st.slider("What Level do you feel like the Bin '{}' is at right now?".format(b), 0, 100)

                                        # UTC Heroku to local user timezone, Time Zone conversion here for closeness to true time
                                        bin_datestamp = strftime("%Y-%m-%d %H:%M:%S", localtime())  # UTC in Heroku
                                        bin_datestamp = bin_datestamp.replace(tzinfo = from_zone)
                                        bin_datestamp = bin_datestamp.astimezone(to_zone)

                                        if st.button('Add new Level data for {}'.format(b)):
                                            add_bin_dates(bin_datestamp, bin_level, username, b)
                                            st.success('Added Level data for Bin "{}" '.format(b) + str(random.choice(emojis))) # add machine learning later for proper emoji to use
                                
                                elif activity == "See Trends":
                                    # Animated Plot
                                    st.subheader('See an Animated Plot of your Bin Levels over time')
                                    st.info("Please choose a start date, end date, and Bin below. NOTE: If you get errors, make sure you choose **proper** start and end dates that the Bin exists in.")
                                    st.write("_More Levels data will smoothen the animation over time!_")
                                    res = get_all_bin_dates_data(username)
                                    bins_df = pd.DataFrame(res, columns = ['Bin', 'Datestamp', 'Level'])

                                    bins_df['Date'] = pd.to_datetime(bins_df['Datestamp']).dt.strftime('%Y-%m-%d')

                                    st.write(bins_df)

                                    bin_options = bins_df['Bin'].unique().tolist()

                                    stamps = st.checkbox('Select this box if you want to see trends based on dates **and timestamps**. Otherwise, only dates will appear as options.')
                                    if stamps:
                                        date_type = 'Datestamp'
                                    else:
                                        date_type = 'Date'
                                    datestamp_options = bins_df[date_type].unique().tolist()
                                    st_datestamp = st.selectbox("What start date would you like to see from?", datestamp_options)
                                    end_datestamp = st.selectbox("What end date would you like to see until?", datestamp_options)
                                    bins = st.select('Which Bin would you like to see?', bin_options) # removed multislect
                                    if st_datestamp <= end_datestamp:
                                        if bins:
                                            bins_df = bins_df[bins_df['Bin'].isin(bins)]
                                            bins_df = bins_df[bins_df[date_type]>=st_datestamp]
                                            bins_df = bins_df[bins_df[date_type]<=end_datestamp]
                                            fig = px.bar(bins_df, x  = "Bin", y = "Level", color = "Bin", range_y = [-10, 110], animation_frame = date_type, animation_group = 'Bin', range_x = [-len(bins),len(bins)*2])
                                            fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 200
                                            fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 200/6
                                            fig.update_geos(projection_type="equirectangular", visible=True, resolution=110)
                                            fig.update_layout(width = 800)
                                            st.write(fig)
                                        else:
                                            st.warning('Please choose a Bin') 
                                    else:
                                        st.warning('Please ensure start date is before end date')

                                elif activity == 'Add Bin':
                                    st.subheader('Add a New Bin')
                                    
                                    # Initial

                                    # UTC Heroku to local user timezone, Time Zone conversion here for closeness to true time
                                    new_bin_date = strftime("%Y-%m-%d %H:%M:%S", localtime())  # UTC in Heroku
                                    new_bin_date = new_bin_date.replace(tzinfo = from_zone)
                                    new_bin_date = new_bin_date.astimezone(to_zone)

                                    display_bin_date = strftime("%Y-%m-%d %I:%M:%S %p", localtime())  # UTC in Heroku
                                    display_bin_date = display_bin_date.replace(tzinfo = from_zone)
                                    display_bin_date = display_bin_date.astimezone(to_zone)

                                    st.write('New Bin initial datestamp:', display_bin_date)
                                    new_bin_status = False 
                                    st.write('New Bin initial completion status:', new_bin_status)
                                    
                                    new_bin = st.text_input("Please enter the new Bin's name:")

                                    if new_bin:
                                        new_bin_level = st.slider('Initially, what Level is this Bin at?', 0, 100)
                                        if new_bin_level:
                                            new_bin_completion_date = st.date_input('What is the ideal completion date of this Bin?')
                                            if str(new_bin_completion_date) > new_bin_date:
                                                if st.button('Add Bin'):
                                                        
                                                        add_bin(username, new_bin, new_bin_date, new_bin_level, new_bin_completion_date, new_bin_status)
                                                        st.success('Added the new Bin!')
                                            else:
                                                st.warning('Please ensure the ideal completion date of the Bin is a future date')
                                        else:
                                            st.warning('Please select the new Bin Level')
                                    else:
                                        st.warning('Please enter a Bin name')
                                    
                                    st.warning('NOTE: Please ensure the Bin is/was not already added (case-sensitive)')
                                
                                elif activity == 'Edit Bin Details':
                                    st.subheader("Edit a Bin's high level Details")

                                    # result = view_all_bins_data(username)

                                    # bins_df = pd.DataFrame(result, columns = ['Bin', 'Datestamp', 'Level', 'Ideal Completion Date', 'Status'])
                                    
                                    #with st.expander("Current Bins"):
                                    #    st.dataframe(bins_df)
                                    
                                    list_of_bins = [i[0] for i in view_all_bins_details(username)]

                                    selected_bin = st.selectbox('Select a Bin to update: ', list_of_bins)

                                    selected_result = get_bin_details_data(selected_bin, username)

                                    if selected_result:
                                        bin = selected_result[0][0]
                                        bin_completion_date = selected_result[0][1] # should all be same
                                        bin_status = selected_result[0][2]

                                        # Layout
                                        new_bin = st.text_area("Enter a new name for the Bin:", bin)
                                        st.caption('Current ideal completion date: ' + str(bin_completion_date))
                                        new_bin_completion_date = st.date_input('What is the new ideal completion date of this Bin?')

                                        # UTC Heroku to local user timezone, Time Zone conversion here for closeness to true time
                                        # new_bin_completion_date = strftime("%Y-%m-%d %H:%M:%S", localtime())  # UTC in Heroku
                                        new_bin_completion_date = new_bin_completion_date.replace(tzinfo = from_zone)
                                        new_bin_completion_date = new_bin_completion_date.astimezone(to_zone)
                                        
                                        if not bin_status:
                                            st.caption('Current Bin completion status: False')
                                        else:
                                            st.caption('Current Bin completion status: True')
                                        new_bin_status = st.checkbox('Is this Bin now completed?', [True, False])

                                        if new_bin:
                                            
                                            # UTC Heroku to local user timezone, Time Zone conversion here for closeness to true time
                                            current_datetime = strftime("%Y-%m-%d %H:%M:%S", localtime())  # UTC in Heroku
                                            current_datetime = current_datetime.replace(tzinfo = from_zone)
                                            current_datetime = current_datetime.astimezone(to_zone)

                                            if str(new_bin_completion_date) > current_datetime:
                                                        if st.button('Update Bin Details'):
                                                            update_bin_details(new_bin, new_bin_completion_date, new_bin_status, username, bin)
                                                            st.success('Successfully updated the details for the Bin: ' + str(new_bin))
                                            else:
                                                st.warning('Please ensure the new ideal completion date for the Bin is a future date')
                                        else:
                                            st.warning('Please enter a new name for the Bin')
                                elif activity == 'Delete Bin':
                                    st.subheader('Delete Bin and Bin Data')
                                    st.warning('NOTE: Deleting a Bin will delete all of its associated data, including your Levels. Please be careful to ensure no data loss.')

                                    list_of_bins = [i[0] for i in view_all_bins_details(username)]

                                    selected_bin = st.selectbox('Select a Bin to delete: ', list_of_bins)

                                    selected_bins_details = get_bin_details_data(selected_bin, username)
                                    selected_bins_dates = get_bin_dates_data(selected_bin, username)

                                    delete_email = st.text_input("Begin deletion process by entering your account's associated email address:")
                                    if delete_email == str(result[0][2]): # matches email on hand for account

                                        if st.checkbox('Are you sure you want to **PERMANENTLY** Delete ALL records of Bins with a Bin of ' + str(selected_bin) +"?"):
                                            
                                                st.error("About to delete Bin with details of records: " + str(selected_bins_details))
                                                st.error("About to delete associated Bin datestamps with records of: " + str(selected_bins_dates))
                                                
                                                if st.button('Yes, Proceed and Delete'):
                                                    delete_bins(username, selected_bin) 
                                                    st.error('Successfully Deleted all records containing Bin ' + str(selected_bin))
                                    else:
                                        st.warning('No email match on hand')



                else:
                    st.warning('Incorrect username or password, please try again...')
        else:
                st.session_state['current_user'] = '' 

                # Postgres data migration at logout for LT storage
                # postgresql-concave-71120

                #import the relevant sql library 
                from sqlalchemy import create_engine
                # link to your database
                engine = create_engine('postgresql-concave-71120', echo = False)
                # attach the data frame (df) to the database with a name of the 
                # table; the name can be whatever you like
                
                users = pd.DataFrame(view_all_bins_users(), columns = ['username', 'password', 'email', 'phone', 'carrier', 'timezone'])

                bins = pd.DataFrame(view_all_bins_table_data(), columns = ['username', 'bin', 'bin_completion_date', 'bin_status'])
                bins_dates = pd.DataFrame(view_all_bin_dates_table_data(), columns = ['bin_datestamp', 'bin_level', 'username', 'bin'])

                users.to_sql('users_bins_table', con = engine, if_exists='append')

                bins.to_sql('bins_table', con = engine, if_exists='append')
                bins_dates.to_sql('bin_dates_table', con = engine, if_exists='append')
                # run a quick test // add to
                # print(engine.execute(“SELECT * FROM phil_nlp”).fetchone())                              

    elif choice == "Create Account":

        special_chars = {'~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/'}

        new_username = st.text_input('Username')
        
        if new_username:
                new_password = st.text_input("Password", type = 'password')
                if new_password:   
                        if len(new_password) >= 6: 
                                l, u, p, d = 0, 0, 0, 0
                                for i in new_password:
                                        # counting lowercase alphabets
                                        if (i.islower()):
                                                l+=1           
                                
                                        # counting uppercase alphabets
                                        if (i.isupper()):
                                                u+=1           
                                
                                        # counting digits
                                        if (i.isdigit()):
                                                d+=1           
                                
                                        # counting the mentioned special characters
                                        if(i in special_chars):
                                                p+=1          
                                if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(new_password)):
                                        confirm_password = st.text_input('Confirm Password', type = 'password')
                                        if confirm_password: 
                                                if new_password == confirm_password:
                                                        st.success('Passwords match!')
                                                        new_email = st.text_input('Email address')
                                                        if new_email: 
                                                            if '@' in new_email:
                                                                if email_provider_verifier(new_email) or is_uni_email(new_email):
                                                                    new_phone = st.text_input('Phone number (digits only)')

                                                                    if new_phone:
                                                                        if len(new_phone) >= 10: #US
                                                                            
                                                                            invalids = ['-', '(', ')', '+', ' ']
                                                                            res = [i for i in invalids if(i in new_phone)]
                                                                            
                                                                            if not res:
                                                                                    new_carrier = st.radio("Your Carrier (US)", ["AT&T", "Boost Mobile", "Cricket Wireless",  "Google Project Fi",  "Republic Wireless","Sprint", "Straight Talk", "T-Mobile",
                                                                        "Ting", "U.S. Cellular", "Verizon", "Virgin Mobile" ])
                                                                                    if new_carrier:
                                                                                        new_timezone = st.selectbox("Please select a timezone:", set(datetime.pytz.all_timezeones_set)) # list of all timezeones
                                                                                        if new_timezone:    
                                                                                            st.success('Everything looks good, press Submit to create an account!')
                                                                                            if st.button('Submit'):
                                                                                                    st.empty()
                                                                                                    create_users_bins_table()
                                                                                                    hashed_new_password = generate_hashes(new_password)
                                                                                                    add_users_bins_data(new_username, hashed_new_password, new_email, new_phone, new_carrier, new_timezone)
                                                                                                    st.success('You have successfully created a new account!')
                                                                                                    st.info('Login to get started with the Bins SMS App from the Sidebar!')
                                                                                        else:
                                                                                            st.warning('Please select a timezone')
                                                                                    else:
                                                                                        st.warning("Please select a carrier")
                                                                            else:
                                                                                st.warning("Please enter a phone number with digits only")
                                                                        else:
                                                                            st.warning('Phone must be greater than or equal to 10 digits long') #US
                                                                    else:
                                                                        st.warning("Enter a phone number")
                                                                else:
                                                                    st.warning('Email must have a real provider domain (personal or university)')
                                                            else:
                                                                st.warning('@ must be in email')
                                                        else:
                                                            st.warning('Enter an email')
                                                else: 
                                                        st.warning('Passwords are not the same!')
                                        else:
                                                st.warning('Please enter a confirm password')
                                else:
                                        st.warning('Password must contain an uppercase, a lowercase, a digit, and a special character')
                        else:
                                st.warning('Password must be at least 6 characters long')
                else:
                    st.warning('Please enter a password')
        else:
                st.warning('Please enter a username')
        st.caption('**Note: username and password are case sensitive!**')
        st.caption('**Ensure that the username and phone number are not associated with any other accounts!**')
    
    elif choice == "Edit Account":
        st.subheader('Edit Account Details')

        current_username = st.text_input("Current Username")
        current_password = st.text_input("Current Password", type = 'password')

        create_users_bins_table()
        hashed_current_password = generate_hashes(current_password)
        result = login_bins_user(current_username, verify_hashes(current_password, hashed_current_password))

        if current_username and current_password:
            if result:
                # st.write(result)

                st.write("Please use the checkbox(es) below to edit the corresponding field(s) below, and leave checked until the button is pressed:")

                special_chars = {'~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/'}

                st.write("------")

                # Username
                if st.checkbox('Edit Username'):
                    st.caption('**Note: username is case sensitive and must not already be claimed**')

                    username = st.text_input('Please enter a new username', result[0][0])
                    if username:
                        if username != result[0][0]:
                            st.success('New username looks good')
                            new_username = username
                        else:
                            st.warning('New username cannot be the same as the old one')
                    else:
                        st.warning('Please enter a new username')
                else:
                    new_username = current_username
                
                st.write("------")
                
                # Password
                if st.checkbox('Change Password'):
                    st.caption("**NOTE: password is case sensitive**")
                    password = st.text_input('Please enter a new password', type = 'password')
                    if password:
                        if generate_hashes(password) != result[0][1]:
                            if len(password) >= 6: 
                                l, u, p, d = 0, 0, 0, 0
                                for i in password:
                                    # counting lowercase alphabets
                                    if (i.islower()):
                                        l+=1           
                            
                                    # counting uppercase alphabets
                                    if (i.isupper()):
                                        u+=1           
                            
                                    # counting digits
                                    if (i.isdigit()):
                                        d+=1           
                                            
                                    # counting the mentioned special characters
                                    if(i in special_chars):
                                        p+=1          
                                if (l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(password)):
                                    confirm_password = st.text_input('Confirm New Password', type = 'password')
                                    if confirm_password: 
                                        if password == confirm_password:
                                            st.success('New password looks good')
                                            new_password = generate_hashes(password) # store new hashed password
                                        else:
                                            st.warning('New password and confirm new password are not the same!')
                                    else:
                                        st.warning('Please enter a confirm new password')
                                        
                                else:
                                    st.warning('New password must contain an uppercase, a lowercase, a digit, and a special character')                                   
                            else:
                                st.warning('New password must be at least 6 characters long')
                        else:
                            st.warning('New password cannot be the same as the old one')
                    else:
                        st.warning('Please enter a new password')
                else:
                    new_password = hashed_current_password

                st.write("------")

                # Email
                if st.checkbox('Edit Email'):
                    # with st.expander('Email'):
                        email = st.text_input('Please enter a new email', result[0][2])
                        if email:
                            if email != result[0][2]:
                                if '@' in email:
                                    if email_provider_verifier(email):
                                        st.success('New email looks good')
                                        new_email = email
                                    else:
                                        st.warning('New email must have a real provider domain')
                                else:
                                    st.warning('@ must be in new email')
                            else:
                                st.warning('New email cannot be the same as the old one')
                else:
                    new_email = result[0][2] # same as old email
                
                st.write("------")

                # Phone
                if st.checkbox('Edit Phone'):

                    phone = st.text_input('Please enter a new phone number (digits only)', result[0][3])
                    if phone:
                        if phone != result[0][3]:
                            if len(phone) >= 10: # US
                                invalids = ['-', '(', ')', '+', ' ']
                                res = [i for i in invalids if(i in phone)]
                                if not res:
                                    st.success("New phone looks good")
                                    new_phone = phone
                                                                                
                                else:
                                    st.warning("Please enter a new phone number with digits only")
                            else:
                                st.warning('New Phone must be greater than or equal to 10 digits long') #US
                        else:
                            st.warning('New phone cannot be the same as the old one')
                    else:
                        st.warning("Please enter a new phone number")
                else:
                    new_phone = result[0][3] # same as old phone

                st.write("------")

                # Carrier
                if st.checkbox('Edit Carrier'):
                    st.text("Current carrier: " + str(result[0][4]))
                    carrier = st.radio("Select a new Carrier (US)", ["AT&T", "Boost Mobile", "Cricket Wireless",  "Google Project Fi",  "Republic Wireless","Sprint", "Straight Talk", "T-Mobile",
                                                                            "Ting", "U.S. Cellular", "Verizon", "Virgin Mobile" ])
                    if carrier:
                        if carrier != str(result[0][4]):
                            new_carrier = carrier
                            st.success('New carrier looks good')
                        else:
                            st.warning("New carrier cannot be the same as previous")
                    else:
                        st.warning('Please select a carrier')
                else:
                    new_carrier = result[0][4] # same as old carrier

                # Carrier
                if st.checkbox('Edit Timezone'):
                    st.text("Current timezone: " + str(result[0][5]))
                    timezone = st.selectbox("Please select a new timezone:", set(datetime.pytz.all_timezeones_set)) 
                    if timezone:
                        if timezone != str(result[0][5]):
                            new_timezone = timezone
                            st.success('New timezone looks good')
                        else:
                            st.warning('New timezone cannot be the same as previous')
                    else:
                        st.warning('Please enter a new timezone')
                else:
                    new_timezone = result[0][5] # same as old timezone
                
                st.write("-----")
                if st.button('Save all user account edits'):
                    st.success('You have successfully edited the account (now) with a username of ' + str(new_username))
                    st.info('Please login again with your new credenitals from the Sidebar to continue using the Bins SMS App')
                    update_bins_user_data(new_username, new_password, new_email, new_phone, new_carrier, new_timezone, current_username, hashed_current_password, result[0][2], result[0][3], result[0][4], result[0][5])
                
            else:
                st.warning("No such username/password match, please re-try")

main()