###################################
## Adventure Bot "Dennis"        ##
## commands/go.py                ##
## Copyright 2013 PariahSoft LLC ##
###################################

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

##############
# Go Command #
##############

from helpers import *

def C_GO(S, DB, sender, args):
	roomid = getroom(DB, sender)
	roominfo = roomstat(DB, roomid)

	if len(args) == 0: # Just list all the exits.
		body = "" # Build exit list.
		for n, exit in enumerate(roominfo["exits"].keys()):
			if len(roominfo["exits"].keys()) == 1:
				body += exit + "."
				break
			elif len(roominfo["exits"].keys()) > 1:
				if n < len(roominfo["exits"].keys()) - 1:
					body += exit + ", "
				else:
					body += "and " + exit + "."

		if not body: # List exits.
			send(S, sender, "There are no exits.")
		else:
			send(S, sender, "Exits are {0}".format(body))

	else:
		if " ".join(args).lower() in roominfo["exits"].keys():
			playerinfo = playerstat(DB, sender) # Announce player's exit.
			announce_room(S, DB, roomid, "{0} used exit \"{1}\".".format(playerinfo["name"], " ".join(args).lower()))

			enterroom(DB, roominfo["exits"][" ".join(args).lower()], sender) # Enter new room.

			roomid = roominfo["exits"][" ".join(args).lower()]
			announce_room(S, DB, roomid, "{0} entered the room.".format(playerinfo["name"])) # Announce entrance.

		else:
			send(S, sender, "No such exit.")

