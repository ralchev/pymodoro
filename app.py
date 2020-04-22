#!./venv python3
from os.path import isfile
import pyttsx3
import time
import sqlite3 as sqlite
from datetime import datetime

database = 'database.db'
records_table = '''
                CREATE TABLE IF NOT EXISTS records (
                    id integer PRIMARY KEY,
                    task text NOT NULL,
                    period integer NOT NULL,
                    time text NOT NULL);
                '''
menu = {
    'Start working': 'W',
    'Run analysis': 'A',
    'Take a break': 'B',
    'Exit': 'E'
}

# Currently only checks if we have a database file (not what its schema is) and if we don't, creates it using the records_table statement.
def check_db():
    if not isfile(database):
        new_database = sqlite.connect(database)
        cursor = new_database.cursor()
        cursor.execute(records_table)
        new_database.commit()
        new_database.close()

def write(task, period):
    working_db = sqlite.connect(database)
    cursor = working_db.cursor()
    cursor.execute('INSERT INTO records (task, period, time) VALUES (?, ?, ?)',(task, period, datetime.now()))
    working_db.commit()
    working_db.close()

def run_analysis():
    working_db = sqlite.connect(database)
    cursor = working_db.cursor()
    cursor.execute('''SELECT * FROM records WHERE time BETWEEN date('now') AND date('now', '+1 day');''')
    work_records = cursor.fetchall()
    working_db.close()
    work_log = {}
    total_time = 0
    for record in work_records:
        if record[1] in work_log:
            work_log[record[1]] += record[2]
        else:
            work_log.update({record[1]: record[2]})
    speak('Let us see what you have work on today.')
    print('\nToday you have worked on:')
    for task, time in work_log.items():
        total_time += time
        print('{}: {} minutes'.format(task, time))
    print('\nIn total, you have spent {} hours and {} minutes.\n'.format(total_time // 60, total_time % 60))

def speak(string):
    speak_engine = pyttsx3.init()
    speak_engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')
    speak_engine.say(string)
    speak_engine.runAndWait()

def start_work(task_list=[]):
    if task_list:
        print('This is what you have worked on until now:')
        for task in task_list:
            print(task)
    task = input('What are you going to work on?\n')
    period = int(input('For how long?\n'))
    write(task, period)
    if task not in task_list:
        task_list.append(task)
    speak('Okay, you have {} minutes. Get started!'.format(period))
    print('Working for {} minutes.'.format(period))
    time.sleep(period * 60)
    speak('Okay, time to get up and move.')
    init()

def take_break():
    print('Break for 5 minutes.')
    speak('Okay, stop and take a short break.')
    time.sleep(300)

def init(cont='none'):
    for action, hotkey in menu.items():
        print('{} ({})'.format(action.ljust(13), hotkey))
    command = input()
    if command.lower() == 'w':
        start_work()
        init()
    if command.lower() == 'b':
        take_break()
        init()
    if command.lower() == 'a':
        run_analysis()
        init()
    if command.lower() == 'e':
        print('Bye!')
        exit()
    else:
        print('Wrong choice. Try again.')
        init()

if __name__ == '__main__':
    check_db()
    init()