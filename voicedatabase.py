import os
import time
import speech_recognition as sr
import mysql.connector as sql
import random
import pandas as pd
import pyttsx3
import subprocess
import time
import datetime

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
commands = (
    " Connect to Database \n"
    " Show Databases \n"
    " Select Database [Name] \n"
    " Show TABLES \n"
    " Show TABLE Data \n"
    " Say exit to terminte \n"
)
def Greetings():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
        print("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
        print("Good Afternoon!")

    else:
        speak("Good Evening!")
        print("Good Evening!")

    ass = ("unicorn")
    speak("Welcome to Virtual Environment of Database.I am here to Assist you,by the way I am ")
    print("Welcome to Virtual Environment of Database.I am here to Assist you,by the way I am ")
    speak(ass)
    print(ass)
def speak(audio): #text to speech
    engine.say(audio)
    engine.runAndWait()

def takeCommand(): #speech to text
    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        #r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print("User said:",query)

    except Exception as e:
        print(e)
        print("Unable to Recognize your voice.")
        return "None"

    return query
def connection(status):
    if status:
        resp = ("Yes! your Connection Estabilished .\n"
                "Now go head to explore your data world ! \n")
        print(resp)
        speak(resp)
        print(commands)
    else:
        print("There is a problem with Data Server, I am unable to reach it.")
        speak("There is a problem with Data Server, I am unable to reach it.")
        exit(0)

def db_connect():
    try:

        db_connection = sql.connect(host='localhost', database='', user='root', password='@manvi vanaB2001')
        if db_connection:
            return (db_connection)
        else:
            # resp="Oh! sorry, something went Wrong! while estabilshing the Connection with Database"
            # print(resp)
            # speak(resp)
            return (False)

    except:
        connection(False)

def show_dbs():
    if 'connect to database' not in recorded:
        speak('Please wait ! I am estabilishing secure connection to database !')
        print('Please wait ! I am estabilishing secure connection to database !')
        if db_connect():
            recorded.append('connect to database')
            sce = db_connect()
            db_cursor = sce.cursor()
            db_cursor.execute('show databases')
            table_rows = db_cursor.fetchall()
            df = pd.DataFrame(table_rows)
            speak("Here is the list of Databases available in your store. ")
            print(df)
            return df.values.tolist()
    else:
        if db_connect() is not False:
            # global db_connection
            sce = db_connect()
            db_cursor = sce.cursor()
            db_cursor.execute('show databases')
            table_rows = db_cursor.fetchall()
            df = pd.DataFrame(table_rows)
            speak("Here is the list of Databases available in your store. ")
            print(df)
            return df.values.tolist()
        else:
            exit(0)

def db_select():
    rows = show_dbs()
    l = []
    for i in range(len(rows)):
        l.append(rows[i][0])
    # print("rows",l)
    print("Please Select any one of the given databases")
    speak("You can select any one of the given databases")
    return l

def db_selected():
    rows = db_select()
    for i in range(5):
        dbname = takeCommand()
        # print(rows)
        if dbname in rows:
            print("Yes ,", dbname, " Database is in given list !")
            speak("Yes ," + dbname + " Database is in given list !")
            break
        else:
            print(dbname, " Not matched in given databases list")
            speak(dbname + " Not matched in given databases list")

    db_connection2 = sql.connect(host='localhost', database=dbname, user='root', password='@manvi vanaB2001')
    if db_connection2:
        print("{} Selected. Now you can access the TABLES".format(dbname))
        speak(str(dbname) + " Selected . Now you can access the TABLES. ")
        return db_connection2, dbname

def show_tables():
    conn, dtbname = db_selected()
    if conn is not False:
        # global db_connection

        db_cursor = conn.cursor()
        db_cursor.execute('show tables')
        table_rows1 = db_cursor.fetchall()
        df1 = pd.DataFrame(table_rows1)
        speak("Here is the list of Tables available in " + dtbname + " Database.")
        print(df1)
        return df1.values.tolist(), conn
    else:
        exit(0)

if __name__ == '__main__': #main function
    recorded = []
    Greetings()
    speak("What can i call you?")
    print("What can i call you?")
    x = takeCommand()
    speak("Hello " + x)
    print("Hello " + x)
    speak("here is the list of commands that you can work on Virtual Environment of Database")
    print("here is the list of commands that you can work on Virtual Environment of Database")
    speak(commands)
    print(commands)

    while True:

        query = takeCommand().lower()

        # All the commands said by user will be
        # stored here in 'query' and will be
        # converted to lower case for easily
        # recognition of command
        print(query)
        if query == 'connect to database':
            if query not in recorded:
                if db_connect():
                    connection(True)
                    recorded.append(query)
            else:
                print(' Hey! Cool. I already did that :)- ')
                speak(' Hey! Cool. I already did that !')

        if query == 'show databases':
            show_dbs()
        if query == 'select database':
            db_selected()
        if query == "show tables":
            show_tables()
        if query == 'show table data':
            table, conn = show_tables()
            tables = []
            for i in range(len(table)):
                tables.append(table[i][0])
            print("tables", tables)
            for i in range(5):
                tbname = takeCommand()
                # print(rows)
                if tbname in tables:
                    print("Right! ", tbname, " table is in given list")
                    speak("Right! " + tbname + " Table is in given list")
                    break
                else:
                    print(tbname, " Not matched in given Tables list")
                    speak(tbname + " Not matched in given Tables list")

            db_cursor = conn.cursor()
            qry = 'select * from ' + tbname
            db_cursor.execute(qry)
            table_rows2 = db_cursor.fetchall()
            df2 = pd.DataFrame(table_rows2)
            speak("Here is the Data of the " + tbname + " Table available in your database.")
            print(df2)
        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])

        elif "hibernate" in query or "sleep" in query:
            speak("Hibernating")
            subprocess.call("shutdown / h")

        elif "log off" in query or "sign out" in query:
            speak("Make sure all the application are closed before sign-out")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])

        elif 'exit' in query:
            speak("Thanks for giving me your time")
            exit()