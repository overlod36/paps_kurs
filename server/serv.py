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
					if l_res[0][1] == l_data[2] and l_res[0] not in users_connected and l_res[0][2] == 'Сотрудник':
						self.request.sendall('Employee Authorized!'.encode('utf-8'))
						users_connected.append(l_res[0])
					elif l_res[0][1] == l_data[2] and l_res[0] not in users_connected and l_res[0][2] == 'Администратор':
						self.request.sendall('Admin Authorized!'.encode('utf-8'))
						users_connected.append(l_res[0])
					elif l_res[0] in users_connected:
						self.request.sendall('There is already such a user!'.encode('utf-8'))
					else:
						self.request.sendall('Wrong password!'.encode('utf-8'))
			else:
				self.request.sendall('No such a user in a system!'.encode('utf-8'))
		elif l_data[0] == '2':
			print('Пришло время работы сотрудника...')
			print('-> ' + l_data[1])
			self.request.sendall('Time Is On My Side!'.encode('utf-8'))

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
log INTEGER NOT NULL,
FOREIGN KEY (log) REFERENCES users(login)
)
""")

sql_1.execute("""CREATE TABLE IF NOT EXISTS users(
	login TEXT PRIMARY KEY,
	password TEXT NOT NULL,
	emp_position TEXT NOT NULL,
	UNIQUE(password)
	) 
	""")

db.execute(f"INSERT INTO users VALUES(?,?,?)", ("admin", "admin", 'Администратор'))
db.execute(f"INSERT INTO users VALUES(?,?,?)", ("Dima", "1234", 'Сотрудник'))
with socketserver.TCPServer((HOST, PORT), TCPHandler) as serv:
	print("Сервер запущен! Порт - > ", PORT)
	serv.serve_forever()



