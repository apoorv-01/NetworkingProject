import socket
import subprocess
import pickle # changing python objects to byte streams to send over tcp connections.
import boardClient
from kivy.app import App
import time
import threading
from kivy.core.window import Window
def clientConnectToServer():

    port = 9999 # Server's port where you want to connect
    host = '127.0.0.1' # Host's address where you want to connect
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((host, port)) # only will move down after connecting
    return clientSocket

def sendFromClient(clientSocket, msg):
    msgFromClient = str(msg)
    clientSocket.sendall(msgFromClient.encode('utf-8'))

class receiveInBackground(object):
    clientSocket = socket.socket()
    msgFromServer = ''
    flag = 0
    interval = 0

    def __init__(self, s, interval = 0.5):
        self.interval = interval
        self.clientSocket = s
        thread = threading.Thread(target = self.receiveFromServer, args = ())
        thread.daemon = True
        thread.start()

    """Method That runs Once In Background when this class is invoked But the while loops help to simulate forevernes all in a different thread"""
    def receiveFromServer(self):
        while True:
            while True:
                app = App.get_running_app()
                # print('Client is Waiting for move from Server')
                self.msgFromServer = (self.clientSocket.recv(1024)).decode('utf-8') # Will not move down until something is received
                if self.msgFromServer == 'lost':
                    print('MEOW')
                    app.stop()
                    Window.close()
                    self.flag = 1
                    break
                if self.msgFromServer != '':
                    break
                # time.sleep(self.interval)
            if self.flag == 1:
                self.clientSocket.shutdown()
                self.clientSocket.close()
                break
            time.sleep(self.interval)
            app.root.updateMoveFromServer(self.msgFromServer)