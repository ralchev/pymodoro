#!./venv python3
from os.path import isfile
import pyttsx3
import time
import sqlite3 as sqlite
from datetime import datetime

def check_database():
    database = 'database.db'
    if not isfile(database):
        database = sqlite.connect(database)
        create_table(database)
        database.close()
        return database
    return database

def create_table(database):
    records_table = ''' CREATE TABLE IF NOT EXISTS records (
                            id integer PRIMARY KEY,
                            task text NOT NULL,
                            period integer NOT NULL,
                            time text NOT NULL);
                            '''
    cursor = database.cursor()
    cursor.execute(records_table)

def write_to_database(task, period):
    db = check_database()
    database = sqlite.connect(db)
    with database:
        cursor = database.cursor()
        cursor.execute('INSERT INTO records (task, period, time) VALUES (?, ?, ?)',(task, period, datetime.now()))
        database.commit()
        cursor.close()

def speak(string):
    speak_engine = pyttsx3.init()
    speak_engine.say(string)
    speak_engine.runAndWait()

def start_work():
    speak('What are you going to work on?')
    task = input('Task: \n')
    speak('For how long?')
    period = int(input('Period in minutes: \n'))
    write_to_database(task, period)
    speak('Okay, you have {} minutes. Get started!'.format(period))
    time.sleep(period * 60)
    speak('Okay, do you plan to work some more?')
    to_work = input('y for YES and n for NO \n')
    if to_work.lower() == 'y':
        speak('Stop and take a short break.')
        print('Break for 5 minutes.')
        time.sleep(300)
        start_work()
    else:
        speak('Go get some sleep now!')
        #And here it will print how much time I have spent during the day

def main():
    check_database()
    start_work()

main()
