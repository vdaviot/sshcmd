#!/usr/bin/python

import paramiko, cmd, getpass


class SSHELL(cmd.Cmd):

	intro = "\tWelcome to SSH@AMD\n\ttype Help for more infos\n"
	prompt = "SSH@AMD>"

	def	__init__(self):
		cmd.Cmd.__init__(self)
		self.connected = 0
		self.hosts = []
		self.connections = []

	def do_add(self, args):
		'''Add an host to the known list. Usage: add <host> <user>'''
		if args:
			self.hosts.append(args.split(' '))
			print "Added {} to known hosts list.".format(args)
		else:
			print "Usage: add <host> <user>" 


	def do_connect(self, host=""):
		'''Syntax: connect <host> <user>'''
		name = 'admin'
		host = '62.210.208.23:8070'
		try:
			for host in self.hosts:
				client = paramiko.SSHClient()
				client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				client.connect(host, name, password=getpass.getpass("Type in your password:"))
				print "Connecting to {} as {}.".format(host, name)
				self.connections.append(client)
				self.connected = 1
		except paramiko.ssh_exception.AuthenticationException as e:
			self.connected = 0
			print(e)
		print "Connected."

	def do_run(self, command):
		'''Usage: run <yourcommand>'''
		if command:
			for host, conn in zip(self.hosts, self.connections):
				stdin, stdout, stderr = conn.exec_command(command)
				stdin.close()
				for line in stdout.read().splitlines():
					print("host: {} {}".format(host[0], line))
		else:
			print("Usage: run <yourcommand>")


	def do_close(self, args):
		'''Usage: close'''
		for conn in self.connections:
			print "Connection {} closed.".format(conn)
			conn.close()

if __name__ == '__main__':
	cli = SSHELL()
	cli.cmdloop()
