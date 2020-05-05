from socket import *
from _thread import *
import random

#Server initialization
serverPort = 13009
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(10)
print("The server is ready to recieve")

#File names
loginInfo = "accounts.txt"
questionsFile = "questions.txt"

def createFiles():
    accounts = open(loginInfo,"a+")
    accounts.close()
    questions = open(questionsFile,"a+")
    questions.close()
createFiles()

def pickQuestion():
    #picks a random question from the file
    lines = open(questionsFile).read().splitlines()
    return random.choice(lines)

def playGame(connectionSocket):
    question = pickQuestion()
    print(question.split("\t")[0],"was picked\n")
    #sends question + playgame method to the client
    toClientMsg = "playGame\t"
    for i in range(0,len(question.split("\t"))-1):
        toClientMsg += question.split("\t")[i].strip()+"\t"
    connectionSocket.send(toClientMsg.encode())
    
    while True:
        answer = connectionSocket.recv(1024).decode("ascii")
        if answer == "NextQuestion":
            break
        if answer.split("\t")[0].strip() == "Gameover":
            recordFile = open("playRecord.txt","a+")
            record = answer.split("\t")[1].strip() + "\t" + answer.split("\t")[2].strip() + "\n"
            recordFile.write(record)
            recordFile.close()
            return

        for i in range(1,len(question.split("\t"))):
            if question.split("\t")[i].lower() == answer:
                msg = question.split("\t")[i+1]
                break
            else:
                msg = "Incorrect"
        connectionSocket.send(msg.encode())

def login(connectionSocket,message):
    username = message.split("\t")[1]
    password = message.split("\t")[2]
    print("user logging in")
    #loginFile = open(loginInfo,"r")
    for line in open(loginInfo).readlines():
        account = line.split("\t")
        #first one checks for username, the second ensures the password
        if account[0].strip() == username:
            if account[1].strip() == password:
                #account was found
                print("\nA player with username " + username + " logged in")
                #Sends the username to the main menu function which acts as the login
                mainMenu(username)
        else:
            wrongLogin(connectionSocket)

def wrongLogin(connectionSocket):
    print("\nSomeone used the wrong login information")
    toClientMsg = "wrongLogin"
    connectionSocket.send(toClientMsg.encode())

def register(connectionSocket,message):
    print(message)
    username = message.split("\t")[1]
    password = message.split("\t")[2]
    for line in open(loginInfo).readlines():
        account = line.split("\t")
        print(account[0] + username)
        #Check to see if the account already exists
        if account[0].strip() == username:
            accountExists(connectionSocket)
            return
        
    addAccount = open(loginInfo,"a+")
    addAccount.write(username + "\t" + password + "\n")
    addAccount.close()
    print("\nAccount with username " + username + " added")

def accountExists(connectionSocket):
    print("\nThe account with username " + username + " already exitsts")
    toClientMsg = "alreadyRegistered"
    connectionSocket.send(toClientMsg.encode())
                
def serverMain(connectionSocket,addr):
    clientInput = connectionSocket.recv(1024).decode("ascii")
    method = clientInput.split("\t")[0].strip()

    if method == "playGame":
        playGame(connectionSocket)
    elif method == "CheckIndBestRecord":
        checkIndRecord(connectionSocket,clientInput)
    elif method == "CheckBestRecord":
        checkBest(connectionSocket,clientInput)
    elif method == "register":
        register(connectionSocket,clientInput)
    elif method == "login":
        login(connectionSocket,clientInput)

def main():
    while True:
        connectionSocket, addr = serverSocket.accept()
        print(addr,"connected")
        start_new_thread(serverMain, (connectionSocket,addr,))

main()
