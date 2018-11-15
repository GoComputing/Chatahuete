from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

class ClientGUI(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)

        self.master = master
        self.master.title("Chatahuete")
        self.master.geometry("{}x{}".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        

        self.username = ""
        self.init_window()
        self.set_username()

    def init_window(self):

        # Create rooms view
        self.rooms = ttk.Treeview(self)
        self.rooms.heading("#0", text="Rooms")
        
        # Create entry text widget
        self.chat_entry = Entry(self)

        # Create canvas
        self.canvas = Canvas(self, bg="#2b5279")

        # Create scrollbar for the canvas
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview, bg="light blue")

        # Create frame inside the canvas
        self.frame = Frame(self.canvas, bg="#2b5279")
        self.canvas_frame = self.canvas.create_window(0, 0, window=self.frame, anchor=NW)

        # Create menu
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        file = Menu(self.master)
        file.add_command(label="Change username", command=self.set_username)
        self.menu.add_cascade(label="User", menu=file)



        # Pack all the widgets
        self.pack(fill="both", expand=1)
        self.rooms.pack(side=LEFT, fill=Y)
        self.chat_entry.pack(side="bottom", fill="x")
        self.chat_entry.focus()                
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="right", fill=BOTH, expand=1)
        
       

        
#        img = ImageTk.PhotoImage(Image.open("1.png"))
#        l = Label(self.frame, image=img)
#        l.image = img
#        l.pack()

        # Set scrollbar to canvas
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Bindings
        self.master.bind("<Return>", self._get_text)
        self.frame.bind("<Configure>", self._scroll_chat)
        self.canvas.bind("<Configure>", self._frame_width)


                
        
    def _frame_width(self, event):
        
        """Resize frame inside canvas"""
        
        canvas_width = event.width
        canvas_height = event.height
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)
        
    def _scroll_chat(self, event):

        """Scroll canvas to the end"""
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview(MOVETO, 1.0)
        
        
    def set_username(self):

        """Create a new window asking for the username"""
        
        username_window = Tk()
        username_window.title("Username")
        username_window.attributes("-topmost", True)
        
        func = lambda event: (self._change_username(username_entry.get(), username_window), username_window.destroy())
        
        w=200
        h=100
        y = username_window.winfo_screenheight() / 2 - h / 2
        x = username_window.winfo_screenwidth() / 2  - w / 2
        
        username_window.geometry("{}x{}+{}+{}".format(str(w), str(h), str(int(x)), str(int(y))))
        welcome_text = Label(username_window, text="Welcome to Chatahete!\nIntroduce your username.")
        username_entry = Entry(username_window)
        b = Button(username_window, text="Done!", command=func)
        
        welcome_text.pack()
        username_entry.pack()
        username_entry.focus()
        b.pack()

                
        username_window.bind("<Return>", func)
        username_window.mainloop()

    def _change_username(self, username, window):

        self.username = username
        messagebox.showinfo("Information", "Your username has been successfully changed!", parent=window)
        
    def _get_text(self, event):

        """Get text from the Entry widget and create a new Label with this text."""
        
        s = self.chat_entry.get()
        self.chat_entry.delete(0, END)
        if s != "":
            l = Label(self.frame, text=self.username + ": " + s, bg="#2b5279", fg="white", font="Manjaro 12")
            l.pack(anchor=NW)
    
        
            

master = Tk()


cliente = ClientGUI(master)

master.mainloop()
