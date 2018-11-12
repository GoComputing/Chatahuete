from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk




class ServerGUI(Frame):

    def __init__(self, master):

        Frame.__init__(self, master)

        self.master = master

        self.init_window()

    def init_window(self):

        self.master.title("Servidor")
        self.master.attributes("-zoomed", True)
        self.pack(fill=BOTH, expand=True)

        style = ttk.Style()
        style.configure("Treeview", background="pink", fieldbackground="pink")
        self.rooms = ttk.Treeview(self)
        self.rooms_dict = {}

        
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        self.label = Label(self.master)
        file.add_command(label="Exit", command=self.server_exit)

        menu.add_cascade(label="File", menu=file)

        edit = Menu(menu)
        self.label.pack(fill=BOTH)
        self.master.after(0, self.update, 0)

        edit.add_command(label="New room", command=self.insert_room)
        edit.add_command(label="Delete room", command=self.delete_room)

        menu.add_cascade(label="Edit", menu=edit)
        self.rooms.pack(fill=BOTH, expand=True)

        self.rooms.bind('<<TreeviewSelect>>', self.insert_user)

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
        e.grid(row=0, column=1)

        window.bind("<Return>", lambda event: (self.rooms_dict.update({e.get() : self.rooms.insert("", END, text=e.get())}), window.destroy()))
        window.mainloop()

    def insert_user(self, event):

        print(self.rooms.item(self.rooms.selection()[0])['text'])
        
    def delete_room(self):

        window = Tk()
        window.title("Delete Room")

        w = 200
        h = 30        
        y = window.winfo_screenheight() / 2 - h / 2
        x = window.winfo_screenwidth() / 2  - w / 2
        
        s = str(w) + "x" + str(h) + "+" + str(int(x)) + "+" + str(int(y))
        window.geometry(s)

        room_name = StringVar()
        label_name = Label(window, text="Name").grid(row=0)
        e = Entry(window)
        e.grid(row=0, column=1)
        window.bind("<Return>", lambda event: (self.rooms.delete(self.rooms_dict[e.get()]), window.destroy()))
        window.mainloop()
        
    def update(self, x):

        img = PhotoImage(file='rem.gif',format='gif -index ' + str(x))
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
#        img.place(x=0, y=0)


    def server_exit(self, event=None):
        self.master.destroy()
    
    

master = Tk()
master.geometry("400x300")

servidor = ServerGUI(master)
#servidor.insertar_sala("Sala 1")
#servidor.insertar_usuario("Sala 1", "Usuario 1")

#servidor.insertar_sala("Sala 2")
#servidor.insertar_usuario("Sala 2", "Usuario 2")

master.mainloop()


