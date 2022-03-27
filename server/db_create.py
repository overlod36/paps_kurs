db1 = sqlite3.connect('tasks.db')
sql_1 = db1.cursor()

sql_1.execute("""CREATE TABLE IF NOT EXISTS tasks(
	task_id INTEGER PRIMARY KEY,
	task_type TEXT NOT NULL, #важность, либо функциональный тип
	task_name TEXT NOT NULL,
	task_description TEXT,
	date_to_do TEXT NOT NULL,
	task_status TEXT NOT NULL,
	emp_id INTEGER NOT NULL,
	)
	""")
sql_1.execute("""CREATE TABLE IF NOT EXISTS employees(
	employee_id INTEGER PRIMARY KEY,
	employee_position TEXT NOT NULL,
	
	)
	""")
