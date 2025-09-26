import pygame
from math import *
from settings import *
import random

class Game:
    
    active: bool = False
    countdown: int = 3
    
    def __init__(self, id: str, name: str) -> None:
        
        self.id = id
        self.grid = Grid()
        self.snake = Snake(START_POS[id], START_DIR[id], START_LEN, COLORS[id], name)
        
        self.bonusPos = vec2(random.randint(0, COL_NUM-1)*SIZE, random.randint(0, ROW_NUM-1)*SIZE)
        while(not self.placeIsFree(self.bonusPos)):
            self.bonusPos = vec2(random.randint(0, COL_NUM-1)*SIZE, random.randint(0, ROW_NUM-1)*SIZE)
        self.bonus = Bonus(self.bonusPos, COLORS[id])
        
        pygame.time.set_timer(pygame.USEREVENT+1, 1000)

    def update(self):
        self.snake.update()
        if self.snake.pos == self.bonus.pos:
            del self.bonus
            self.bonusPos = vec2(random.randint(0, COL_NUM-1)*SIZE, random.randint(0, ROW_NUM-1)*SIZE)
            while(not self.placeIsFree(self.bonusPos)):
                self.bonusPos = vec2(random.randint(0, COL_NUM-1)*SIZE, random.randint(0, ROW_NUM-1)*SIZE)
            self.bonus = Bonus(self.bonusPos, COLORS[self.id])
            self.bonus = Bonus(self.bonusPos, COLORS[self.id])
            pass
        else:
            self.snake.body.pop()
    
    def check_event(self, event: pygame.event.Event):
            # Countdown Start
        if not self.active:
            if event.type == pygame.USEREVENT+1:
                self.countdown -= 1
                pygame.time.set_timer(pygame.USEREVENT+1, 1000)
            if self.countdown == 0:
                self.active = True
            # Game Running
        else:
            self.snake.check_event(event)
    
    def draw(self, screen: pygame.Surface):
        
        self.grid.draw(screen)
        self.snake.draw(screen)
            #Draw Countdwon
        if not self.active:
            surf = FONT_GAMEOVER.render(str(self.countdown), True, COLORS[self.id])
            screen.blit(surf, CENTER-vec2(surf.get_size())//2)
        else:
            self.bonus.draw(screen)

    def placeIsFree(self, vec2):
        return True

class Grid:
    
    def __init__(self):
        pass
    
    def draw(self, screen: pygame.surface):
        for x in range(0, COL_NUM):
            start = (x*SIZE, 0)
            end = (x*SIZE, WIDTH)
            pygame.draw.line(screen, "white", start, end)
        for y in range(0, ROW_NUM):
            start = (0, y*SIZE)
            end = (WIDTH, y*SIZE)
            pygame.draw.line(screen, "white", start, end)
                

class Snake:
    
    def __init__(self, startPos: vec2, startDir: float, startLen: int, color, name=""):
        
        self.len = startLen
        self.dir = startDir
        self.color = color
        self.x, self.y = self.pos = startPos
        self.surfName = FONT_GUI.render(name, True, color)
        
        self.body = []
        for i in range(self.len):
            self.body.append((self.pos + vec2(cos(self.dir)*SIZE*i, sin(self.dir)*SIZE*i)))
        
    def update(self):
        
        self.pos += vec2(int(cos(self.dir)*SIZE), -int(sin(self.dir)*SIZE))
        self.pos.x %= WIDTH
        self.pos.y %= HEIGHT
        self.body.insert(0, self.pos.copy())
            
    def updateData(self, data: list[vec2]):
        self.pos = data[0]
        self.body = data
        
    def check_event(self, event: pygame.event.Event):
        
        if event.type == pygame.KEYDOWN:
            if event.key in KEYS:
                
                keys = KEYS.copy()
                index = KEYS.index(event.key) 
                    
                if self.dir >= pi:
                    keys.insert(0, keys.pop())
                if self.dir >= 3*pi/2:
                    keys.insert(0, keys.pop())
                if self.dir == 0:
                    keys.append(keys.pop(0))
                    
                if keys[index] == KEY_RIGHT:
                    self.dir -= pi/2
                elif keys[index] == KEY_LEFT:
                    self.dir += pi/2
                    
                self.dir %= 2*pi
        
    def draw(self, screen):
        rect = pygame.Rect(0, 0, SIZE, SIZE)
        for pos in self.body:
            rect.topleft = pos
            pygame.draw.rect(screen, self.color, rect.copy())
        screen.blit(self.surfName, self.pos-(0, SIZE))
        
class Bonus:
    
    def __init__(self, startPos: vec2, color):
        
        self.x, self.y = self.pos = startPos
        self.color = color
    
    def draw(self, screen):
        rect = pygame.Rect(self.x+SIZE/4, self.y+SIZE/4, SIZE/2, SIZE/2)
        pygame.draw.rect(screen, self.color, rect)
        
    def updateData(self, data: vec2):
        self.pos = data
        