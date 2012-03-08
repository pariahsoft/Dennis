# Adventure Bot "Dennis" Functions
# Copyright 2012 Michael D. Reiley and OmegaSDG <http://omegasdg.com>
# Released under the MIT/Expat License.

import socket, time, random, hashlib
from database import get, put
from database import escape as E
from helpers import *

### Version Info ###

VERSION = [
	"{0} {1}\nBy {2}\n{3} {4} {5}",
	"Adventure Bot \"Dennis\"",
	"Pre-Alpha",
	"Michael D. Reiley",
	"Copyright (c) 2012",
	"Omega Software Development Group",
	"<omegasdg.com>"
]

### Help Entries ###

help = [
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
	["room SET", "room SET name|desc|lock <text>", "Set current room's name, description, or lock flag."],
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

### ADVENTURE FUNCTIONS ###

## CONSOLE INPUT PROCESSOR ##

def process(S, DB, line, nick):
	global info
	
	for char in line:
		if not char in string.printable: # Ignore weird characters.
			line = line.replace(char, "")

	complete = line[1:].split(':',1) # Split message into sections
	info = complete[0].split(' ') # Pieces of message

	try:
		info[1]
		msgpart=complete[1].rstrip()
	except IndexError: # Fake line
		return

	sender = info[0].split('!')[0] # Sender info

	if info[1].lower() == "quit": # Did a player leave IRC?
		rows = get(DB, "SELECT username FROM players WHERE online='1'")
		for player in rows:
			if player[0] == sender.lower():
				C_QUIT(S, DB, sender, [])
				break

	if len(msgpart) > 0 and len(info) >= 3 and info[1].lower() == "privmsg" and info[2].lower() == nick.lower(): # Commands
			cmd = msgpart.rstrip().split(' ')
			if cmd[0].lower() != "join":
				print "[{0}] <{1}> :: {2}".format(int(time.time()), sender, msgpart.rstrip())

			if cmd[0].lower() == "help":
				C_HELP(S, DB, sender.lower(), cmd[1:])
			elif cmd[0].lower() == "join":
				C_JOIN(S, DB, sender.lower(), cmd[1:])
			elif cmd[0].lower() == "version":
				C_VERSION(S, DB, sender.lower(), cmd[1:])
			elif online(DB, sender.lower()): # Online Commands
				if cmd[0].lower() == "quit":
					C_QUIT(S, DB, sender.lower(), cmd[1:])
				elif cmd[0].lower() == "say":
					C_SAY(S, DB, sender.lower(), cmd[1:])
				elif cmd[0].lower() == "shout":
					C_SHOUT(S, DB, sender.lower(), cmd[1:])
				elif cmd[0].lower() == "roll":
					C_ROLL(S, DB, sender.lower(), cmd[1:])
				elif cmd[0].lower() == "me":
					C_ME(S, DB, sender.lower(), cmd[1:])
				elif cmd[0].lower() == "look":
					C_LOOK(S, DB, sender.lower(), cmd[1:])
				elif cmd[0].lower() == "go":
					C_GO(S, DB, sender.lower(), cmd[1:])
				elif cmd[0].lower() == "list":
					C_LIST(S, DB, sender.lower(), cmd[1:])
				elif cmd[0].lower() == "self":
					C_SELF(S, DB, sender.lower(), cmd[1:])
				elif cmd[0].lower() == "mkroom":
					C_MKROOM(S, DB, sender.lower(), cmd[1:])
				elif cmd[0].lower() == "room":
					C_ROOM(S, DB, sender.lower(), cmd[1:])
				elif cmd[0].lower() == "exit":
					C_EXIT(S, DB, sender.lower(), cmd[1:])
				elif cmd[0].lower() == "mkitem":
					C_MKITEM(S, DB, sender.lower(), cmd[1:])
				elif cmd[0].lower() == "item":
					C_ITEM(S, DB, sender.lower(), cmd[1:])
				elif cmd[0].lower() == "tp":
					C_TP(S, DB, sender.lower(), cmd[1:])
				else:
					C_HELP(S, DB, sender.lower(), ["help"])
			else:
				send(S, sender, "No such command or you must join first.")

## HELP COMMAND ##

def C_HELP(S, DB, sender, args):
	if len(args) == 0: # List commands.
		body = "Commands: "
		for n, h in enumerate(help):
			if n < len(help) - 1:
				body += h[0] + ", "
			else:
				body += h[0]
		send(S, sender, body)

	else: # Look for this command.
		body = ""
		for h in help:
			if h[0].lower() == " ".join(args).lower(): # Return command help.
				body = "{0}: {1}".format(h[1], h[2])
				send(S, sender, body)
				return
		C_HELP(S, DB, sender, ["help"])

## JOIN COMMAND ##

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
		send(S, sender, "Your password was incorrect.")

## QUIT COMMAND ##

def C_QUIT(S, DB, sender, args):
	if len(args) != 0:
		C_HELP(S, DB, sender, ["quit"])
		return

	setonline(DB, sender, 0)

	roomid = getroom(DB, sender)
	leaveroom(DB, roomid, sender) # Remove player from their room.

	playerinfo = playerstat(DB, sender)
	send(S, sender, "Goodbye, {0}.".format(playerinfo["name"])) # Say goodbye.
	announce(S, DB, "{0} left the game.".format(playerinfo["name"]))
	announce_room(S, DB, roomid, "{0} left the room.".format(playerinfo["name"]))

## SAY COMMAND ##

def C_SAY(S, DB, sender, args):
	if len(args) == 0:
		C_HELP(S, DB, sender, ["say"])
		return

	roomid = getroom(DB, sender)
	playerinfo = playerstat(DB, sender)
	announce_room(S, DB, roomid, "<{0}> {1}".format(playerinfo["name"], " ".join(args)))

## SHOUT COMMAND ##

def C_SHOUT(S, DB, sender, args):
	if len(args) == 0:
		C_HELP(S, DB, sender, ["shout"])
		return

	playerinfo = playerstat(DB, sender)
	announce(S, DB, "<<<{0}>>> {1}".format(playerinfo["name"], " ".join(args)))

## ROLL COMMAND ##

def C_ROLL(S, DB, sender, args):
	if len(args) != 2:
		C_HELP(S, DB, sender, ["roll"])
		return

	roomid = getroom(DB, sender)
	playerinfo = playerstat(DB, sender)
	try:
		announce_room(S, DB, roomid, "{0} rolled {1} out of {2} to {3}.".format(playerinfo["name"], random.randint(int(args[0]), int(args[1])), int(args[0]), int(args[1])))
	except (ValueError):
		C_HELP(S, DB, sender, ["roll"])

## ME COMMAND ##

def C_ME(S, DB, sender, args):
	if len(args) == 0:
		C_HELP(S, DB, sender, ["me"])
		return

	roomid = getroom(DB, sender)
	playerinfo = playerstat(DB, sender)
	announce_room(S, DB, roomid, "* {0} {1}".format(playerinfo["name"], " ".join(args)))

## LOOK COMMAND ##

def C_LOOK(S, DB, sender, args):
	roomid = getroom(DB, sender)
	roominfo = roomstat(DB, roomid)

	# ROOM #
	if len(args) == 0: # Look at the room.
		send(S, sender, "{0} ({1})".format(roominfo["name"], roomid))
		send(S, sender, "-----")
		send(S, sender, "{0}".format(roominfo["desc"]))
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
		occu = roominfo["occupants"]
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
		roomowner = playerstat(DB, roominfo["owner"])["name"]
		if roominfo["locked"] == 1:
			send(S, sender, "The room is owned by {0}. It is set locked.".format(roomowner))
		else:
			send(S, sender, "The room is owned by {0}. It is set unlocked.".format(roomowner))

	else: # Look at something in particular.
		items = roominfo["items"]
		for n, item in enumerate(items): # Items
			if " ".join(args).lower() == item["name"].lower():
				send(S, sender, "{0} ({1})".format(item["name"], str(n)))
				send(S, sender, "-----")
				send(S, sender, "{0}".format(item["desc"]))
				return

		for occupant in roominfo["occupants"]: # Occupants
			playerinfo = playerstat(DB, occupant)
			if " ".join(args).lower() == playerinfo["name"].lower() or " ".join(args).lower() == occupant:
				send(S, sender, "{0} ({1})".format(playerinfo["name"], occupant))
				send(S, sender, "-----")
				send(S, sender, "{0}".format(playerinfo["desc"]))
				return

		send(S, sender, "I don't see {0} here.".format(" ".join(args)))

## GO COMMAND ##

def C_GO(S, DB, sender, args):
	roomid = getroom(DB, sender)
	roominfo = roomstat(DB, roomid)

	if len(args) == 0: # Just list all the exits.
		body = "" # Build exit list.
		for n, exit in enumerate(roominfo["exits"].keys()):
			if len(roominfo["exits"].keys()) == 1:
				body += exit + "."
				break
			elif len(roominfo["exits"].keys()) > 1:
				if n < len(roominfo["exits"].keys()) - 1:
					body += exit + ", "
				else:
					body += "and " + exit + "."

		if not body: # List exits.
			send(S, sender, "There are no exits.")
		else:
			send(S, sender, "Exits are {0}".format(body))

	else:
		if " ".join(args).lower() in roominfo["exits"].keys():
			leaveroom(DB, roomid, sender)# Leave current room.

			playerinfo = playerstat(DB, sender) # Announce player's exit.
			announce_room(S, DB, roomid, "{0} exited {1}.".format(playerinfo["name"], " ".join(args).lower()))

			enterroom(DB, roominfo["exits"][" ".join(args).lower()], sender) # Enter new room.
			
			roomid = roominfo["exits"][" ".join(args).lower()]
			announce_room(S, DB, roomid, "{0} entered the room.".format(playerinfo["name"])) # Announce entrance.

		else:
			send(S, sender, "No such exit.")

## LIST COMMAND ##

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

## SELF COMMAND ##

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
			put(DB, "UPDATE players SET desc='{0}' WHERE username='{1}'".format(E(" ".join(args[2:])), sender))
			send(S, sender, "Description updated.")
		else:
			C_HELP(S, DB, sender, ["self set"])

	elif args[0].lower() == "set":
		C_HELP(S, DB, sender, ["self set"])
	else:
		C_HELP(S, DB, sender, ["self"])

## MKROOM COMMAND ##

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

## ROOM COMMAND ##

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

### EXIT COMMAND ###

def C_EXIT(S, DB, sender, args):
	if len(args) == 0:
		C_GO(S, DB, sender, [])

	elif len(args) >= 3 and args[0].lower() == "set": # Add an exit.
		roomid = getroom(DB, sender)
		roominfo = roomstat(DB, roomid)

		if roominfo["owner"] == sender or roominfo["locked"] == 0: # Do we have permission to add an exit?
			try:
				test = get(DB, "SELECT * FROM rooms WHERE id='{0}'".format(int(args[1]))) # Does the target room exist?
				if not len(test):
					send(S, sender, "The target room does not exist.")
					return

				else: # Set an exit.
					if goodname(" ".join(args[2:])):
						exits = roominfo["exits"]
						exits[" ".join(args[2:]).lower()] = int(args[1])
						put(DB, "UPDATE rooms SET exits='{0}' WHERE id='{1}'".format(obj2str(exits), roomid))
						send(S, sender, "Exit \"{0}\" leads to room ID {1}.".format(" ".join(args[2:]).lower(), int(args[1])))
					else:
						send(S, sender, "Invalid name.")
			except (ValueError):
				C_HELP(S, DB, sender, ["exit set"])

		else:
			send(S, sender, "The room is set to locked and you are not the owner.")

	elif len(args) >= 2 and args[0].lower() == "del": # Delete an exit.
		roomid = getroom(DB, sender)
		roominfo = roomstat(DB, roomid)

		if roominfo["owner"] == sender or roominfo["locked"] == 0: # Do we have permission to delete an exit?
			if " ".join(args[1:]).lower() in roominfo["exits"]: # Delete the exit.
				exits = roominfo["exits"]
				del exits[" ".join(args[1:]).lower()]
				put(DB, "UPDATE rooms SET exits='{0}' WHERE id='{1}'".format(obj2str(exits), roomid))
				send(S, sender, "Exit \"{0}\" deleted.".format(" ".join(args[1:])))
			else:
				send(S, sender, "No such exit.")

		else:
			send(S, sender, "The room is set to locked and you are not the owner.")

	elif args[0].lower() == "set":
		C_HELP(S, DB, sender, ["exit set"])
	elif args[0].lower() == "del":
		C_HELP(S, DB, sender, ["exit del"])
	else:
		C_HELP(S, DB, sender, ["exit"])

## MKITEM COMMAND ##

def C_MKITEM(S, DB, sender, args):
	if len(args) == 0:
		C_HELP(S, DB, sender, ["mkitem"])

	else:
		roomid = getroom(DB, sender)
		roominfo = roomstat(DB, roomid)

		if roominfo["owner"] == sender or roominfo["locked"] == 0: # Do we have permission to modify an item?
			for item in roominfo["items"]: # Check if the item exists.
				if " ".join(args[3:]).lower() == item["name"].lower():
					send(S, sender, "An item by that name already exists.")
					return

			if goodname(" ".join(args)): # Add the new item.
				items = roominfo["items"]
				items.append({"name": " ".join(args), "desc": " "})
				put(DB, "UPDATE rooms SET items='{0}' WHERE id='{1}'".format(obj2str(items), roomid))
				send(S, sender, "Created new item \"{0}\", ID {1}.".format(" ".join(args), len(items)-1))
			else:
				send(S, sender, "Invalid name.")

## ITEM COMMAND ##

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

## TP COMMAND ##

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
				leaveroom(DB, roomid, sender) # Leave this room.
				announce_room(S, DB, roomid, "{0} teleported out of the room.".format(playerinfo["name"]))
				enterroom(DB, int(args[0]), sender) # Join new room.
				announce_room(S, DB, int(args[0]), "{0} teleported into the room.".format(playerinfo["name"]))
			except (ValueError): # Bad argument.
				C_HELP(S, DB, sender, ["tp"])

		else: # No such room.
			C_HELP(S, DB, sender, ["tp"])

## VERSION COMMAND ##

def C_VERSION(S, DB, sender, args):
	if len(args):
		C_HELP(S, DB, sender, ["VERSION"])
		return

	vmsg = VERSION[0].format(*VERSION[1:]).split("\n")

	for line in vmsg:
		send(S, sender, line)
	
