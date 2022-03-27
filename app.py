import pyautogui
from threading import Thread
from tkinter import *
import socket
import sys
import time

stop_thread = False
def connect_func():
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

def aboba(root):
	global stop_thread
	stop_thread = True
	root.destroy()


def main():
	root = Tk()
	root.protocol("WM_DELETE_WINDOW", lambda r = root: aboba(r))
	root.geometry("600x400")
	b_connect = Button(root, text='Подключение', command=connect_func)
	b_connect.place(x=300, y=200)
	root.mainloop()

def screenshot_func():
	i = 1
	while True:
		pyautogui.screenshot('e:/projects/paps_kurs/screenshots' + str(i) + '.jpg')
		time.sleep(5)
		i+=1
		if stop_thread is True:
			break

if __name__ == "__main__":
	th1 = Thread(target=main)
	th2 = Thread(target=screenshot_func)
	th1.start()
	th2.start()

