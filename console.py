######################################
## Adventure Bot "Dennis"           ##
## console.py                       ##
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

####################
# Console Handling #
####################

import socket, string, time
from database import get
from helpers import *

### Command Imports ###

from commands.help    import C_HELP, help_entries
from commands.version import C_VERSION, version_info
from commands.join    import C_JOIN
from commands.quit    import C_QUIT
from commands.say     import C_SAY
from commands.shout   import C_SHOUT
from commands.roll    import C_ROLL
from commands.me      import C_ME
from commands.look    import C_LOOK
from commands.go      import C_GO
from commands.list    import C_LIST
from commands.self    import C_SELF
from commands.mkroom  import C_MKROOM
from commands.room    import C_ROOM
from commands.exit    import C_EXIT
from commands.mkitem  import C_MKITEM
from commands.item    import C_ITEM
from commands.tp      import C_TP

### Command Hooks ###

CH_OFFLINE = { # Offline Commands
	"help":    C_HELP,
	"version": C_VERSION,
	"join":    C_JOIN
}

CH_ONLINE = { # Online Commands
	"quit":   C_QUIT,
	"say":    C_SAY,
	"shout":  C_SHOUT,
	"roll":   C_ROLL,
	"me":     C_ME,
	"look":   C_LOOK,
	"go":     C_GO,
	"list":   C_LIST,
	"self":   C_SELF,
	"mkroom": C_MKROOM,
	"room":   C_ROOM,
	"exit":   C_EXIT,
	"mkitem": C_MKITEM,
	"item":   C_ITEM,
	"tp":     C_TP
}

### Console Input Processor ###

def process(S, DB, line, nick):
	global info

	for char in line:
		if not char in string.printable: # Ignore weird characters.
			line = line.replace(char, "")

	complete = line[1:].split(':',1) # Split message into sections
	info = complete[0].split(' ') # Pieces of message

	try:
		info[1]
		msgpart=complete[1].rstrip()
	except IndexError: # Fake line
		return

	sender = info[0].split('!')[0] # Sender info

	if info[1].lower() == "quit": # Did a player leave IRC?
		rows = get(DB, "SELECT username FROM players WHERE online='1'")
		for player in rows:
			if player[0] == sender.lower():
				C_QUIT(S, DB, sender, [])
				break

	if len(msgpart) > 0 and len(info) >= 3 and info[1].lower() == "privmsg" and info[2].lower() == nick.lower(): # Commands
			cmd = msgpart.rstrip().split(' ')
			if cmd[0].lower() != "join":
				print "[{0}] <{1}> :: {2}".format(int(time.time()), sender, msgpart.rstrip())

			if cmd[0].lower() in CH_OFFLINE: # Offline Commands
				CH_OFFLINE[cmd[0].lower()](S, DB, sender.lower(), cmd[1:])
			elif online(DB, sender.lower()): # Online Commands
				if cmd[0].lower() in CH_ONLINE:
					CH_ONLINE[cmd[0].lower()](S, DB, sender.lower(), cmd[1:])
			else:
				send(S, sender, "No such command or you must join first.")

