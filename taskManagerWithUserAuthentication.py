import csv
import pandas as pd
import random

global username
global randomNumber
randNumLst = []

#Welcome function
def welcome():
    print("Welcome to Task Management \n")
    print("""select: \n
            1. Login \n
            2. Register \n""")
    selOpt = input()
    
    if(selOpt == "1"):
        login()
    elif(selOpt == "2"):
        if(not register()):
            isLogInSuccesfful = login()
            if(isLogInSuccesfful):
                selectOptions()
        else:
            exit()
    else:
        print("Invalid selection")
        selAgain = input("Need to try again ? Y/N :")
        if(selAgain == "Y"):
            welcome()
        else:
            print("Good Bye !! \n")
            exit()

#Login function    
def login():
    global username
    username = input("Enter user name: \n")
    password = input("Enter password: \n")

    isloggedIn = authenticateUser(username.lower(), password)
    if(bool(isloggedIn)):
        print(f'Welcome {username} !! \n', username)
        selectOptions()
    else:
        print("Invalid username or Password \n")
        tryAgain = input("Try Again ? Y/N :")
        if(tryAgain.lower() == "y"):
            login()
        else:
            print("Good Bye !! \n")
            exit()

#Register function
def register():
    username = input("Enter User Name :\n")
    df = pd.read_csv('C:/lsm/projects/taskManagerWithUserAuthentication/userDetalils.csv') 
    tryAgain = "Y"
    df = df.loc[(df['username'] == username)]
    doExit = False
    while(df.size > 1 and tryAgain.lower() == "y"):
        print("This user Name already exists \n")
        tryAgain = input("Try Again ? Y/N :")
        if(tryAgain.lower() == "y"):
            username = input("Enter User Name :\n")
            df = df.loc[(df['username'] == username)]
            if(df.size <= 1):
                break
        else:
            print("Good Bye !!")
            return True
    password = input("Enter Password :\n")
    file = open('C:/lsm/projects/taskManagerWithUserAuthentication/userDetalils.csv', 'a', newline='')
    writer = csv.writer(file)
    writer.writerow([username, password])
    file.close()
    print("Successfully Registered \n")
    print("Login again : \n")
    return False

#Display Task operations
def selectOptions():
    print("Select Operation : \n")
    print("1. Add Task \n")
    print("2. View Task \n")
    print("3. Update status of Task \n")
    print("4. Delete Task \n")
    print("5. Log Out \n")
    
    selOpt = int(input())
    if(selOpt == 1):
        addTask()
    elif(selOpt == 2):
        viewTask()
    elif(selOpt == 3):
        updateTask()
    elif(selOpt == 4):
        deleteTask()
    elif(selOpt == 5):
        logOut()
    else:
         print("Invalid option \n")
         print("Try Again ? Y/N :")
         tryAgain = console()
         if(tryAgain == "Y"):
             selectOptions()
         else:
             print("Good Bye !! \n")
             exit()

#Display Task Lists
def showTaskList():
    global username 
    df = pd.read_csv("C:/lsm/projects/taskManagerWithUserAuthentication/taskList.csv")
    df = df.loc[df['userName'] == username, ['taskId', 'description', 'status']]
    if(df.size <= 1):
        print("No Tasks Exists")
        print("\n")
    else:
        print(df)
        print("\n")

def viewTask():
    showTaskList()
    selectOptions()

#Add Task function
def addTask():
    global username
    global randomNumber
    global randNumLst
    isNumNotExist = False;
    while(not isNumNotExist):
        randNum = random.randint(1,100000)
        if(randNum not in randNumLst):
            randNumLst.append(randNum)
            randomNumber = randNum
            isNumNotExist = True
    taskId = "task"+str(randomNumber)
    print("Enter description : \n")
    description = input()
    file = open('C:/lsm/projects/taskManagerWithUserAuthentication/taskList.csv', 'a', newline='')
    writer = csv.writer(file)
    writer.writerow([username,taskId, description, "Pending"])
    file.close()
    print("Added Task Successfully \n")
    selectOptions()

#Complete Task function
def updateTask():
    global username
    showTaskList()
    print("Enter TaskId to Complete the task :")
    taskId = input()
    df = pd.read_csv("C:/lsm/projects/taskManagerWithUserAuthentication/taskList.csv") 
    df.loc[(df['userName'] == username) & (df['taskId'] == taskId), ['taskId', 'description', 'status']]
    df['status'] = df['status'].replace({'Pending': 'Completed'}) 
    df.to_csv("C:/lsm/projects/taskManagerWithUserAuthentication/taskList.csv", index=False)    
    print(f"Completed {taskId} Successfully !!", taskId)
    viewTask()

#Delete Task function
def deleteTask():
    global username
    showTaskList()
    print("Enter TaskId to Delete the task :")
    taskId = input()
    df = pd.read_csv("C:/lsm/projects/taskManagerWithUserAuthentication/taskList.csv") 
    i = df.loc[(df['userName'] == username) & (df['taskId'] == taskId)].index
    df = df.drop(i)
    df.to_csv("C:/lsm/projects/taskManagerWithUserAuthentication/taskList.csv", index=False)
    print(f"{taskId} is deleted successfully", taskId)
    viewTask()

#Authenticate user by username and password
def authenticateUser(username, password):
    df = pd.read_csv('C:/lsm/projects/taskManagerWithUserAuthentication/userDetalils.csv') 
    df = df.loc[(df['username'] == username) & (df['password'] == password)]
    if(df.size > 1):
        return True
    else:
        return False
#Log out function
def logOut():
    print("Logged Out Successfully !!! \n")
    welcome()

welcome()