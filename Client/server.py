import socket
from _thread import *
import os
import keyboard

os.chdir("../")

tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = socket.gethostbyname(socket.gethostname())
port = 7777

try:
    tcpsocket.bind((server_ip, port))

except socket.error as e:
    print(e)
    
tcpsocket.listen(2)
print("Waiting for a connection")

currentId = "0"
pos = ["0:50,50", "1:100,100"]

def threadedClient(conn, addr):
    global currentId, pos
    conn.send(currentId.encode())
    currentId = "1"
    reply = ''
    
    while(True):
        
        try:
            data = conn.recv(2048)
            reply = data.decode()
            
                # Close connection
            if not data:
                conn.send("Goodbye".encode())
                break
            
                # Process the data
            else:
                print("Recieved: " + reply)
                arr = reply.split(":")
                id = int(arr[0])
                pos[id] = reply

                if id == 0: nid = 1
                if id == 1: nid = 0

                reply = pos[nid][:]
                print("Sending: " + reply)

                # Send the reply
            conn.sendall(str(reply).encode())
            
        except:
            break
        
    print("Connection Closed with: ", addr)
    conn.close()

while True:
    if keyboard.is_pressed('q'):
        print("ici")
    conn, addr = tcpsocket.accept()
    print("Connected to: ", addr)
    start_new_thread(threadedClient, (conn, addr))