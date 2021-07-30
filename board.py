import kivy
from kivy.app import App # this is a class named App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.togglebutton import Button
from functools import partial
import random

class MyGrid(GridLayout): # Everytime while creating the board we will have to consider the button pressed list.
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        symbol = 'X'
        self.cols = 3
        self.rows = 3
        allButtons = [] # list of button objects
        for i in range(9): # adding all the buttons to the list and to the grid.
            allButtons.append(ToggleButton())
            allButtons[i].bind(
                on_press = partial(self.pressed, i, allButtons)
                )
            self.add_widget(allButtons[i])
    def pressed(self, *args): # defining button press
        allButtons = args[1]
        i = args[0]
        allButtons[i].background_down = 'cross.jpg'
        allButtons[i].state = 'down'
        buttonPressed = str(i).encode('utf-8')

        print(self.checkWinner(allButtons))
    
    def checkWinner(self, allButtons):
        cnt = 0
        for i in range(9):
            if allButtons[i].background_down == 'cross.jpg':
                cnt += 1
        return cnt


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()