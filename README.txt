Adventure Bot "Dennis"
Copyright (c) 2012 Michael D. Reiley <mreiley@omegasdg.com>
http://wiki.omegasdg.com/index.php?title=Dennis

Released under the MIT/Expat License.

Dennis is a Python IRC bot which hosts a multiplayer, sandbox text adventure. It uses a private message console system to facilitate interaction between players, and a customizable world. Players can add and edit rooms and scenery, and talk to each other as they build and explore. There are no monsters, no scripted events, and no inventories; the emphasis is on scenery, exploration, and interaction.

Has something like this been done before? I'm not sure. IRC has been around since 1988, and text adventures have existed much longer. What happens when you combine two ancient, time-proven constructs?

Something awesome.

I realized one day that the simplicity and structure of IRC make it a perfect medium for a text adventure console. Within hours, I had created the first version of Dennis. However, that version was never released. This is a full rewrite of my original Dennis bot, coded to fix some of the numerous mistakes in the first implementation. It uses a basic IRC bot skeleton and an sqlite3 world data format.

This is alpha software. It's guaranteed to run, not to work. It's probably full of bugs, and useless or vestigial code, and the only documentation is in the source. In addition, the database structure is subject to change. Test at your own risk.

Usage:
* Edit config.py to your liking.
* Run "dennis.py" in your console.
* Private message "help" to the bot.

File List:
* dennis.py : Main Program
* config.py : User Configuration
* console.py : Console Handling
* database.py : SQLite Database Handling
* helpers.py : Helper Functions
* commands/*.py: Command Modules

