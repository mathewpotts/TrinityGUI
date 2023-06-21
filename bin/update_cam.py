#!/usr/bin/env python3
# Import Libs
import subprocess
import sys
import pexpect

# Which image?
IMG = sys.argv[1]

PATH = sys.argv[2]

# Image from web
cmd = f'wget -q https://trinity.physics.gatech.edu/wp-content/uploads/demonstrator-uploads/{IMG}.jpg -O {PATH}/{IMG}.jpg'
subprocess.run(cmd.split())

