# Introduction

DupSweeper is an useful python utility to find possible duplicates of files living in one or multiple paths. DupSweeper works by recursively searching through user-provided path to look for md5 hash collision of first couple of data chunks(e.g. 1 MiB) to form equivalence class of files. User can also choose to delete all duplicate copies of files when iterating through these paths.For convenience, user can specify "keep" keywords in which DupSweeper will always leave alone to avoid data loss and to specify which copy to keep.

# Caution 
**CAUTION: Use the utility at your own risk! I'm not responsible for any data loss or data corruption caused by this utility!
To avoid data loss, do not include "-r" option in your intial run. Check the output of your initial run to decide whether to switch on the actual remove option "-r".**

# CLI options
```bash
usage: dupSweeper.py [-h] [--video] [--document] [--archive] [--image] [--music] -d DIRS [--keep KEEPKEYWORD] [-r] [--probe-size PROBESIZE]

options:
  -h, --help            show this help message and exit
  --video               Scan video files: {'rmvb', 'avi', 'mkv', 'wmv', 'mp4', 'mpg'}
  --document            Scan document files: {'doc', 'epub', 'mobi', 'pdf', 'azw3'}
  --archive             Scan archive files: {'tar', 'rar', 'iso', 'zip'}
  --image               Scan image files: {'webm', 'jpeg', 'png', 'tiff', 'jpg'}
  --music               Scan music files: {'ape', 'mp3', 'aac', 'flac', 'wav', 'm4a'}
  -d DIRS, --dir DIRS   Setting dirs to search
  --keep KEEPKEYWORD    Setting keywords in file to always keep
  -r, --remove          Remove duplicates after searching
  --probe-size PROBESIZE
                        Size of data chunk (in MB) to hash of each file.
```

# Installation
## Dependency
A not so ancient python3 should be fine.
```
pip3 install hashlib argparse rich
```
On a unix-like system:
```
sudo cp dupSweeper.py /usr/local/sbin
```

# Examples

```bash
dupSweeper.py -d /mnt/SATASSDEXT4 -d /home --document --keep NutStore
# find document file duplicates in two directories, always keep file whose path contains keyword "NutStore".

dupSweeper.py -d /mnt/SATASSDEXT4 -d /home --video --keep NutStore -r
# similar to above, but only scan video files. removes duplicates.
```

# Caveat
Several shorting comings of the current implementation:
1. Slow `os.walk()` compared to system utility like `find`
2. Only hashing head chunks of data could cause false duplicate included in results, but hashing whole data could cause performance issue.
