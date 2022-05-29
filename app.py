import pyautogui
from threading import Thread
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as mb
import socket
import sys
import time
import json
import keyboard
import datetime
from threading import Timer

stop_thread = False
user_login = ''

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

	def set_time(self, str):
		st = list(str.split(':'))
		self.hours = int(st[0])
		self.minutes = int(st[1])
		self.seconds = int(st[2])


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
	global user_login
	HOST, PORT = "localhost", 8080
	data = i_list[0] + " " + i_list[1].get() + " " + i_list[2].get()
	for_log = list(data.split(" "))
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
			user_login = for_log[1]
		elif received == 'Admin Authorized!':
			mb.showinfo("Информация", 'Авторизация администратора прошла успешно!')
			s_admin_interface(wind, w_list)
			user_login = for_log[1]
		elif received == 'Header Authorized!':
			mb.showinfo("Информация", 'Авторизация руководителя прошла успешно!')
			s_header_interface(wind, w_list)
			user_login = for_log[1]
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
	global user_login
	obj.pause()
	HOST, PORT = "localhost", 8080
	st1, st2, st3 =  f'{obj.hours}' if obj.hours > 9 else f'0{obj.hours}', f'{obj.minutes}' if obj.minutes > 9 else f'0{obj.minutes}', f'{obj.seconds}' if obj.seconds > 9 else f'0{obj.seconds}'
	res = st1 + ':' + st2 + ':' + st3
	data = '6' + " " + 'set_time ' + user_login + " " + res
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

def add_task(t_name, t_descr):
	HOST, PORT = "localhost", 8080
	if len(t_name.get()) != 0 and len(t_descr.get(1.0, "end")) != 0:
		description = t_descr.get(1.0, "end")
		data = '5' + " " + 'add_task' + " " + t_name.get() + " " + description[0:len(description)-1]
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

def get_users(list_u):
	HOST, PORT = "localhost", 8080
	data = '4' + " " + 'all_users'
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
	if len(received) != 0:
		list_u.delete(0, END)
		rec = list(received.split(" "))
		for el in rec:
			list_u.insert(END, el)

def get_user_task(list_t):
	global user_login
	HOST, PORT = "localhost", 8080
	data = '4' + " " + 'task_user' + " " + user_login
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
	if len(received) != 0:
		list_t.delete(0, END)
		rec = list(received.split(" "))
		for el in rec:
			list_t.insert(END, el)

def get_tasks(list_t):
	HOST, PORT = "localhost", 8080
	data = '4' + " " + 'all_tasks'
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
	if len(received) != 0:
		list_t.delete(0, END)
		rec = list(received.split(" "))
		for el in rec:
			list_t.insert(END, el)

def checkin_task(td, status, user):
	HOST, PORT = "localhost", 8080
	data = '4' + " " + 'check_task ' + td.get(td.curselection())
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
	res = list(received.split(' '))
	user.config(state="normal")
	status.config(state="normal")
	user.delete(0, END)
	status.delete(0, END)
	user.insert(END, res[0])
	status.insert(END, res[1])
	user.config(state="disabled")
	status.config(state="disabled")

def link_task(list_t, list_u):
	HOST, PORT = "localhost", 8080
	data = '5' + " " + 'link_task ' + list_u.get(list_u.curselection()) + " " + list_t.get(list_t.curselection())
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

def user_choose(tb, but, obj):
	global user_login
	HOST, PORT = "localhost", 8080
	data = '6' + " " + 'choose_task' + " " + tb.get(tb.curselection()) + " " + user_login
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
	if received == 'to_start':
		print('Начало работы...')
		obj.set_time('00:00:00')
		obj.start()
	elif received == 'not_to_start':
		print('Работа уже началась...')
	else:
		res = list(received.split(' '))
		obj.set_time(res[1])
		obj.start()


