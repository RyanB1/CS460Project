from socket import * 

#def playGame(clientSocket):
    
#def personalBest(clientSocket):

#def allScores(clientSocket):

#def bestOverall(clientSocket):

#def specificPlayer(clientSocket):


def clientMain():
    serverName = "localhost"
    serverPort = 13009
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    #Login

    #Choosing what player wants to do
    print("""
    1.Play Game
    2.Check Your Best Score 
    3.Check All Scores
    4.Check Best Overall Score
    5.Check Best Specific Player Score
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
        specificPlayer(clientSocket)
    else:
        print("Exiting the Program....")
        clientSocket.close()
        
clientMain()

