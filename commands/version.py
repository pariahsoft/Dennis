########################################
## Adventure Bot "Dennis"             ##
## commands/version.py                ##
## Copyright 2012-2013 PariahSoft LLC ##
########################################

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

###################
# Version Command #
###################

from helpers import *

from help import C_HELP

def C_VERSION(S, DB, sender, args):
	if len(args):
		C_HELP(S, DB, sender, ["VERSION"])
		return

	vmsg = version_info[0].format(*version_info[1:]).split("\n")

	for line in vmsg:
		send(S, sender, line)

### Version Info ###

version_info = [
	"{0} {1}\nBy {2}\n{3} {4} {5}",
	"Adventure Bot \"Dennis\"",
	"Alpha",
	"Michael D. Reiley",
	"Copyright (c) 2012",
	"Omega Software Development Group",
	"<omegasdg.com>"
]

