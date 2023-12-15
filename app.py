import sys
import gc
import os
import time
import datetime
from getpass import getpass
import json
import mysql.connector
import requests
import bs4


#MYSQL DATABASE CREDENTIALS HERE, CREATING notedb DATABASE EVEN IF IT IS NOT AVAILABLE IN THE SYSTEM
try:
    #TRYING TO CONNECT EXISTING DATABASE
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR PASSWORD",
        database="notedb"
    )
    mycursor = mydb.cursor()
    os.system('clear')
    print("Connected to the database successfully.....")
    time.sleep(3)
except:
    #CREATION A NEW DATABASE
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR PASSWORD"
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE notedb")
    os.system('clear')
    print("Database Created successfully......")
    time.sleep(2)
    #CONNECTING TO THE DATABASE
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="882200485@Vv",
        database="notedb"
    )
    mycursor = mydb.cursor()
    #CREATION USER TABLE
    mycursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
    print("Users table created successfully......")
    time.sleep(2)
    #CREATION USER ACCOUNTS
    sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
    val = [
    ('user1', 'pass1'),
    ('user2', 'pass2')
    ]
    mycursor.executemany(sql, val)
    mydb.commit()
    print("User profiles created successfully......")
    time.sleep(2)
    #CREATION NOTES TABLE
    mycursor.execute("CREATE TABLE notes (id INT AUTO_INCREMENT PRIMARY KEY, subject VARCHAR(255), note VARCHAR(255), userId INT, FOREIGN KEY(userId) REFERENCES users(id), www VARCHAR(255), date DATE)")
    print("Notes table created successfully......")
    time.sleep(2)



#USER CLASS 
class User:
        def __init__(self, name, password):
            self.name = name
            self.password = password
            self.notes = []

        def __str__(self):
            return f"{self.name}({self.password})"    
        #Adding notes
        def add_note(self, note):
            self.notes.append(note)

# NOTES CLASS
class Note:
        def __init__(self, subject, note, user, www, date):
            self.subject = subject
            self.note = note
            self.user = user
            self.date = date
            self.www = www
        
        def __str__(self):
            return f"{self.id}{self.subject}{self.note}{self.user}{self.date}"

note_instances = []
userAuth = False
 
#PASSING USER INPUT TO INT 
def try_parse(input, base = None):
    try:
        return int(input, base) if base else int(input)
    except Exception:
        return 0

#CHECKING USER INPUT HAVING BLANK OR NONE 
def string_blank_input(input):
    if(input == "" or input.isspace()):
        return True
    else:
        return False

#GETTING URL TILE 
def get_title(url):
    try:
        x = requests.request('GET', url)
        html = bs4.BeautifulSoup(x.text, features="html.parser")
        print("URL title fetched :", html.title.text)
        time.sleep(2)
    except:
        print("Fetching unsuccessful !, you may check your internet connection or URL entered. ")

#READING JSON FILE
def read_json(path, dataBaseString, user):
    try:
        file = open(path, "r")
        content = file.read()
        os.system('clear')
        print("__READING JSON MENU__")
        note = json.loads(content)
        print("")
        print(" SUBJECT         : ",note["subject"])
        print(" BODY            : ",note["text"])
        print(" www             : ",note["www"])
        print(" DATE            : ",note["date"])
        print("")
        time.sleep(2)
        get_title(note["www"])
        choice = input("Add to the database (Y/N) : ")
        choice = choice.upper()
        if(choice == "Y"):
            date_string = note["date"]
            date_format = '%Y-%m-%d'
            try:
                dateObject = datetime.datetime.strptime(date_string, date_format)
                date = dateObject
            except ValueError:
                print("Incorrect data format, should be YYYY-MM-DD, Today date added..")
                time.sleep(2)
                date = datetime.datetime.now()
            sql = "INSERT INTO notes (subject, note, userId, www, date) VALUES (%s, %s, %s, %s, %s)"
            val = (note["subject"], note["text"], user, note["www"], date)
            dataBaseString.execute(sql, val)
            mydb.commit()
            time.sleep(1)
            print("")
            print("Note added successfully...")
            time.sleep(2)
    except:
        os.system('clear')
        print("Sorry ! ")
        print("File can not be found ! ..")
        time.sleep(2)

    

