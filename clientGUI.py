from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from mttkinter import mtTkinter
from PIL import Image, ImageTk
from client import client, connect

class ClientGUI(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)

        self.master = master
        self.master.title("Chatahuete")
        self.master.geometry("{}x{}".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
        self.user = connect("localhost")


        self.canvas = None
        self.username = ""
        self.current_room = None
        

        # Callbacks
        self.user.set_nick_changed_callback(self._change_nick) # Work
        self.user.set_rooms_changed_callback(self._rooms_changed) # Work
        self.user.set_user_nick_changed_callback(self._user_nick_changed) # Work
        self.user.set_deleted_room_callback(self._deleted_room) # Test
        self.user.set_new_message_callback(self._new_message) # Test
        self.init_window()
        self.set_username()
        print("Username {}".format(self.username))
       
        
    def init_window(self):

        # Create rooms view
        self.rooms_frame = Frame(self, bg="light pink", relief=SUNKEN, width=self.master.winfo_screenwidth() * 0.1)
        self.rooms_list = {}
        
        self.user.request_rooms()
        # Create entry text widget
        self.chat_entry = Entry(self)

        # Create canvas
        self.canvas = Canvas(self, bg="#2b5279")

        # Create scrollbar for the canvas
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview, bg="light blue")

        # Create frame inside the canvas
        self.frames = []


        # Create menu
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        file = Menu(self.master)
        file.add_command(label="Change username", command=self.set_username)
        file.add_command(label="Exit", command=self.close)
        self.menu.add_cascade(label="User", menu=file)


        # Pack all the widgets
        self.pack(fill="both", expand=1)
        self.rooms_frame.pack(side="left", fill=Y)
        self.rooms_frame.pack_propagate(0)
        self.chat_entry.pack(side="bottom", fill=X)
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
        self.master.bind("<Control-q>", self.close)
        self.master.bind("<Return>", self._get_text)
        self.canvas.bind("<Configure>", self._frame_width)
        

    def add_room(self, room_name):
        
        new_frame = Frame(self.canvas, bg="#2b5279")
        new_canvas_frame = self.canvas.create_window(0, 0, window=new_frame, anchor=NW)
        self.canvas.itemconfigure(new_canvas_frame, state='hidden')
        
        new_room = Label(self.rooms_frame, text=room_name, font="Manjari 12", bg="#2b5279", fg="white", anchor=NW, relief=GROOVE)
        new_room.pack(fill='x')
        new_room.bind("<Button-1>", lambda event: (self.select_room(room_name, new_canvas_frame)))
        new_frame.bind("<Configure>", self._scroll_chat)
        self.rooms_list[room_name] = [new_room, new_canvas_frame, new_frame]

    def select_room(self, room_name, room_canvas):
        self.set_current_room(room_name)
        for room in self.rooms_list.values():
            self.canvas.itemconfigure(room[1], state="hidden")
        self.canvas.itemconfigure(room_canvas, state="normal")


    def delete_room(self, room_name):
        
        self.current_room = None

    def set_current_room(self, room_name):
        
        self.current_room = room_name
        print(self.current_room)
        self.user.connect_to_room(self.current_room)

    def _deleted_room(self):
        print("The room has been deleted.")
        self.current_room = None
        

    def _user_nick_changed(self, room_name, old_nick, new_nick):
        
        print("The user " + old_nick + " connected to the room " + room_name + " has changed his nick to " + new_nick + ".") 
        
    def _rooms_changed(self, rooms):

        
        for room in rooms:
            if room not in self.rooms_list.keys():
                self.add_room(room)
                
        r = dict(self.rooms_list)
        for room_name, room_widget in self.rooms_list.items():
            if room_name not in rooms:
                del r[room_name]
                room_widget[0].destroy()
                self.canvas.delete(room_widget[1])
                room_widget[2].destroy()
        self.rooms_list = r


        
                
    def _new_message(self, user, room, msg):


        if (room == self.current_room):
            l = Label(self.rooms_list[room][2], text=user + ": " + msg[0], bg="#2b5279", fg="white", font="Manjari 12")
            l.pack(anchor=NW)

        
    
        
    def _frame_width(self, event):
        
        """Resize frame inside canvas"""
        
        canvas_width = event.width
        canvas_height = event.height
        for room in self.rooms_list.values():
            self.canvas.itemconfig(room[1], width = canvas_width)
        
    def _scroll_chat(self, event):

        """Scroll canvas to the end"""
        
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview(MOVETO, 1.0)
        
        
    def set_username(self):

        """Create a new window asking for the username"""
        
        username_window = Tk()
        username_window.title("Username")
        username_window.attributes("-topmost", True)
        
        func = lambda event: (self._change_username(username_entry.get()), username_window.destroy())
        
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

    def _change_username(self, username):

        self.username = username
        self.user.try_change_nick(username)        

    def _change_nick(self, changed, nick):

        if not changed:
            messagebox.showerror("Error", "The nick " + nick + " is not available.")

            if nick == None:
                self.set_username()
        else:
            self.username = nick
            messagebox.showinfo("Information", "Your username has been successfully changed!")

        
    def _get_text(self, event):

        """Get text from the Entry widget and create a new Label with this text."""
        
        if self.current_room != None:
            s = self.chat_entry.get()

            self.chat_entry.delete(0, END)
            if s != "":
                l = Label(self.rooms_list[self.current_room][2], text=self.username + ": " + s, bg="#2b5279", fg="white", font="Manjari 12")
                
                self.user.send_message(s)
                l.pack(anchor=NW)

    def close(self, event):
        self.master.destroy()
        self.user.close()

        
            

master = Tk()


cliente = ClientGUI(master)
cliente.user.request_rooms()
master.mainloop()
