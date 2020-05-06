from socket import *
import random
import os
from _thread import *

# Setup server
serverPort = 13009
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",serverPort))
serverSocket.listen(10)
print("The server is ready to recieve")

loginInfo = "accounts.txt"
questionsFile = "questions.txt"
#bestRecord = "bestRecord.txt"
playRecord = "playRecord.txt"

username = ""
password = ""

def createFiles():
    #This function simply will create the files if they dont already exist
    accounts = open(loginInfo,"a+")
    accounts.close()
    questions = open(questionsFile,"a+")
    questions.close()
    #bestRecordFile = open(bestRecord,"a+")
    #bestRecordFile.close()
    playRecordFile = open(playRecord,"a+")
    playRecordFile.close()
    
createFiles()

def pickQuestion():
    pickedNumArray = [0] * 50
    randomNum = 0
    
    # keep picking a random number until it is a number not in pickedNumArray
    while randomNum not in pickedNumArray:
        randomNum = random.randint(1,50)
        pickedNumArray.append(randomNum)
            
    f = open(questionsFile)
    lines = f.readlines()
    return lines[randomNum]
    #lines = open(questionsFile).read().splitlines()
    #return random.choice(lines)

def playGame(connectionSocket,username):
    
    question = pickQuestion()
    print(question.split("\t")[0],"was picked\n")
    #sends question + playgame method to the client
    toClientMsg = "playGame\t"
    for i in range(0,len(question.split("\t"))-1):
        toClientMsg += question.split("\t")[i].strip()+"\t"
    connectionSocket.send(toClientMsg.encode())
    
    while True:
        answer = connectionSocket.recv(1024).decode("ascii")
        print("Player sent",answer)
        if answer == "NextQuestion":
            print("Player went on to next question")
            #serverMain(connectionSocket)
            #question = pickQuestion()
            break
        if answer.split("\t")[0].strip() == "Gameover":
            print("Game ended")
            recordFile = open(playRecord,"a+")
            record = answer.split("\t")[1].strip() + "\t" + answer.split("\t")[2].strip() + "\n"
            #fileChanges(record)
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
                #I send the username to the main menu to indicate he was logged in

                toServerMsg = "loggedIn"
                connectionSocket.send(toServerMsg.encode())
                return username
                
            else:
                print("\nSomeone used the wrong login information")
                toClientMsg = "wrongLogin"
                connectionSocket.send(toClientMsg.encode())
                

def register(connectionSocket,message):
    username = message.split("\t")[1]
    password = message.split("\t")[2]
    print(username)
    for line in open(loginInfo).readlines():
        account = line.split("\t")
        #Check to see if the account already exists
        if account[0].strip() == username:
            print("\nThe account with username ", username," already exitsts")
            toClientMsg = "alreadyRegistered"
            connectionSocket.send(toClientMsg.encode())
            
            return username
        
    addAccount = open(loginInfo,"a+")
    addAccount.write(username + "\t" + password + "\n")
    addAccount.close()

    toClientMsg = "Registered"
    connectionSocket.send(toClientMsg.encode())
    

    print("\nAccount with username " + username + " added")
    return username

def checkIndRecord(connectionSocket,username):
    bestScore = 0
    for line in open(playRecord).readlines():
        if username == line.split("\t")[0]:
            if int(line.split("\t")[1]) > bestScore:
                bestScore = int(line.split("\t")[1])
                
    print(username + " best score was ",bestScore)
    toClientMsg = "CheckIndBestRecord" + "\t" + str(bestScore)
    connectionSocket.send(toClientMsg.encode())
            

def checkBest(connectionSocket):
    bestScore = 0
    for line in open(playRecord).readlines():
        if int(line.split("\t")[1]) > bestScore:
            bestScore = int(line.split("\t")[1])

    print("The best score is ",bestScore)
    toClientMsg = "CheckBestRecord" + "\t" + str(bestScore)
    connectionSocket.send(toClientMsg.encode())

##def fileChanges(record):
##    #best overall
##    bestRecordFiler = open(bestRecord,"r")
##    score = record.split("\t")[1].strip()
##    print("score",score)
##    username = record.split("\t")[0].strip()
##    print(bestRecordFiler.read().strip())
##    if (score > bestRecordFiler.read().strip()):
##        print("new best score")
##        bestRecordFiler.close()
##        os.remove(bestRecord)
##        bestRecordFileO = open(bestRecord,"a+")
##        bestRecordFileO.write(score)
##        bestRecordFileO.close()
    

def serverMain(connectionSocket):
    while True:
        clientInput = connectionSocket.recv(1024).decode("ascii")
        method = clientInput.split("\t")[0].strip()
        print(method)
        if method == "playGame":
            playGame(connectionSocket,username)
        elif method == "CheckIndBestRecord":
            checkIndRecord(connectionSocket,username)
        elif method == "CheckBestRecord":
            checkBest(connectionSocket)
        elif method == "register":
            username = register(connectionSocket,clientInput)
        elif method == "login":
            username = login(connectionSocket,clientInput)
        else:
            print("Ending Program...")
            connectionSocket.close()
            return

def main():
    
    connectionSocket, addr = serverSocket.accept()
    print(addr,"connected")
    start_new_thread(serverMain, (connectionSocket,))
    

main()

