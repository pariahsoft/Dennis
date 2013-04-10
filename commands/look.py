###################################
## Adventure Bot "Dennis"        ##
## commands/look.py              ##
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
# Look Command #
################

from helpers import *

def C_LOOK(S, DB, sender, args):
	roomid = getroom(DB, sender)
	roominfo = roomstat(DB, roomid)

	# ROOM #
	if len(args) == 0: # Look at the room.
		send(S, sender, "{0} ({1})".format(roominfo["name"], roomid))
		send(S, sender, "-----")
		desc = roominfo["desc"].split("\n")
		for n, dmsg in enumerate(desc):
			send(S, sender, dmsg)
			if n < len(desc) - 1:
				send(S, sender, " ")
		send(S, sender, "-----")

		# EXITS #
		exits = roominfo["exits"]
		body = "" # Build exit list.
		for n, exit in enumerate(exits.keys()):
			if len(exits.keys()) == 1:
				body += exit + "."
				break
			elif len(exits.keys()) > 1:
				if n < len(exits.keys()) - 1:
					body += exit + ", "
				else:
					body += "and " + exit + "."

		if not body: # List exits.
			send(S, sender, "There are no exits.")
		else:
			send(S, sender, "Exits are {0}".format(body))

		# ITEMS #
		items = roominfo["items"]
		body = "" # Build item list.
		for n, item in enumerate(items):
			if len(items) == 1:
				body += item["name"] + " (" + str(n) + ")."
				break
			elif len(items) > 1:
				if n < len(items) - 1:
					body += item["name"] + " (" + str(n) + "), "
				else:
					body += "and " + item["name"] + " (" + str(n) + ")."

		if not body: # List items.
			send(S, sender, "The room is empty.")
		else:
			send(S, sender, "The room contains {0}".format(body))

		# OCCUPANTS #
		occu = occupants(DB, roomid)
		body = "" # Build occupant list.
		if sender in occu:
			occu.remove(sender)
		if len(occu) == 0:
				body = "no one."
		for n, occupant in enumerate(occu):
			playerinfo = playerstat(DB, occupant)
			name = playerinfo["name"]
			if len(occu) != 0:
				if len(occu) == 1: # Yourself and one other.
					body += name + "."
				elif n < len(occu) - 1:
					body += name + ", "
				else:
					body += "and " + name + "."

		send(S, sender, "You are accompanied by {0}".format(body)) # List occupants.

		# LOCKED #
		roomowner = playerstat(DB, roominfo["owner"])
		if roominfo["locked"] == 1:
			send(S, sender, "The room is owned by {0} ({1}). It is set locked.".format(roomowner["name"], roominfo["owner"]))
		else:
			send(S, sender, "The room is owned by {0} ({1}). It is set unlocked.".format(roomowner["name"], roominfo["owner"]))

	else: # Look at something in particular.
		items = roominfo["items"]
		for n, item in enumerate(items): # Items
			if " ".join(args).lower() == item["name"].lower():
				send(S, sender, "{0} ({1})".format(item["name"], str(n)))
				send(S, sender, "-----")
				desc = item["desc"].split("\n")
				for n, dmsg in enumerate(desc):
					send(S, sender, dmsg)
					if n < len(desc) - 1:
						send(S, sender, " ")
				return

		for occupant in occupants(DB, roomid): # Occupants
			playerinfo = playerstat(DB, occupant)
			if " ".join(args).lower() == playerinfo["name"].lower() or " ".join(args).lower() == occupant:
				send(S, sender, "{0} ({1})".format(playerinfo["name"], occupant))
				send(S, sender, "-----")
				desc = playerinfo["desc"].split("\n")
				for n, dmsg in enumerate(desc):
					send(S, sender, dmsg)
					if n < len(desc) - 1:
						send(S, sender, " ")
				return

		send(S, sender, "I don't see {0} here.".format(" ".join(args)))

