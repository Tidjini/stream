import socket
import threading
import pickle
import numpy as np
import struct
import cv2
import pyautogui


class Sender:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        self.__sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__running = False

    def start(self):
        if self.__running:
            print(
                "Sender Still running and send to {}:{}".format(
                    self.__host, self.__port
                )
            )
            return
        print("Send streaming to {}:{}".format(self.__host, self.__port))
        self.__running = True
        threading.Thread(target=self.__start).start()

    def __start(self):
        self.__sender.connect((self.__host, self.__port))

        while self.__running:
            frame = None
            _, frame = cv2.imencode(".jpg", frame, self.__encoding_parameters)
            data = pickle.dumps(frame, 0)
            size = len(data)

            try:
                self.__sender.sendall(struct.pack(">L", size) + data)
            except ConnectionResetError:
                self.__running = False
            except ConnectionAbortedError:
                self.__running = False
            except BrokenPipeError:
                self.__running = False

        cv2.destroyAllWindows()
