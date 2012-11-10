######################################
## Adventure Bot "Dennis"           ##
## commands/self.py                 ##
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
# Self Command #
################

from helpers import *
from database import get, put
from database import escape as E

from help import C_HELP
from look import C_LOOK

def C_SELF(S, DB, sender, args):
	if len(args) == 0: # Look at youself.
		C_LOOK(S, DB, sender, [sender])

	elif len(args) >= 3 and args[0].lower() == "set": # Modify yourself.
		if args[1].lower() == "name": # Set name.
			pnames = get(DB, "SELECT name FROM players")
			for name in pnames: # Check if name is taken.
				if " ".join(args[2:]).lower() == name[0].lower():
					send(S, sender, "A player by that name already exists.")
					return

			if goodname(" ".join(args[2:])):
				put(DB, "UPDATE players SET name='{0}' WHERE username='{1}'".format(E(" ".join(args[2:])), sender))
				send(S, sender, "Name updated.")
			else:
				send(S, sender, "Invalid name.")

		elif args[1].lower() == "desc": # Set description.
			if args[2].startswith("\\\\"): # Append for long description.
				curr = get(DB, "SELECT desc FROM players WHERE username='{0}'".format(sender))
				newdesc = "{0}\n{1}".format(E(curr[0][0]), E(" ".join(args[2:])[2:]))
				put(DB, "UPDATE players SET desc='{0}' WHERE username='{1}'".format(newdesc, sender))
			else:
				put(DB, "UPDATE players SET desc='{0}' WHERE username='{1}'".format(E(" ".join(args[2:])), sender))
			send(S, sender, "Description updated.")
		else:
			C_HELP(S, DB, sender, ["self set"])

	elif args[0].lower() == "set":
		C_HELP(S, DB, sender, ["self set"])
	else:
		C_HELP(S, DB, sender, ["self"])

