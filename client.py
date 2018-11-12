from tkinter import simpledialog
from tkinter import messagebox
from tkinter import Tk
from threading import Thread
import socket
import time

from common import *


class client:
    
    def __init__(self, connection):
        
        self.connection = connection
        self.should_continue = False
        self.thread = None
    
    
    def connect(self, ip, port=3856):
        
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((ip, port))
            code, _ = read_message(self.connection)
            if code == CODE_SERVER__OK:
                self.thread = Thread(target=self.server_thread)
                self.thread.start()
                return code
            else:
                self.connection.close()
                return code
        except Exception as e:
            print(e)
            return None
    
    
    def server_thread(self):
        
        self.should_continue = True
        while self.should_continue:
            try:
                code, msg = read_message(self.connection)
                if code == CODE_COMMON__ERROR:
                    self.should_continue = False
                else:
                    print(str_code(code), msg)
            except:
                self.should_continue = False
    
    
    def close(self):
        
        self.should_continue = True
        if self.connection != None:
            self.connection.close()
        if self.thread != None:
            self.thread.join()



















def connect(ip):
    
    root = Tk()
    root.withdraw()
    
    user = client(None)
    while user.connection == None:
        if ip == None:
            ip = simpledialog.askstring("IP", "Enter server IP: ")
            if ip == None:
                exit()
        res = user.connect(ip)
        if res != CODE_SERVER__OK:
            if res == None:
                msg = "Connection refused"
            else:
                msg = "Error thrown by server: "+str_code(res)
            messagebox.showerror("Error", msg)
            user.connection = None
            ip = None
    
    root.destroy()
    return user




















if __name__ == "__main__":
    user = connect(None)
    
    # TO-DO
    while True:
        send_message(user.connection, CODE_CLIENT__IDLE, "Hola")
        time.sleep(1)
    
    connection.close()
