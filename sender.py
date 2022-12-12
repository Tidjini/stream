import cv2
import pyautogui


class Sender:
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
