import socket
import netifaces
from threading import Thread

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
        self.listener.listen(max_listen)
    
    
    def listen(self):
        
        connection, ip = self.listener.accept()
        print("INFO: New connection: ", ip)
        connection.close()
    
    
    def clean(self):
        
        self.listener.close()




serv = server(3856, 1)
serv.listen()
serv.clean()
