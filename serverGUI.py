from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk




class ServerGUI(Frame):

    def __init__(self, master):

        Frame.__init__(self, master)

        self.master = master
        self.master.title("Servidor")
        self.master.geometry("{}x{}".format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))

        self.init_window()

    def init_window(self):

        

        style = ttk.Style()
        style.configure("Treeview", background="#2b5279", fieldbackground="#2b5279", foreground="white", font="Manjari 12")
        self.rooms = ttk.Treeview(self, show="tree")

        # Pack widgets
        self.pack(fill=BOTH, expand=True)
        self.rooms.pack(fill=BOTH, expand=True)

        # Menu
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)
        file.add_command(label="Exit", command=self.server_exit)
        edit = Menu(menu)
        menu.add_cascade(label="File", menu=file)
        menu.add_cascade(label="Edit", menu=edit)
        edit.add_command(label="New room", command=self.insert_room)
        edit.add_command(label="Delete room", command=self.delete_room)

        
        self.rooms.bind('<<TreeviewSelect>>', self.insert_user)
        
        self.master.after(0, self.update, 0)
        
    def insert_room(self):
        
        window = Tk()
        window.title("New Room")

        w = 200
        h = 30        
        y = window.winfo_screenheight() / 2 - h / 2
        x = window.winfo_screenwidth() / 2  - w / 2
        
        s = str(w) + "x" + str(h) + "+" + str(int(x)) + "+" + str(int(y))
        window.geometry(s)
        room_name = StringVar()
        label_name = Label(window, text="Name").grid(row=0)
        e = Entry(window)
        e.focus()
        e.grid(row=0, column=1)

        window.bind("<Return>", lambda event: (self.rooms.insert("", END, text=e.get()), messagebox.showinfo("Information", e.get() + " has been created!", parent=window), window.destroy()))
                    
        window.mainloop()

    def insert_user(self, event):

        print(self.rooms.item(self.rooms.selection()[0]))
        
    def delete_room(self):

        window = Tk()
        window.title("Delete Room")                
        
        contador = 0
        for room in self.rooms.get_children():
            room_label = Label(window, text=self.rooms.item(room)['text'], bg="#2b5279", relief=SUNKEN, fg="white", font="Manjaro 12", )
            room_label.pack(fill=X, anchor=NW)
            room_name = self.rooms.item(room)['text']
            room_label.bind("<Button-1>", lambda event: (self.rooms.delete(room), messagebox.showinfo("Information", room_name  + " has been deleted :(", parent=window), window.destroy()))
            contador += 1

        w = 300
        h = contador * room_label.winfo_reqheight()
        y = (window.winfo_screenheight() - h) / 2 
        x = (window.winfo_screenwidth() - w) / 2 
        s = str(w) + "x" + str(h) + "+" + str(int(x)) + "+" + str(int(y))
        window.geometry(s)
        

        window.mainloop()
        
    def update(self, x):

        img = PhotoImage(file='Images/rem.gif',format='gif -index ' + str(x))
        dimg = img.subsample(2, 2)

        x += 1
        if x > 9: x = 0
        self.master.tk.call('wm', 'iconphoto', self.master._w, dimg)

        self.master.after(100, self.update, x)

    def show_img(self):
        load = Image.open("1.png")
        render = ImageTk.PhotoImage(load)
        
        img = Label(self, image=render)
        img.image = render
        img.pack()

    def server_exit(self, event=None):
        self.master.destroy()
    
    

master = Tk()


servidor = ServerGUI(master)
#servidor.insertar_usuario("Sala 1", "Usuario 1")

#servidor.insertar_sala("Sala 2")
#servidor.insertar_usuario("Sala 2", "Usuario 2")

master.mainloop()


