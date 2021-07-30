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
        self.cols = 2
        self.rows = 1

        allButtons = []

        for i in range(2):
            x = input()
            allButtons.append(Button(
                text = x
            ))
            allButtons[i].bind(
                on_press = partial(self.pressed, allButtons, i)
            )
            self.add_widget(allButtons[i])
    
    def pressed(self, *args):
        allButtons = args[0]
        i = args[1]
        allButtons[i].text = 'Kill'
        allButtons[i].disabled = True



class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()