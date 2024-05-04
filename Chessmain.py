import Chessengine
import pygame
from pygame import mixer

mixer.init()

WIDHT = HEIGHT = 560
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60
IMAGES = {}

def loadImages():
    IMAGES['wp'] = pygame.transform.smoothscale(pygame.image.load('w-pawn.png'),(SQ_SIZE,SQ_SIZE)).convert_alpha()
    IMAGES['wB'] = pygame.transform.smoothscale(pygame.image.load('w-bishop.png'),(SQ_SIZE,SQ_SIZE)).convert_alpha()
    IMAGES['wR'] = pygame.transform.smoothscale(pygame.image.load('w-elephant.png'),(SQ_SIZE,SQ_SIZE)).convert_alpha()
    IMAGES['wN'] = pygame.transform.smoothscale(pygame.image.load('w-knight.png'),(SQ_SIZE,SQ_SIZE)).convert_alpha()
    IMAGES['wK'] = pygame.transform.smoothscale(pygame.image.load('w-king.png'),(SQ_SIZE,SQ_SIZE)).convert_alpha()
    IMAGES['wQ'] = pygame.transform.smoothscale(pygame.image.load('w-queen.png'),(SQ_SIZE,SQ_SIZE)).convert_alpha()
    IMAGES['bp'] = pygame.transform.smoothscale(pygame.image.load('pawn.png'),(SQ_SIZE,SQ_SIZE)).convert_alpha()
    IMAGES['bB'] = pygame.transform.smoothscale(pygame.image.load('bishop.png'),(SQ_SIZE,SQ_SIZE)).convert_alpha()
    IMAGES['bR'] = pygame.transform.smoothscale(pygame.image.load('elephant.png'),(SQ_SIZE,SQ_SIZE)).convert_alpha()
    IMAGES['bN'] = pygame.transform.smoothscale(pygame.image.load('knight.png'),(SQ_SIZE,SQ_SIZE)).convert_alpha()
    IMAGES['bK'] = pygame.transform.smoothscale(pygame.image.load('king.png'),(SQ_SIZE,SQ_SIZE)).convert_alpha()
    IMAGES['bQ'] = pygame.transform.smoothscale(pygame.image.load('queen.png'),(SQ_SIZE,SQ_SIZE)).convert_alpha()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDHT,HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('white'))
    gs = Chessengine.GameState()
    positionHighlight = (233, 116, 81)
    loadImages()
    mixer.music.load('assets_default_game-start.mp3')
    mixer.music.play()
    holdingPiece = ''
    drawGameState(screen,gs)
    running = True
    sqSelected = () # no square is selected initially its a tuple (row and column)

    playerClicks = [] # keep track of player's clicks
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    sqSelected = ()
                    playerClicks = []
                    holdingPiece = ''
                    gs.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bp','bp','bp','bp','bp','bp','bp','bp'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wp','wp','wp','wp','wp','wp','wp','wp'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR'],
        ]
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0]//SQ_SIZE # to get the column
                row = location[1]//SQ_SIZE # to get the row
                if sqSelected == (row,col): # undo action
                    sqSelected = ()
                    playerClicks = []
                    if gs.board[row][col] == '--':
                        gs.board[row][col] = holdingPiece
                    holdingPiece = ''
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected) # append for both first and second clicks

                if len(playerClicks) == 1:
                    if holdingPiece == '' and gs.board[playerClicks[0][0]][playerClicks[0][1]] != '--':
                        holdingPiece = gs.board[playerClicks[0][0]][playerClicks[0][1]]
                        gs.board[playerClicks[0][0]][playerClicks[0][1]] = '--'

                if len(playerClicks) == 2:
                    validMoves = None
                    if holdingPiece != '--' and holdingPiece != '':
                        if gs.board[playerClicks[1][0]][playerClicks[1][1]][0] != holdingPiece[0]:
                            if gs.board[playerClicks[1][0]][playerClicks[1][1]][0] == 'w' and holdingPiece[0] == 'b' or gs.board[playerClicks[1][0]][playerClicks[1][1]][0] == 'b' and holdingPiece[0] == 'w':
                                mixer.music.load('assets_default_capture.mp3')
                                mixer.music.play()
                            else:
                                mixer.music.load('assets_default_move-self.mp3')
                                mixer.music.play()

                            if holdingPiece == 'wp':
                                validMoves = gs.whitepawnMoves
                            if holdingPiece == 'bp':
                                 validMoves = gs.blackpawnMoves
                            if holdingPiece[1] == 'N':
                                validMoves = gs.knightMoves
                            if holdingPiece[1] == 'R':
                                validMoves = gs.rookMoves
                            if holdingPiece[1] == 'K':
                                validMoves = gs.kingMoves
                            if holdingPiece[1] == 'Q':
                                validMoves = gs.queenMoves
                            if holdingPiece[1] == 'B':
                                validMoves = gs.bishopMoves
                            if holdingPiece[1] == 'Q':
                                validMoves = gs.queenMoves


                            if validMoves != None:
                                validMoveFound = False
                                if validMoves == gs.whitepawnMoves:
                                    if len(playerClicks) == 2:
                                        x1 = playerClicks[0][1]
                                        y1 = playerClicks[0][0]
                                        onepos = (x1 + 1 ,y1 - 1)
                                        secondpos = (x1 - 1, y1 - 1 )
                                        x2 = playerClicks[1][1]
                                        y2 = playerClicks[1][0]
                                        if (onepos[0] == x2 and onepos[1] == y2 and gs.board[y2][x2][0] == 'b') or (secondpos[0] == x2 and secondpos[1] == y2 and gs.board[y2][x2][0] == 'b'):
                                            validMoveFound = True

                                if validMoves == gs.blackpawnMoves:
                                    if len(playerClicks) == 2:
                                        x1 = playerClicks[0][1]
                                        y1 = playerClicks[0][0]
                                        onepos = (x1 + 1 ,y1 + 1)
                                        secondpos = (x1 - 1, y1  + 1)
                                        x2 = playerClicks[1][1]
                                        y2 = playerClicks[1][0]
                                        if (onepos[0] == x2 and onepos[1] == y2 and gs.board[y2][x2][0] == 'w') or (secondpos[0] == x2 and secondpos[1] == y2 and gs.board[y2][x2][0] == 'w'):
                                            validMoveFound = True

                                y1 = playerClicks[0][0]
                                x1 = playerClicks[0][1]
                                y2 = playerClicks[1][0]
                                x2 = playerClicks[1][1]

                                for i in validMoves:
                                    if holdingPiece != 'wp' and holdingPiece !='bp' and holdingPiece != 'wR' and holdingPiece != 'bR':
                                        if x1 + i[0] == x2 and y1 + i[1] == y2:
                                            validMoveFound = True
                                        else:
                                            # gs.board[y1][x1] = holdingPiece
                                            continue

                                if holdingPiece == 'bQ':
                                    moves = []

                                    for i in range(1,x1 + 1):
                                        if gs.board[y1][x1 - i] == '--':
                                            moves.append([x1 - i,y1])
                                        elif gs.board[y1][x1 - i][0] == 'w':
                                            moves.append([x1 - i,y1])
                                            break
                                        else:
                                            break

                                    for j in range(x1 + 1,8):
                                        if gs.board[y1][j] == '--':
                                            moves.append([j,y1])
                                        elif gs.board[y1][j][0] == 'w':
                                            moves.append([j,y1])
                                            break
                                        else:
                                            break

                                    for k in range(1,y1 + 1):
                                        if gs.board[y1 - k][x1] == '--':
                                            moves.append([x1,y1 - k])
                                        elif gs.board[y1 - k][x1][0] == 'w':
                                            moves.append([x1,y1 - k])
                                            break
                                        else:
                                            break

                                    for l in range(y1 + 1,8):
                                        if gs.board[l][x1] == '--':
                                            moves.append([x1,l])
                                        elif gs.board[l][x1][0] == 'w':
                                            moves.append([x1,l])
                                            break
                                        else:
                                            break

                                    for o in range(1,y1 + 1):
                                        if gs.board[y1 - o][x1 - o] == '--':
                                            moves.append([x1 - o,y1 - o])
                                        elif gs.board[y1 - o][x1 - o][0] == 'w' :
                                            moves.append([x1 - o,y1 - o])
                                            break
                                        else:
                                            break

                                    for m in range(1,y1 + 1):
                                        if x1 + m < len(gs.board[0]):
                                            if gs.board[y1 - m][x1 + m] == '--':
                                                moves.append([x1 + m,y1 - m])
                                            elif gs.board[y1 - m][x1 + m][0] == 'w' :
                                                moves.append([x1 + m,y1 - m])
                                                break
                                            else:
                                                break

                                    for n in range(y1 + 1,8):
                                        if gs.board[n][x1 - (n-y1)] == '--':
                                            moves.append([x1 - (n-y1),n])
                                        elif gs.board[n][x1 - (n-y1)][0] == 'w':
                                            moves.append([x1 - (n-y1),n])
                                            break
                                        else:
                                            break

                                    for g in range(y1 + 1,8):
                                        if x1 + (g-y1) < len(gs.board[0]):
                                            if gs.board[g][x1 + (g-y1)] == '--':
                                                moves.append([x1 + (g-y1),g])
                                            elif gs.board[g][x1 + (g-y1)][0] == 'w':
                                                moves.append([x1 + (g-y1),g])
                                                break
                                            else:
                                                break

                                    for move in moves:
                                        if x2 == move[0] and y2 == move[1]:
                                            validMoveFound = True

                                if holdingPiece == 'wQ':
                                    moves = []

                                    for i in range(1,x1 + 1):
                                        if gs.board[y1][x1 - i] == '--':
                                            moves.append([x1 - i,y1])
                                        elif gs.board[y1][x1 - i][0] == 'b':
                                            moves.append([x1 - i,y1])
                                            break
                                        else:
                                            break

                                    for j in range(x1 + 1,8):
                                        if gs.board[y1][j] == '--':
                                            moves.append([j,y1])
                                        elif gs.board[y1][j][0] == 'b':
                                            moves.append([j,y1])
                                            break
                                        else:
                                            break

                                    for k in range(1,y1 + 1):
                                        if gs.board[y1 - k][x1] == '--':
                                            moves.append([x1,y1 - k])
                                        elif gs.board[y1 - k][x1][0] == 'b':
                                            moves.append([x1,y1 - k])
                                            break
                                        else:
                                            break

                                    for l in range(y1 + 1,8):
                                        if gs.board[l][x1] == '--':
                                            moves.append([x1,l])
                                        elif gs.board[l][x1][0] == 'b':
                                            moves.append([x1,l])
                                            break
                                        else:
                                            break

                                    for o in range(1,y1 + 1):
                                        if gs.board[y1 - o][x1 - o] == '--':
                                            moves.append([x1 - o,y1 - o])
                                        elif gs.board[y1 - o][x1 - o][0] == 'b' :
                                            moves.append([x1 - o,y1 - o])
                                            break
                                        else:
                                            break

                                    for m in range(1,y1 + 1):
                                        if x1 + m < len(gs.board[0]):
                                            if gs.board[y1 - m][x1 + m] == '--':
                                                moves.append([x1 + m,y1 - m])
                                            elif gs.board[y1 - m][x1 + m][0] == 'b' :
                                                moves.append([x1 + m,y1 - m])
                                                break
                                            else:
                                                break

                                    for n in range(y1 + 1,8):
                                        if gs.board[n][x1 - (n-y1)] == '--':
                                            moves.append([x1 - (n-y1),n])
                                        elif gs.board[n][x1 - (n-y1)][0] == 'b':
                                            moves.append([x1 - (n-y1),n])
                                            break
                                        else:
                                            break

                                    for g in range(y1 + 1,8):
                                        if x1 + (g-y1) < len(gs.board[0]):
                                            if gs.board[g][x1 + (g-y1)] == '--':
                                                moves.append([x1 + (g-y1),g])
                                            elif gs.board[g][x1 + (g-y1)][0] == 'b':
                                                moves.append([x1 + (g-y1),g])
                                                break
                                            else:
                                                break

                                    for move in moves:
                                        if x2 == move[0] and y2 == move[1]:
                                            validMoveFound = True
                                
                                if len(holdingPiece) > 0 and holdingPiece == 'wB':
                                    moves = []
                             
                                    for k in range(1,y1 + 1):
                                        if gs.board[y1 - k][x1 - k] == '--':
                                            moves.append([x1 - k,y1 - k])
                                        elif gs.board[y1 - k][x1 - k][0] == 'b' :
                                            moves.append([x1 - k,y1 - k])
                                            break
                                        else:
                                            break

                                    for m in range(1,y1 + 1):
                                        if x1 + m < len(gs.board[0]):
                                            if gs.board[y1 - m][x1 + m] == '--':
                                                moves.append([x1 + m,y1 - m])
                                            elif gs.board[y1 - m][x1 + m][0] == 'b' :
                                                moves.append([x1 + m,y1 - m])
                                                break
                                            else:
                                                break

                                    for l in range(y1 + 1,8):
                                        if gs.board[l][x1 - (l-y1)] == '--':
                                            moves.append([x1 - (l-y1),l])
                                        elif gs.board[l][x1 - (l-y1)][0] == 'b':
                                            moves.append([x1 - (l-y1),l])
                                            break
                                        else:
                                            break

                                    for g in range(y1 + 1,8):
                                        if x1 + (g-y1) < len(gs.board[0]):
                                            if gs.board[g][x1 + (g-y1)] == '--':
                                                moves.append([x1 + (g-y1),g])
                                            elif gs.board[g][x1 + (g-y1)][0] == 'b':
                                                moves.append([x1 + (g-y1),g])
                                                break
                                            else:
                                                break

                                    for move in moves:
                                        if x2 == move[0] and y2 == move[1]:
                                            validMoveFound = True

                                if len(holdingPiece) > 0 and holdingPiece == 'bB':
                                    moves = []
                             
                                    for k in range(1,y1 + 1):
                                        if gs.board[y1 - k][x1 - k] == '--':
                                            moves.append([x1 - k,y1 - k])
                                        elif gs.board[y1 - k][x1 - k][0] == 'w' :
                                            moves.append([x1 - k,y1 - k])
                                            break
                                        else:
                                            break

                                    for m in range(1,y1 + 1):
                                        if x1 + m < len(gs.board[0]):
                                            if gs.board[y1 - m][x1 + m] == '--':
                                                moves.append([x1 + m,y1 - m])
                                            elif gs.board[y1 - m][x1 + m][0] == 'w' :
                                                moves.append([x1 + m,y1 - m])
                                                break
                                            else:
                                                break

                                    for l in range(y1 + 1,8):
                                        if gs.board[l][x1 - (l-y1)] == '--':
                                            moves.append([x1 - (l-y1),l])
                                        elif gs.board[l][x1 - (l-y1)][0] == 'w':
                                            moves.append([x1 - (l-y1),l])
                                            break
                                        else:
                                            break

                                    for g in range(y1 + 1,8):
                                        if x1 + (g-y1) < len(gs.board[0]):
                                            if gs.board[g][x1 + (g-y1)] == '--':
                                                moves.append([x1 + (g-y1),g])
                                            elif gs.board[g][x1 + (g-y1)][0] == 'w':
                                                moves.append([x1 + (g-y1),g])
                                                break
                                            else:
                                                break

                                    for move in moves:
                                        if x2 == move[0] and y2 == move[1]:
                                            validMoveFound = True

                                if holdingPiece == 'wR':
                                    moves = []
                                    for i in range(1,x1 + 1):
                                        if gs.board[y1][x1 - i] == '--':
                                            moves.append([x1 - i,y1])
                                        elif gs.board[y1][x1 - i][0] == 'b':
                                            moves.append([x1 - i,y1])
                                            break
                                        else:
                                            break

                                    for j in range(x1 + 1,8):
                                        if gs.board[y1][j] == '--':
                                            moves.append([j,y1])
                                        elif gs.board[y1][j][0] == 'b':
                                            moves.append([j,y1])
                                            break
                                        else:
                                            break

                                    for k in range(1,y1 + 1):
                                        if gs.board[y1 - k][x1] == '--':
                                            moves.append([x1,y1 - k])
                                        elif gs.board[y1 - k][x1][0] == 'b':
                                            moves.append([x1,y1 - k])
                                            break
                                        else:
                                            break

                                    for l in range(y1 + 1,8):
                                        if gs.board[l][x1] == '--':
                                            moves.append([x1,l])
                                        elif gs.board[l][x1][0] == 'b':
                                            moves.append([x1,l])
                                            break
                                        else:
                                            break

                                    for move in moves:
                                        if x2 == move[0] and y2 == move[1]:
                                            validMoveFound = True

                                if holdingPiece == 'bR':
                                    moves = []
                                    for i in range(1,x1 + 1):
                                        if gs.board[y1][x1 - i] == '--':
                                            moves.append([x1 - i,y1])
                                        elif gs.board[y1][x1 - i][0] == 'w':
                                            moves.append([x1 - i,y1])
                                            break
                                        else:
                                            break

                                    for j in range(x1 + 1,8):
                                        if gs.board[y1][j] == '--':
                                            moves.append([j,y1])
                                        elif gs.board[y1][j][0] == 'w':
                                            moves.append([j,y1])
                                            break
                                        else:
                                            break

                                    for k in range(1,y1 + 1):
                                        if gs.board[y1 - k][x1] == '--':
                                            moves.append([x1,y1 - k])
                                        elif gs.board[y1 - k][x1][0] == 'w':
                                            moves.append([x1,y1 - k])
                                            break
                                        else:
                                            break

                                    for l in range(y1 + 1,8):
                                        if gs.board[l][x1] == '--':
                                            moves.append([x1,l])
                                        elif gs.board[l][x1][0] == 'w':
                                            moves.append([x1,l])
                                            break
                                        else:
                                            break

                                    for move in moves:
                                        if x2 == move[0] and y2 == move[1]:
                                            validMoveFound = True

                                # Bishop here

                                

                                if holdingPiece == 'wp':
                                    moves = []
                                    end = 3
                                    if y1 < 6:
                                        end = 2
                                    for i in range(1,end):
                                        if gs.board[y1 - i][x1] == '--':
                                            moves.append([x1,y1-i])
                                        else:
                                            break

                                    for move in moves:
                                        if x2 == move[0] and y2 == move[1]:
                                            validMoveFound = True
                                           
                                

                                if holdingPiece == 'bp':
                                    moves = []
                                    end = 3
                                    if y1 > 1:
                                        end = 2
                                    for i in range(1,end):
                                        if y1 + i < len(gs.board) and gs.board[y1 + i][x1] == '--':
                                            moves.append([x1,y1+i])
                                        else:
                                            break
                                  

                                    for move in moves:
                                        if x2 == move[0] and y2 == move[1]:
                                            validMoveFound = True
                                  

                                if validMoveFound:
                                    gs.board[playerClicks[1][0]][playerClicks[1][1]] = holdingPiece
                                else:
                                    mixer.music.load('illegal.mp3')
                                    mixer.music.play()
                                    gs.board[playerClicks[0][0]][playerClicks[0][1]] = holdingPiece
                                    holdingPiece = ''
                                    playerClicks = []
                                    sqSelected = ()
                           
                            else:
                                gs.board[playerClicks[1][0]][playerClicks[1][1]] = holdingPiece

                        else:
                            mixer.music.load('illegal.mp3')
                            mixer.music.play()
                            gs.board[playerClicks[0][0]][playerClicks[0][1]] = holdingPiece

                    playerClicks = []
                    sqSelected = ()
                    holdingPiece = ''



        # the loop and the printing stuff going on here 

        drawGameState(screen,gs)
        if len(playerClicks) > 0:
            for i in playerClicks:
                pygame.draw.rect(screen,'skyblue',(i[1] * SQ_SIZE,i[0] * SQ_SIZE,SQ_SIZE,SQ_SIZE))

        if holdingPiece != '' or '--' and len(playerClicks) == 1:
            if len(holdingPiece) > 0 and holdingPiece[1] == 'N':
                x = sqSelected[1]
                y = sqSelected[0]
                for i in range(len(gs.knightMoves)):
                    if y + gs.knightMoves[i][0] <= len(gs.board) - 1:
                        if x + gs.knightMoves[i][1] <= len(gs.board[y + gs.knightMoves[i][0]]) - 1:
                            if gs.board[y + gs.knightMoves[i][0]][x + gs.knightMoves[i][1]][0] != holdingPiece[0]:
                                if gs.board[y + gs.knightMoves[i][0]][x + gs.knightMoves[i][1]] == '--':
                                    pygame.draw.rect(screen,positionHighlight,((x + gs.knightMoves[i][1]) * SQ_SIZE,(y + gs.knightMoves[i][0]) * SQ_SIZE,SQ_SIZE,SQ_SIZE))
                                elif  gs.board[y + gs.knightMoves[i][0]][x + gs.knightMoves[i][1]] != '--':
                                    pygame.draw.circle(screen,positionHighlight,((x + gs.knightMoves[i][1]) * SQ_SIZE + (SQ_SIZE//2),(y + gs.knightMoves[i][0]) * SQ_SIZE + (SQ_SIZE//2)),SQ_SIZE//2,5)

            if len(holdingPiece) > 0 and holdingPiece[1] == 'K':
                x = sqSelected[1]
                y = sqSelected[0]
                for i in range(len(gs.kingMoves)):
                    if y + gs.kingMoves[i][0] <= len(gs.board) - 1:
                        if x + gs.kingMoves[i][1] <= len(gs.board[y + gs.kingMoves[i][0]]) - 1:
                            if gs.board[y + gs.kingMoves[i][0]][x + gs.kingMoves[i][1]][0] != holdingPiece[0]:
                                if gs.board[y + gs.kingMoves[i][0]][x + gs.kingMoves[i][1]] == '--':
                                    pygame.draw.rect(screen,positionHighlight,((x + gs.kingMoves[i][1]) * SQ_SIZE,(y + gs.kingMoves[i][0]) * SQ_SIZE,SQ_SIZE,SQ_SIZE))
                                elif  gs.board[y + gs.kingMoves[i][0]][x + gs.kingMoves[i][1]] != '--':
                                    pygame.draw.circle(screen,positionHighlight,((x + gs.kingMoves[i][1]) * SQ_SIZE + (SQ_SIZE//2),(y + gs.kingMoves[i][0]) * SQ_SIZE + (SQ_SIZE//2)),SQ_SIZE//2,5)
                                
            if len(holdingPiece) > 0 and holdingPiece == 'wp':
                x = sqSelected[1]
                y = sqSelected[0]
                pos1 = (x - 1,y - 1)
                pos2 = (x + 1, y - 1)
                if pos1[1] < len(gs.board):
                        if pos1[0] < len(gs.board[pos1[1]]):
                            if gs.board[pos1[1]][pos1[0]][0] == 'b' :
                                pygame.draw.rect(screen,'limegreen',(pos1[0] * SQ_SIZE,pos1[1] * SQ_SIZE,SQ_SIZE,SQ_SIZE))
                if pos2[1] < len(gs.board):
                        if pos2[0] < len(gs.board[pos2[1]]):
                            if gs.board[pos2[1]][pos2[0]][0] == 'b' :
                                pygame.draw.rect(screen,'limegreen',(pos2[0] * SQ_SIZE,pos2[1] * SQ_SIZE,SQ_SIZE,SQ_SIZE))
                movesWhite = []
                endWhite = 3
                if y < 6:
                    endWhite = 2
                for i in range(1,endWhite):
                    if gs.board[y - i][x] == '--':
                        movesWhite.append([x,y-i])
                    else:
                        break

                for move in movesWhite:
                        pygame.draw.rect(screen,positionHighlight,(move[0] * SQ_SIZE,move[1] * SQ_SIZE,SQ_SIZE,SQ_SIZE))

            if holdingPiece == 'wQ':
                moves = []

                x1 = sqSelected[1]
                y1 = sqSelected[0]

                for i in range(1,x1 + 1):
                    if gs.board[y1][x1 - i] == '--':
                        moves.append([x1 - i,y1])
                    elif gs.board[y1][x1 - i][0] == 'b':
                        moves.append([x1 - i,y1])
                        break
                    else:
                        break

                for j in range(x1 + 1,8):
                    if gs.board[y1][j] == '--':
                        moves.append([j,y1])
                    elif gs.board[y1][j][0] == 'b':
                        moves.append([j,y1])
                        break
                    else:
                        break

                for k in range(1,y1 + 1):
                    if gs.board[y1 - k][x1] == '--':
                        moves.append([x1,y1 - k])
                    elif gs.board[y1 - k][x1][0] == 'b':
                        moves.append([x1,y1 - k])
                        break
                    else:
                        break

                for l in range(y1 + 1,8):
                    if gs.board[l][x1] == '--':
                        moves.append([x1,l])
                    elif gs.board[l][x1][0] == 'b':
                        moves.append([x1,l])
                        break
                    else:
                        break

                for o in range(1,y1 + 1):
                    if gs.board[y1 - o][x1 - o] == '--':
                        moves.append([x1 - o,y1 - o])
                    elif gs.board[y1 - o][x1 - o][0] == 'b' :
                        moves.append([x1 - o,y1 - o])
                        break
                    else:
                        break

                for m in range(1,y1 + 1):
                    if x1 + m < len(gs.board[0]):
                        if gs.board[y1 - m][x1 + m] == '--':
                            moves.append([x1 + m,y1 - m])
                        elif gs.board[y1 - m][x1 + m][0] == 'b' :
                            moves.append([x1 + m,y1 - m])
                            break
                        else:
                            break

                for n in range(y1 + 1,8):
                    if gs.board[n][x1 - (n-y1)] == '--':
                        moves.append([x1 - (n-y1),n])
                    elif gs.board[n][x1 - (n-y1)][0] == 'b':
                        moves.append([x1 - (n-y1),n])
                        break
                    else:
                        break

                for g in range(y1 + 1,8):
                    if x1 + (g-y1) < len(gs.board[0]):
                        if gs.board[g][x1 + (g-y1)] == '--':
                            moves.append([x1 + (g-y1),g])
                        elif gs.board[g][x1 + (g-y1)][0] == 'b':
                            moves.append([x1 + (g-y1),g])
                            break
                        else:
                            break

                for move in moves:
                    pygame.draw.rect(screen,positionHighlight,(move[0] * SQ_SIZE,move[1] * SQ_SIZE,SQ_SIZE,SQ_SIZE))

            if holdingPiece == 'bQ':
                moves = []

                x1 = sqSelected[1]
                y1 = sqSelected[0]

                for i in range(1,x1 + 1):
                    if gs.board[y1][x1 - i] == '--':
                        moves.append([x1 - i,y1])
                    elif gs.board[y1][x1 - i][0] == 'w':
                        moves.append([x1 - i,y1])
                        break
                    else:
                        break

                for j in range(x1 + 1,8):
                    if gs.board[y1][j] == '--':
                        moves.append([j,y1])
                    elif gs.board[y1][j][0] == 'w':
                        moves.append([j,y1])
                        break
                    else:
                        break

                for k in range(1,y1 + 1):
                    if gs.board[y1 - k][x1] == '--':
                        moves.append([x1,y1 - k])
                    elif gs.board[y1 - k][x1][0] == 'w':
                        moves.append([x1,y1 - k])
                        break
                    else:
                        break

                for l in range(y1 + 1,8):
                    if gs.board[l][x1] == '--':
                        moves.append([x1,l])
                    elif gs.board[l][x1][0] == 'w':
                        moves.append([x1,l])
                        break
                    else:
                        break

                for o in range(1,y1 + 1):
                    if gs.board[y1 - o][x1 - o] == '--':
                        moves.append([x1 - o,y1 - o])
                    elif gs.board[y1 - o][x1 - o][0] == 'w' :
                        moves.append([x1 - o,y1 - o])
                        break
                    else:
                        break

                for m in range(1,y1 + 1):
                    if x1 + m < len(gs.board[0]):
                        if gs.board[y1 - m][x1 + m] == '--':
                            moves.append([x1 + m,y1 - m])
                        elif gs.board[y1 - m][x1 + m][0] == 'w' :
                            moves.append([x1 + m,y1 - m])
                            break
                        else:
                            break

                for n in range(y1 + 1,8):
                    if gs.board[n][x1 - (n-y1)] == '--':
                        moves.append([x1 - (n-y1),n])
                    elif gs.board[n][x1 - (n-y1)][0] == 'w':
                        moves.append([x1 - (n-y1),n])
                        break
                    else:
                        break

                for g in range(y1 + 1,8):
                    if x1 + (g-y1) < len(gs.board[0]):
                        if gs.board[g][x1 + (g-y1)] == '--':
                            moves.append([x1 + (g-y1),g])
                        elif gs.board[g][x1 + (g-y1)][0] == 'w':
                            moves.append([x1 + (g-y1),g])
                            break
                        else:
                            break

                for move in moves:
                    pygame.draw.rect(screen,positionHighlight,(move[0] * SQ_SIZE,move[1] * SQ_SIZE,SQ_SIZE,SQ_SIZE))

            if len(holdingPiece) > 0 and holdingPiece == 'wR':
                moves = []
                x1 = sqSelected[1]
                y1 = sqSelected[0]
                for i in range(1,x1 + 1):
                    if gs.board[y1][x1 - i] == '--':
                        moves.append([x1 - i,y1])
                    elif gs.board[y1][x1 - i][0] == 'b':
                        moves.append([x1 - i,y1])
                        break
                    else:
                        break

                for j in range(x1 + 1,8):
                    if gs.board[y1][j] == '--':
                        moves.append([j,y1])
                    elif gs.board[y1][j][0] == 'b':
                        moves.append([j,y1])
                        break
                    else:
                        break

                for k in range(1,y1 + 1):
                    if gs.board[y1 - k][x1] == '--':
                        moves.append([x1,y1 - k])
                    elif gs.board[y1 - k][x1][0] == 'b':
                        moves.append([x1,y1 - k])
                        break
                    else:
                        break

                for l in range(y1 + 1,8):
                    if gs.board[l][x1] == '--':
                        moves.append([x1,l])
                    elif gs.board[l][x1][0] == 'b':
                        moves.append([x1,l])
                        break
                    else:
                        break

                for move in moves:
                    if gs.board[move[1]][move[0]] == '--':
                        pygame.draw.rect(screen,positionHighlight,(move[0] * SQ_SIZE,move[1] * SQ_SIZE,SQ_SIZE,SQ_SIZE))
                    else:
                        pygame.draw.rect(screen,(255,0,0,0),(move[0] * SQ_SIZE,move[1] * SQ_SIZE,SQ_SIZE,SQ_SIZE))
            
            if len(holdingPiece) > 0 and holdingPiece == 'bR':
                moves = []
                x1 = sqSelected[1]
                y1 = sqSelected[0]
                for i in range(1,x1 + 1):
                    if gs.board[y1][x1 - i] == '--':
                        moves.append([x1 - i,y1])
                    elif gs.board[y1][x1 - i][0] == 'w':
                        moves.append([x1 - i,y1])
                        break
                    else:
                        break

                for j in range(x1 + 1,8):
                    if gs.board[y1][j] == '--':
                        moves.append([j,y1])
                    elif gs.board[y1][j][0] == 'w':
                        moves.append([j,y1])
                        break
                    else:
                        break

                for k in range(1,y1 + 1):
                    if gs.board[y1 - k][x1] == '--':
                        moves.append([x1,y1 - k])
                    elif gs.board[y1 - k][x1][0] == 'w':
                        moves.append([x1,y1 - k])
                        break
                    else:
                        break

                for l in range(y1 + 1,8):
                    if gs.board[l][x1] == '--':
                        moves.append([x1,l])
                    elif gs.board[l][x1][0] == 'w':
                        moves.append([x1,l])
                        break
                    else:
                        break

                for move in moves:
                    if gs.board[move[1]][move[0]] == '--':
                        pygame.draw.rect(screen,positionHighlight,(move[0] * SQ_SIZE,move[1] * SQ_SIZE,SQ_SIZE,SQ_SIZE))
                    else:
                        pygame.draw.rect(screen,(255,0,0,0),(move[0] * SQ_SIZE,move[1] * SQ_SIZE,SQ_SIZE,SQ_SIZE))

            if len(holdingPiece) > 0 and holdingPiece == 'bB':
                moves = []
                x1 = sqSelected[1]
                y1 = sqSelected[0]
                for k in range(1,y1 + 1):
                    if gs.board[y1 - k][x1 - k] == '--':
                        moves.append([x1 - k,y1 - k])
                    elif gs.board[y1 - k][x1 - k][0] == 'w' :
                        moves.append([x1 - k,y1 - k])
                        break
                    else:
                        break

                for m in range(1,y1 + 1):
                    if x1 + m < len(gs.board[0]):
                        if gs.board[y1 - m][x1 + m] == '--':
                            moves.append([x1 + m,y1 - m])
                        elif gs.board[y1 - m][x1 + m][0] == 'w' :
                            moves.append([x1 + m,y1 - m])
                            break
                        else:
                            break

                for l in range(y1 + 1,8):
                    if gs.board[l][x1 - (l-y1)] == '--':
                        moves.append([x1 - (l-y1),l])
                    elif gs.board[l][x1 - (l-y1)][0] == 'w':
                        moves.append([x1 - (l-y1),l])
                        break
                    else:
                        break

                for g in range(y1 + 1,8):
                    if x1 + (g-y1) < len(gs.board[0]):
                        if gs.board[g][x1 + (g-y1)] == '--':
                            moves.append([x1 + (g-y1),g])
                        elif gs.board[g][x1 + (g-y1)][0] == 'w':
                            moves.append([x1 + (g-y1),g])
                            break
                        else:
                            break

                for move in moves:
                    pygame.draw.rect(screen,positionHighlight,(move[0] * SQ_SIZE,move[1] * SQ_SIZE,SQ_SIZE,SQ_SIZE))

            if len(holdingPiece) > 0 and holdingPiece == 'wB':
                moves = []
                x1 = sqSelected[1]
                y1 = sqSelected[0]
                for k in range(1,y1 + 1):
                    if gs.board[y1 - k][x1 - k] == '--':
                        moves.append([x1 - k,y1 - k])
                    elif gs.board[y1 - k][x1 - k][0] == 'b' :
                        moves.append([x1 - k,y1 - k])
                        break
                    else:
                        break

                for m in range(1,y1 + 1):
                    if x1 + m < len(gs.board[0]):
                        if gs.board[y1 - m][x1 + m] == '--':
                            moves.append([x1 + m,y1 - m])
                        elif gs.board[y1 - m][x1 + m][0] == 'b' :
                            moves.append([x1 + m,y1 - m])
                            break
                        else:
                            break

                for l in range(y1 + 1,8):
                    if gs.board[l][x1 - (l-y1)] == '--':
                        moves.append([x1 - (l-y1),l])
                    elif gs.board[l][x1 - (l-y1)][0] == 'b':
                        moves.append([x1 - (l-y1),l])
                        break
                    else:
                        break

                for g in range(y1 + 1,8):
                    if x1 + (g-y1) < len(gs.board[0]):
                        if gs.board[g][x1 + (g-y1)] == '--':
                            moves.append([x1 + (g-y1),g])
                        elif gs.board[g][x1 + (g-y1)][0] == 'b':
                            moves.append([x1 + (g-y1),g])
                            break
                        else:
                            break

                for move in moves:
                    pygame.draw.rect(screen,positionHighlight,(move[0] * SQ_SIZE,move[1] * SQ_SIZE,SQ_SIZE,SQ_SIZE))

            if len(holdingPiece) > 0 and holdingPiece == 'bp':
                x = sqSelected[1]
                y = sqSelected[0]
                pos1 = (x - 1,y + 1)
                pos2 = (x + 1, y + 1)
                if pos1[1] < len(gs.board):
                        if pos1[0] < len(gs.board[pos1[1]]):
                            if gs.board[pos1[1]][pos1[0]][0] == 'w' :
                                pygame.draw.rect(screen,'limegreen',(pos1[0] * SQ_SIZE,pos1[1] * SQ_SIZE,SQ_SIZE,SQ_SIZE))
                if pos2[1] < len(gs.board):
                        if pos2[0] < len(gs.board[pos2[1]]):
                            if gs.board[pos2[1]][pos2[0]][0] == 'w' :
                                pygame.draw.rect(screen,'limegreen',(pos2[0] * SQ_SIZE,pos2[1] * SQ_SIZE,SQ_SIZE,SQ_SIZE))
                movesBlack = []
                endBlack = 3
                if y > 1:
                    endBlack = 2
                for i in range(1,endBlack):
                    if y + i < len(gs.board):
                        if gs.board[y + i][x] == '--':
                            movesBlack.append([x,y+i])
                        else:
                            break

                for move in movesBlack:
                        pygame.draw.rect(screen,positionHighlight,(move[0] * SQ_SIZE,move[1] * SQ_SIZE,SQ_SIZE,SQ_SIZE))
            

        scaleFactor = 1.375
        if holdingPiece != '':
                screen.blit(pygame.transform.smoothscale(IMAGES[holdingPiece].convert_alpha(),(SQ_SIZE * scaleFactor,SQ_SIZE * scaleFactor)),(pygame.mouse.get_pos()[0] - (SQ_SIZE * scaleFactor//2),pygame.mouse.get_pos()[1] - (SQ_SIZE * scaleFactor//2)))

        clock.tick(MAX_FPS)

        pygame.display.update()

def drawBoard(screen):
    colors = [(149,69,53),(242,210,189)]

    for i in range(DIMENSION):

        for j in range(DIMENSION):

            if (i+j) % 2 == 0:
                pygame.draw.rect(screen,colors[0],(SQ_SIZE*i,SQ_SIZE*j,SQ_SIZE,SQ_SIZE))
            else:
                pygame.draw.rect(screen,colors[1],(SQ_SIZE*i,SQ_SIZE*j,SQ_SIZE,SQ_SIZE))

def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--' and piece != '':
                screen.blit(IMAGES[piece],(c*SQ_SIZE,r*SQ_SIZE))


def drawGameState(screen,gs):
    drawBoard(screen) # draw the squares
    # can add more functions for piece highlighting and all
    drawPieces(screen,gs.board) # draws the pieces 

if __name__ == "__main__":
    main()
    
