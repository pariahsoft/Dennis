# Adventure Bot "Dennis" IRC Bot Core
# Copyright 2012 Michael D. Reiley and OmegaSDG <http://omegasdg.com>
# Released under the MIT/Expat License.

import socket, time, sqlite3, time, sys, signal, dennis
from database import opendb, put

### INTERNAL VARIABLES ###

conf = {} # Configuration
linebuf = [] # Data Buffer
DB = sqlite3.Connection # Convenient Hackery

def sigint_handler(signum, frame): # Kick off all the users before killing the bot.
	print "[{0}] Shutting down.".format(int(time.time()))
	put(DB, "UPDATE rooms SET occupants='gAJdcQAu'") # Remove occupants from all rooms.
	put(DB, "UPDATE players SET online='0'") # Set all users offline.
	sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

### IRC FUNCTIONS ###

def connect(S): # Connect to server.
	global linebuf
	while True:
		try:
			S.connect((conf["server"][0], conf["server"][1]))
			S.setblocking(0)
			S.send('NICK '+conf["nick"]+'\r\n')
			if receive(S, 1) == "BADNICK": # Nick is in use.
				print "[{0}] Nickname \"{1}\" is in use.".format(int(time.time()), conf["nick"])
				S.close()
				return False
			if conf["server"][2]: # Server has a password.
				S.send('PASS {0}\r\n'.format(conf["server"][2]))
			S.send('USER {0} 8 * :{1}\r\n'.format(conf["user"], conf["real"]))
			return True # We were able to connect.
		except socket.error:
			return False

def receive(S, opt = 0): # Receive data.
	global linebuf
	ret = True
	buf = ''
	try:
		buf = S.recv(32)
		while not buf.endswith('\n'):
			buf += S.recv(32)
		linebuf.extend(buf.split('\n')) # Buffer server messages.
	except socket.error: # Nothing was received.
		return

	for line in linebuf:
		if len(line) > 0: # You've got mail!
			try:
				if opt == 1:
					if line.split(' ')[1] == "443": # Nick is in use.
						ret = "BADNICK"
				elif line.split(' ')[1] == "002": # We're connected.
					print "[{0}] Connected successfully.".format(int(time.time()))
					S.send('MODE {0} +B\r\n'.format(conf["nick"]))
					if conf["nickpass"]:
						S.send('PRIVMSG NICKSERV :IDENTIFY {0}\r\n'.format(conf["nickpass"])) #Identify with nickserv.
					for chan in conf["channels"]: # Join channels.
						if len(chan):
							S.send('JOIN {0} {1}\r\n'.format(chan[0], chan[1]))
							print "[{0}] Joined channel \"{1}\".".format(int(time.time()), chan[0])
				else:
					process(S, line)
			except (IndexError):
				pass

	linebuf = [] # Clear buffer.
	return ret

def process(S, line):
	if line[0:4] == 'PING': # Ping received.
		print "[{0}] Received ping from server.".format(int(time.time()))
		S.send('PONG {0}\r\n'.format(line[5:])) # Respond with pong.

	dennis.process(S, DB, line, conf["nick"]) # Start Dennis.

### MAIN ###

def run(CONFIG):
	global conf, DB
	conf = CONFIG
	DB = opendb(conf["worldfile"])

	socket.setdefaulttimeout(conf["timeout"])
	S = socket.socket()
	
	print "[{0}] Starting up.".format(int(time.time()))

	if not connect(S): # Connection failed.
		print "[{0}] Connection failed.".format(int(time.time()))
		S.close()
		DB.close()
		time.sleep(conf["retryrate"]) # Wait a bit.
		print "[{0}] Retrying connection.".format(int(time.time()))
		run(CONFIG) # Try again.

	while True: # Main Loop
		receive(S)
		time.sleep(0.04) # 1/25 Second. Let's not be too conspicuous.

