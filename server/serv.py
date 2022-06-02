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
					if l_res[0][1] == l_data[2] and l_res[0] not in users_connected and l_res[0][2] == 'employee':
						self.request.sendall('Employee Authorized!'.encode('utf-8'))
						users_connected.append(l_res[0])
					elif l_res[0][1] == l_data[2] and l_res[0] not in users_connected and l_res[0][2] == 'admin':
						self.request.sendall('Admin Authorized!'.encode('utf-8'))
						users_connected.append(l_res[0])
						print(list(sql_1.execute(f"SELECT * FROM users")))
					elif l_res[0][1] == l_data[2] and l_res[0] not in users_connected and l_res[0][2] == 'header':
						self.request.sendall('Header Authorized!'.encode('utf-8'))
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
		elif l_data[0] == '3':
			login = l_data[1]
			password = l_data[2]
			pos = l_data[3]
			checkin = list(db.execute(f"SELECT * FROM users WHERE login == ?", (login,)))
			if len(checkin) == 0:
				db.execute(f"INSERT INTO users(login,password,emp_position) VALUES (?,?,?)", (login, password, pos))
				db.commit()
				self.request.sendall('Addin user is done!'.encode('utf-8'))
		elif l_data[0] == '4':
			if l_data[1] == 'all_users':
				st = list(db.execute(f"SELECT login FROM users WHERE emp_position == ?", ('employee',)))
				res = ""
				for el in st:
					res += el[0]
					res += " "
				self.request.sendall(res.encode('utf-8'))
			elif l_data[1] == 'all_tasks':
				st = list(db.execute(f"SELECT task_name FROM tasks"))
				res = ""
				for el in st:
					res += el[0]
					res += " "
				self.request.sendall(res.encode('utf-8'))
			elif l_data[1] == 'task_user':
				print('Отображение задач пользователя -> ' + l_data[2])
				st = list(db.execute(f"SELECT task_name FROM tasks WHERE log == ? AND task_status != ? AND task_status != ?", (l_data[2], 'CHECKING', 'DONE')))
				print(st)
				res = ""
				for el in st:
					res += el[0]
					res += " "
				self.request.sendall(res.encode('utf-8'))
			elif l_data[1] == 'check_task':
				print('Проверка статуса задачи -> ' + l_data[2])
				st = list(db.execute(f"SELECT log, task_status FROM tasks WHERE task_name == ?", (l_data[2],)))
				if str(type(st[0][0])) != "<class 'NoneType'>":
					res = st[0][0] + " " + st[0][1]
				else:
					res = 'NO_EMPLOYEE' + " " + st[0][1]
				self.request.sendall(res.encode('utf-8'))
			elif l_data[1] == 'admin_request':
				res = ''
				print('Администратор запрашивает список пользователей!')
				st = list(db.execute(f"SELECT login, password, emp_position FROM users"))
				for el in st:
					res += (el[0] + ' ' + el[1] + ' ' + el[2] + ' ')
				self.request.sendall(res.encode('utf-8'))

		elif l_data[0] == '5':
			if l_data[1] == 'add_task':
				print('Добавление задачи -> ' + l_data[2])
				db.execute(f"INSERT INTO tasks(task_type,task_name,task_description,date_to_do,task_status) VALUES (?,?,?,?,?)", ('task', l_data[2], l_data[3], 'today', 'NOT_APPOINTED'))
				db.commit()
				ch = list(db.execute(f"SELECT * FROM tasks"))
				print(ch)
			elif l_data[1] == 'link_task':
				src = list(db.execute(f"SELECT log FROM tasks WHERE task_name == ?", (l_data[3],)))
				if src[0][0] == None:
					db.execute(f"UPDATE tasks SET log = ?, task_status = ? WHERE task_name = ?", (l_data[2], 'APPOINTED' ,l_data[3]))
					db.commit()
					print("Задача " + l_data[3] + " назначена сотруднику -> " + l_data[2])
				else:
					print('Задача уже назначена!')
		elif l_data[0] == '6':
			if l_data[1] == 'choose_task':
				bool_stuff = 0

				print('Проверка текущей задачи сотрудника -> ' + l_data[3])
				print(list(db.execute(f"SELECT * FROM tasks")))
				for_check = list(db.execute(f"SELECT task_status FROM tasks WHERE log = ?", (l_data[3],)))
				for el in for_check:
					if el[0] == 'IN_PROGRESS':
						bool_stuff = 1
						break
					elif el[0] == 'IN_PAUSE':
						bool_stuff = 2

				if bool_stuff == 0:
					print('Начинается выполнение задачи -> ' + l_data[2])
					db.execute(f"UPDATE tasks SET task_status = ? WHERE task_name = ?", ('IN_PROGRESS',l_data[2]))
					db.commit()
					self.request.sendall('to_start'.encode('utf-8'))
				elif bool_stuff == 1:
					print('Сотрудник уже выполняет задачу!')
					self.request.sendall('not_to_start'.encode('utf-8'))
				elif bool_stuff == 2:
					rs = list(db.execute(f"SELECT task_status FROM tasks WHERE task_name = ?", (l_data[2],)))
					if rs[0][0] == 'IN_PAUSE':
						print('Продолжается выполнение задачи!')
						res = list(db.execute(f"SELECT doing_time FROM tasks WHERE task_name = ?", (l_data[2],)))
						db.execute(f"UPDATE tasks SET task_status = ? WHERE task_name = ?", ('IN_PROGRESS',l_data[2]))
						db.commit()
						st = 'after_pause ' + res[0][0]
						self.request.sendall(st.encode('utf-8'))
					elif rs[0][0] == 'APPOINTED':
						print('Начинается выполнение задачи -> ' + l_data[2])
						db.execute(f"UPDATE tasks SET task_status = ? WHERE task_name = ?", ('IN_PROGRESS',l_data[2]))
						db.commit()
						self.request.sendall('to_start'.encode('utf-8'))

			elif l_data[1] == 'set_time':
				print('Проверка текущей задачи сотрудника -> ' + l_data[3])
				print(list(db.execute(f"SELECT * FROM tasks")))
				db.execute(f"UPDATE tasks SET doing_time = ?, task_status = ? WHERE task_name = ?", (l_data[3], 'IN_PAUSE' , l_data[2]))
				db.commit()
				print('Остановка выполнения работы!')
			elif l_data[1] == 'check':
				print('Задача -> ' + l_data[2] + ' отправлена на проверку!')
				db.execute(f"UPDATE tasks SET task_status = ?, doing_time = ? WHERE task_name = ?", ('CHECKING', l_data[3], l_data[2]))
				db.commit()
			elif l_data[1] == 'final_yes':
				print('Полное одобрение задачи!')
				db.execute(f"UPDATE tasks SET task_status = ? WHERE task_name = ?", ('DONE', l_data[2]))
				db.commit()
			elif l_data[1] == 'final_no':
				print('Задача проверку не прошла!')
				db.execute(f"UPDATE tasks SET task_status = ? WHERE task_name = ?", ('IN_PAUSE', l_data[2]))
				db.commit()
			elif l_data[1] == 'check_for_final':
				ls = list(db.execute(f"SELECT task_status FROM tasks WHERE task_name = ?", (l_data[2],)))
				if ls[0][0] == 'CHECKING':
					self.request.sendall('yes'.encode('utf-8'))
				else:
					self.request.sendall('no'.encode('utf-8'))
		elif l_data[0] == '7':
			ls = list(db.execute(f"SELECT emp_position FROM users WHERE login = ?", (l_data[1],)))
			if ls[0][0] == 'employee':
				res = ''
				lt = list(db.execute(f"SELECT * FROM tasks WHERE log = ?", (l_data[1],)))
				print(lt)
				for el in lt:
					if el[6] == "DONE":
						status = 'Выполнена!'
					elif el[6] == "IN_PROGRESS":
						status = 'В процессе выполнения!'
					elif el[6] == "IN_PAUSE":
						status = 'На паузе!'
					elif el[6] == "APPOINTED":
						status = 'Назначена, не выполнялась!'
					elif el[6] == "CHECKING":
						status = 'На проверке!'
					res += (str(el[0]) + "_" + el[2] + "_" + el[3] + "_" + el[5] + "_" + status + "_")
				self.request.sendall(res.encode('utf-8'))
			else:
				self.request.sendall('no'.encode('utf-8'))
		elif l_data[0] == '8':
			print('Пользователь ' + l_data[1] + ' вышел из сети!')
			for user in users_connected:
				if user[0] == l_data[1]:
					users_connected.remove(user)




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
doing_time TEXT,
task_status TEXT NOT NULL,
log INTEGER,
FOREIGN KEY (log) REFERENCES users(login),
UNIQUE(task_name)
)
""")


sql_1.execute("""CREATE TABLE IF NOT EXISTS users(
	login TEXT PRIMARY KEY,
	password TEXT NOT NULL,
	emp_position TEXT NOT NULL,
	UNIQUE(password)
) 
""")

#sql_1.execute("""DROP TABLE tasks""")



with socketserver.TCPServer((HOST, PORT), TCPHandler) as serv:
	print("Сервер запущен! Порт - > ", PORT)
	serv.serve_forever()



