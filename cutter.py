#!/usr/bin/env python
print "starting script"
import subprocess, sys

cuts = sys.stdin.read().split()
edit_list = []



for i in range(len(cuts)):
	try:
		edit_list.append((cuts[i], cuts[i+1]))
	except IndexError:
		edit_list.append((cuts[i], ""))
		
for i in range(len(edit_list)):
	print "Cutting " + edit_list[i][0] + " to " + edit_list[i][1] 
	if i == len(edit_list):
		subprocess.call(["ffmpeg", "-i", sys.argv[1], "-ss", edit_list[i][0], "-acodec", "copy", "-vcodec", "copy","-vsync", "2", "output" + str(i) + "." + sys.argv[1].split(".")[-1]])
	else:
		subprocess.call(["ffmpeg", "-i", sys.argv[1], "-ss", edit_list[i][0], "-to", edit_list[i][1], "-vf", "setpts='PTS-STARTPTS'", "output" + str(i) + "." + sys.argv[1].split(".")[-1]])
	print "Done with cut number " + str(i) + ".\n"
	
	