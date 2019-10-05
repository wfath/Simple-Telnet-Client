import socket
import select
global userInfo


#this prints all of the socket information
#print(socket.getaddrinfo("www.goatgoose.com", 12000))

#takes in the socket the host and the port
#tries connecting and then returns true or false respectively
def connectServer(sock, url, port):
    try:
        sock.connect((url, port))
        print("Connection Established")
        return True
    except:
        print("Connection Unable to be established")
        return False

#just cleaning up the inputs
def getServerInfo():
    hostname = input("Please enter the server hostname: ")
    portNum = int(input("Please enter the server port number: "))


    return hostname, portNum

#see above
def getUserInfo():
    username = input("Please enter a username: ")
    password = input("Please enter a password: ")

    return username, password

#the main function that handles all of the options and incoming messages
def pickOption(sock):
    #this is a poll with the select library
    poll = select.poll()
    #this register reacts to incoming messages
    poll.register(sock, select.POLLIN)
    #this register reacts to user input
    poll.register(1, select.POLLIN)

    print("Choose an option:")
    print("1. List online users")
    print("2. Send someone a message")
    # print("3. Receive all messages sent to you")
    print("3. Sign Off")
        #poll() also returns an event, but i dont think we really need it
    for inp, event in poll.poll():
        if(inp == 1):
            sel = input()
            try:
                sel = int(sel)
            except:
                sel = 99
           # try:
            if sel == 1:
                # list online users
                listUsers(sock)

            elif sel == 2:
                #send messag
                sendMessage(sock)

            elif sel == 3:
                #receive the whole buffer
                print("Closing Connection. Goodbye.")
                sayGoodbye(sock)
                exit()

            else:
                print("Please enter a valid number")
        #this is what handles any input comin in from the socket
        else:
            msg = sock.recv(1000)
            msg = msg.decode("ASCII")
            print(msg)



def sayHello(sock):
    sock.send(b"HELLO\n")

def sayGoodbye(sock):
    sock.send(b"BYE\n")

#i dont use this function anymore
#but i left the one million buffer in memory of all the good times we had on this assignment
def recvAllMsg(s):
    try:
        msg = s.recv(1000000)
        msg = msg.decode("ASCII")
        print(msg)
    except(socket.timeout):
        print("No Messages currently")

    except:
        print("No Messages")

#this function still gets a buffer of 32000 though
def recvMsg(s):
    msg = s.recv(32000)
    msg = msg.decode("ASCII")
    return msg

#this function gets the username and password and tries it, returning true or false likewise
def authenticate(sock, u, p):
    string = "AUTH:" + u + ":" + p + "\n"
    #print(string.encode('ASCII'))
    sock.send(string.encode('ASCII'))
    m = recvMsg(sock)
    # print(m)
    if m == 'AUTHYES\n':
        print("Authenticated")
        print(recvMsg(sock))
        return True
    else:
        print("Not Authenticated")
        return False

#sends the message to list the users
def listUsers(sock):
    sock.send(b"LIST\n")
    m = recvMsg(sock)
    #it didnt like the single print statement so i split it up and it works
    print("Online Users: ", end="")
    print(m)

#handles everything needed to send a message
def sendMessage(sock):
    recvr = input("Who would you like to send the message to? ")
    userM = input("What is the message you would like to send? ")
    string = "To:" + recvr + ":" + userM + "\n"
    try:
        sock.send(string.encode('ASCII'))
        print("Message sent!")
    except:
        print("Message Unable to be sent")

def main():

    s = socket.socket()
    s.settimeout(5)

    host, port = getServerInfo()

    #host = "www.goatgoose.com"

    connect = connectServer(s, host, port)
    while(connect == False):
        print("please enter valid hostname and port number")
        host, port = getServerInfo()
        connect = connectServer(s, host, port)
    # connectServer(s, host, port)
    sayHello(s)
    message = recvMsg(s)

    uname, passw = getUserInfo()
    while(authenticate(s, uname, passw) == False):
        print("Please enter a valid user")
        uname, passw = getUserInfo()

    while(True):
        pickOption(s)

    #pass in input and socket to select function

main()







