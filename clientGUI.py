from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class ClientGUI(Frame):

    def __init__(self, master):

        Frame.__init__(self, master, bg="light pink")
        self.master = master
        self.init_window()

    def init_window(self):
        h = self.master.winfo_screenheight()
        w = self.master.winfo_screenwidth()

        self.frame = Frame(self.master, bg="#0e1621")


        self.master.title("Chatahuete")
        self.master.attributes("-zoomed", True)
        self.pack(fill=BOTH, side=LEFT, ipadx=0.01*w, ipady=h)

        self.rooms = ttk.Treeview(self)
        self.rooms.heading('#0', text="Rooms")
        self.rooms.pack(fill=BOTH, expand=True, side=LEFT)
        self.frame.pack(fill=Y, expand=0, ipadx=0.99*w, ipady=h, side=LEFT)
        self.labels = []
        self.label = Label(self.frame, text="Usuario 1: hola", bg="#2b5279", fg="white", font="Manjaro 12")
        self.label.place(x=20, y=20, anchor=NW)
        
        self.chat_entry = Entry(self.frame)
        self.chat_entry.icursor(0)
        self.chat_entry.pack(side=BOTTOM, fill=X, expand=0)
        
        self.master.bind("<Return>", self.get_text)
        self.username=""
        self.set_username()
        print("Username: ", self.username)

    def set_username(self):
        
        username_window = Tk()
        username_window.title("Username")
        username_window.attributes("-topmost", True)
        w=200
        h=100
        y = username_window.winfo_screenheight() / 2 - h / 2
        x = username_window.winfo_screenwidth() / 2  - w / 2
        
        s = str(w) + "x" + str(h) + "+" + str(int(x)) + "+" + str(int(y))
        username_window.geometry(s)
        l = Label(username_window, text="Welcome to Chatahete!\nIntroduce your username.")
        l.pack()
        e = Entry(username_window)
        e.pack()

        b = Button(username_window, text="Done!", command=lambda: (strcpy(self.username, e.get())))
        b.pack()
        username_window.mainloop()
        
        
    def get_text(self, event):
        s = self.chat_entry.get()
        self.chat_entry.delete(0, END)
        l = Label(self.frame, text=s, bg="#2b5279", fg="white", font="Manjaro 12")
        l.pack()


master = Tk()


cliente = ClientGUI(master)

master.mainloop()
