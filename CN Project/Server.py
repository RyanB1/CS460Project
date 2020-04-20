def serverMain():
    serverPort = 13009
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(("",serverPort))
    serverSocket.listen(10)
    print ("The server is ready to receive")
         
serverMain()
