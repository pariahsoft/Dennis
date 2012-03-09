# Adventure Bot "Dennis" Configuration File

# Edit this before using.
config = {
	"nick"      : "[OSDG]Dennis", # Nickname
	"user"      : "dennis",  # Username
	"real"      : "Dennis Alpha", # Realname
	"nickpass"  : "Rhombus!", # Nickserv Password
	"worldfile" : "world.db", # World Database File
	"timeout"   : 5, # Connection Timeout in Seconds
	"retryrate" : 3, # Connection Retry Rate in Seconds

	# ["HOST", PORT, "SERVPASS"]
	"server"    : ["authadeia.datnode.net", 6667, ""], # Server to join.
	
	# [["CHANNEL", "PASS"], ["CHANNEL, "PASS"]]
	"channels"  : []#[["#uboachan", ""], ["#animu", ""], ["#hacking", ""]] # Channels to join.
}

