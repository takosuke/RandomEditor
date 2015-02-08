    #!/usr/bin/env python
import subprocess, sys, os, argparse
from random import shuffle
from os import getcwd
from os.path import isdir, exists, expanduser, devnull
import io


# Argument parsing
option_parser = argparse.ArgumentParser(
        description="Break movie clip apart and put it back together in random order")
option_parser.add_argument('filename'),
option_parser.add_argument('--numshots', '-n',type=int, 
        help='Number of shots to be included in the final edit')
args = option_parser.parse_args()
filename = args.filename
numshots = args.numshots
output_path = os.getcwd()


class RandomEditor(object):
    def __init__(self, filename, numshots):
        if exists(filename):
            self.fullsourcepath = filename
            self.filename = os.path.basename(filename)
            self.extension = os.path.splitext(filename)[1][1:]
        else:
            raise IOError
        self.numshots = numshots
        self.edit_list, self.error = subprocess.Popen(r"""ffprobe -show_frames -of compact=p=0 -f lavfi \
        'movie=%s,select=gt(scene\,0.4)' | sed  's/.*pkt_pts_time=\([0-9.]\{8,\}\)\|.*/\1/'""" % self.fullsourcepath, \
                        stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True).communicate()
        self.edit_list = self.edit_list.split() 
        self.edit_list = [(self.edit_list[x], self.edit_list[x+1]) for x in range(len(self.edit_list)- 1)]
        self.numshots = args.numshots and args.numshots or len(self.edit_list)
        self.edit_list = self.edit_list[:self.numshots]
        self.output_path = output_path
        shuffle(self.edit_list)
        

    def setup(self):
        self.tmpdir = os.path.join(self.output_path, self.filename + "_tmp")
        subprocess.call(["mkdir", self.tmpdir])

    def cut(self):
        self.cutfiles_list = ""
        for i, v in enumerate(self.edit_list):
            tmp_filename = os.path.join(self.tmpdir, os.path.splitext(self.filename)[0] + "_tmp_" + str(i) + "." + self.extension)
            subprocess.call(["ffmpeg", "-i", self.fullsourcepath, "-ss", v[0], "-to", v[1], "-vf", "setpts='PTS-STARTPTS'", tmp_filename])
            self.cutfiles_list += ("file '" + tmp_filename + "'\n")
            print i,tmp_filename
        pass

    def assemble(self):
        print self.cutfiles_list
#        with io.BytesIO(bytes(self.cutfiles_list)) as f:
        with open("./templist.txt", "w") as templist:
            templist.write(self.cutfiles_list)
        try:
            subprocess.call(["ffmpeg", "-f", "concat", "-i", "templist.txt","-c", "copy", os.path.join(self.output_path, self.filename + "Randomized." + self.extension)])
        except IOError:
            self.cleanup()


    def cleanup(self):
        subprocess.call(["rm", "-rf", self.tempdir])


if __name__ == '__main__':
    print "Getting list of cuts."
    editor = RandomEditor(filename, numshots)
    print "Creating temporary directory"
    editor.setup()
    try:
        print "Making temporary cuts in tmp directory"
        editor.cut()
        print "assembling the shit"
        editor.assemble()
        print "OK DONE"
    except:
        editor.cleanup()
