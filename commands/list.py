########################################
## Adventure Bot "Dennis"             ##
## commands/list.py                   ##
## Copyright 2012-2013 PariahSoft LLC ##
########################################

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
# List Command #
################

from helpers import *
from database import get

def C_LIST(S, DB, sender, args):
	roomlist = get(DB, "SELECT id,name FROM rooms")

	if len(args) == 0: # List all the rooms.
		body = "Rooms: " # Rooms
		for n, room in enumerate(roomlist):
			if n < len(roomlist) - 1:
				body += room[1] + " (" + str(room[0]) + "), "
			else:
				body += room[1] + " (" + str(room[0]) + ")"
		send(S, sender, body)

	else:
		for room in roomlist:
			if room[1].lower() == " ".join(args).lower():
				send(S, sender, "{0} ({1})".format(room[1], str(room[0])))
				return
		send(S, sender, "No such room.")

