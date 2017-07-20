# **************************************************************************** #
# 																			   #
#                                                         :::      ::::::::    #
#    ftp.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: vdaviot <marvin@42.fr>                     +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2017/06/29 14:39:48 by vdaviot           #+#    #+#              #
#    Updated: 2017/06/29 14:39:51 by vdaviot          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ftplib import error_temp
from ftplib import error_perm
from ftplib import FTP
import sys, cmd, getpass, ftplib, os, datetime

COMMAND_LIST = ['help', 'connect', 'cd', 'dc', 'dl', 'upload', 'ls', 'rename', 'rm', 'exit', 'rename']
EXTENSION_LIST = ['.py', '.c', '.html', '.txt', '.xml']

def logDecoractor(function):
	def wrapper(self, *args, **kwargs):
		ret = function(self, *args, **kwargs)
		if ret: _FTP.writeToLog(self, ret)
	return wrapper

class _FTP(cmd.Cmd):

	intro = "\tWelcome in FTP@AMD\n\ttype Help for more infos\n"
	prompt = 'Anonymous>'

	logFile = 'log.txt'
	errorLog = 'error.txt'

	def __init__(self, host="localhost", user="anonymous"):
		
		cmd.Cmd.__init__(self)
		self.host, self.user = host, user
		self.connected = 0
		self.home = '/'

	def __str__(self):
		return self.user + '@' + self.host + ' -> ' + self.home

	def writeToLog(self, msg):
		with open(_FTP.logFile, 'a+') as f:
			try:
				f.write(str(datetime.datetime.today()) + ": {}\n".format(msg))
				f.close
			except IOError as e:
				f.close()
				raise e

	@logDecoractor
	def do_connect(self, host=""): # Should be ok, needs polishing
		'''Syntax: connect <host> <user>'''
		if self.connected == 1:
			print("You are already connected to " + self.host + " as " + self.user) # Si deja connecté on omet
			return
		if host == "" and self.host == "localhost":
			self.host = input("\nPlease type your host addr\n\t> ")
		elif host != "":
			self.host = host
		user = input("\nPlease type your username\n\t> ")
		self.user = user
		passwd = getpass.getpass("\nPlease type your password\n\t> ")
		print ("Beginning connection to " + self.host + " as " + self.user + "..")
		try:
			self.server = ftplib.FTP(self.host)
			self.server.login(self.user, passwd)
			self.connected = 1
			_FTP.prompt = self.user + "@" + self.host + "> "
			print("Connected to " + self.host + "\n")
			print("Server infos:\n\t" + self.server.getwelcome() + "\n")
			self.home = self.server.pwd()
			print("Located in " + self.home)
			print("Available commands:\n\t" + ', '.join(COMMAND_LIST))
		except error_perm or error_temp as e:
			return e
		return "Connected to {} as {}.".format(self.host, self.user)

	@logDecoractor
	def do_ls(self, arg): 
		'''List the content of a directory. Usage: ls <dir>'''
		if self.connected == 0:
			return "Not connected to any server.\n\tTry connecting before trying any commands."
		try:
			directory = arg if arg != "" else "."
			self.server.dir(directory)
			return "Ls command on {}".format(arg)
		except:
			return "Failed to list directory content."

	@logDecoractor
	def do_rename(self, target): # working properly
		'''Rename a file or directory. Usage: rename <toRename> <newName>'''
		if self.connected == 0:
			return "Not connected to any server.\n\tTry connecting before trying any commands."
		try:
			target, name = target.split()[0], target.split()[1]
			self.server.rename(target, name)
			return "File {} renamed to {}.".format(target, name)
		except:
			return "Failed to rename."

	@logDecoractor
	def do_rm(self, arg):
		'''Delete a file from server. Usage rm <file or directory>'''
		if self.connected == 0:
			return "Not connected to any server.\n\tTry connecting before trying any commands."
		if arg == "":
			return "No argument given to rm command."
		try:
			self.server.delete(arg)
			return "File {} deleted.".format(arg)
		except:
			return "Failed to delete {}.".format(arg)

	@logDecoractor
	def do_dc(self, arg): # seems to be working, need more testing
		'''Disconnect from the server. Usage: dc'''
		if self.connected == 0:
			return "Not connected to any server.\n\tTry connecting before trying any commands."
		try:
			self.server.quit()
			self.connected = 0
			print("Closed connection to host {}".format(self.host))
			return "Closed connection to host {}".format(self.host)
		except error_perm or error_temp:
			return "Failed to disconnect from the server."


	def do_pwd(self, arg): #working properly
		'''Know your actual path. Usage: pwd'''
		if self.connected == 0:
			print ("Not connected to any server.\n\tTry connecting before trying any commands.")
		try:
			print(self.server.pwd())
		except:
			pass

	@logDecoractor
	def do_cd(self, path): # seems to be ok, may need more testing
		'''Move to directory. Usage: cd <path of dir>'''
		if self.connected == 0:
			return "Not connected to any server.\n\tTry connecting before trying any commands."
		try:
			if path is "":
				self.server.cwd(self.home)
			else:
				self.server.cwd(path)
			print(self.server.pwd())
			return "Moved to {}.".format(self.server.pwd())
		except:
			return "Failed to move to {}.".format(path)

	@logDecoractor
	def do_dl(self, file, savePath="./"):
		'''Download a file from the server. Usage: dl <path of file> <savePath>'''
		pwd = self.server.pwd() + '/' + file
		print (pwd)
		if self.connected == 0:
			return "Not connected to any server.\n\tTry connecting before trying any commands."
		with open(savePath + file, 'w+') as f:
			# if '.' in pwd:
				# p = pwd.split('.')[1]
			if p in EXTENSION_LIST: self.server.retrlines('RETR %s' % pwd, f.write) # A modifier
			else: self.server.retrbinary('RETR %s' & pwd, f.write)
			f.close()
			return "File {} downloaded to {}.".format(file, savePath + file)


	@logDecoractor
	def do_upload(self, file, name=""):
		'''Upload a file to the server. Usage: upload <yourfile>'''
		if self.connected == 0:
			return "Not connected to any server.\n\tTry connecting before trying any commands."
		if os.path.splitext(file)[1] in EXTENSION_LIST: self.server.storlines("STOR %s" % file, open(file))
		else: self.server.storbinary("STOR " + file, open(file, "rb"), 1024)
		return "File {} uploaded to {}.".format(file, self.server.pwd() + "/{}".format(file))

	def do_exit(self, arg):
		'''Leave the program. Usage: exit'''
		if self.connected == 1:
			self.server.quit()
			print("Disconnected from server.")
		print("Exiting.")
		sys.exit(0)

	def logFileWrite(self, msg):
		with open(self.logFile, 'w+') as fd:
			msg = str(msg)
			fd.write(msg)
			print('\n' + msg + '\n')
			fd.close()

if __name__ == '__main__':
	if len(sys.argv) >= 3:
		serv = _FTP(sys.argv[1], sys.argv[2])
	else:
		serv = _FTP()
	serv.cmdloop()