def s_user_interface(wind, w_list):
	wind.geometry("724x400+200+100")
	for obj in w_list:
		obj.destroy()
	watcher = Label(wind, text="00:00:00")
	watcher.place(x=620, y=50)
	st1 = StWatcher(watcher)
	tasks_t = Label(wind, text="Задачи")
	tasks_t.place(x=110, y=15)
	b_push = Button(wind, text="Пауза")
	b_push.config(command= lambda o = st1: push_time_to_server(o))
	b_push.place(x=495, y = 140)
	tasks_lb = Listbox(wind, width=30, height=5, exportselection=0)
	tasks_lb.place(x=17, y=45)
	up_task_button = Button(wind, text="Обновить")
	up_task_button.place(x=100, y=162)
	up_task_button.config(command= lambda list_t = tasks_lb : get_user_task(list_t))
	choose_task_button = Button(wind, text="Выполнять")
	choose_task_button.place(x=95, y=202)
	choose_task_button.config(command= lambda tb = tasks_lb, but = choose_task_button, obj = st1 : user_choose(tb, but, obj))


def admin_show(ul):
	HOST, PORT = "localhost", 8080
	data = '4' + " " + 'admin_request'
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
	res = list(received.split(" "))
	res = res[:len(res)-1]
	ul.delete(0, END)
	for i in range(0,len(res)-2,3):
		if res[i+2] == 'employee':
			ul.insert(END, "Логин: " + res[i] + " | Пароль: " + res[i+1] + " | Сотрудник")
		elif res[i+2] == 'header':
			ul.insert(END, "Логин: " + res[i] + " | Пароль: " + res[i+1] + " | Руководитель")
		elif res[i+2] == 'admin':
			ul.insert(END, "Логин: " + res[i] + " | Пароль: " + res[i+1] + " | Администратор")
		

def s_admin_interface(wind, w_list):
	wind.geometry("950x400+200+100")
	for obj in w_list:
		obj.destroy()
	main_label = Label(wind, text="Страница Администратора")
	main_label.place(x=205, y=50)
	list_label = Label(wind, text="Список пользователей")
	list_label.place(x=622, y=50)
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
	users_list = Listbox(wind, width=45, height=5)
	users_list.place(x=524,y=100)
	update_button = Button(wind, text="Обновить")
	update_button.place(x=665, y=230)
	update_button.config(command=lambda ul = users_list : admin_show(ul))


def s_header_interface(wind, w_list):
	wind.geometry("748x400+200+100")
	for obj in w_list:
		obj.destroy()
	users_t = Label(wind, text="Сотрудники")
	tasks_t = Label(wind, text="Задачи")
	status = Label(wind, text="Статус задачи")
	user_to_do = Label(wind, text="Исполняющий задачу")
	tasks_lb = Listbox(wind, width=30, height=5, exportselection=0)
	users_lb = Listbox(wind, width=30, height=5, exportselection=0)
	st_entry = Entry(wind, width=15, state='disabled')
	st_user_entry = Entry(wind, width=15, state='disabled')
	users_t.place(x=100, y=15)
	tasks_t.place(x=372,y=15)
	users_lb.place(x=17, y=45)
	tasks_lb.place(x=280, y=45)
	status.place(x=580, y=15)
	st_entry.place(x=570,y=45)
	user_to_do.place(x=550,y=74)
	check_button = Button(wind, text="Проверить")
	st_user_entry.place(x=570, y=100)
	check_button.place(x=586, y=140)
	check_button.config(command= lambda td = tasks_lb, status = st_entry, user = st_user_entry : checkin_task(td, status, user))
	task_name_entry = Entry(wind, width=20)
	task_name_entry.place(x=17, y=210)
	task_descr_entry = Text(wind, width=15, height=7)
	task_descr_entry.place(x=215, y=210)
	update_u_button = Button(wind, text="Обновить")
	update_u_button.place(x=100, y=162)
	update_t_button = Button(wind, text="Обновить")
	update_t_button.place(x=365, y=162)
	add_t_button = Button(wind, text="Добавить")
	add_t_button.place(x=380, y=212)
	add_t_button.config(command= lambda t_name = task_name_entry, t_descr = task_descr_entry : add_task(t_name, t_descr))
	update_t_button.config(command= lambda list_t = tasks_lb : get_tasks(list_t))
	update_u_button.config(command= lambda list_u = users_lb : get_users(list_u))
	link_button = Button(wind, text="Назначить")
	link_button.place(x=380, y=250)
	link_button.config(command= lambda list_t = tasks_lb, list_u = users_lb : link_task(list_t, list_u))


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
	#th3 = Thread(target=keylog_func)
	th1.start()
	th2.start()
	#th3.start()