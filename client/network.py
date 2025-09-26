import socket

class Network:
    
    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addressIp = "127.0.0.1"
        self.port = 7777
        self.id = self.connect()
        
    def connect(self):
        try:
            self.client.connect((self.addressIp, self.port))
        except ConnectionRefusedError:
            print("CONNEXION AU SERVEUR ECHOUEE")
            return -1
        else:
            print("CONNECTE AU SERVEUR")
            return self.client.recv(2048).decode("utf8")
    
    def send(self, data: str)->str:
        try:
            self.client.send(data.encode())
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)
