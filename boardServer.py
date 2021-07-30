import kivy
import random
from kivy.app import App # this is a class named App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.lang import Builder
from functools import partial
import serverx
import clientx
import socket
import threading
import time



class MyGrid(GridLayout): 
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    allButtons = [] # list of button objects
    # newMsg = None
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3
        for i in range(9): # adding all the buttons to the list and to the grid.
            self.allButtons.append(ToggleButton())
            self.allButtons[i].bind(
                on_press = partial(self.pressed, i)
                )
            self.add_widget(self.allButtons[i])
        
        self.clientSocket = serverx.socketDefineAndConnect()

        receiveObject = serverx.receiveInBackground(self.clientSocket) # Creating an new Thread
        self.newMsg = receiveObject.msgFromClient
        print('from Client', self.newMsg)
            

    def pressed(self, *args): # defining button press
        self.flag = 1
        buttonPressed = args[0]
        i = args[0]
        name = 'Server'
        self.allButtons[i].background_down = 'cross.png'
        self.allButtons[i].state = 'down'

        app = App.get_running_app()
        serverx.sendFromServer(self.clientSocket, buttonPressed)
        win = self.checkWinner()
        if win == True:
            name = 'Server (Winner)'
            app.title = name
            serverx.sendFromServer(self.clientSocket, 'lost')

        app.title = name
        #print(len(self.allButtons))

    def updateMoveFromClient(self, moveFromClient):
        i = int(moveFromClient)
        print('From Client:',i)
        self.allButtons[i].background_down = 'circle.png'
        self.allButtons[i].state = 'down'
        app = App.get_running_app()
        app.title = 'Server (YOUR TURN)'

    def checkWinner(self):
        cnt = 0
        # print('HERE')
        for i in range(3): # first row
            # print(i)
            if self.allButtons[i].background_down == 'cross.png':
                # print('YES')
                cnt += 1
        if cnt == 3:
            return True

        cnt = 0
        for i in range(6, 9): # last row
            if self.allButtons[i].background_down == 'cross.png':
                cnt += 1
        if cnt == 3:
            return True

        cnt = 0
        buttonToCheck = [0, 3, 6] # first column
        for i in buttonToCheck:
            if self.allButtons[i].background_down == 'cross.png':
                cnt += 1
        if cnt == 3:
            return True
        
        cnt = 0
        buttonToCheck = [2, 5, 8] # last column
        for i in buttonToCheck:
            if self.allButtons[i].background_down == 'cross.png':
                cnt += 1
        if cnt == 3:
            return True

        cnt = 0
        buttonToCheck = [0, 4, 8] # Diagonal
        for i in buttonToCheck:
            if self.allButtons[i].background_down == 'cross.png':
                cnt += 1
        if cnt == 3:
            return True

        cnt = 0
        buttonToCheck = [2, 3, 6] # opposite diagonal
        for i in buttonToCheck:
            if self.allButtons[i].background_down == 'cross.png':
                cnt += 1
        if cnt == 3:
            return True

        cnt = 0
        buttonToCheck = [3, 4, 5] # 2nd Row
        for i in buttonToCheck:
            if self.allButtons[i].background_down == 'cross.png':
                cnt += 1
        if cnt == 3:
            return True


        cnt = 0
        buttonToCheck = [1, 4, 7] # 2nd Column
        for i in buttonToCheck:
            if self.allButtons[i].background_down == 'cross.png':
                cnt += 1
        if cnt == 3:
            return True

        return False
class MyApp(App):
    def build(self):
        self.title = 'Server (YOUR TURN)'
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()