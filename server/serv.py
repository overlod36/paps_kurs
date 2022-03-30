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
		if l_data[0] == '1':
			print('Происходит авторизация пользователя...')


if __name__ == "__main__":
	HOST = "localhost"
	PORT = 8080

	with socketserver.TCPServer((HOST, PORT), TCPHandler) as serv:
		print("Сервер запущен! Порт - > ", PORT)
		serv.serve_forever()



