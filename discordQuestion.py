
class MyGrid(GridLayout): 
    allButtons = []

    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 3
        self.rows = 3

    def function1(self, i):

    def function2():

class MyApp(App):
    def build(self):
        self.title = 'Server'
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()