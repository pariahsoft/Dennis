#!/usr/bin/env python
######################################
## Adventure Bot "Dennis"           ##
## dennis.py                        ##
## Copyright 2012 Michael D. Reiley ##
######################################

## **********
## Permission is hereby granted, free of charge, to any person obtaining a copy 
## of this software and associated documentation files (the "Software"), to 
## deal in the Software without restriction, including without limitation the 
## rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
## sell copies of the Software, and to permit persons to whom the Software is 
## furnished to do so, subject to the following conditions:
##
## The above copyright notice and this permission notice shall be included in 
## all copies or substantial portions of the Software.
##
## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS 
## IN THE SOFTWARE.
## **********

################
# Main Program #
################

import socket, time, sqlite3, time, sys, signal
import config, console
from database import opendb, put

### INTERNAL VARIABLES ###

linebuf = [] # Data Buffer
DB = sqlite3.Connection # Convenient Hackery

def sigint_handler(signum, frame): # Kick off all the users before killing the bot.
	print "[{0}] Shutting down.".format(int(time.time()))
	put(DB, "UPDATE players SET online='0'") # Set all users offline.
	sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

### IRC FUNCTIONS ###

def connect(S): # Connect to server.
	global linebuf
	while True:
		try:
			S.connect((config.server[0], config.server[1]))
			S.setblocking(0)
			S.send('NICK '+config.nick+'\r\n')
			if receive(S, 1) == "BADNICK": # Nick is in use.
				print "[{0}] Nickname \"{1}\" is in use.".format(int(time.time()), config.nick)
				S.close()
				return False
			if config.server[2]: # Server has a password.
				S.send('PASS {0}\r\n'.format(config.server[2]))
			S.send('USER {0} 8 * :{1}\r\n'.format(config.user, config.real))
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
					S.send('MODE {0} +B\r\n'.format(config.nick))
					if config.nickpass:
						S.send('PRIVMSG NICKSERV :IDENTIFY {0}\r\n'.format(config.nickpass)) #Identify with nickserv.
					for chan in config.channels: # Join channels.
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

	console.process(S, DB, line, config.nick) # Pass the line to the console.

### MAIN ###

def main():
	global DB
	DB = opendb(config.worldfile)

	socket.setdefaulttimeout(config.timeout)
	S = socket.socket()

	print "[{0}] Starting up.".format(int(time.time()))

	if not connect(S): # Connection failed.
		print "[{0}] Connection failed.".format(int(time.time()))
		S.close()
		DB.close()
		time.sleep(config.retryrate) # Wait a bit.
		print "[{0}] Retrying connection.".format(int(time.time()))
		main() # Try again.

	while True: # Main Loop
		receive(S)
		time.sleep(0.04) # 1/25 Second. Let's not be too conspicuous.

main() # Start Dennis.

