
# data typle "ACTION:INFO"

def getReply(action: str, myId: str, clientList: dict, lobbyList: dict)->str:
    """Get the reply

    Args:
        action (str): Action
        myId (str): My id
        clientList (dict): Server Data

    Returns:
        (str): The reply
    """
    reply = ''
        # Connection
    if action == "CONNEXION":
        reply = "CONNEXION"
        
        # Actualize Lobby
    elif action == "ACTUALIZE LOBBY":
        reply = "LOBBY LIST"
        for id, _ in lobbyList.items():
            if id != myId and lobbyList[id]["status"] == "OPEN":
                reply += ":"+str(id) + ";" + str(lobbyList[id]["name"]) + \
                    ";" + str(len(lobbyList[id]["playerId"])) + " " + str(lobbyList[id]["place"])
        
        # Join Lobby
    elif action == "JOIN":
        
        lobbyId = clientList[myId]["lobbyId"]
            # Check if the Lobby exist
        if lobbyId != None:
                # Check if the Lobby is Full
            if myId in lobbyList[lobbyId]["playerId"]:
                reply = "JOIN"
            else:
                reply = "FULL"
        else:
            "NOT EXIST"
        
        # Host Lobby
    elif action == "HOST":
        reply = "HOST"
        
        # Quit Lobby
    elif action == "QUIT LOBBY":
        reply = "QUIT LOBBY"
        
    elif action == "QUIT GAME":
        reply = "QUIT GAME"
        
        # Waiting player
    elif action == "WAITING PLAYER":
        
            # Check if Lobby exist
        if clientList[myId]["lobbyId"] != None:
            lobbyId = clientList[myId]["lobbyId"]
            
                # Lobby if Lobby is In Game
            if lobbyList[lobbyId]["status"] == "IN GAME":
                reply =  "LOBBY READY"+":"+str(lobbyList[lobbyId]["playerId"].index(myId))
            
                # Not ready
            else:
                reply = "PLAYER LIST"
                reply += ":"+str(lobbyList[lobbyId]["place"])
                for playerId in lobbyList[lobbyId]["playerId"]:
                    reply += ":"+str(clientList[playerId]["name"]) + ";" + str(clientList[playerId]["status"])
                    
            # Lobby has been deleted
        else:
            reply = "QUIT LOBBY"
        
        
    elif action == "READY":
        return "READY"
        
        #Setup the Game
    elif action == "GAME SETUP":
        reply = "GAME SETUP"
        
            # Check if Lobby exist
        if clientList[myId]["lobbyId"] != None:
            lobbyId = clientList[myId]["lobbyId"]
                #Check if Lobby is In Game
            if lobbyList[lobbyId]["status"] == "IN GAME":
                for playerId in lobbyList[lobbyId]["playerId"]:
                    
                    dataGame = clientList[playerId]["dataGame"]
                    if dataGame == {}:
                        reply = "FALSE"
                        break
                    elif playerId != myId:
                        gameId = dataGame["gameId"]
                        name = clientList[playerId]["name"]
                        bonusPos = dataGame["bonusPos"]
                        
                        
                        reply += ":" + gameId + "|" + name + "|"  + bonusPos
                        
                # A Player Left
            else:
                reply =  "QUIT GAME"
            # Lobby has been deleted
        else:
            reply = "QUIT LOBBY"
    
        # Get data in Game
    elif action == "GAME UPDATE":
        reply = "GAME UPDATE"
        
            #Check if Lobby exist
        if clientList[myId]["lobbyId"] != None:
            lobbyId = clientList[myId]["lobbyId"]
            
                #Check if Lobby is In Game
            if lobbyList[lobbyId]["status"] == "IN GAME":
                for playerId in lobbyList[lobbyId]["playerId"]:
                    dataGame = clientList[playerId]["dataGame"]
                    if playerId != myId:
                        gameId = dataGame["gameId"]
                        snakeBody = dataGame["snakeBody"]
                        bonusPos = dataGame["bonusPos"]
                        
                        reply += ":" + gameId + "|" + snakeBody + "|" + bonusPos
                        
                # A Player Left  
            else:
                reply = "QUIT GAME"
            # Lobby has been deleted
        else:
            reply = "QUIT LOBBY"
        
        # Quit
    elif action == "QUIT":
        reply = "QUIT"
                    
    return reply
