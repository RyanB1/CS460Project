from socket import *
from _thread import *

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
                mainMenu()
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
        playGame(connectionSocket,addr)
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
