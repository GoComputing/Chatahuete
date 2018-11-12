import socket
import netifaces
from threading import Thread
import time

from common import *
from client import client



def get_ip_from_interface(interface_name):
    
    if netifaces.AF_INET in netifaces.ifaddresses(interface_name):
        return netifaces.ifaddresses(interface_name)[netifaces.AF_INET][0]['addr']
    else:
        return None



def get_ip():
    
    ip = None
    interface_name = ''
    for interface_name in netifaces.interfaces():
        try:
            ip = get_ip_from_interface(interface_name)
            if ip != None and not ip.startswith("127."):
                break
        except IOError:
            pass
    return ip, interface_name








class server:
    
    def __init__(self, port, max_listen):
        
        # Initialize
        self.max_listen = max_listen
        self.clients = []
        self.threads = []
        self.rooms = []
        self.run = True
        
        # We get a local IP which will be used to connect to internet
        ip, interface = get_ip()
        if ip == None:
            print("ERROR: Not valid interface found")
            exit()
            print("Using interface: ", interface)
        
        # Create the listener
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((ip, port))
        self.listener.listen(self.max_listen)
    
    
    def add_room_name(self, room_name):
        
        self.rooms.append(room_name)
        self._notify_rooms_changed()
        
        
    def del_room_name(self, room_name):
        
        if room_name in self.rooms:
            for u in self.clients:
                if u.current_room_name == room_name:
                    u.current_room_name = None
            self.rooms.remove(room_name)
            self._notify_rooms_changed()
    
    
    def signal_close(self):
        
        if self.run:
            self.run = False
            self.listener.close()
    
    
    def listen(self):
        
        while self.run:
            try:
                connection, ip = self.listener.accept()
                if len(self.clients) < self.max_listen:
                    print("INFO: New connection: ", ip)
                    self._new_client(connection)
                else:
                    print("WARNING: New client could not connect (not enought max_listen)")
                    self._send_full(connection)
                    connection.close()
                    time.sleep(1.0)
            except Exception as e:
                print(e)
                self.signal_close()
        
        self._close()
    
    
    def _notify_rooms_changed(self):
        
        msg = ''
        for i,r in enumerate(self.rooms):
            if i != 0:
                msg = msg+"\n"
            msg = msg + r
        for u in self.clients:
            send_message(u.connection, CODE_SERVER__ROOMS_MODIFIED, msg)
    
    
    def _new_client(self, connection):
        user = client(connection)
        self.clients.append(user)
        self._send_ok(connection)
        t = Thread(target=self._client_thread, args=[user])
        self.threads.append(t)
        t.start()
    
    
    def _client_thread(self, user):
        
        should_continue = True
        print("Listening", user.connection.getpeername())
        i = 0
        while should_continue:
            try:
                code, msg = read_message(user.connection)
                if code == CODE_CLIENT__EXIT or code == CODE_COMMON__ERROR:
                    should_continue = False
                elif code == CODE_CLIENT__IDLE:
                    print(user.connection.getpeername(), "   -", str_code(code), "-", msg)
                elif code == CODE_CLIENT__TRY_NICK:
                    self._try_change_nick(user, msg)
                elif code == CODE_CLIENT__CONNECT_ROOM:
                    self._connect_user_to_room(user, msg)
                elif code == CODE_CLIENT__REQUEST_ROOMS:
                    self._notify_rooms_changed()
                elif code == CODE_CLIENT__NEW_MESSAGE:
                    if user.current_room_name != None:
                        print("New message: ", user.nick, ", ", user.current_room_name, ", ", msg, sep='')
                        send_message(user.connection, CODE_SERVER__MESSAGE_OK, '')
                        self._notify_new_message(user, msg)
                    else:
                        send_message(user.connection, CODE_SERVER__BAD_LAST_MESSAGE, '')
                else:
                    self._send_error(user.connection)
                    should_continue = False
            except Exception as e:
                print(e)
                should_continue = False
        print("Stop listening", user.connection.getpeername())
        user.connection.close()
        self.clients.remove(user)
    
    
    def _notify_new_message(self, user, msg):
        
        for u in self.clients:
            if user != u:
                send_message(user.connection, CODE_SERVER__NEW_MESSAGE, user.nick+user.current_room_name+msg)
    
    
    def _try_change_nick(self, user, new_nick):
        
        found = False
        for u in self.clients:
            if u.nick == new_nick:
                found = True
        if found:
            send_message(user.connection, CODE_SERVER__NICK_DENY, '')
        else:
            user.nick = new_nick
            send_message(user.connection, CODE_SERVER__NICK_OK, '')
    
    
    def _connect_user_to_room(self, user, room_name):
        
        if user.nick != None  and room_name in self.rooms:
            user.current_room_name = room_name
            send_message(user.connection, CODE_SERVER__ROOM_CONNECTED, '')
            msg = user.nick
            for u in self.clients:
                if u.current_room_name == room_name and u.nick != user.nick:
                    msg = msg + "\n" + u.nick
            for u in self.clients:
                send_message(u.connection, CODE_SERVER__USERS_ROOM_CHANGED, msg)
        else:
            send_message(user.connection, CODE_SERVER__ROOM_DENY, '')
            
    
    
    def _send_error(self, connection):
        
        error_str = "Bad request"
        msg = header(len(error_str), CODE_COMMON__ERROR) + error_str
        connection.send(msg.encode())
    
    
    def _send_full(self, connection):
        
        msg = header(0, CODE_SERVER__FULL)
        connection.send(msg.encode())
    
    
    def _send_ok(self, connection):
        
        msg = header(0, CODE_SERVER__OK)
        connection.send(msg.encode())
    
    
    def _close(self):
        
        self.run = False
        for connection in self.clients:
            connection.close()
        for t in self.threads:
            t.join()







if __name__ == "__main__":
    serv = server(3856, 1)
    serv.add_room_name("room-prueba")
    serv.add_room_name("computer-craft")
    serv.listen()
