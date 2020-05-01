from socket import * 

#def playGame(clientSocket):

def login(clientSocket):
    username = input("Input your username: ")
    pass = input("Input your password: ")
    message = username + "\t" + pass
    serverMsg = "login"
    clientSocket.send(serverMsg.encode())
    
def register(clientSocket):
    newUsername = input("Input an username: ")
    newPass = input("Input a password: ")
    message = newUsername + "\t" + newPass
    serverMsg = "register"
    clientSocket.send(serverMsg.encode())
    
def alreadyRegistered(clientSocket):
    print("The username you chose was already registered, try again")
    register(clientSocket)
    
def personalBest(clientSocket):
    serverMsg = "checkIndividual"
    clientSocket.send(serverMsg.encode())
    response = clientSocket.recv(1024).decode("ascii")

    if response.split("\t")[0].strip() != "checkIndividual":
        print("Error getting record.")
        return
    
    print("Your personal best is:",response.split("\t")[1].strip(),"points\n")

def allScores(clientSocket):
    serverMsg = "checkAll"
    clientSocket.send(serverMsg.encode())
    response = clientSocket.recv(1024).decode("ascii")
    responseList = response.split("\n")

    if response.split("\t")[0].strip() != "checkAll":
        print("Error getting record.")
        return

    print("Scores for all players:\n")
    for line in range(1,len(responseList)-1):
        print(responseList[line])
    
def bestOverall(clientSocket):
    serverMsg = "checkBestAll"
    clientSocket.send(serverMsg.encode())
    response = clientSocket.recv(1024).decode("ascii")

    if response.split("\t")[0].strip() != "checkBestAll":
        print("Error getting record.")
        return

    print("The best overall score:",response.split("\t")[1].strip(),"points\n")
    
def specificPlayerBest(clientSocket):
    user = input("Input a username to check the players best score: ")
    serverMsg = "checkBestSpecific\t"+user
    clientSocket.send(serverMsg.encode())
    response = clientSocket.recv(1024).decode("ascii")
    
    if response.split("\t")[0].strip() != "checkBestSpecific":
        print("Error getting record.")
        return
    
    print("User "+user+" has a best score of:",response.split("\t")[1].strip(),"points\n")

def clientMain():
    serverName = "localhost"
    serverPort = 13009
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    #Login
    playerStatus = int(input("Welcome to Family Feud! Choose one of the following:\n 1. Login\n 2. Register"))
    if playerStatus == 1:
        login(clientSocket)
    else:
        register(clientSocket)

    #Choosing what player wants to do
    while True:
        print("""
        1.Play Game
        2.Check Your Best Score 
        3.Check All Scores
        4.Check Best Overall Score
        5.Check Specific Players' Best Score
        6.Quit
        """)
        choice = int(input("Enter your choice: "))
                     
        if choice == 1:
            playGame(clientSocket)
        elif choice == 2:
            personalBest(clientSocket)
        elif choice == 3:
            allScores(clientSocket)
        elif choice == 4:
            bestOverall(clientSocket)
        elif choice == 5:
            specificPlayerBest(clientSocket)
        else:
            print("Exiting the Program....")
            clientSocket.close()
            break
        
clientMain()

