# Adventure Bot "Dennis" Helper Functions
# Copyright 2012 Michael D. Reiley and OmegaSDG <http://omegasdg.com>
# Released under the MIT/Expat License.

import string, pickle, base64
from database import get, put

### INTERNAL VARIABLES ###

# Minimum acceptable name size.
minname = 2

# Maximum acceptable name size.
maxname = 32

# Characters allowed in a name. (whitelist)
allowednamechars = string.ascii_letters + string.digits + string.punctuation + string.whitespace

# Characters disallowed in a name. (blacklist)
badnamechars = "{}[]<>()|\\*"

### Helper Functions ###

# Check if a player name is allowed.
def goodname(name):
	if len(name) > maxname:
		return False
	if len(name) < minname:
		return False
	for char in name:
		if not char in allowednamechars:
			return False
	for char in name:
		if char in badnamechars:
			return False
	return True

# Send a message to a player.
def send(S, sender, mesg):
	S.send("PRIVMSG {0} :{1}\n".format(sender, mesg))

# Check if player is signed in.
def online(DB, player):
	rows = get(DB, "SELECT online FROM players WHERE username='{0}'".format(player))
	if len(rows) and rows[0][0]:
		return True
	else:
		return False

# Set player's online status.
def setonline(DB, player, status):
	put(DB, "UPDATE players SET online='{0}' WHERE username='{1}'".format(status, player))

# Find which room a player is in.
def getroom(DB, player):
	return get(DB, "SELECT room FROM players WHERE username='{0}'".format(player))[0][0]

# Get room info by ID.
def roomstat(DB, room):
	name = get(DB, "SELECT name FROM rooms WHERE id='{0}'".format(room))[0][0]
	desc = get(DB, "SELECT desc FROM rooms WHERE id='{0}'".format(room))[0][0]
	owner = get(DB, "SELECT owner FROM rooms WHERE id='{0}'".format(room))[0][0]
	occupants = str2obj(get(DB, "SELECT occupants FROM rooms WHERE id='{0}'".format(room))[0][0])
	exits = str2obj(get(DB, "SELECT exits FROM rooms WHERE id='{0}'".format(room))[0][0])
	items = str2obj(get(DB, "SELECT items FROM rooms WHERE id='{0}'".format(room))[0][0])
	locked = get(DB, "SELECT locked FROM rooms WHERE id='{0}'".format(room))[0][0]

	return {"name": name, "desc": desc, "owner": owner, "occupants": occupants,
		"exits": exits, "items": items, "locked": locked}

# Get player info by username.
def playerstat(DB, player):
	name = get(DB, "SELECT name FROM players WHERE username='{0}'".format(player))[0][0]
	desc = get(DB, "SELECT desc FROM players WHERE username='{0}'".format(player))[0][0]
	online = get(DB, "SELECT online FROM players WHERE username='{0}'".format(player))[0][0]
	room = get(DB, "SELECT room FROM players WHERE username='{0}'".format(player))[0][0]

	return {"name": name, "desc": desc, "online": online, "room": room}

# Make player leave a room.
def leaveroom(DB, room, player):
	roominfo = roomstat(DB, room) # Get current room info.

	if player in roominfo["occupants"]: # Remove player from room's occupants.
		occu = roominfo["occupants"]
		occu.remove(player)
		occu = obj2str(occu)
		put(DB, "UPDATE rooms SET occupants='{0}' WHERE id='{1}'".format(occu, room))

# Make player enter a room.
def enterroom(DB, room, player):
	roominfo = roomstat(DB, room) # Get new room info.

	put(DB, "UPDATE players SET room='{0}' WHERE username='{1}'".format(room, player)) # Set new room.

	occu = roominfo["occupants"] # Add player to new room's occupants.
	occu.append(player)
	occu = obj2str(occu)
	put(DB, "UPDATE rooms SET occupants='{0}' WHERE id='{1}'".format(occu, room))

# Make all players leave all rooms.
def leaveall(DB):
	put(DB, "UPDATE rooms SET occupants='gAJdcQAu'")

# Create a new room.
def newroom(DB, name, owner):
	roomids = get(DB, "SELECT id FROM rooms") # Find highest room ID.
	newid = 0
	for rid in roomids:
		if rid[0] > newid:
			newid = rid[0]
	newid += 1

	put(DB, """INSERT INTO rooms (name, desc, owner, occupants, exits, items, id, locked) VALUES ('{0}', ' ', '{1}', 'gAJdcQAu', 'gAJ9cQAu', 'gAJdcQAu', '{2}', '1')""".format(name, owner, newid))

	return newid

# Send a message to all players.
def announce(S, DB, mesg):
	rows = get(DB, "SELECT username FROM players WHERE online='1'")
	for player in rows:
		send(S, player[0], mesg)

# Send a message to all players in a room.
def announce_room(S, DB, room, mesg):
	rows = get(DB, "SELECT username FROM players WHERE online='1' AND room='{0}'".format(room))
	for player in rows:
		send(S, player[0], mesg)

# Convert object to base64 pickled string.
def obj2str(obj):
	return base64.b64encode(pickle.dumps(obj, 2))

# Convert base64 pickled string to object.
def str2obj(strobj):
	return pickle.loads(base64.b64decode(strobj))

