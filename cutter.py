#!/usr/bin/env python
print "starting script"
import subprocess, sys, string, os
from random import shuffle

cuts = sys.stdin.read().split()
edit_list = []
tmp_file_list = []
extension = sys.argv[1].split(".")[-1]

os.system("mkdir tmp") 



for i in range(len(cuts)):
	try:
		edit_list.append((cuts[i], cuts[i+1]))
	except IndexError:
		edit_list.append((cuts[i], ""))
		
for i in range(len(edit_list)-1):
    filename = "tmp/tmp_output_" + str(i).rjust(6,'0') + "." + extension
    if i == len(edit_list):
		subprocess.call(["ffmpeg", "-i", sys.argv[1], "-ss", edit_list[i][0], "-acodec", "copy", "-vcodec", "copy","-vsync", "2", filename])
    else:
		subprocess.call(["ffmpeg", "-i", sys.argv[1], "-ss", edit_list[i][0], "-to", edit_list[i][1], "-vf", "setpts='PTS-STARTPTS'", filename])
    print "Done with cut number " + str(i) + ".\n"
    tmp_file_list.append("file '" + filename + "'\n")

print tmp_file_list
shuffle(tmp_file_list)
shuffled_args = string.join(tmp_file_list)
with open("temp.list", "w") as templist:
	templist.write(shuffled_args)

print shuffled_args


os.system("ffmpeg -f concat -i temp.list -c copy OUTPUT." + extension)	

#Clear temp directory
subprocess.call("rm tmp/*.*", shell=True)