#MAIN MENU FUNCTION
def main_menu(auth, user):
    start = True
    while start:
        if(auth):
            os.system('clear')
            print("WELCOME TO THE NOTE APP")
            time.sleep(0.5)
            print("User Account : " + user[1])
            print("")
            time.sleep(0.5)
            print("__MAIN MENU__")
            print("")
            print("1. Create a note ")
            print("2. Retrieve a note")
            print("3. Access JSON file")
            print("4. Logout")
            print("")
            userChoice = input("Make your choice : ")
            
            #Parsing user input between 1 - 3 options
            while try_parse(userChoice) > 4 or try_parse(userChoice) < 1:
                #print(try_parse(userChoice))
                print("invalid Input !, ")
                userChoice = input("Make your choice : ")
            userChoice = int(userChoice)

            #Checking user choice 1
            if(userChoice == 1):
                os.system('clear')
                print("__CREATE NOTES MENU__")
                print("")
                continueFrame = True
                while continueFrame:
                    userSubject = input("Add the Subject : ")

                    #Handling Can not leave the subject blank
                    while try_parse(string_blank_input(userSubject)):
                        print("Subject cannot leave blank,")
                        userSubject = input("Add the Subject : ")
                    time.sleep(0.25)
                    userNote = input("Add the note : ")

                    #Handling Can not leave the note body blank
                    while try_parse(string_blank_input(userNote)):
                        print("Note body cannot leave blank,")
                        userNote = input("Add the note : ")
                    time.sleep(0.25)
                    userWWW = input("Add your web address : ")
                    userDate = datetime.datetime.now()
                    
                    #Adding data to database
                    mycursor = mydb.cursor()
                    sql = "INSERT INTO notes (subject, note, userId, www, date) VALUES (%s, %s, %s, %s, %s)"
                    val = (userSubject, userNote, user[0], userWWW, userDate)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    time.sleep(1)
                    print("")
                    print("Note added successfully...")

                    choice = input("You want to continue (Y/N) : ")
                    choice = choice.upper()
                    if(choice == "Y"):
                        continueFrame = True
                        os.system('clear')
                    else:
                        continueFrame = False
                        os.system('clear')
            #Checking user choice 2
            elif(userChoice == 2):
                os.system('clear')
                print("__RETRIEVE NOTES MENU__")
                print("")
                #Printing all notes
                print("%-10s %-25s %15s %25s %15s" % ("ID", "SUBJECT", "USER", "WWW","DATE"))

                #GET RENDERED THE note TABLE
                mycursor = mydb.cursor()
                mycursor.execute("SELECT notes.id, notes.subject, users.username, notes.www, notes.date, notes.note FROM notes INNER JOIN users ON notes.userID=users.id")
                notes = mycursor.fetchall()

                for note in notes:
                    print("%-10s %-25s %15s %25s %15s" % (note[0], note[1], note[2], note[3] ,note[4]))
                    time.sleep(0.5)
                print("")
                print("You have a Search option")
                print("1. Search by ID")
                print("2. Search by keyword")
                print("3. Main Menu")
                userSearchChoice = input("Your Choice : ")
                #Parsing user input between 1 - 3 options
                while try_parse(userSearchChoice) > 3 or try_parse(userSearchChoice) < 1:
                    print("invalid Input")
                    userSearchChoice = input("Make your choice : ")
                userSearchChoice = int(userSearchChoice)

                #Searching Notes by it's ID
                if(userSearchChoice == 1):
                    userSerachedID = input("Type note id : ")
                    #Checking user input is a numeric value
                    while try_parse(not userSerachedID.isnumeric()):
                        print("invalid input!,")
                        userSerachedID = input("Type note id : ")
                    os.system('clear')
                    print("__FULL NOTE VIEW__")
                    print("")
                    userSerachedID = int(userSerachedID)

                    for note in notes:
                        if(userSerachedID == note[0]):
                                print(" ID              : ",(note[0]))
                                print(" SUBJECT         : ",(note[1]))
                                print(" BODY            : ",(note[5]))
                                print(" USER            : ",(note[2]))
                                print(" www             : ",(note[3]))
                                print(" DATE            : ",(note[4]))
                                print("")
                                print("fetching URL title........")
                                time.sleep(2)
                                print("")
                                #GETTING TITLE OF THE WEB PAGE
                                get_title(note[3])
                                print("")
                                choice = input("Continue (Y/N) : ")
                                choice = choice.upper()
                                if(choice == "Y"):
                                    if(user[1] == note[2]):
                                        userDeleteChoice = input("Do you want to delete this (Y/N) : ")
                                        userDeleteChoice = userDeleteChoice.upper()
                                        if(userDeleteChoice == "Y"):
                                            #Deleting note 
                                            sql = f"DELETE FROM notes WHERE id = {userSerachedID}"
                                            mycursor.execute(sql)
                                            mydb.commit()
                                            os.system('clear')
                                            print("Please wait ....")
                                            time.sleep(0.5)
                                            print("Note successfully deleted ! ")
                                            time.sleep(2)
                                            os.system('clear')
                                            continue
                                        else:
                                            os.system('clear')
                                            continue
                                else:
                                    os.system('clear')
                #Searching Notes by it's substring from note_instances list
                elif(userSearchChoice == 2):
                    userSearchedString = input("Type your key word : ")
                    userSearchedString = userSearchedString.upper()
                    os.system('clear')

                    mycursor.execute("SELECT notes.id, notes.subject, users.username, notes.www, notes.date, notes.note FROM notes INNER JOIN users ON notes.userID=users.id")
                    notes = mycursor.fetchall()
                    for note in notes:
                        if(userSearchedString in note[1].upper() or userSearchedString in note[5].upper()):
                            print("%-10s %-25s %15s %15s" % ("ID", "SUBJECT", "USER", "DATE"))
                            print("%-10s %-25s %15s %15s" % (note[0], note[1], note[2], note[4]))
                            time.sleep(0.5)
                            choice = input("continue (Y/N) : ")
                            choice = choice.upper()
                            if(choice == "Y"):
                                os.system('clear')
                                continue
                            else:
                                os.system('clear')
                                break
                #Back to the previous loop
                elif(userSearchChoice == 3):
                    continue
            elif(userChoice == 3):
                #Reading JSON file here
                mycursor = mydb.cursor()
                path = input("Add you json file path here : ")
                read_json(path, mycursor, user[0])
                
            else:
                return main

#MAIN FUNCTION
def main() -> int:
    while True:
        os.system('clear')
        userName = input("Username : ")
        password = getpass("Password : ")

#CHECK USER LOGIN
        #Getting users from the database
        mycursor.execute("SELECT * FROM users")
        users = mycursor.fetchall()
        for user in users:
            if(userName == user[1] and password == user[2]):
                userAuth = True
                os.system('clear')
                break
            else:
                userAuth = False
        if(userAuth):
             main_menu(userAuth, user)
        else:
             print("Invalid user credentials, Try again...")
             time.sleep(1)
             continue

#RUNNING THE MAIN FUNCTION
if __name__ == '__main__':
    sys.exit(main())