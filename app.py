import pyautogui
from threading import Thread
from tkinter import *
import socket
import sys
import time

stop_thread = False


class Client:
	def __init__(self):
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect()

	def connect(self):
		try:
			self.client.connect(('localhost', 1234))
		except:
			print('Произошла ошибка...')

	def send(self, data):
		self.client.sendall(data)
		return self.client.recv(1024)

def connect_func(i_list):
	HOST, PORT = "localhost", 8080
	data = i_list[0].get()
	print(i_list[0].get(), i_list[1].get())
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #SOCK_STREAM - TCP сокет
			sock.connect((HOST, PORT))
			sock.sendall(bytes(data + "\n", "utf-8"))
			received = str(sock.recv(1024), "utf-8")
			print("Отправленная информация -> ", str(data))
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
	login_entry = Entry(root, width=23)
	login_label = Label(root, text="Логин")
	password_entry = Entry(root, width=23, show="*")
	password_label = Label(root, text="Пароль")
	login_label.place(x=190, y =114)
	password_entry.place(x = 260, y = 174)
	password_label.place(x = 190, y = 174)
	b_connect = Button(root, text='Подключение', command=lambda l = [login_entry, password_entry]: connect_func(l))
	login_entry.place(x = 260, y = 115)
	b_connect.place(x=243, y=265)
	root.mainloop()

def screenshot_func():
	i = 1
	while True:
		pyautogui.screenshot('e:/projects/paps_kurs/screenshots/' + str(i) + '.jpg')
		time.sleep(5)
		i+=1
		if stop_thread is True:
			break

if __name__ == "__main__":
	th1 = Thread(target=main)
	th2 = Thread(target=screenshot_func)
	th1.start()
	th2.start()

