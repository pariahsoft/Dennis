###################################
## Adventure Bot "Dennis"        ##
## commands/help.py              ##
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
# Help Command #
################

from helpers import *

def C_HELP(S, DB, sender, args):
	if len(args) == 0: # List commands.
		body = "Commands: "
		for n, h in enumerate(help_entries):
			if n < len(help_entries) - 1:
				body += h[0] + ", "
			else:
				body += h[0]
		send(S, sender, body)

	else: # Look for this command.
		body = ""
		for h in help_entries:
			if h[0].lower() == " ".join(args).lower(): # Return command help.
				body = "{0}: {1}".format(h[1], h[2])
				send(S, sender, body)
				return
		C_HELP(S, DB, sender, ["help"])

### Help Entries ###

help_entries = [
	["help", "help [command]", "List commands or give usage for specified command."],
	["join", "join <pass>", "Authenticate and join the game. Creates account with pass on first join."],
	["quit", "quit", "Leave the game."],
	["say", "say <text>", "Say something in the current room's chat."],
	["shout", "shout <text>", "Say something in the entire world's chat."],
	["roll", "roll <min> <max>", "Roll a random number between min and max."],
	["me", "me <text>", "Perform an action in the current room's chat."],
	["look", "look [item|player]", "Look at current room, or specified item or player."],
	["go", "go [exit]", "List exits in current room or use specified exit."],
	["list", "list [name]", "List all rooms, or return the ID of the named room."],
	["self", "self", "Look at yourself."],
	["self SET", "self SET name|desc <text>", "Set your own name or description."],
	["mkroom", "mkroom <name>", "Create a new named room and return its ID."],
	["room", "room", "Look at the current room."],
	["room SET", "room SET name|desc|lock|owner <text>", "Set current room's name, description, lock flag, or owner."],
	["room UNLINK", "room UNLINK", "Remove all exits to the current room. Must be room owner."],
	["exit", "exit", "List the current room's exits."],
	["exit SET", "exit SET <id> <name>", "Create named exit in current room to specified room ID."],
	["exit DEL", "exit DEL <name>", "Delete the named exit from current room."],
	["mkitem", "mkitem <name>", "Create a new named item and return its ID."],
	["item", "item", "List items in current room."],
	["item SET", "item SET <id> name|desc <text>", "Set the item's name or description."],
	["item DEL", "item DEL <id>", "Delete the named item from current room."],
	["tp", "tp <id>", "Warp to the specified room by ID."],
	["version", "version", "Print bot info and version."],
]

