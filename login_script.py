# importing required packages
from pynput.keyboard import Key, Controller
import time
import webbrowser
from datetime import datetime
from datetime import timedelta
import pandas as pd

# Importing my schedule as CSV and adjusting the format so it maches
# the format displayed by strftime()
schedule = pd.read_csv("schedule.csv")
schedule
schedule['tomorrow'] = pd.to_datetime(schedule['Day']) + timedelta(days=1)
schedule['tomorrow_str'] = schedule['tomorrow'].dt.strftime("%d/%b/%y")
schedule['Login_time'] = schedule['Day'].apply(str) + " " + schedule['Schedule'].str[:5]
schedule['Start_Lunch'] = schedule['Day'].apply(str) + " " + schedule['Lunch'].str[:5]
schedule['End_Lunch'] = schedule['Day'].apply(str) + " " + schedule['Lunch'].str[-5:]
schedule['Logout_time'] = schedule['tomorrow_str'].apply(str) + " " + schedule['Schedule'].str[-5:]
schedule['Login_time'] = schedule['Login_time'].str.replace("-", "/")
schedule['Start_Lunch'] = schedule['Start_Lunch'].str.replace("-", "/")
schedule['End_Lunch'] = schedule['End_Lunch'].str.replace("-", "/")
schedule['Logout_time'] = schedule['Logout_time'].str.replace("-", "/")
schedule.head()


keyboard = Controller()
# assign link to the forms that will be filled, to variables
login = 'https://docs.google.com/forms/d/e/1FAIpQLSfbqVtCXifwi2LZBJNTn37Q8PskNvry4lNPXe8zCCaKvLDhig/viewform'
logout = 'https://docs.google.com/forms/d/e/1FAIpQLSdJowd2MKjycmZUZ1QrZQUya2CqchQiLki5rsrqQCxWcfYXtQ/viewform'

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M
dt_string = now.strftime("%d/%b/%y %H:%M")

# comparing the time on schedule to the current time
check_login = schedule['Login_time'].str.contains(pat=dt_string).any()
check_lunch_start = schedule['Start_Lunch'].str.contains(pat=dt_string).any()
check_lunch_end = schedule['End_Lunch'].str.contains(pat=dt_string).any()
check_logout = schedule['Logout_time'].str.contains(pat=dt_string).any()

# setting instructions to fill the form depending on the time
if check_login:
    webbrowser.open_new_tab(login)
    time.sleep(2)
    keyboard.press(Key.tab)
    keyboard.press(Key.tab)
    keyboard.press(Key.space)
    time.sleep(1)
    keyboard.press(Key.tab)
    keyboard.press(Key.enter)
elif check_lunch_start:
    webbrowser.open_new_tab(logout)
    time.sleep(2)
    keyboard.press(Key.tab)
    keyboard.press(Key.tab)
    keyboard.press(Key.down)
    time.sleep(1)
    keyboard.press(Key.tab)
    keyboard.press(Key.enter)
elif check_lunch_end:
    webbrowser.open_new_tab(login)
    time.sleep(2)
    keyboard.press(Key.tab)
    keyboard.press(Key.tab)
    keyboard.press(Key.down)
    time.sleep(1)
    keyboard.press(Key.tab)
    keyboard.press(Key.enter)
elif check_logout:
    webbrowser.open_new_tab(logout)
    time.sleep(2)
    keyboard.press(Key.tab)
    keyboard.press(Key.tab)
    keyboard.press(Key.space)
    time.sleep(1)
    keyboard.press(Key.tab)
    keyboard.press(Key.enter)
# print is only to check the result when it's not the time to login/logout
else:
    print(dt_string)
    print(check_login)
    print(check_lunch_start)
    print(check_lunch_end)
    print(check_logout)
