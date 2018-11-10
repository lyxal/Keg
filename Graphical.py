import Keg, tkinter

class Textbox():
    def __init__(self, root, width, height, args):
        self.frame = tkinter.Frame(root, width=width, height=height)
        self.width, self.height = width, height

        self.widget = tkinter.Text(self.frame, args)
        self.widget.pack(expand=tkinter.YES, fill=tkinter.BOTH)

    def place(self, *args, **kwargs):
        self.frame.place(*args, **kwargs)
        self.frame.place_configure(width=self.width, height=self.height)
        self.frame.config(bd=1, relief="solid", highlightbackground="#ffffff")

def grun():
    Keg.stack = []
    Keg.register = None
    Keg.comment = False
    Keg.escape = False
    Keg.printed = False
    Keg.grun(codebox.widget.get("1.0", tkinter.END), prepop.get())
    
root = tkinter.Tk()
root.geometry('800x600')

codebox = Textbox(root, 800, 300, {'height': '300', 'width': '800'})
codebox.place(x=0, y=0)

submit = tkinter.Button(root, text="Run Program", command=grun)
submit.place(x=0, y=301)

tkinter.Label(root, text="Values to prepopulate stack").place(x=0, y=330)
prepop = tkinter.Entry(root, width=50)
prepop.place(x=0, y=350)
