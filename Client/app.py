import pygame
import sys
from settings import *
import gameObects
import guiObjects
from network import Network

class App:
    
    def __init__(self):
        
        self.screen = pygame.display.set_mode(RES)
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        
        self.net = Network()
        self.game = None

        self.table = [["ID", "NAME", "PING"],
                      [1, "Khalil", 48],
                      [2, "Sarah", 16]]
        
        if self.net.id == -1:
            self.initialization("OFFLINE")
        else:
            self.initialization("LOGIN")
        
    def update(self):
        
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
            # Update gui
        for element in self.guiList:
            element.update()
            
            # OFFLINE
        if self.state == "OFFLINE":
            
                # Actualize
            if self.actuButton.press:

                del self.net
                self.net = Network()

                if self.net.id != -1:
                    self.initialization("LOGIN")
                    
            # LOGIN PAGE
        elif self.state == "LOGIN":
            if self.entryName.text != '':
                self.validateButton.active = True
            else:
                self.validateButton.active = False
                
            if self.validateButton.press:
                self.name = self.entryName.text
                self.sendData(f"CONNEXION:{self.name}")
                self.initialization("HOMEPAGE")
        
            # HOMEPAGE
        elif self.state == "HOMEPAGE":
            
                # Actualize Lobby list
            if self.actuButton.press:
                self.data = self.sendData(f"ACTUALIZE LOBBY")
                self.lobbyTable = self.readData(self.data)
                self.guiList.remove(self.tableLobby)
                del self.tableLobby
                self.tableLobby = guiObjects.Table(CENTER+vec2(-4*SIZE, SIZE), self.lobbyTable)
                self.guiList.append(self.tableLobby)
                # Create a Lobby
            if self.hostButton.press:
                self.initialization("CREATE LOBBY")
                
            if self.tableLobby.selectedRow and self.tableLobby.selectedRow[0] != '':
                self.joinButton.active = True
            else:
                self.joinButton.active = False
            
                #Join a Lobby
            if self.joinButton.press:   
                row = self.tableLobby.selectedRow
                self.lobbyId = row[0]
                self.initialization("JOIN LOBBY")
                
            # CREATE LOBBY
        elif self.state == "CREATE LOBBY":
            
            if self.entryName.text != '':
                self.validateButton.active = True
            else:
                self.validateButton.active = False
                
            if self.validateButton.press:
                self.lobbyId = self.id
                self.sendData(f"HOST:{self.entryName.text}:2")
                self.initialization("IN QUEUE")
        
            # JOIN LOBBY
        elif self.state == "JOIN LOBBY":
            pass
        
            # IN QUEUE
        elif self.state == "IN QUEUE":
            
                # Quit Lobby
            if self.quitButton.press:
                    #Destroy Lobby if host
                self.sendData("QUIT LOBBY")
                self.initialization("HOMEPAGE")
                
            elif self.readyButton.press:
                self.sendData("READY")
                
            # GAME RUNNING
        elif self.state == "IN GAME":
            pass
            
            # GAME OVER
        elif self.state == "GAMEOVER":
            pass

    def check_event(self):
        
        for event in pygame.event.get():
            
                # Quit
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.type == pygame.K_ESCAPE):
                if self.net.id != -1:
                    self.sendData("QUIT")
                pygame.quit()
                sys.exit()
                
                # check event for gui
            for element in self.guiList:
                element.check_event(event)
            
                # IN QUEUE
            if self.state == "IN QUEUE":
                
                 # Actualize queue List
                if event.type == pygame.USEREVENT:
                    self.data = self.sendData("WAITING PLAYER")
                    self.table = self.readData(self.data)
                    
                        # Quit the Lobby
                    if self.table[0] == "QUIT LOBBY":
                        self.sendData("QUIT LOBBY")
                        self.initialization("HOMEPAGE")
                        
                        # Lobby is Ready
                    elif self.table[0] == "LOBBY READY":
                        self.gameId = self.table[1]
                        self.initialization("IN GAME")
                        
                        # Get the List of the Players
                    elif type(self.table[0]) == list:
                        self.guiList.remove(self.tableQueue)
                        del self.tableQueue
                        self.tableQueue = guiObjects.Table(CENTER+vec2(0, 2*SIZE), self.table, isClickable=False)
                        self.guiList.append(self.tableQueue)
                 
                 # GAME RUNNING    
            elif self.state == "IN GAME":
                self.game.check_event(event)
                
                if self.game.active:
                    if event.type == pygame.USEREVENT:
                        
                        pygame.time.set_timer(pygame.USEREVENT, GAME_SPEED)
                        self.game.update()
                        
                        package = self.generateGamePackage(self.game)
                        otherData = self.sendData(f"GAME UPDATE:{package}")
                        otherData = self.readData(otherData)
                        
                        if type(otherData) == dict:
                            for snakeId, objects in self.gameObjectList.items():
                                objects["snake"].updateData(otherData[snakeId]["snakeBody"])
                                objects["bonus"].updateData(otherData[snakeId]["bonusPos"])
                        
                        elif otherData[0] == "QUIT LOBBY":
                            self.sendData("QUIT LOBBY")
                            self.initialization("HOMEPAGE")
                            
                        elif otherData[0] == "QUIT GAME":
                            self.sendData("QUIT GAME")
                            self.initialization("IN QUEUE")
                
                # GAME OVER
            elif self.state == "GAMEOVER":
                pass
            
    def drawOffline(self):
        pass
        
    def drawLogin(self):
        pass
        
    def drawHomepage(self):
        pass

    def drawQueue(self):
        pass
    
    def drawGame(self):
        
        self.game.draw(self.screen)

        for _, objects in self.gameObjectList.items():
            objects["snake"].draw(self.screen)
            objects["bonus"].draw(self.screen)
        
    def drawGameOver(self):
        pass
          
    def draw(self):
        
        self.screen.fill(BG_COLOR)
        
            # draw gui
        for element in self.guiList:
            element.draw(self.screen)
        
        if self.state == "OFFLINE":
            self.drawOffline()
            
        elif self.state =="HOMEPAGE":
            self.drawHomepage()
            
        elif self.state == "IN GAME":
            self.drawGame()
            
        elif self.state == "GAMEOVER":
            self.drawGameOver()
        
        pygame.display.flip()
        
    def run(self):
        
        while(True):
            self.check_event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
    def initialization(self, stateName: str):
        """Init of the different scenes
        """
        
            # Update state of th game
        self.state = stateName
            # Clear the gui list
        try:
            for element in self.guiList:
                del element
        except AttributeError:
            self.guiList = []
        else:
            self.guiList.clear()
        
            # OFFLINE
        if stateName == "OFFLINE":
            
            self.actuButton = guiObjects.Button(CENTER, "RETRY")
            self.guiList.append(self.actuButton)
        
            # LOGIN
        elif stateName == "LOGIN":
            self.id = self.net.id
            self.entryName = guiObjects.EntryText(CENTER)
            self.guiList.append(self.entryName)
            self.guiList.append(guiObjects.Label(CENTER + vec2(0, 2*SIZE), 
                                                 "ENTER YOUR NAME"))
            self.validateButton = guiObjects.Button(CENTER + vec2(0, 6*SIZE), "VALIDATE", active=False)
            self.guiList.append(self.validateButton)
        
            # HOMEPAGE
        elif stateName == "HOMEPAGE":
            
            self.guiList.append(guiObjects.Label(CENTER + vec2(0, -8*SIZE), 
                                                 "SELECT A LOBBY"))
            self.actuButton = guiObjects.Button(CENTER+vec2(5*SIZE, 0), "ACTUALIZE", size=(8*SIZE, 2*SIZE))
            self.hostButton = guiObjects.Button(CENTER+vec2(5*SIZE, 3*SIZE), "HOST", size=(8*SIZE, 2*SIZE))
            self.joinButton = guiObjects.Button(CENTER+vec2(5*SIZE, 6*SIZE), "JOIN", active=False, size=(8*SIZE, 2*SIZE))
            self.guiList.append(self.actuButton)
            self.guiList.append(self.hostButton)
            self.guiList.append(self.joinButton)
            
            self.data = self.sendData(f"ACTUALIZE LOBBY")
            self.lobbyTable = self.readData(self.data)
            self.tableLobby = guiObjects.Table(CENTER+vec2(-4*SIZE, SIZE), self.lobbyTable)
            self.guiList.append(self.tableLobby)

            # CREATE LOBBY
        elif stateName == "CREATE LOBBY":
            self.entryName = guiObjects.EntryText(CENTER)
            self.guiList.append(self.entryName)
            self.guiList.append(guiObjects.Label(CENTER + vec2(0, 2*SIZE), 
                                                 "LOBBY NAME"))
            self.validateButton = guiObjects.Button(CENTER + vec2(0, 6*SIZE), "VALIDATE", active=False)
            self.guiList.append(self.validateButton)
        
            # JOIN LOBBY
        elif stateName == "JOIN LOBBY":
            self.data = self.sendData(f"JOIN:{self.lobbyId}")
            
                #Lobby is Full
            if self.data == "FULL":
                self.initialization("HOMEPAGE")
                #Join the Lobby
            elif self.data == "JOIN":
                self.initialization("IN QUEUE")
                #Lobby doesn't exist
            elif self.data == "NOT EXIST":
                self.initialization("HOMEPAGE")
        
            # IN QUEUE
        elif stateName == "IN QUEUE":
            
            self.data = self.sendData("WAITING PLAYER")
            self.table = self.readData(self.data)

            self.guiList.append(guiObjects.Label(CENTER + vec2(0, -4*SIZE), 
                                                "WAITING FOR PLAYER"))
            self.readyButton = guiObjects.Button(CENTER+vec2(-4*SIZE, 8*SIZE), "READY", size=(8*SIZE, 2*SIZE))
            self.quitButton = guiObjects.Button(CENTER+vec2(4*SIZE, 8*SIZE), "QUIT", size=(8*SIZE, 2*SIZE))
            self.tableQueue = guiObjects.Table(CENTER+vec2(0, 2*SIZE), self.table, isClickable=False)
            self.guiList.append(self.tableQueue)
            self.guiList.append(self.readyButton)
            self.guiList.append(self.quitButton)
            
            pygame.time.set_timer(pygame.USEREVENT, 500)
        
            # GAME
        elif stateName == "IN GAME":
            
                # Clear the gameObject list
            try:
                for gameObject in self.gameObjectList:
                    del gameObject
            except AttributeError:
                self.gameObjectList = {}
            else:
                self.gameObjectList.clear()
            
                # SELF GAME
            self.game = gameObects.Game(self.gameId, self.name)
            
                # GET OTHER DATA
            package = self.generateGamePackage(self.game)
            otherData = self.sendData(f"GAME SETUP:{package}")
            otherDataList = self.readData(otherData)
            
            while otherDataList[0] == "FALSE":
                otherData = self.sendData(f"GAME SETUP:{package}")
                otherDataList = self.readData(otherData)
                
                # Game Setup
            if otherDataList[0] == "GAME SETUP":

                for dataGame in otherDataList[1:]:
                    snakeId = dataGame["gameId"]
                    snakeName = dataGame["name"]
                    snakeObject = gameObects.Snake(START_POS[snakeId], 
                                                START_DIR[snakeId],
                                                START_LEN,
                                                COLORS[snakeId],
                                                snakeName)
                    bonusPos = dataGame["bonusPos"]
                    bonusObject = gameObects.Bonus(bonusPos, COLORS[snakeId])
                    
                    self.gameObjectList[snakeId] = {"snake": snakeObject,
                                                    "bonus": bonusObject}  
                # Qui Game
            elif otherDataList[0] == "QUIT GAME":
                self.sendData("QUIT GAME")
                self.initialization("IN QUEUE")         
                
                # Qui Lobby
            elif otherDataList[0] == "QUIT LOBBY":
                self.sendData("QUIT LOBBY")
                self.initialization("HOMEPAGE")     
            
            pygame.time.set_timer(pygame.USEREVENT, GAME_SPEED)
            
            # GAME OVER
        elif stateName == "GAMEOVER":
            pass
        
        
    def sendData(self, data)->str:
        print(f"Sending: {data}")
        reply = self.net.send(data)
        print(f"Reply: {reply}")
        return reply
    
    @staticmethod
    def readData(data: str):
        dataList = data.split(":")
        
            # Get Lobby Table [[ID, NAME, MAX, CURRENT]]
        if dataList[0] == "LOBBY LIST":
                # HEAD
            lobbyTable = [["ID", "NAME", "PEOPLE"]]
                # DATA ROW
            for row in dataList[1:]:
                lobbyTable.append(row.split(";"))
                # EMPTY ROW
            if len(lobbyTable) < 8:
                for _ in range(8-len(lobbyTable)):
                    lobbyTable.append(["", "", ""])
            return lobbyTable
        
            # Get Queue Table [[Name]]
        elif dataList[0] == "PLAYER LIST":
            maxPlayer = int(dataList[1])
                # HEAD
            queueTable = [["PLAYER", "READY"]]
                # DATA ROW
            for row in dataList[2:]:
                queueTable.append(row.split(";"))
                # EMPTY ROW
            if len(queueTable) <= maxPlayer:
                for _ in range(maxPlayer-len(queueTable)+1):
                    queueTable.append(["", ""])
            return queueTable
        
        elif dataList[0] == "QUIT LOBBY":
            return dataList
        
        elif dataList[0] == "QUIT GAME":
            return dataList
        
        elif dataList[0] == "LOBBY READY":
            return dataList
        
        elif dataList[0] == "GAME SETUP":
            dataGameList = ["GAME SETUP"]
            
            for gameData in dataList[1:]:
                gameDataList = gameData.split("|")
                gameId = gameDataList[0]
                name = gameDataList[1]

                pos = gameDataList[2].split(",")
                bonusPos = vec2(float(pos[0]), float(pos[1]))
                
                data = {"gameId": gameId, "name": name, "bonusPos": bonusPos}
                dataGameList.append(data)
            
            return dataGameList
        
        elif dataList[0] == "GAME UPDATE":
            dataGame = {}
            
            for gameData in dataList[1:]:
                gameDataList = gameData.split("|")
                gameId = gameDataList[0]
                snakeBody = []
                snakeBodyList = gameDataList[1].split(";")
                for body in snakeBodyList:
                    pos = body.split(",")
                    snakeBody.append(vec2(float(pos[0]), float(pos[1])))
                
                pos = gameDataList[2].split(",")
                bonusPos = vec2(float(gameDataList[2][0]), float(gameDataList[2][1]))
                
                data = {"snakeBody": snakeBody, "bonusPos": bonusPos}
                dataGame[gameId] = data
                
            return dataGame
                
        elif dataList[0] == "FALSE":
            return dataList
            
     
    @staticmethod
    def generateGamePackage(game: gameObects.Game)->str:
        
            #Id
        id = game.id
            # Snake Body Pos
        snake = game.snake
        snakeBody = ""
        for pos in snake.body:
            snakeBody += f"{pos.x},{pos.y}"+";"
        snakeBody = snakeBody[:-1]
            # Bonus Pos
        bonus = game.bonus
        bonusPos = f"{bonus.pos.x},{bonus.pos.y}"
        
        package = id + ":" + snakeBody + ":" + bonusPos
        return package
        
        

