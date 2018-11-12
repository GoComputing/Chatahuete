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
        self.nick = None
        self.new_nick = None
        self.nick_changed_callback = None
        self.rooms_changed_callback = None
        self.current_room_name = None
        self.deletec_room_callback = None
        self.new_room = None
        self.connected_to_room_callback = None
        self.users_room_changed_callback = None
        self.message_received_callback = None
        self.new_message_callback = None
    
    
    def connect(self, ip, port=3856):
        
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((ip, port))
            code, _ = read_message(self.connection)
            if code == CODE_SERVER__OK:
                self.thread = Thread(target=self._server_thread)
                self.thread.start()
                return code
            else:
                self.connection.close()
                return code
        except Exception as e:
            print(e)
            return None
    
    
    def _server_thread(self):
        
        self.should_continue = True
        while self.should_continue:
            try:
                code, msg = read_message(self.connection)
                if code == CODE_COMMON__ERROR:
                    self.should_continue = False
                elif code == CODE_SERVER__NICK_OK:
                    print("Changed nick to", self.new_nick)
                    self.nick = self.new_nick
                    if self.nick_changed_callback != None:
                        self.nick_changed_callback(self.nick)
                elif code == CODE_SERVER__NICK_DENY:
                    print("Could not change nick to", self.new_nick)
                elif code == CODE_SERVER__ROOMS_MODIFIED:
                    rooms = msg.splitlines()
                    if self.current_room_name not in rooms:
                        self.current_room_name = None
                        if self.deleted_room_callback != None:
                            self.deleted_room_callback()
                    if self.rooms_changed_callback != None:
                        self.rooms_changed_callback(rooms)
                elif code == CODE_SERVER__ROOM_CONNECTED:
                    print("Changed to room", self.new_room)
                    self.current_room_name = self.new_room
                    if self.connected_to_room_callback != None:
                        self.connected_to_room_callback(self.current_room_name)
                elif code == CODE_SERVER__ROOM_DENY:
                    print("Could not connect to room '", self.new_room, "'")
                elif code == CODE_SERVER__USERS_ROOM_CHANGED:
                    if self.users_room_changed_callback != None:
                        self.users_room_changed_callback(msg.splitlines())
                elif code == CODE_SERVER__BAD_LAST_MESSAGE:
                    print("Could not send last message")
                elif code == CODE_SERVER__MESSAGE_OK:
                    if self.message_received_callback != None:
                        self.message_received_callback()
                elif code == CODE_SERVER__NEW_MESSAGE:
                    if self.new_message_callback != None:
                        messages = msg.splitlines()
                        user = messages[0]
                        room = messages[1]
                        del messages[0]
                        del messages[1]
                        self.new_message_callback(user, room, messages)
                else:
                    print(str_code(code), msg)
            except:
                self.should_continue = False
    
    
    def try_change_nick(self, new_nick):
        
        print("Trying to change nick to", new_nick)
        send_message(self.connection, CODE_CLIENT__TRY_NICK, new_nick)
        self.new_nick = new_nick
    
    
    def set_nick_changed_callback(self, fnc):
        
        self.nick_changed_callback = fnc
    
    
    def set_rooms_changed_callback(self, fnc):
        
        self.rooms_changed_callback = fnc
    
    
    def set_deleted_room_callback(self, fnc):
        
        self.deleted_room_callback = fnc
    
    
    def connect_to_room(self, room_name):
        
        send_message(self.connection, CODE_CLIENT__CONNECT_ROOM, room_name)
        self.new_room = room_name
    
    
    def set_connected_to_room_callback(self, fnc):
        
        self.connected_to_room_callback = fnc
    
    
    def set_users_room_changed_callback(self, fnc):
        
        self.users_room_changed_callback = fnc
    
    
    def request_rooms(self):
        
        send_message(self.connection, CODE_CLIENT__REQUEST_ROOMS, '')
    
    
    def send_message(self, message):
        
        send_message(self.connection, CODE_CLIENT__NEW_MESSAGE, message)
    
    
    def set_message_received_callback(self, fnc):
        
        self.message_received_callback = fnc
    
    
    def set_new_message_callback(self, fnc):
        
        self.new_message_callback = fnc
    
    
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
    def rooms_changed_callback(rooms):
        
        print("Rooms changed/request:")
        for r in rooms:
            print("  ", r, sep='')
    
    def new_message_callback(user, room, msg):
        
        print(user, ": ", room, ". ", msg, sep='')
    
    def message_received_callback():
        
        print("Server received message")
    
    user = connect(None)
    user.set_rooms_changed_callback(rooms_changed_callback)
    user.set_new_message_callback(new_message_callback)
    user.set_message_received_callback(message_received_callback)
    user.try_change_nick("Carlos")
    user.connect_to_room("room-prueba")
    user.request_rooms()
    
    # TO-DO
    while True:
        send_message(user.connection, CODE_CLIENT__IDLE, "Hola")
        user.send_message("Hola")
        time.sleep(1)
    
    connection.close()
