def clientMain():
    serverName = "localhost"
    serverPort = 13009
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

clientMain()
#test
