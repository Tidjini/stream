import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 8000))


# from threading import Thread
# from vidstream import CameraClient
# from vidstream import VideoClient
# from vidstream import ScreenShareClient

# # Choose One
# # client1 = CameraClient("127.0.0.1", 9999)
# # client2 = VideoClient("127.0.0.1", 9999, "video.mp4")
# client3 = ScreenShareClient("127.0.0.1", 9999)


# t = Thread(target=client3.start_stream)
# t.start()

# while input("") != "q":
#     continue

# client3.stop_stream()

# # client2.start_stream()
# # client3.start_stream()
