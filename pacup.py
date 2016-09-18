#!/usr/bin/env python3
#########################################################
# Update pacman mirrorlist.

import os
import urllib.request
import subprocess

server_list_url = "https://www.archlinux.org/mirrorlist/?country=US&protocol=http&protocol=https&ip_version=4&ip_version=6"
main_mirror_list = "/etc/pacman.d/mirrorlist"
old_mirror_list = "/etc/pacman.d/mirrorlist.old"

# If not user root exit
testUser = os.getuid()
if testUser != 0:
    print("Must be run as root")
    quit()

# Download the new server list
with urllib.request.urlopen(server_list_url) as response:
  html = response.read()
  mirror_list = html.decode()

# Count lines containing "http" as basic sanity test
number_of_servers = mirror_list.count("http")
if number_of_servers <= 10:
  print("There was a problem downloading the new server list... quitting")
  quit()

# Format the downloaded server list for use on the system
mirror_list = mirror_list.replace("#Server", "Server")

# Run rankmirrors to get best 6 servers
print("Ranking mirrors for speed. This will take a few minutes.")
run_proc = subprocess.Popen(['rankmirrors', '-n', '6', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
mirror_list, _ = run_proc.communicate(mirror_list)

# Move current mirrorlist to mirrorlist.old
if os.path.isfile(old_mirror_list): 
  os.remove(old_mirror_list)
if os.path.isfile(main_mirror_list):
  os.rename(main_mirror_list, old_mirror_list)

file = open(main_mirror_list, "w")
file.write(mirror_list)
file.close()

quit()