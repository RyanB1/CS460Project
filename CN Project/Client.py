from socket import * 

def playGame(clientSocket,username):
    points = 0
    numOfQuestions = 0
    correctAnswers = []
    while numOfQuestions != 5:
        wrong = 3
        serverMsg = "playGame\t"
        clientSocket.send(serverMsg.encode())
        question = clientSocket.recv(1024).decode("ascii")
        
        if question.split("\t")[0].strip() != "playGame":
            print("Error receiving question.")
            return
        
        print(question.split("\t")[1].strip()+"\n")
        
        i = 2
        while i < len(question.split("\t")):
            if question.split("\t")[i].strip() == "":
                break
            correctAnswers.append(question.split("\t")[i].strip().lower())
            i+=2
        numOfAnswers = len(correctAnswers)

        while True:
            answer = input("Enter an Answer: ")
            answer = answer.lower()
            clientSocket.send(answer.encode())
            response = clientSocket.recv(1024).decode("ascii")
            
            for i in range(0, len(correctAnswers)):
                if correctAnswers[i] == answer:
                   print("You got an answer correct. You Earned",response.split("\t")[0].strip(),"points.")
                   points += int(response.split("\t")[0].strip())
                   numOfAnswers-=1
                   correctAnswers.remove(answer)
                   print(numOfAnswers,"answers left to guess.\n") 
                   break
               
            if numOfAnswers == 0:
                print("You got all answers correct for this question.")
                print("Point Total:",points)
                numOfQuestions+=1
                if numOfQuestions == 5:
                    print("Game over! You have earned a total of",points,"points.")
                    break

                print("New Question is loading...\n\n")
                clientSocket.send("NextQuestion".encode())
                correctAnswers = []
                break
                
            if response.split("\t")[0].strip() == "Incorrect":
               wrong-=1
               if(wrong == 0):
                   numOfQuestions+=1
                   print("You have run out of chances.")
                   print("Point Total:",points)
                   print("The Remaining Correct Answers were:",end=" ")
                   for i in correctAnswers:
                       print(i,end=", ")
                       
                   if numOfQuestions == 5:
                       print("\nGame over! You have earned a total of",points,"points.")
                       break
                
                   print("\nNew question loading...\n\n")
                   clientSocket.send("NextQuestion".encode())
                   correctAnswers = []
                   break
               
               print("You answered incorrectly. You have",wrong,"chance(s) left\n")
                
    serverMsg = "Gameover\t" + username + "\t" + str(points)
    clientSocket.send(serverMsg.encode())
       
def login(clientSocket):
    logged = False
    while not(logged):
        username = input("Input your username: ")
        password = input("Input your password: ")
        serverMsg = "login\t" + username + "\t" + password
        #print(serverMsg)
        clientSocket.send(serverMsg.encode())
        returnedMsg = clientSocket.recv(1024).decode("ascii")
        #print(returnedMsg)
        if returnedMsg == "loggedIn":
            print("Successfully Logged in")
            logged = True
        else:
            print("Incorrect login information")
            username = ""
            password = ""
            #clientSocket.recv(1024).decode("ascii")
    return username
    
def register(clientSocket):
    registered = False
    while not(registered):
        newUsername = input("Input an username: ")
        newPass = input("Input a password: ")
        serverMsg = "register\t" + newUsername + "\t" + newPass
        clientSocket.send(serverMsg.encode())
        if clientSocket.recv(1024).decode("ascii") == "alreadyRegistered":
            print("The username you chose was already registered, try again")
            newUsername = ""
            newPass = ""
        else:
            registered = True
            print("Your account was successfully registered")
    return newUsername
       
def personalBest(clientSocket):
    serverMsg = "CheckIndBestRecord\t"
    clientSocket.send(serverMsg.encode())
    response = clientSocket.recv(1024).decode("ascii")

    if response.split("\t")[0].strip() != "CheckIndBestRecord":
        print("Error getting record.\n")
        return
    
    print("Your personal best is:",response.split("\t")[1].strip(),"points\n")
    
def bestOverall(clientSocket):
    serverMsg = "CheckBestRecord\t"
    clientSocket.send(serverMsg.encode())
    response = clientSocket.recv(1024).decode("ascii")

    if response.split("\t")[0].strip() != "CheckBestRecord":
        print("Error getting record.\n")
        return

    print("The best overall score is:",response.split("\t")[1].strip(),"points\n")
    

def clientMain():
    serverName = "localhost"
    serverPort = 13009
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    #Login
    playerStatus = int(input("Welcome to Family Feud! Choose one of the following:\n 1. Login\n 2. Register\nEnter your choice: "))
    if playerStatus == 1:
        username = login(clientSocket)
    else:
        username = register(clientSocket)

    #Choosing what player wants to do
    while True:
        print("""
        1.Play Game
        2.Check Your Best Score 
        3.Check Best Overall Score
        4.Quit
        """)
        choice = int(input("Enter your choice: "))
                     
        if choice == 1:
            playGame(clientSocket,username)
        elif choice == 2:
            personalBest(clientSocket)
        elif choice == 3:
            bestOverall(clientSocket)
        else:
            print("Exiting the Program....")
            clientSocket.close()
            break
        
clientMain()

