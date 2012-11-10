######################################
## Adventure Bot "Dennis"           ##
## commands/mkitem.py               ##
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

##################
# MKItem Command #
##################

from helpers import *
from database import put

from help import C_HELP

def C_MKITEM(S, DB, sender, args):
	if len(args) == 0:
		C_HELP(S, DB, sender, ["mkitem"])

	else:
		roomid = getroom(DB, sender)
		roominfo = roomstat(DB, roomid)

		if roominfo["owner"] == sender or roominfo["locked"] == 0: # Do we have permission to modify an item?
			for item in roominfo["items"]: # Check if the item exists.
				if " ".join(args).lower() == item["name"].lower():
					send(S, sender, "An item by that name already exists.")
					return

			if goodname(" ".join(args)): # Add the new item.
				items = roominfo["items"]
				items.append({"name": " ".join(args), "desc": " "})
				put(DB, "UPDATE rooms SET items='{0}' WHERE id='{1}'".format(obj2str(items), roomid))
				send(S, sender, "Created new item \"{0}\", ID {1}.".format(" ".join(args), len(items)-1))
			else:
				send(S, sender, "Invalid name.")

