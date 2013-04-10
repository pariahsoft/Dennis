###################################
## Adventure Bot "Dennis"        ##
## commands/mkroom.py            ##
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

##################
# MKRoom Command #
##################

from helpers import *
from database import get

from help import C_HELP

def C_MKROOM(S, DB, sender, args):
	if len(args) == 0:
		C_HELP(S, DB, sender, ["mkroom"])

	else:
		rnames = get(DB, "SELECT name FROM rooms")
		for name in rnames: # Check if the room exists.
			if " ".join(args).lower() == name[0].lower():
				send(S, sender, "A room by that name already exists.")
				return

		if goodname(" ".join(args)):
			newid = newroom(DB, " ".join(args), sender)
			send(S, sender, "Created new room \"{0}\", ID {1}.".format(" ".join(args), newid))
		else:
			send(S, sender, "Invalid name.")

