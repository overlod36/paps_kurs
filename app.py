from pyautogui import *
import socket
import sys

HOST, PORT = "localhost", 8080
data = " ".join(sys.argv[1:])

try:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #SOCK_STREAM - TCP сокет
		sock.connect((HOST, PORT))
		sock.sendall(bytes(data + "\n", "utf-8"))
		received = str(sock.recv(1024), "utf-8")
		print("Отправленная информация -> ", data)
	print("Полученная информация -> ", received)
except ConnectionRefusedError:
	print("Соединение не было установлено!")


