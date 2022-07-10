import socket
from _thread import *
import pickle
from game import Game


RED = (255, 0 , 0)
BLUE = (0, 0, 255)

server = socket.gethostbyname(socket.gethostname())
port = 5555

FORMAT = "utf-8"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen()
print("Waiting for a connection, Server Started")


connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data == 'win':
                        game.wins[p] += 1
                    elif data == "tie":
                        if p == 0:
                            game.ties += 1
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn ,addr = s.accept()
    print("Connected to:", addr)
    
    idCount += 1
    gameId = (idCount - 1)//2
    p = 0

    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        p = 1
        games[gameId].ready = True

    start_new_thread(threaded_client, (conn, p, gameId))


