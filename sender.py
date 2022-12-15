import socket
import threading
import pickle
import numpy as np
import struct
import cv2
import pyautogui
import time


class Sender:
    def __init__(self, host, port, x_res=1024, y_res=576, restart=0):
        self.__host = host
        self.__port = port
        self.__intialize()
        self.__encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        self.__x_res = x_res
        self.__y_res = y_res
        self.__restart_time = restart
        self.__lock = threading.Lock()

    def __intialize(self):
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

    def __restart(self, exception=None):
        if exception:
            print("Exception du to: ", exception)
        print(f"Restart in {self.__restart_time} seconds")
        time.sleep(self.__restart_time)

        self.__lock.acquire()
        self.__sender.close()
        self.__intialize()
        self.start()
        self.__lock.release()

    def __start(self):
        try:
            self.__sender.connect((self.__host, self.__port))
        except (ConnectionRefusedError, OSError) as e:
            if self.__restart_time:
                self.__restart(e)
            return
        restart = False
        while self.__running:
            frame = self._get_frame()
            _, frame = cv2.imencode(".jpg", frame, self.__encoding_parameters)
            data = pickle.dumps(frame, 0)
            size = len(data)

            try:
                self.__sender.sendall(struct.pack(">L", size) + data)
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError) as e:
                restart = True
                break

        if restart and self.__restart_time:
            self.__restart(exception="From Breacking point")

        cv2.destroyAllWindows()

    def stop(self):
        if not self.__running:
            print("Sender not send data")
            return

        self.__running = False
        # to stop restarting
        self.__restart_time = 0

    def _get_frame(self):
        """
        Gets the next screenshot.

        Returns
        -------

        frame : the next screenshot frame to be processed
        """
        screen = pyautogui.screenshot()
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(
            frame, (self.__x_res, self.__y_res), interpolation=cv2.INTER_AREA
        )
        return frame


# todo get arguments from console
# pyinstaller --onefile sender.py
if __name__ == "__main__":

    import sys

    host = None

    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if host is None:
        host = input("Enter your host: ")

    sender = Sender(host=host, port=8000, restart=10)
    threading.Thread(target=sender.start).start()

    while input("") != "q":
        continue

    sender.stop()
