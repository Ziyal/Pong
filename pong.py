import pygame, sys, os
from pygame.locals import * 

# Changing this value speeds up or slows down the game
FPS = 200

# Global variables
WINDOWWIDTH = 800
WINDOWHEIGHT = 500
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20

# Game colors
BLACK = (0,0,0)
WHITE = (255,255,255)

# Creates the arena/borders
def drawArena():
    DISPLAYSURF.fill((0,0,0))
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2),0),((WINDOWWIDTH/2),WINDOWHEIGHT), (LINETHICKNESS/4))

# Creates paddles
def drawPaddle(paddle):
    if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
        paddle.bottom = WINDOWHEIGHT - LINETHICKNESS
    elif paddle.top < LINETHICKNESS:
        paddle.top = LINETHICKNESS

    pygame.draw.rect(DISPLAYSURF, WHITE, paddle)

def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)

def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1
    if ball.left == (LINETHICKNESS) or ball.right == (WINDOWWIDTH - LINETHICKNESS):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY

def checkPoints(paddle1, ball, score, ballDirX):
    # When left wall is hit
    if ball.left == LINETHICKNESS: 
        return 0
    elif ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        score += 1
        return score
    elif ball.right == WINDOWWIDTH - LINETHICKNESS:
        score += 5
        return score
    else:
        return score
    
def computerPlayer(ball, ballDirX, paddle2):
    if ballDirX == -1:
        if paddle2.centery < (WINDOWHEIGHT/2):
            paddle2.y += 1
        elif paddle2.centery > (WINDOWHEIGHT/2):
            paddle2.y -=1
    elif ballDirX == 1:
        if paddle2.centery < ball.centery:
            paddle2.y += 1
        else:
            paddle2.y -= 1
    return paddle2

def checkHitBall(ball, paddle1, paddle2, ballDirX):
    if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
        return -1
    elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
        return -1
    else:
         return 1


def displayScore(score):
    resultSurf = BASICFONT.render('Score: %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 150, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)

def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    global DISPLAYSURF, BASICFONT
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption("Pong")

    # Creates balls
    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2

    # Creates player paddles
    playerOne = (WINDOWHEIGHT - PADDLESIZE)/2
    playerTwo = (WINDOWHEIGHT - PADDLESIZE)/2
    
    # Balls direction
    ballDirX = -1
    ballDirY = -1

    # Score
    score = 0

    # Draws movie parts (paddles and ball)
    paddle1 = pygame.Rect(PADDLEOFFSET, playerOne, LINETHICKNESS, PADDLESIZE)
    paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, playerTwo, LINETHICKNESS, PADDLESIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    # Draws starting point
    drawArena()
    drawPaddle(paddle1)
    drawPaddle(paddle2)
    drawBall(ball)

    pygame.mouse.set_visible(0)

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                paddle1.y = mousey
                
        drawArena()
        drawPaddle(paddle1)
        drawPaddle(paddle2)
        drawBall(ball)

        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        score = checkPoints(paddle1, ball, score, ballDirX)
        ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)
        paddle2 = computerPlayer(ball, ballDirX, paddle2)

        displayScore(score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()