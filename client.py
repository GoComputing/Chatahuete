from tkinter import simpledialog
from tkinter import messagebox
from tkinter import Tk
import socket

def connect(ip, port):
    
    root = Tk()
    root.withdraw()
    
    connection = None
    while connection == None:
        if ip == None:
            ip = simpledialog.askstring("IP", "Enter server IP: ")
            if ip == None:
                exit()
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect((ip, port))
        except:
            messagebox.showerror("Error", "Error connecting using this IP. Try again")
            connection.close()
            connection = None
            ip = None
    
    root.destroy()
    return connection





connection = connect(None, 3856)

# TO-DO

connection.close()
