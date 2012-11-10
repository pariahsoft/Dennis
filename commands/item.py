######################################
## Adventure Bot "Dennis"           ##
## commands/item.py                 ##
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
# Item Command #
################

from helpers import *
from database import put

from help import C_HELP

def C_ITEM(S, DB, sender, args):
	roomid = getroom(DB, sender)
	roominfo = roomstat(DB, roomid)

	if len(args) == 0:
		body = ""

		for n, item in enumerate(roominfo["items"]): # Build item list.
			if len(roominfo["items"]) == 1:
				body += item["name"] + " (" + str(n) + ")."

			elif len(roominfo["items"]) > 1:
				if n < len(roominfo["items"]) - 1:
					body += item["name"] + " ("+  str(n) + "), "
				else:
					body += "and " + item["name"] + " (" + str(n) + ")."

		if not body: # List items.
			send(S, sender, "The room is empty.")
		else:
			send(S, sender, "The room contains {0}".format(body))

	elif len(args) >= 4 and args[0].lower() == "set": # Modify an item.
		if roominfo["owner"] == sender or roominfo["locked"] == 0: # Do we have permission to modify an item?

			if args[2].lower() == "name": # Set name.
				for item in roominfo["items"]: # Check if name is taken.
					if " ".join(args[3:]).lower() == item["name"].lower():
						send(S, sender, "An item by that name already exists.")
						return

				if goodname(" ".join(args[3:])): # Update the name.
					try:
						items = roominfo["items"]
						items[int(args[1])]["name"] = " ".join(args[3:])
						put(DB, "UPDATE rooms SET items='{0}' WHERE id='{1}'".format(obj2str(items), roomid))
						send(S, sender, "Name updated.")
					except (ValueError, IndexError):
						C_HELP(S, DB, sender, ["item set"])

				else:
					send(S, sender, "Invalid name.")

			elif args[2].lower() == "desc": # Update the description.
				try:
					items = roominfo["items"]
					if args[3].startswith("\\\\"): # Append for long description.
						curr = items[int(args[1])]["desc"]
						newdesc = "{0}\n{1}".format(curr[0][0], " ".join(args[3:])[2:])
						items[int(args[1])]["desc"] = newdesc
					else:
						items[int(args[1])]["desc"] = " ".join(args[3:])
					put(DB, "UPDATE rooms SET items='{0}' WHERE id='{1}'".format(obj2str(items), roomid))
					send(S, sender, "Description updated.")
				except (ValueError, IndexError):
					C_HELP(S, DB, sender, ["item set"])

			else:
				C_HELP(S, DB, sender, ["item set"])

	elif len(args) == 2 and args[0].lower() == "del": # Delete an item.
		if roominfo["owner"] == sender or roominfo["locked"] == 0: # Do we have permission to delete an item?

			try: # Update item list.
				items = roominfo["items"]
				items.pop(int(args[1]))
				put(DB, "UPDATE rooms SET items='{0}' WHERE id='{1}'".format(obj2str(items), roomid))
				send(S, sender, "Item ID {0} deleted.".format(args[1]))
			except (ValueError, IndexError):
				C_HELP(S, DB, sender, ["item del"])

	elif args[0].lower() == "set":
		C_HELP(S, DB, sender, ["item set"])
	elif args[0].lower() == "del":
		C_HELP(S, DB, sender, ["item del"])
	else:
		C_HELP(S, DB, sender, ["item"])

