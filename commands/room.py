###################################
## Adventure Bot "Dennis"        ##
## commands/room.py              ##
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
# Room Command #
################

from helpers import *
from database import get, put
from database import escape as E

from help import C_HELP
from look import C_LOOK

def C_ROOM(S, DB, sender, args):
	if len(args) == 0:
		C_LOOK(S, DB, sender, [])

	elif len(args) >= 3 and args[0].lower() == "set": # Modify the room.
		roomid = getroom(DB, sender)
		roominfo = roomstat(DB, roomid)

		if roominfo["owner"] == sender or roominfo["locked"] == 0: # Do we have permission to edit the room?
			if args[1].lower() == "name": # Set name.
				if goodname(" ".join(args[2:])):
					put(DB, "UPDATE rooms SET name='{0}' WHERE id='{1}'".format(E(" ".join(args[2:])), roomid))
					send(S, sender, "Name updated.")
				else:
					send(S, sender, "Invalid name.")

			elif args[1].lower() == "desc": # Set description.
				if args[2].startswith("\\\\"): # Append for long description.
					curr = get(DB, "SELECT desc FROM rooms WHERE id='{0}'".format(roomid))
					newdesc = "{0}\n{1}".format(E(curr[0][0]), E(" ".join(args[2:])[2:]))
					put(DB, "UPDATE rooms SET desc='{0}' WHERE id='{1}'".format(newdesc, roomid))
				else:
					put(DB, "UPDATE rooms SET desc='{0}' WHERE id='{1}'".format(E(" ".join(args[2:])), roomid))
				send(S, sender, "Description updated.")

			elif args[1].lower() == "lock": # Set lock flag.
				if roominfo["owner"] == sender: # Do we have permission to lock the room?
					if args[2].lower() in ["1", "true", "yes", "on"]:
						put(DB, "UPDATE rooms SET locked='1' WHERE id='{0}'".format(roomid))
						send(S, sender, "Room set to locked.")
					else:
						put(DB, "UPDATE rooms SET locked='0' WHERE id='{0}'".format(roomid))
						send(S, sender, "Room set to unlocked.")
				else:
					send(S, sender, "Only the owner can lock or unlock a room.")

			elif args[1].lower() == "owner": # Change room ownership.
				if roominfo["owner"] == sender: # Do we currently own the room?
					check = get(DB, "SELECT username FROM players WHERE username='{0}'".format(args[2].lower()))
					if check:
						put(DB, "UPDATE rooms SET owner='{0}' WHERE id='{1}'".format(args[2].lower(), roomid))
						send(S, sender, "Room ownership given to {0}.".format(args[2].lower()))
					else:
						send(S, sender, "User \"{0}\" does not exist.".format(args[2].lower()))
				else:
					send(S, sender, "Only the owner can change ownership of a room.")

			else:
				C_HELP(S, DB, sender, ["room set"])
		else:
			send(S, sender, "The room is set to locked and you are not the owner.")

	elif len(args) == 1 and args[0].lower() == "unlink": # Unlink the room.
		roomid = getroom(DB, sender)
		roominfo = roomstat(DB, roomid)

		if roominfo["owner"] == sender: # Do we have permission to unlink the room?
			rooms = get(DB, "SELECT exits,id FROM rooms") # Get list of exits from every room.

			for n, room in enumerate(rooms): # Find and delete linked exits from rooms.
				for exit in room[0]:
					if room[0][exit] == roomid:
						del rooms[n][0][exit]

			for room in rooms: # Delete exits from database.
				put(DB, "UPDATE rooms SET exits='{0}' WHERE id='{1}'".format(obj2str(room[0]), room[1]))
			put(DB, "UPDATE rooms SET name='{0}' WHERE id='{1}'".format(roominfo["name"]+" (UNLINKED)", roomid)) # Mark room unlinked.

		else:
			send(S, sender, "Only the owner can unlink a room.")

	elif args[0].lower() == "set":
		C_HELP(S, DB, sender, ["room set"])
	elif args[0].lower() == "unlink":
		C_HELP(S, DB, sender, ["room unlink"])
	else:
		C_HELP(S, DB, sender, ["room"])

