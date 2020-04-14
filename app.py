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
    print('\nToday you have worked on:')
    for task, time in work_log.items():
        total_time += time
        print('{}: {} minutes'.format(task, time))
    print('\nIn total, you have spent {} hours and {} minutes'.format(total_time // 60, total_time % 60))

def speak(string):
    speak_engine = pyttsx3.init()
    speak_engine.say(string)
    speak_engine.runAndWait()

def start_work(task_list=[]):
    print('What are you going to work on?')
    if task_list:
        print('This is what you have worked on until now:')
        for task in task_list:
            print(task + '\n')
    task = input('Task: \n')
    print('For how long?')
    period = int(input('Period in minutes: \n'))
    write(task, period)
    if task not in task_list:
        task_list.append(task)
    speak('Okay, you have {} minutes. Get started!'.format(period))
    print('Working for {} minutes.'.format(period))
    time.sleep(period * 60)
    speak('Okay, time to get up and move.')
    print('Are you going to work some more?')
    to_work = input('y for YES and n for NO \n')
    if to_work.lower() == 'y':
        speak('Stop and take a short break.')
        print('Break for 5 minutes.')
        time.sleep(300)
        speak('Okay, break is over. Come back here!')
        start_work(task_list)
    else:
        speak('Let\'s us see what you have worked on today.')
        run_analysis()
        speak('Now go get some sleep!')

if __name__ == '__main__':
    check_db()
    start_work()
