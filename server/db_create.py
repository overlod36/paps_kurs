import sqlite3

db1 = sqlite3.connect('tasks.db')
sql_1 = db1.cursor()

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
sql_1.execute(f"INSERT INTO users VALUES(?,?,?)", ("Dima", "1234", 1))
l = list(sql_1.execute(f"SELECT * FROM users"))
print(l)

