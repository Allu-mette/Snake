import socket
import sys
import threading
import configparser
import processData

tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = socket.gethostbyname(socket.gethostname())

server_ip = "127.0.0.1"
port = 7777

try:
    tcpsocket.bind((server_ip, port))

except socket.error as e:
    print(e)
    
tcpsocket.listen(5)
tcpsocket.settimeout(1.0)

currentId = 0
pos = ["0:50,50", "1:100,100"]
clientList = {}
lobbyList = {}


class clientThread(threading.Thread):
    
    global clientList
    global lobbyList
    
    def __init__(self, conn, addr: tuple, id: str):
        threading.Thread.__init__(self)
        self.name = f"Client {id} Thread"
        
        self.conn = conn
        self.addr = addr
        self.id = id
        self.clientName = ""
        self.reply = ''
        
        conn.send(id.encode())
        clientList[id] = {"addr":addr, "name":self.clientName, "statue":"LOGIN", "lobbyId":None, "dataGame":{}}
        
    def run(self):
        
        while(True):
            
            try:
                message = self.conn.recv(2048).decode()
                
                    # Close connection
                if not message:
                    
                    self.quitLobby()
                    print("CONNEXION LOST")
                    break
                
                    # Process the message
                else:
                    
                    print(f"Recieved from {self.addr}, {self.clientName}: {message}")
                    arr = message.split(":")
                    action = arr[0]
                    
                    if action == "CONNEXION":
                        self.clientName = arr[1]
                        clientList[self.id]["name"] = self.clientName
                        clientList[self.id]["status"] = "CONNECTED"
                        
                    elif action == "ACUTALIZE LOBBY":
                        pass
                    
                    elif action == "JOIN":
                        
                        lobbyId = arr[1]
                            #Check if Lobby is Open
                        if lobbyList[lobbyId]["status"] == "OPEN":
                                # Add self in the player List of the Lobby
                            lobbyList[lobbyId]["playerId"].append(self.id)
                            
                                #Check if the Lobby is Full
                            if lobbyList[lobbyId]["place"] == len(lobbyList[lobbyId]["playerId"]):
                                lobbyList[lobbyId]["status"] = "FULL"
                                
                                # Update ClientList
                            clientList[self.id]["status"] = "IN LOBBY"
                            clientList[self.id]["lobbyId"] = lobbyId
                    
                    elif action == "HOST":
                        
                            # Create Lobby in LobbyList
                        lobbyList[self.id] = {"name":arr[1], "place":int(arr[2]), "playerId":[self.id], "status":"OPEN"}
                            # Update ClientList
                        clientList[self.id]["status"] = "IN LOBBY"
                        clientList[self.id]["lobbyId"] = self.id
                        
                    elif action == "WAITING PLAYER":
                            
                        lobbyId = clientList[self.id]["lobbyId"]
                            #Check if Lobby exist
                        if lobbyId != None:
                                # Check if Lobby is In Game
                            if lobbyList[lobbyId]["status"] == "IN GAME":
                                clientList[self.id]["status"] == "IN GAME"
                    
                    elif action == "READY":
                        
                            # Set client List
                        clientList[self.id]["status"] = "READY"
                            #Check if the Lobby is ready
                        lobbyId = clientList[self.id]["lobbyId"]
                        place = lobbyList[lobbyId]["place"]
                        current = 0
                        for playerId in lobbyList[lobbyId]["playerId"]:
                            status = str(clientList[playerId]["status"])
                            if status == "READY":
                                current += 1
                            # Set the lobby Ready
                        if current == place:
                            lobbyList[lobbyId]["status"] = "IN GAME"      
                            
                    elif action == "GAME SETUP":
                        
                        # Update Data Game in Client list
                        gameId = arr[1]
                        snakeBody = arr[2]
                        bonusPos = arr[3]                    
                        dataGame = {"gameId": gameId,
                                    "snakeBody": snakeBody,
                                    "bonusPos": bonusPos}
                        
                        clientList[self.id]["dataGame"] = dataGame
                    
                    elif action == "GAME UPDATE":
                        
                        # Update Data Game in Client list
                            gameId = arr[1]
                            snakeBody = arr[2]
                            bonusPos = arr[3]                    
                            dataGame = {"gameId": gameId,
                                        "snakeBody": snakeBody,
                                        "bonusPos": bonusPos}
                            
                            clientList[self.id]["dataGame"] = dataGame
                    
                    elif action == "QUIT GAME":
                        self.quitGame()
                    
                    elif action == "QUIT LOBBY":
                        self.quitLobby()
                    
                    elif action == "QUIT":
                        self.quitLobby()
                        break
                    
                    reply = processData.getReply(action, self.id, clientList, lobbyList)
                    print(f"Reply to {self.addr}: {reply}")

                    # Send the reply
                self.conn.sendall(str(reply).encode())
                
            except Exception as e:
                print(f"{type(e).__name__}: {e}. Line: {sys.exc_info()[-1].tb_lineno}")
                break
            
        print("Connection Closed with: ", self.addr)
        self.conn.close()
        
    def quitLobby(self):
    
            # Check if Client exist
        if self.id in clientList:
            lobbyId = clientList[self.id]["lobbyId"]
            
                # Check if the Client is in a Lobby
            if lobbyId != None:
                
                    # Host
                if self.id == lobbyId:
                        # Update Client List
                    for playerId in lobbyList[lobbyId]["playerId"]:
                        clientList[playerId]["status"] = "CONNECTED"
                        clientList[playerId]["lobbyId"] = None
                        clientList[playerId]["dataGame"] = {}
                        # Delete the Lobby in the Lobby List
                    lobbyList.pop(lobbyId)
                    
                    # Join
                else:
                    
                        # Update self in the Client List
                    clientList[self.id]["status"] = "CONNECTED"
                    clientList[self.id]["lobbyId"] = None
                    clientList[self.id]["dataGame"] = {}
                        # Remove Self in the Player List of the Lobby
                    lobbyList[lobbyId]["playerId"].remove(self.id)
                    
                        # Check if Lobby was Full
                    if lobbyList[lobbyId]["status"] == "FULL":
                            # Update the Lobby status
                        lobbyList[lobbyId]["status"] = "OPEN"
                        
                        # Check if Lobby was In Game
                    elif lobbyList[lobbyId]["status"] == "IN GAME":
                            # Update the Lobby status
                        lobbyList[lobbyId]["status"] = "OPEN"
                        
                            # Update Client List
                        for playerId in lobbyList[lobbyId]["playerId"]:
                            clientList[playerId]["status"] = "IN LOBBY"
                            clientList[playerId]["dataGame"] = {}

        else:
            print(f"ERROR: this clientId: {self.id} doesn't exist")
            
    def quitGame(self):
        
            # Check if Client exist
        if self.id in clientList:
            lobbyId = clientList[self.id]["lobbyId"]
            
                # Check if the Client is in a Lobby
            if lobbyId != None:
                
                    # Check if the Lobby is In Game
                if lobbyList[lobbyId]["status"] == "IN GAME":
                         
                         #Check if Lobby is Full               
                    if lobbyList[lobbyId]["place"] == len(lobbyList[lobbyId]["playerId"]):
                        lobbyList[lobbyId]["status"] = "FULL"
                    else:
                        lobbyList[lobbyId]["status"] = "OPEN"
                    
                        # Update Client List
                    for playerId in lobbyList[lobbyId]["playerId"]:
                        clientList[playerId]["status"] = "IN LOBBY"
                        clientList[playerId]["dataGame"] = {}
                    
                
        else:
            print(f"ERROR: this clientId: {self.id} doesn't exist")

try:
    print("\nServer running...Press Ctrl+C to stop.")
    print("-----------------\n")
    print("Waiting for connection...")
    while True:
        
        try:    
            conn, addr = tcpsocket.accept()
        except socket.timeout:
            continue
        print("Connected to: ", addr)
        client = clientThread(conn, addr, str(currentId))
        client.start()

        currentId += 1 
    
except KeyboardInterrupt:
    print("\nServer closed...")

finally:
    tcpsocket.close()

    

    
    

    