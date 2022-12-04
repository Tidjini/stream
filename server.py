import threading
import socket
import pickle
import struct
import numpy as np

import cv2
import pyautogui


def intial_socket():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 8000))
    return server


def listening(server: socket.socket):
    server.listen()
    print("Start listening at localhost:8000")
    while True:
        connexion, address = server.accept()
        print("Connexion: {}, Address: {}".format(connexion, address))


if __name__ == "__main__":
    server = intial_socket()
    t = threading.Thread(target=listening, args=(server,))
    t.start()


# from threading import Thread
# from vidstream import StreamingServer

# server = StreamingServer("127.0.0.1", 9999)
# server.start_server()

# t = Thread(target=server.start_server)
# t.start()

# while input("") != "q":
#     continue


# # When You Are Done
# server.stop_server()
