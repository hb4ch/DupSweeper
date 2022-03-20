#!/usr/bin/python

import os
import sys
import hashlib
import argparse
from rich import print

videoFileExt = {"avi", "mkv", "mp4", "mpg", "wmv", "rmvb"}
docsExt = {"doc", "pdf", "epub", "mobi", "azw3"}
archiveExt = {"rar", "zip", "tar", "iso"}
imageExt = {"jpeg", "jpg", "png", "tiff", "webm"}
musicExt = {"mp3", "m4a", "flac", "ape", "wav", "aac"}

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']:
        if size < 1024.0 or unit == 'PiB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"

parser = argparse.ArgumentParser()
parser.add_argument('--video', dest="video", action='store_true',
    help="Scan video files: {}".format(videoFileExt))
parser.add_argument('--document', dest="doc", action='store_true',
    help="Scan document files: {}".format(docsExt))
parser.add_argument('--archive', dest="archive", action='store_true',
    help="Scan archive files: {}".format(archiveExt))
parser.add_argument('--image', dest="image", action='store_true',
    help="Scan image files: {}".format(imageExt))
parser.add_argument('--music', dest="music", action='store_true',
    help="Scan music files: {}".format(musicExt))
parser.add_argument('-d', '--dir', required=True, dest="dirs", action='append',
    help="Setting dirs to search")
parser.add_argument('--keep', dest="keepKeyword", action='append',
    help="Setting keywords in file to always keep")
parser.add_argument('-r', '--remove', dest='remove', action='store_true', 
    help="Remove duplicates after searching")
parser.add_argument('--probe-size', type=int, dest='probesize', default=1,
    help="Size of data chunk (in MB) to hash of each file.")
args = parser.parse_args()

if (not args.video and not args.doc and not args.archive and not args.image and not args.music):
    print("[bold red]Not specified one file type to search for, quiting![/bold red]")
    quit(1)

if (args.probesize <= 0):
    print("[bold red]Invalid probe size, probe size has to be positive, quiting![/bold red]")
    quit(1)

cwd = os.getcwd()

directory = []

for d in args.dirs:
    if (sys.argv[1][0] == '.'):
        directory.append(os.path.realpath(os.path.join(cwd, d)))
    else:
        directory.append(d)

md5File = dict()

def buildHashTable(extList, realname):
    for ext in extList:
        extDot = "." + ext
        if (realname.find(extDot) != -1):
            with open(realname, "rb") as f:
                try:
                    readSize = 1024 * 1024 * args.probesize
                    bytes = f.read(readSize)
                    hashValue = hashlib.md5(bytes).hexdigest()
                    fileList = md5File.get(hashValue, -1)
                    if (fileList == -1):
                        md5File[hashValue] = [realname]
                    else:
                        md5File[hashValue].append(realname)
                except Exception:
                    print("Error opening {}!".format(realname))
            break            

for dir in directory:
    print("Scanning directory: " + dir)
    for root, dirs, files in os.walk(dir):
        for filename in files:
            realname = os.path.join(root, filename)
            if (args.video):
                buildHashTable(videoFileExt, realname)
            if (args.doc):
                buildHashTable(docsExt, realname)
            if (args.archive):
                buildHashTable(archiveExt, realname)
            if (args.image):
                buildHashTable(imageExt, realname)
            if (args.music):
                buildHashTable(musicExt, realname)

deleteFiles = 0
freedSize = 0
duplicateSets = 0

for key, value in md5File.items():
    if len(value) > 1:
        keeplist = []
        duplicateSets += 1
        if args.keepKeyword is not None:
            for keyword in args.keepKeyword:
                for realname in value:
                    if (realname.find(keyword) != -1):
                        keeplist.append(realname)
        if len(keeplist) == 0:
            keeplist.append(value[0])

        for keepfile in keeplist:
            print("keeping [bold green]{}[/bold green]".format(keepfile))
        for realname in value:
            if (args.remove):
                if realname not in keeplist: 
                    currSize = os.path.getsize(realname)
                    print("removing: [bold red]" + realname + "[/bold red]")
                    os.remove(realname)
                    deleteFiles += 1
                    freedSize += currSize
            else:
                if realname not in keeplist:
                    print("plan to remove: [bold red]" + realname + "[/bold red]")
        print("")

print("[bold yellow]Scanning through {} files, duplicate group:{} \ndeleting {} files, saving {} of space[/bold yellow]".format \
    (len(md5File), duplicateSets, deleteFiles, human_readable_size(freedSize)))