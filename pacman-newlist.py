#!/usr/bin/env python3
############################################
#
#   Update pacman mirrorlist. Rotate current
#   list to "mirrorlist.old" removing backup
#   if one already exists. And place new
#   list in place.
#

import os
import sys
import re
import subprocess
import urllib.request

# Set alias' for files to be used
NEW_LIST = "/etc/pacman.d/mirrorlist.new"
MAIN_LIST = "/etc/pacman.d/mirrorlist"
OLD_LIST = "/etc/pacman.d/mirrorlist.old"
TEMP_LIST_1 = "/tmp/pacman-mirrorlist-update.tmp"
TEMP_LIST_2 = "/tmp/pacman-mirrorlist-update_second-file.tmp."

# If not root exit
testUser = os.getuid()
if testUser != 0:
    print("Must be run as root" '\n')
    sys.exit()

# Emulates linux "cat" command
def cat(openfile):
   with open(openfile) as file:
     return file.read()

print("Downloading new list..." '\n')
urllib.request.urlretrieve("https://www.archlinux.org/mirrorlist/?country=US&protocol=http&ip_version=4", TEMP_LIST_1)

# Count lines of downloaded mirror list, if less than 20 download is corrupt
numLines = sum(1 for line in open(TEMP_LIST_1))
if numLines < 20:
    print("There was an error downloading the mirrorlsit" '\n')
    sys.exit()
else:
    print("Download seems to have gone well" '\n')
#print(numLines) ## Testing - print line count of downloaded mirror list file

#print(cat(TEMP_LIST_1)) ## Testing -- print downloaded mirror list file

# Remove leading '#' from each line of downloaded file
print("Formatting new list for use" '\n')

with open(TEMP_LIST_1, 'r+') as f:
    modified = re.sub('^.', '', f.read(), flags=re.MULTILINE)
    with open(TEMP_LIST_2, 'w+') as t:
        t.write(modified)

#print(cat(TEMP_LIST_2)) ## Testing -- print downloaded mirror list file

# Use system app "rankmirrors" to get fastest servers
print("Ranking the new mirror list for best servers")
print("NOTE: This can take a few minutes..." '\n')
subprocess.call("/usr/bin/rankmirrors -n 6 " + TEMP_LIST_2 + " > " + NEW_LIST, shell=True)
'''
TODO: Find a way to accomplish running "rankmirrors"
that does not require the use of 'shell=True'
'''

# Rotate current list to mirrorlist.old
# and new list to mirrorlist
print("Moving current mirrorlist to \"/etc/pacman.d/mirrorlist.old\"" '\n')
os.rename(MAIN_LIST, OLD_LIST)
print("Moving new mirrorlist to \"/etc/pacman.d/mirrorlist\"" '\n')
os.rename(NEW_LIST, MAIN_LIST)

print("All done ;)")

sys.exit()
