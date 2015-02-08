#!/usr/bin/env python
import subprocess, sys, os, argparse
from random import shuffle
from os import getcwd
from os.path import isdir, exists, expanduser, devnull


# Argument parsing
option_parser = argparse.ArgumentParser(
        description="Break movie clip apart and put it back together in random order")
option_parser.add_argument('filename'),
option_parser.add_argument('--numshots', '-n',type=int, 
        help='Number of shots to be included in the final edit')
args = option_parser.parse_args()
filename = args.filename
numshots = args.numshots


class RandomEditor(object):
    def __init__(self, filename, numshots):
        if exists(filename):
            self.filename = filename
        else:
            raise IOError
        self.numshots = numshots
        self.edit_list, self.error = subprocess.Popen(r"""ffprobe -show_frames -of compact=p=0 -f lavfi \
        'movie=%s,select=gt(scene\,0.4)' | sed  's/.*pkt_pts_time=\([0-9.]\{8,\}\)\|.*/\1/'""" % self.filename, \
                        stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True).communicate()
        self.edit_list = self.edit_list.split() 
        self.edit_list = [(self.edit_list[x], self.edit_list[x+1]) for x in range(len(self.edit_list)- 1)]
        self.numshots = args.numshots and args.numshots or len(self.edit_list)
        shuffle(self.edit_list)
        



    def cut():
        pass

    def assemble():
        pass

    def cleanup():
        subprocess.call(["rm", "-rf", tempdir])


if __name__ == '__main__':
    print "Getting list of cuts."
    editor = RandomEditor(filename, numshots)
    print editor.edit_list
    print "OK DONE"
