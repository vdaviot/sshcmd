import paramiko, cmd, getpass


class SSHELL(cmd.Cmd):

	intro = "\tWelcome to SSH@AMD\n\ttype Help for more infos\n"
	prompt = "SSH@AMD>"

	def	__init__(self):
		cmd.Cmd.__init__(self)
		self.hosts = []
		self.connections = []

	def do_add(self, args):
		'''Add an host to the known list. Usage: add <host> <user>'''
		if args:
			self.hosts.append(args.split(' '))
		else:
			print("Usage: add <host> <user>")


	def do_connect(self, host=""):
		'''Syntax: connect <host> <user>'''
		try:
			for host in self.hosts:
				client = paramiko.SSHClient()
				client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				client.connect(host[0], username=host[1], password=getpass.getpass("Type in your password:"))
				self.connections.append(client)
		except paramiko.ssh_exception.AuthenticationException as e:
			print(e)

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
			conn.close()

if __name__ == '__main__':
	cli = SSHELL()
	cli.cmdloop()
