import socket
import pickle # changing python objects to byte streams to send over tcp connections.
import boardServer
import threading
import time
from kivy.app import App
from kivy.core.window import Window


def socketDefineAndConnect():
    host = '127.0.0.1'
    port = 9999

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serverSocket.bind((host, port))


    print("Socket Binded To Host - {0} and Port - {1} and Listening".format(host, port))
    serverSocket.listen()

    
    clientSocket, addr = serverSocket.accept() # will only move down from here if a connection comes
    print('Got connection from', addr, clientSocket)
    return clientSocket

def sendFromServer(clientSocket, msg):
    msgFromServer = str(msg)
    clientSocket.sendall(msgFromServer.encode('utf-8'))
    #msgFromClient = clientSocket.recv(1024).decode('utf-8') # Will not move down ultil something is recieved.

class receiveInBackground(object):
    clientSocket = socket.socket()
    msgFromClient = ''
    flag = 0
    interval = 0
    
    def __init__(self, s, interval = 0.5):
        self.interval = interval
        self.clientSocket = s
        thread = threading.Thread(target = self.receiveFromClient, args = ())
        thread.daemon = True
        thread.start()

    """Method That runs Once In Background as another Thread But the while loops help to simulate forevernes"""
    def receiveFromClient(self):
        print('Here')
        app = App.get_running_app()
        while True:
            if  app.title == 'Server (Winner)':
                    break
            while True:
                print('Server is Waiting for move from Client')
                if  app.title == 'Server (Winner)':
                    break
                self.msgFromClient = (self.clientSocket.recv(1024)).decode('utf-8') # Will not move down ultil something is recieved.
                if self.msgFromClient == 'lost':
                    print('HERE')
                    app.stop()
                    Window.close()
                    
                    self.flag = 1
                    break
                if self.msgFromClient != '':
                    break
                # time.sleep(self.interval)
            if self.flag == 1:
                self.clientSocket.shutdown()
                self.clientSocket.close()
                break
            time.sleep(self.interval)
            app.root.updateMoveFromClient(self.msgFromClient)


# while True: # It will keep looking for connections until it accepts after that it goes to chat function
#     clientSocket, addr = serverSocket.accept()
#     print('Got connection from', addr)
#     chatx(clientSocket)



