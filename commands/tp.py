######################################
## Adventure Bot "Dennis"           ##
## commands/tp.py                   ##
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

##############
# TP Command #
##############

from helpers import *
from database import get

from help import C_HELP

def C_TP(S, DB, sender, args):
	if len(args) != 1:
		C_HELP(S, DB, sender, ["tp"])

	else:
		roomid = getroom(DB, sender)
		roominfo = roomstat(DB, roomid)
		playerinfo = playerstat(DB, sender)
		test = get(DB, "SELECT id FROM rooms WHERE id='{0}'".format(args[0])) # See if room exists.

		if len(test):
			try:
				announce_room(S, DB, roomid, "{0} teleported out of the room.".format(playerinfo["name"]))
				enterroom(DB, int(args[0]), sender) # Join new room.
				announce_room(S, DB, int(args[0]), "{0} teleported into the room.".format(playerinfo["name"]))
			except (ValueError): # Bad argument.
				C_HELP(S, DB, sender, ["tp"])

		else: # No such room.
			C_HELP(S, DB, sender, ["tp"])

