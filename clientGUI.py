from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class ClientGUI(Frame):

    def __init__(self, master):

        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):

        self.master.title("Chatahuete")
        self.master.attributes("-zoomed", True)
        self.pack(fill=BOTH, side=LEFT)

        self.rooms = ttk.Treeview(self)
        self.rooms.heading('#0', text="Rooms")
        self.rooms.pack(fill=BOTH, expand=True, side=LEFT)
        
        self.frame = Frame(self.master, width=700, height=500)
        self.frame.pack(side=LEFT, expand=True, fill=BOTH)

        self.label = Label(self.frame)
#        self.label.pack(side=TOP, fill=BOTH, expand=True, padx=1000, pady=490)
        self.chat_entry = Entry(self.frame)
        self.chat_entry.pack(side=BOTTOM, fill=X, expand=True)


    def get_text(self, event):
        pass


master = Tk()


cliente = ClientGUI(master)

master.mainloop()
