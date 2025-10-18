#!/usr/bin/env python3
import os
import re
import sys

directory = sys.argv[1]

for filename in os.listdir(directory):
    match = re.match(r'^(.+_)(\d+)(\..+)$', filename)
    if match:
        prefix, number, ext = match.groups()
        new_name = f"{prefix}{int(number):04d}{ext}"
        if filename != new_name:
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_name)
            print(f"{filename} -> {new_name}")
            os.rename(old_path, new_path)
