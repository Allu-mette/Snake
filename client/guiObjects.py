import pygame
from settings import *


class Button:
    
    def __init__(self, pos: vec2, text: str, size= (), active= True, activeColor=ACTIVE_COLOR_BUTTON,
                 inactiveColor=INACTIVE_COLOR_BUTTON, textColor=TEXT_COLOR_BUTTON, 
                 outlineColor=OUTLINE_COLOR_BUTTON):
        
        
        self.activeColor = activeColor
        self.inactiveColor = inactiveColor
        self.textColor = textColor
        self.outlineColor = outlineColor
        self.textSurf = FONT_GUI2.render(text, True, self.textColor)
        
        if size != ():
            self.w, self.h = size
        else:
            self.w, self.h = self.textSurf.get_rect().size
            self.w += 2*BORDER_BUTTON_SIZE + 2*BUTTON_MARGIN
            self.h += 2*BORDER_BUTTON_SIZE + 2*BUTTON_MARGIN
        self.rectButton = pygame.Rect(0, 0, self.w, self.h)
        self.rectButton.center = pos
        self.posText = self.rectButton.center - vec2(self.textSurf.get_width() // 2 -1,
                                                     self.textSurf.get_height() // 2 +1)
        
        self.active = active
        self.press = False
        self.overfly = False
        
    def check_event(self, event: pygame.event.Event):
        
        self.press = False
        if self.active:
            if self.overfly and event.type == pygame.MOUSEBUTTONDOWN:
                self.press = True
    
    def update(self):
        
            # Overfly selection
        if self.rectButton.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.overfly = True
        else:
            self.overfly = False
    
    def draw(self, screen: pygame.Surface):
        
        if self.active:
            pygame.draw.rect(screen, self.activeColor, self.rectButton)
            if self.overfly:
                pygame.draw.rect(screen, self.outlineColor, self.rectButton, BORDER_BUTTON_SIZE)
            self.textSurf.set_alpha(255)
        else:
            pygame.draw.rect(screen, self.inactiveColor, self.rectButton)
            self.textSurf.set_alpha(50)
                    
        screen.blit(self.textSurf, self.posText)
        
class EntryText:
    
    def __init__(self, pos: vec2, width=(SIZE*12), backColor=BACK_COLOR_ENTRY, outlineColor=OUTLINE_COLOR_ENTRY,
                 textColor=TEXT_COLOR_ENTRY):
        
        self.text = ""
        self.backColor = backColor
        self.outlineColor = outlineColor
        self.textColor = textColor
        self.textHeight = FONT_GUI2.render(self.text, True, "white").get_height()
        self.w = width
        self.h = self.textHeight
        
            # Rect EntryBox
        self.rectEntryBox = pygame.Rect(0, 0, self.w + 2*BORDER_ENTRY_SIZE + 2*ENTRY_MARGIN, 
                                        self.h + 2*BORDER_ENTRY_SIZE + 2*ENTRY_MARGIN)
        self.rectEntryBox.center = pos
            # Text Cursor Surface
        self.textSurface = pygame.Surface((self.w, self.h))
        self.textSurface.fill(self.backColor)
        #self.textSurface.set_colorkey(self.backColor)
        self.posText = vec2(self.rectEntryBox.x + BORDER_ENTRY_SIZE + ENTRY_MARGIN, 
                            self.rectEntryBox.y + BORDER_ENTRY_SIZE + ENTRY_MARGIN-1)
            # Rect Cursor Text
        self.rectCursor = pygame.Rect(0, 0, ENTRY_MARGIN, BORDER_ENTRY_SIZE // 2)
        self.rectCursor.bottomleft = (0, self.h)

        self.active = True
        self.timer = 0
        
    def update(self):

            # Overfly selection
        if self.rectEntryBox.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            
            # Active
        if self.active:
                # Update Timer                
            self.timer = (self.timer + 1) % 60
             
             # Not Active       
        elif not self.active:
            self.timer = 0
        
    def check_event(self, event: pygame.event.Event):
        
            # Active
        if self.active:
            
                # Add text 
            if event.type == pygame.TEXTINPUT:
                self.text += event.text
                # Delete text
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            
            # Set Active/Not Active
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rectEntryBox.collidepoint(event.pos):
                self.active = True
                self.timer = 0
            else:
                self.active = False
        
    def draw(self, screen: pygame.Surface):
        self.textSurface.fill(self.backColor)
        
            # Draw text
        surf = FONT_GUI2.render(self.text, True, self.textColor)
        if surf.get_width() > self.w - 2*ENTRY_MARGIN:
            self.textSurface.blit(surf, (self.w-surf.get_width()-2*ENTRY_MARGIN, 0))
            self.rectCursor.left = self.w-2*ENTRY_MARGIN
        else:
            self.textSurface.blit(surf, (0, 0))
            self.rectCursor.left = surf.get_width()
        
            # Draw TextCursor
        if self.active:
            if self.timer <= 30:
                self.textSurface.fill(self.textColor, self.rectCursor) 
            else:
                self.textSurface.fill(self.backColor, self.rectCursor)
        
        pygame.draw.rect(screen, self.outlineColor, self.rectEntryBox, BORDER_ENTRY_SIZE)
        screen.blit(self.textSurface, self.posText)

class Label:
     
    def __init__(self, pos: vec2, text: str, size= (), backColor=BACK_COLOR_LABEL, outlineColor=OUTLINE_COLOR_LABEL,
                 textColor=TEXT_COLOR_LABEL, isOutline=False):
        
        self.backColor = backColor
        self.outlineColor = outlineColor
        self.textColor = textColor
        self.isOutline = isOutline
        self.textSurf = FONT_GUI2.render(text, True, self.textColor)
         
        if size != ():
            self.w, self.h = size
        else:
            self.w, self.h = self.textSurf.get_rect().size
            self.w += 2*BORDER_LABEL_SIZE + 2*LABEL_MARGIN
            self.h += 2*BORDER_LABEL_SIZE + 2*LABEL_MARGIN
            
        self.rectBack = pygame.Rect(0, 0, self.w, self.h)
        self.rectBack.center = pos
        self.posText = self.rectBack.center - vec2(self.textSurf.get_width() // 2 -1,
                                                     self.textSurf.get_height() // 2 +1)
     
    def update(self):
         pass
     
    def check_event(self, event: pygame.event.Event):
        pass
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.backColor, self.rectBack)
        if self.isOutline:
            pygame.draw.rect(screen, self.outlineColor, self.rectBack, BORDER_LABEL_SIZE)
        screen.blit(self.textSurf, self.posText)
        
class Table:
    
    def __init__(self, pos: vec2, table: list[list], size=(), isClickable=True, backColor=BACK_COLOR_TABLE, 
                 headColor=HEADBACK_COLOR_TABLE,overflyColor=OVERFLY_COLOR_TABLE, 
                 outlineColor=OUTLINE_COLOR_TABLE, textColor=TEXT_COLOR_TABLE):
        
            #Color Init
        self.backColor = backColor
        self.headColor = headColor
        self.overflyColor = overflyColor
        self.selectedColor = overflyColor
        self.outlineColor = outlineColor
        self.textColor = textColor
        
            # Other stuff
        self.isClickable = isClickable
        self.table = table
        self.overflyInd = None
        self.selectedInd = None
        self.selectedRow = None

            # Create tableRows List (2D)
        self.tableRows = []
        for ind, row in enumerate(table):
            self.tableRows.append([])
            for text in row:
                self.tableRows[ind].append(FONT_GUI.render(str(text), True, self.textColor))
                    
            # Set Columns Width List
        self.columnWidth = []
        for ind, textSurf in enumerate(self.tableRows[0]):
            maxW = textSurf.get_width()
            for row in self.tableRows:
                textSurf = row[ind]
                width = textSurf.get_width()
                if width > maxW:
                    maxW = width
            self.columnWidth.append(maxW)
            
            # Set Rows Height List
        self.rowHeight = []
        for row in self.tableRows:
            maxH = row[0].get_height()
            for textSurf in row:
                height = textSurf.get_height()
                if height > maxH:
                    maxH = height
            self.rowHeight.append(maxH)
        
            #Set Table Width/Height
        self.tableWidth, self.tableHeight = 0, 0
        
        for width in self.columnWidth:
            self.tableWidth += width + 2*TABLE_MARGIN
            
        for height in self.rowHeight:
            self.tableHeight += height + 2*TABLE_MARGIN
            
            # Create rectBack
        self.rectBack = []
        self.rectBackColor = []
        self.posTopLeft = pos - vec2(self.tableWidth // 2, self.tableHeight // 2)
        coord = self.posTopLeft.copy()
        for ind, row in enumerate(self.tableRows):
            self.rectBack.append(pygame.Rect(0, 0, self.tableWidth, self.rowHeight[ind]+2*TABLE_MARGIN))
            if ind == 0:
                self.rectBackColor.append(self.headColor)
            else:
                self.rectBackColor.append(self.backColor)
            self.rectBack[-1].topleft = coord
            coord += vec2(0, TABLE_MARGIN*2) + vec2(0, self.rowHeight[ind])
        
    def update(self):
        
        if self.isClickable:
                # Set Overfly indice  
            self.overflyInd = None
            for ind, rect in enumerate(self.rectBack[1:]):
                
                self.rectBackColor[ind+1] = self.backColor
                if rect.collidepoint(pygame.mouse.get_pos()):
                    self.overflyInd = ind+1          
            
                # Overfly Back Color
            if self.overflyInd:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.rectBackColor[self.overflyInd] = self.overflyColor
                
                # Selected Back Color and Row Selected
            self.selectedRow = None
            if self.selectedInd:
                self.rectBackColor[self.selectedInd] = self.selectedColor
                self.selectedRow = self.table[self.selectedInd]

    
    def check_event(self, event: pygame.event.Event):
        
        if self.isClickable:
                # Set Selected Indice
            if event.type == pygame.MOUSEBUTTONUP:
                if self.overflyInd:
                    self.selectedInd = self.overflyInd
                else:
                    self.selectedInd = None
    
    def draw(self, screen: pygame.Surface):
        
            # Draw the back
        for ind, rect in enumerate(self.rectBack):
            pygame.draw.rect(screen, self.rectBackColor[ind], rect)
        
            # Draw the columns lines
        for ind in range(len(self.columnWidth)+1):
            startPos = self.posTopLeft + vec2(sum(self.columnWidth[:ind]), 0) + vec2(TABLE_MARGIN, 0)*2*ind
            endPos = self.posTopLeft + vec2(sum(self.columnWidth[:ind]), self.tableHeight) + vec2(TABLE_MARGIN, 0)*2*ind
            pygame.draw.line(screen, self.outlineColor, startPos, endPos)
            # Draw the rows lines
        for ind in range(len(self.rowHeight)+1):
            startPos = self.posTopLeft + vec2(0, sum(self.rowHeight[:ind])) + vec2(0, TABLE_MARGIN)*2*ind
            endPos = self.posTopLeft + vec2(self.tableWidth, sum(self.rowHeight[:ind])) + vec2(0, TABLE_MARGIN)*2*ind
            pygame.draw.line(screen, self.outlineColor, startPos, endPos)
            
            # Draw text
        for num, row in enumerate(self.tableRows):
            for ind, text in enumerate(row):
                pos = self.posTopLeft + vec2(TABLE_MARGIN, TABLE_MARGIN) + \
                    vec2(TABLE_MARGIN*ind*2, TABLE_MARGIN*num*2) + vec2(sum(self.columnWidth[:ind]), 0) + \
                        vec2(0, sum(self.rowHeight[:num]))
                screen.blit(text, pos)
            
        
     