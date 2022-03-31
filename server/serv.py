import os
import socketserver
import sqlite3

class TCPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		self.data = self.request.recv(1024).strip()
		print(self.client_address[0])
		self.data_proc()

	def data_proc(self):
		l_data = self.data.decode('utf-8').replace('"', '')
		l_data = list(l_data.split(" "))
		if l_data[0] == '1':
			print('Происходит авторизация пользователя...')
			l_res = list(sql_1.execute(f"SELECT * FROM users WHERE login == ?", (l_data[1],)).fetchall())
			if len(l_res) != 0:
				if l_res[0][0] == l_data[1]:
					if l_res[0][1] == l_data[2] and l_res[0] not in users_connected:
						self.request.sendall('Authorized!'.encode('utf-8'))
						users_connected.append(l_res[0])
					elif l_res[0] in users_connected:
						self.request.sendall('There is already such a user!'.encode('utf-8'))
					else:
						self.request.sendall('Wrong password!'.encode('utf-8'))
			else:
				self.request.sendall('No such a user in a system!'.encode('utf-8'))

users_connected = []

db = sqlite3.connect('tasks.db')
sql_1 = db.cursor()

HOST = "localhost"
PORT = 8080
sql_1.execute("""CREATE TABLE IF NOT EXISTS tasks(
task_id INTEGER PRIMARY KEY,
task_type TEXT NOT NULL,
task_name TEXT NOT NULL,
task_description TEXT,
date_to_do TEXT NOT NULL,
task_status TEXT NOT NULL,
emp_id INTEGER NOT NULL,
FOREIGN KEY (emp_id) REFERENCES employees(employee_id)
)
""")
sql_1.execute("""CREATE TABLE IF NOT EXISTS employees(
	employee_id INTEGER PRIMARY KEY,
	employee_position TEXT NOT NULL
	)
	""")

sql_1.execute("""CREATE TABLE IF NOT EXISTS users(
	login TEXT PRIMARY KEY,
	password TEXT NOT NULL,
	emp_id INTEGER NOT NULL,
	UNIQUE(password),
	UNIQUE(emp_id),
	FOREIGN KEY (emp_id) REFERENCES employees(employee_id)
	) 
	""")

db.execute(f"INSERT INTO employees VALUES(?, ?)", (1, 'Сотрудник'))
db.execute(f"INSERT INTO users VALUES(?,?,?)", ("Dima", "1234", 1))
with socketserver.TCPServer((HOST, PORT), TCPHandler) as serv:
	print("Сервер запущен! Порт - > ", PORT)
	serv.serve_forever()



