import threading
import socket
import pickle
import struct
import cv2


class Receiver:
    # host, port for socket

    def __init__(self, host="127.0.0.1", port=8000, quit_key="q"):
        self.__host = host
        self.__port = port
        self.__quit_key = quit_key
        self.__receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__receiver.bind((self.__host, self.__port))
        self.__running = False
        self.__lock = threading.Lock()

    def start(self):
        print(
            "Start receiving at : {}:{}, (q to quit program)".format(
                self.__host, self.__port
            )
        )
        if self.__running:
            print("Receiver is running at {}:{}".format(self.__host, self.__port))
            return

        self.__running = True
        threading.Thread(target=self.__start).start()

    def __start(self):
        self.__receiver.listen()
        while self.__running:
            connection, addr = self.__receiver.accept()
            threading.Thread(
                target=self.__on_sender_connect, args=(connection, addr)
            ).start()

    def __on_sender_connect(self, connection: socket, addr):
        payload_size = struct.calcsize(">L")
        data = b""

        while self.__running:

            break_loop = False

            while len(data) < payload_size:
                received = connection.recv(4096)
                if received == b"":
                    connection.close()
                    break_loop = True
                    break
                data += received

            if break_loop:
                break

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]

            msg_size = struct.unpack(">L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += connection.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow(str(addr), frame)
            if cv2.waitKey(1) == ord(self.__quit_key):
                connection.close()
                break

    def stop_receiving(self):
        if not self.__running:
            print("Receiver is not running")

        self.__running = False
        self.__lock.acquire()
        self.__receiver.close()
        self.__lock.release()


# def intial_socket():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind(("localhost", 8000))
#     return server


# def listening(server: socket.socket):
#     server.listen()
#     print("Start listening at localhost:8000")
#     while True:
#         connexion, address = server.accept()
#         print("Connexion: {}, Address: {}".format(connexion, address))


# if __name__ == "__main__":
#     server = intial_socket()
#     t = threading.Thread(target=listening, args=(server,))
#     t.start()


# # from threading import Thread
# # from vidstream import StreamingServer

# # server = StreamingServer("127.0.0.1", 9999)
# # server.start_server()

# # t = Thread(target=server.start_server)
# # t.start()

# # while input("") != "q":
# #     continue


# # # When You Are Done
# # server.stop_server()


if __name__ == "__main__":
    receiver = Receiver()

    threading.Thread(target=receiver.start).start()

    while input("") != "q":
        continue

    receiver.stop_receiving()
