__author__ = 'mrittha'


from Tkinter import *

from Tkinter import *

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.text=Text(frame)
        self.question=Text(frame)

        self.text.pack(side=TOP)
        self.question.pack(side=TOP)

        self.button = Button(
            frame, text="QUIT", fg="red", command=frame.quit
            )
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print self.set_text("Study text")

    def set_text(self,text):
        self.text.insert(INSERT,text)

    def set_question(self,text):
        self.question.insert(INSERT,text)


root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see descript

