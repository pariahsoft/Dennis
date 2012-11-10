######################################
## Adventure Bot "Dennis"           ##
## commands/join.py                 ##
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
# Join Command #
################

import hashlib
from helpers import *
from database import get, put

from help import C_HELP

def C_JOIN(S, DB, sender, args):

	if len(args) != 1:
		C_HELP(S, DB, sender, ["join"])
		return

	rows = get(DB, "SELECT username FROM players WHERE username='{0}'".format(sender))
	if not len(rows): # It's a new player.
		put(DB, "INSERT INTO players (username, name, desc, room, pass) VALUES ('{0}', '{0}', ' ', '0', '{1}')".format(sender, hashlib.sha256(args[0]).hexdigest()))
		send(S, sender, "Created new player \"{0}\". Your password is \"{1}\".".format(sender, args[0]))

	passhash = get(DB, "SELECT pass FROM players WHERE username='{0}'".format(sender))
	if passhash[0][0] == hashlib.sha256(args[0]).hexdigest(): # Authenticated successfully.
		setonline(DB, sender, 1)

		roomid = getroom(DB, sender)
		enterroom(DB, roomid, sender) # Add player to their room.

		playerinfo = playerstat(DB, sender)
		send(S, sender, "Welcome, {0}.".format(playerinfo["name"])) # Greet player.
		announce(S, DB, "{0} joined the game.".format(playerinfo["name"]))
		announce_room(S, DB, roomid, "{0} entered the room.".format(playerinfo["name"]))

	else: # Bad login.
		send(S, sender, "Incorrect password for registered player.")

