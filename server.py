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
    
    
    def signal_close(self):
        
        if self.run:
            self.run = False
            self.listener.close()
    
    
    def close(self):
        
        self.run = False
        for connection in self.clients:
            connection.close()
        for t in self.threads:
            t.join()
    
    
    def listen(self):
        
        while self.run:
            try:
                connection, ip = self.listener.accept()
                if len(self.clients) < self.max_listen:
                    print("INFO: New connection: ", ip)
                    self.new_client(connection)
                else:
                    print("WARNING: New client could not connect (not enought max_listen)")
                    self.send_full(connection)
                    connection.close()
                    time.sleep(1.0)
            except Exception as e:
                print(e)
                self.signal_close()
        
        self.close()
    
    
    def new_client(self, connection):
        user = client(connection)
        self.clients.append(user)
        self.send_ok(connection)
        t = Thread(target=self.client_thread, args=[user])
        self.threads.append(t)
        t.start()
    
    
    def client_thread(self, user):
        
        should_continue = True
        print("Listening", user.connection.getpeername())
        while should_continue:
            try:
                code, msg = read_message(user.connection)
                if code == CODE_CLIENT__EXIT or code == CODE_COMMON__ERROR:
                    should_continue = False
                elif code == CODE_CLIENT__IDLE:
                    print(user.connection.getpeername(), "   -", str_code(code), "-", msg)
                else:
                    self.send_error(user.connection)
                    should_continue = False
            except Exception as e:
                print(e)
                should_continue = False
        print("Stop listening", user.connection.getpeername())
        user.connection.close()
        self.clients.remove(user)
    
    
    def send_error(self, connection):
        
        error_str = "Bad request"
        msg = header(len(error_str), CODE_COMMON__ERROR) + error_str
        connection.send(msg.encode())
    
    
    def send_full(self, connection):
        
        msg = header(0, CODE_SERVER__FULL)
        connection.send(msg.encode())
    
    
    def send_ok(self, connection):
        
        msg = header(0, CODE_SERVER__OK)
        connection.send(msg.encode())




if __name__ == "__main__":
    serv = server(3856, 1)
    serv.listen()
