from tkinter import simpledialog
from tkinter import messagebox
from tkinter import Tk
import socket
import time

from common import *



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
code, _ = read_message(connection)
print(str_code(code))
if code == CODE_SERVER__FULL:
    messagebox.showerror("Error", "Server full")
elif code == CODE_SERVER__OK:
    while True:
        send_message(connection, CODE_CLIENT__IDLE, "Hola")
        time.sleep(1)
else:
    messagebox.showerror("Error", "Unknown error")

connection.close()
