###################################
## Adventure Bot "Dennis"        ##
## commands/exit.py              ##
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

################
# Exit Command #
################

from helpers import *
from database import get, put

from help import C_HELP
from go import C_GO

def C_EXIT(S, DB, sender, args):
	if len(args) == 0:
		C_GO(S, DB, sender, [])

	elif len(args) >= 3 and args[0].lower() == "set": # Add an exit.
		roomid = getroom(DB, sender)
		roominfo = roomstat(DB, roomid)

		if roominfo["owner"] == sender or roominfo["locked"] == 0: # Do we have permission to add an exit?
			try:
				test = get(DB, "SELECT * FROM rooms WHERE id='{0}'".format(int(args[1]))) # Does the target room exist?
				if not len(test):
					send(S, sender, "The target room does not exist.")
					return

				else: # Set an exit.
					if goodname(" ".join(args[2:])):
						exits = roominfo["exits"]
						exits[" ".join(args[2:]).lower()] = int(args[1])
						put(DB, "UPDATE rooms SET exits='{0}' WHERE id='{1}'".format(obj2str(exits), roomid))
						send(S, sender, "Exit \"{0}\" leads to room ID {1}.".format(" ".join(args[2:]).lower(), int(args[1])))
					else:
						send(S, sender, "Invalid name.")
			except (ValueError):
				C_HELP(S, DB, sender, ["exit set"])

		else:
			send(S, sender, "The room is set to locked and you are not the owner.")

	elif len(args) >= 2 and args[0].lower() == "del": # Delete an exit.
		roomid = getroom(DB, sender)
		roominfo = roomstat(DB, roomid)

		if roominfo["owner"] == sender or roominfo["locked"] == 0: # Do we have permission to delete an exit?
			if " ".join(args[1:]).lower() in roominfo["exits"]: # Delete the exit.
				exits = roominfo["exits"]
				del exits[" ".join(args[1:]).lower()]
				put(DB, "UPDATE rooms SET exits='{0}' WHERE id='{1}'".format(obj2str(exits), roomid))
				send(S, sender, "Exit \"{0}\" deleted.".format(" ".join(args[1:])))
			else:
				send(S, sender, "No such exit.")

		else:
			send(S, sender, "The room is set to locked and you are not the owner.")

	elif args[0].lower() == "set":
		C_HELP(S, DB, sender, ["exit set"])
	elif args[0].lower() == "del":
		C_HELP(S, DB, sender, ["exit del"])
	else:
		C_HELP(S, DB, sender, ["exit"])

