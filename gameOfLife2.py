import pygame
# import random

pygame.init()
pygame.display.set_caption("Conway's Game of Life")

windowWidth = 1920
windowHeight = 800
cellSize = 20
WHITE = (255,255,255)
GRAY = (50,50,50)
BLACK = (0,0,0)
lineThickness = 2
lineLenght = 1000
lineColor = GRAY
font = pygame.font.SysFont('comicsans', 25, True)
spaceBarPressed = False
buildMode = True

window=pygame.display.set_mode((windowWidth,windowHeight), pygame.RESIZABLE)

class cell:
    def __init__(self, pos, cellSize, number, neighbourList):
        self.state = False
        self.liveNeighbours = 0
        self.pos = pos
        self.button = pygame.Rect(pos[0], pos[1], cellSize, cellSize)
        self.number = number
        self.neighbourList = neighbourList
    
    def draw(self, window):
        if self.state:
            pygame.draw.rect(window, WHITE, self.button)
        else:
            pygame.draw.rect(window, BLACK, self.button)
    
    def updateLiveNeighbourCount(self):
        self.liveNeighbours = 0
        for i in self.neighbourList :
            if i.state:
                self.liveNeighbours +=1

linesList = []
linex = 0
liney = 0
for i in range(windowWidth//cellSize + 1):
    # vertical lines-
    linesList.append((linex,0,5,windowHeight))
    linex += (cellSize + lineThickness)

for i in range(windowHeight//cellSize + 1):
    # horizontal lines-
    linesList.append((0,liney,windowWidth,5))
    liney += (cellSize + lineThickness)

buttonCordsList = []
buttonx, buttony = lineThickness, lineThickness
cells = []
cells2 = []
cellsIndex2 = 0

for i in range(1,windowHeight//cellSize + 1):
    l=[]
    for j in range(1,windowWidth//cellSize + 1):
        buttonCordsList.append((buttonx,buttony))
        c = cell((buttonx,buttony),cellSize,(cellsIndex2,j-1),[])
        cells.append(c)
        l.append(c)
        buttonx += (cellSize+lineThickness)
    buttony += (cellSize+lineThickness)
    buttonx = lineThickness
    cellsIndex2 += 1
    cells2.append(l)

cList = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
cList2 = [(-1,-1),(1,-1),(0,-1),(-1,0),(1,0),(0,1),(-1,1),(1,1)]
listOfAllNeighbours = []

a=len(cells2[0])
b=len(cells2)
for i in range(b):
    l1 = []
    for j in range(a):
        l2=[]
        if i==0 and j==0:
            for cords in [(0,1),(1,0),(1,1)]:
                l2.append(cells2[i+cords[0]][j+cords[1]])
        elif i==0 and j==a-1:
            for cords in [(0,-1),(1,0),(1,-1)]:
                l2.append(cells2[i+cords[0]][j+cords[1]])
        elif i==b-1 and j==0:
            for cords in [(0,1),(-1,0),(-1,1)]:
                l2.append(cells2[i+cords[0]][j+cords[1]])
        elif i==b-1 and j==a-1:
            for cords in [(0,-1),(-1,0),(-1,-1)]:
                l2.append(cells2[i+cords[0]][j+cords[1]])
        elif i==0:
            for cords in cList[3:]:
                l2.append(cells2[i+cords[0]][j+cords[1]])
        elif i==b-1:
            for cords in cList[:-3]:
                l2.append(cells2[i+cords[0]][j+cords[1]])
        elif j==0:
            for cords in cList2[3:]:
                l2.append(cells2[i+cords[0]][j+cords[1]])
        elif j==a-1:
            for cords in cList2[:-3]:
                l2.append(cells2[i+cords[0]][j+cords[1]])
        else:
            for cords in cList:
                l2.append(cells2[i+cords[0]][j+cords[1]])
        l1.append(l2)
    listOfAllNeighbours.append(l1)

for i in range(len(cells2)):
    for j in range(len(cells2[i])):
        cells2[i][j].neighbourList = listOfAllNeighbours[i][j]


def updateLiveNeighbours():
    for i in range(len(cells2)):
        for j in range(len(cells2[i])):
            cells2[i][j].updateLiveNeighbourCount()

def updateStateOfCells():
    for i in range(len(cells2)):
        for j in range(len(cells2[i])):
            c = cells2[i][j]
            if  c.liveNeighbours < 2:
                c.state = False
            if c.liveNeighbours > 3:
                c.state =False
            if c.state == False and c.liveNeighbours == 3:
                c.state = True

def redrawGameWindow():
    for line in linesList:
        pygame.draw.rect(window, lineColor, line)
    
    for cell in cells:
        cell.draw(window)
    
    text1 = font.render("Paused",1,WHITE)
    text2 = font.render("Playing",1,WHITE)
    text3 = font.render("Building",1,WHITE)
    text4 = font.render("Destroying",1,WHITE)
    textCords = (10,10)
    if spaceBarPressed:
        window.blit(text2, textCords)
    else:
        window.blit(text1, textCords)
        if buildMode:
            window.blit(text3, (10,50))
        else:
            window.blit(text4, (10,50))

    pygame.display.update()

run= True
while run:
    pygame.time.delay(100)

    buttons = pygame.mouse.get_pressed()

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            run = False
        
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_SPACE:
                spaceBarPressed = not(spaceBarPressed)
            if events.key == pygame.K_q:
                run = False
            if events.key == pygame.K_b:
                buildMode = not(buildMode)
        
        if events.type == pygame.MOUSEBUTTONDOWN and not(spaceBarPressed):
            for cel in cells2:
                for ce in cel:
                    buton = ce.button
                    if buton.collidepoint(events.pos):
                        ce.state = not(ce.state)
        
        if buttons[0] and not(spaceBarPressed):
            for cel in cells2:
                for ce in cel:
                    buton = ce.button
                    if buton.collidepoint(events.pos):
                        if buildMode:
                            if ce.state == False:
                                ce.state = not(ce.state)
                        else:
                            if ce.state == True:
                                ce.state = not(ce.state)
        

    updateLiveNeighbours()
    if spaceBarPressed:
        updateStateOfCells()
    redrawGameWindow()

pygame.quit()