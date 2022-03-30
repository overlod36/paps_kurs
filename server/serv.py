import os
import socketserver
import sqlite3

class TCPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		self.data = self.request.recv(1024).strip()
		print(self.data)
		print(self.client_address[0])
		self.data_proc()
		self.request.sendall(self.data)

	def data_proc(self):
		l_data = self.data.decode('utf-8').replace('"', '')
		l_data = list(l_data.split(" "))
		print(l_data)
		l_res = sql_1.execute(f"SELECT * FROM users").fetchall()
		print(l_res)
		if l_data[0] == '1':
			print('Происходит авторизация пользователя...')
			l_res = sql_1.execute(f"SELECT * FROM users WHERE login == ?", (l_data[1],)).fetchall()
			#l_res = list(sql.execute(f"SELECT * FROM users WHERE login == ?", (l_data[1],)))
			print(l_res)

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
db.execute(f"INSERT INTO users VALUES(?,?,?)", ("Dima", "1234", 1))
l_res = db.execute(f"SELECT * FROM users").fetchall()
print(l_res)
with socketserver.TCPServer((HOST, PORT), TCPHandler) as serv:
	print("Сервер запущен! Порт - > ", PORT)
	serv.serve_forever()



