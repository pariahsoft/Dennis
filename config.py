# Adventure Bot "Dennis" Configuration File

# Edit this before using.
config = {
	"nick"      : "[OSDG]Dennis", # Nickname
	"user"      : "dennis",  # Username
	"real"      : "Dennis Alpha", # Realname
	"nickpass"  : "", # Nickserv Password
	"worldfile" : "world.db", # World Database File
	"timeout"   : 5, # Connection Timeout in Seconds
	"retryrate" : 3, # Connection Retry Rate in Seconds

	# ["HOST", PORT, "SERVPASS"]
	"server"    : ["irc.esper.net", 6667, ""], # Server to join.
	
	# [["CHANNEL", "PASS"], ["CHANNEL, "PASS"]]
	"channels"  : [] # Channels to join.
}

