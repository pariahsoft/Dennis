# Adventure Bot "Dennis" Database Handling
# Copyright 2012 Michael D. Reiley and OmegaSDG <http://omegasdg.com>
# Released under the MIT/Expat License.

import sqlite3

### Database Structure ###
"""
rooms:= name, desc, owner, occupants, exits, items, id, locked
	name:= Average Room
	desc:= Just your average boring room.
	owner:= seisatsu
	exits:= {"north": 12, "east": 18} (BASE64)
	items:= [{"name": "Ye Flask", "desc": "You cannot look at ye flask."}] (BASE64)
	id:= 0
	locked:= 0

players:= username, name, desc, online, room
	username:= ircuser32
	name:= Joe Player
	desc:= A man with a beard.
	online:= 0
	room:= 12
	pass:= (SHA256 PASSWORD HASH)
"""

### Internal Variables ###

## Rooms Table ##
# Structure of the rooms table. Changing this will break the software.
rtable = """CREATE TABLE IF NOT EXISTS rooms
         (name TEXT, desc TEXT, owner TEXT, exits TEXT,
         items TEXT, id INTEGER, locked INTEGER)"""

## Players Table ##
# Structure of the players table. Changing this will break the software.
ptable = """CREATE TABLE IF NOT EXISTS players
         (username TEXT, name TEXT, desc TEXT, online INTEGER,
         room INTEGER, pass TEXT)"""

## Initial Room ##
# This is the initial room where all players start. The query contains magic.
initroom = """INSERT INTO rooms (name, desc, owner, exits,
           items, id, locked) VALUES ('Initial Room',
           'The first room to exist.', '/root/', 'gAJ9cQAu',
           'gAJdcQAu', '0', '0')"""

## Root Player ##
# This is a nonexistent player who owns the initial room.
rootplayer = """INSERT INTO players (username, name, desc, online, room, pass)
             VALUES ('/root/', '[root]', 'SYSTEM USER', '0', '-1', '0')"""

### Database Functions ###

# Open database, and initialize if new.
def opendb(dbname):
	conn = sqlite3.connect(dbname)
	C = conn.cursor()
	C.execute(rtable)
	C.execute(ptable)
	conn.commit()
	C.close()

	chk = get(conn, "SELECT * FROM rooms WHERE id='0'") # Check if initial room exists.
	if not len(chk): # Create initial room.
		put(conn, initroom)

	chk = get(conn, "SELECT * FROM players WHERE username='/root/'") # Check if root player exists.
	if not len(chk): # Create root player.
		put(conn, rootplayer)

	return conn

# Get rows from the database.
def get(conn, query):
	C = conn.cursor()
	C.execute(query)
	rows = C.fetchall()
	C.close()
	return rows

# Modify the database.
def put(conn, query):
	C = conn.cursor()
	C.execute(query)
	conn.commit()
	C.close()

# Escape user input.
def escape(userstr):
	return userstr.replace("'", "''")

