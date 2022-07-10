import pygame
from network import Network
import pickle
pygame.font.init()

width = 700
height = 700

WHITE = (255,255,255)
BALCK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
GRAY = (128,128,128)
LIGHT_BLUE = (0, 255,255)


WIDTH, HEIGHT = 700, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")

class Button:
    def __init__(self, text, x , y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, WHITE)
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if (self.x <= x1 <= self.x + self.width) and (self.y <= y1 <= self.y + self.height):
            return True
        else:
            return False
            
def drawGameResults(win, game,  p):
        font = pygame.font.SysFont("comicsans", 30)

        if p == 0:
            wins = font.render(str(game.wins[0]), 1, BALCK)
            ties = font.render(str(game.ties), 1, BALCK)
            losses = font.render(str(game.wins[1]), 1, BALCK)
        else:
            wins = font.render(str(game.wins[1]), 1, BALCK)
            ties = font.render(str(game.ties), 1, BALCK)
            losses = font.render(str(game.wins[0]), 1, BALCK)

        text = font.render("wins:", 1, BALCK)
        win.blit(text, (50, 100))
        win.blit(wins, (text.get_width() + 60, 100))
        text = font.render("ties:", 1, BALCK)
        win.blit(text, (200, 100))
        win.blit(ties, (text.get_width() + 210, 100))
        text = font.render("losses:", 1, BALCK)
        win.blit(text, (350, 100))
        win.blit(losses, (text.get_width() + 360, 100))


def redrawWindow(win, game, p):
    win.fill(GRAY)
    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, RED, True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, LIGHT_BLUE)
        win.blit(text, (50, 200))

        text = font.render("Opponents", 1, LIGHT_BLUE)
        win.blit(text, (390, 200))

        drawGameResults(win, game, p)

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 50, 500, BALCK), Button("Scissors", 250, 500, RED), Button("Paper", 450, 500, GREEN)]
def main():
    run = True
    n = Network()
    clock = pygame.time.Clock()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
                game = n.send("win")
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
                game = n.send("tie")
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))
                game = n.send("get")

            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, RED)
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

if __name__ == "__main__":
    while True:
        menu_screen()
