import pygame
from pygame import mixer
pygame.init()

mixer.init() 


width = 600

rez = 8

screen = pygame.display.set_mode((width,width))

pygame.display.set_caption('CHESS')


# enbkqbne/pppppppp/////PPPPPPPP/ENBKQBNE

fen_string = "enbkqbne/pppppppp/////PPPPPPPP/ENBKQBNE"

size = int(width/rez)

black_knight = pygame.transform.scale(pygame.image.load('knight.png'),(size,size)).convert_alpha()
white_knight = pygame.transform.scale(pygame.image.load('w-knight.png'),(size,size)).convert_alpha()
black_elephant = pygame.transform.scale(pygame.image.load('elephant.png'),(size,size)).convert_alpha()
white_elephant = pygame.transform.scale(pygame.image.load('w-elephant.png'),(size,size)).convert_alpha()
black_bishop = pygame.transform.scale(pygame.image.load('bishop.png'),(size,size)).convert_alpha()
white_bishop = pygame.transform.scale(pygame.image.load('w-bishop.png'),(size,size)).convert_alpha()
black_pawn = pygame.transform.scale(pygame.image.load('pawn.png'),(size,size)).convert_alpha()
white_pawn = pygame.transform.scale(pygame.image.load('w-pawn.png'),(size,size)).convert_alpha()

black_queen = pygame.transform.scale(pygame.image.load('queen.png'),(size,size)).convert_alpha()
white_queen = pygame.transform.scale(pygame.image.load('w-queen.png'),(size,size)).convert_alpha()

black_king = pygame.transform.scale(pygame.image.load('king.png'),(size,size)).convert_alpha()
white_king = pygame.transform.scale(pygame.image.load('w-king.png'),(size,size)).convert_alpha()

pawns = {
    "n" : [white_knight,'white'],
    'N' : [black_knight,'black'],
    'E' : [black_elephant,'black'],
    'e' : [white_elephant,'white'],
    'P' : [black_pawn,'black'],
    'p' : [white_pawn,'white'],
    'b' : [white_bishop,'white'],
    'B' : [black_bishop,'black'],
    'b' : [white_bishop,'white'],
    'B' : [black_bishop,'black'],
    'b' : [white_bishop,'white'],
    'B' : [black_bishop,'black'],
    'k' : [white_king,'white'],
    'K' : [black_king,'black'],
    'q' : [white_queen,'white'],
    'Q' : [black_queen,'black']

}

color1 = 'sienna'
color2 = 'moccasin'

board = []

def making_board():
    color = color1
    for i in range(rez):
        if color == color1:
            color = color2
        elif color == color2:
            color = color1
        for j in range(rez):
            if color == color2:
                color = color1
            else:
                color = color2
            board.append([i*size,j*size,color])

making_board()

pieces = []

def arranging():
    x = 0
    y = 0
    for i in range(len(fen_string)):
        if fen_string[i] == '/':
            x = 0
            y += 1
        else:
            pieces.append([pawns[fen_string[i]][0],x*size,y*size,pawns[fen_string[i]][1],'notPicked',fen_string[i]])
            x += 1

canCheck = True

globalx = 0
globaly = 0

def dragging(x,y):
    global canCheck,globalx,globaly
    for i in range(len(pieces)):
        if (x < (pieces[i][1] + size) and x > pieces[i][1]) and (y < (pieces[i][2] + size) and y > pieces[i][2]) and pygame.mouse.get_pressed()[0] and canCheck:
            pieces[i][4] = 'canPick'
            globalx = pieces[i][1]
            globaly = pieces[i][2]
            canCheck = False

legalMoves = {
    'p' : [[0,size]],
    'P' : [[0,-size]],
    'n' : [[size,2*size],[-size,2*size],[2*size,size],[-2*size,size],[size,-2*size],[-size,-2*size],[2*size,-size],[-2*size,-size]],
    'N' : [[size,2*size],[-size,2*size],[2*size,size],[-2*size,size],[size,-2*size],[-size,-2*size],[2*size,-size],[-2*size,-size]],

}

def showingLegalmoves():
    global globalx ,globaly
    for i in range(len(pieces)):
        if pieces[i][4] == 'canPick':
            if pieces[i][5] in legalMoves:
                for j in legalMoves[pieces[i][5]]:
                    pygame.draw.rect(screen,'skyblue',(globalx + j[0],globaly + j[1],size,size))

def pickingup():
    for i in range(len(pieces)):
        if i < len(pieces):
            if pieces[i][4] == 'canPick' and pygame.mouse.get_pressed()[0]:
                pieces[i][1] = pygame.mouse.get_pos()[0] - int(size/2)
                pieces[i][2] = pygame.mouse.get_pos()[1] -int(size/2)

def killing(index):
    for j in range(len(pieces)):
        if index < len(pieces) and j < len(pieces):
            if index != j and pieces[j][1] == pieces[index][1] and pieces[j][2] == pieces[index][2] and (pieces[index][3] != pieces[j][3]) and pygame.mouse.get_pressed()[0] == False:
                mixer.music.load('assets_default_capture.mp3')
                mixer.music.set_volume(0.7)
                mixer.music.play()
                pieces.remove(pieces[index])

def adjusting():
    global canCheck
    for i in range(len(pieces)):
        killing(i)
        for j in board:
            if i < len(pieces):
                if pygame.mouse.get_pressed()[0] == False:
                    if (pieces[i][1] + int(size/2) < (j[0] + size) and pieces[i][1] + int(size/2) > j[0]) and (pieces[i][2] + int(size/2) < (j[1] + size) and pieces[i][2] + int(size/2) > j[1]) and (pieces[i][2] != j[1] or (pieces[i][1] != j[0])):
                        mixer.music.load("assets_default_move-self.mp3") 
                        mixer.music.set_volume(0.7) 
                        mixer.music.play()
                        pieces[i][1] = j[0]
                        pieces[i][2] = j[1]
                        pieces[i][4] = 'notPicked'
                        canCheck = True

def debug():
    for i in range(len(pieces)):
        if i < len(pieces):
              pygame.draw.circle(screen,'limegreen',(pieces[i][1] + int(size/2),pieces[i][2] + int(size/2)),3)

def placing():
    for i in pieces:
        screen.blit(i[0],(i[1],i[2]))

def displaying_board():
    for i in range(len(board)):
        pygame.draw.rect(screen,board[i][2],(board[i][0],board[i][1],size,size))

arranging()

mixer.music.load('assets_default_game-start.mp3')
mixer.music.set_volume(0.7)
mixer.music.play()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    displaying_board()
    showingLegalmoves()
    adjusting()
    placing()
    # debug()
    pickingup()
    dragging(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1])
    pygame.display.update()
