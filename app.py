import pyautogui
from threading import Thread
from tkinter import *
from tkinter import ttk
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
		if received == 'Employee Authorized!':
			mb.showinfo("Информация", 'Авторизация сотрудника прошла успешно!')
			s_user_interface(wind, w_list)
		elif received == 'Admin Authorized!':
			mb.showinfo("Информация", 'Авторизация администратора прошла успешно!')
			s_admin_interface(wind, w_list)
		elif received == 'Header Authorized!':
			mb.showinfo("Информация", 'Авторизация руководителя прошла успешно!')
			s_header_interface(wind, w_list)
		elif received == 'Wrong password!':
			mb.showinfo("Ошибка", "Неверно введен пароль!")
		elif received == 'No such a user in a system!':
			mb.showinfo('Ошибка', 'Такого пользователя нет в системе!')
		elif received == 'There is already such a user!':
			mb.showinfo('Ошибка', 'Данный пользователь уже авторизован в системе!')
	except ConnectionRefusedError:
		print("Соединение не было установлено!")
		mb.showinfo('Ошибка', 'Не удалось совершить соединение с сервером!')
	
def push_time_to_server(obj):
	HOST, PORT = "localhost", 8080
	st1, st2, st3 =  f'{obj.hours}' if obj.hours > 9 else f'0{obj.hours}', f'{obj.minutes}' if obj.minutes > 9 else f'0{obj.minutes}', f'{obj.seconds}' if obj.seconds > 9 else f'0{obj.seconds}'
	res = st1 + ':' + st2 + ':' + st3
	data = '2' + " " + res
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #SOCK_STREAM - TCP сокет
			sock.connect((HOST, PORT))
			sock.send(json.dumps(data).encode("utf-8"))
			received = str(sock.recv(1024), "utf-8")
			print("Отправленная информация -> ", str(data))
			print("Полученная информация -> ", received)

	except ConnectionRefusedError:
		print("Соединение не было установлено!")
		mb.showinfo('Ошибка', 'Не удалось совершить соединение с сервером!')

def send_new_user(l, p, st):
	HOST, PORT = "localhost", 8080
	if st.get() == "Сотрудник":
		pos = "employee"
	elif st.get() == "Администратор":
		pos = "admin"
	elif st.get() == "Руководитель":
		pos = "header"
	res = l.get() + " " + p.get() + " " + pos
	data = '3' + " " + res
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #SOCK_STREAM - TCP сокет
			sock.connect((HOST, PORT))
			sock.send(json.dumps(data).encode("utf-8"))
			received = str(sock.recv(1024), "utf-8")
			print("Отправленная информация -> ", str(data))
			print("Полученная информация -> ", received)
	except ConnectionRefusedError:
		print("Соединение не было установлено!")
		mb.showinfo('Ошибка', 'Не удалось совершить соединение с сервером!')

		


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
	b_push = Button(wind, text="Отправка данных на сервер")
	b_push.config(command= lambda o = st1: push_time_to_server(o))
	b_push.place(x=795, y = 140)

def s_admin_interface(wind, w_list):
	wind.geometry("600x400+200+100")
	for obj in w_list:
		obj.destroy()
	main_label = Label(wind, text="Страница Администратора")
	main_label.place(x=205, y=50)
	login_label = Label(wind, text="Логин нового сотрудника")
	login_entry = Entry(wind, width=23)
	login_label.place(x=100, y=120)
	login_entry.place(x=310, y=122)
	password_label = Label(wind, text="Пароль нового сотрудника")
	password_entry = Entry(wind, width=23)
	password_label.place(x=100, y=165)
	password_entry.place(x=310, y=167)
	position_label = Label(wind, text="Статус нового сотрудника")
	position_entry = ttk.Combobox(wind, width=20, values=["Сотрудник", "Руководитель", "Администратор"])
	position_label.place(x=100, y=210)
	position_entry.place(x=310, y=212)
	add_button = Button(wind, text="Добавить")
	add_button.place(x=270, y=285)
	add_button.config(command= lambda log = login_entry, passw = password_entry, pos = position_entry : send_new_user(log,passw,pos))

def s_header_interface(wind, w_list):
	wind.geometry("800x600+200+100")
	for obj in w_list:
		obj.destroy()


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

