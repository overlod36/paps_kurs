import pyautogui
from threading import Thread
from tkinter import *
import tkinter.messagebox as mb
import socket
import sys
import time
import json

stop_thread = False


class StWatcher:
	hours, minutes, seconds = 0, 0, 0
	status_run = False
	def __init__(self, lbl):
		self.label = lbl

	def start(self):
		if not self.status_run:
			self.update()
			self.status_run = True
		else:
			self.pause()

	def pause(self):
		if self.status_run:
			self.label.after_cancel(update_time)
			self.status_run = False

	def update(self):
		self.seconds += 1
		if self.seconds == 60:
			self.minutes += 1
			self.seconds = 0
		if self.minutes == 60:
			self.hours += 1
			self.minutes = 0
		h_str = f'{self.hours}' if self.hours > 9 else f'0{self.hours}'
		m_str = f'{self.minutes}' if self.minutes > 9 else f'0{self.minutes}'
		s_str = f'{self.seconds}' if self.seconds > 9 else f'0{self.seconds}'
		self.label.config(text=h_str + ':' + m_str + ':' + s_str)
		global update_time
		update_time = self.label.after(1000, self.update)





'''
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
'''

def connect_func(i_list, wind, w_list):
	HOST, PORT = "localhost", 8080
	data = i_list[0] + " " + i_list[1].get() + " " + i_list[2].get()
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #SOCK_STREAM - TCP сокет
			sock.connect((HOST, PORT))
			sock.send(json.dumps(data).encode("utf-8"))
			received = str(sock.recv(1024), "utf-8")
			print("Отправленная информация -> ", str(data))
			print("Полученная информация -> ", received)
		if received == 'Authorized!':
			mb.showinfo("Информация", 'Авторизация прошла успешно!')
			s_user_interface(wind, w_list)
		elif received == 'Wrong password!':
			mb.showinfo("Ошибка", "Неверно введен пароль!")
		elif received == 'No such a user in a system!':
			mb.showinfo('Ошибка', 'Такого пользователя нет в системе!')
	except ConnectionRefusedError:
		print("Соединение не было установлено!")
	



def aboba(root):
	global stop_thread
	stop_thread = True
	root.destroy()

def s_user_interface(wind, w_list):
	wind.geometry("1024x800+200+100")
	for obj in w_list:
		obj.destroy()
	watcher = Label(wind, text="00:00:00")
	watcher.place(x=920, y=50)
	st1 = StWatcher(watcher)
	b_start = Button(wind, text="Запуск/Пауза")
	b_start.config(command=st1.start)
	b_start.place(x=897, y = 93)




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
	obj_l = [login_entry, login_label, password_entry, password_label]
	b_connect = Button(root, text='Подключение')
	b_connect.config(command=lambda l = ['1', login_entry, password_entry], w = root, wl = obj_l + [b_connect]: connect_func(l, w, wl))
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

