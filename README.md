# SSHCMD is a command-line toolsuit to handle Odoo server operations on Debian based linux.

-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------

To install odoo, run:
	
	 sudo ./install_odoo_v9-0.sh

Some alliases:

	odoo => Start the server.
	restart => Restart the server.
	scaffold => Create a new addon folder with basic stuff inside. (Usage: scaffold <nameOfYourAddon>) 

Odoo's service can be restarted with "sudo service odoo-server restart"

-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------

ftp.py is a little FTP client written in python.

	Available command in FTPSHELL:

		[help, connect, cd, dc, dl, upload, ls, rename, rm, exit, rename]

		(Use help command for more infos)
-------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------

ssh.py is a basic SSH client written in python too using paramiko.

	Available command in SSHELL:

		[help, add, connect, run, close]

		(Use help command for more infos)
