#!/usr/bin/env python3
# Import lib
import sys
import pexpect

# Inputs
PORT      = sys.argv[1]
PHYS_USR  = sys.argv[2]
PHYS_PASS = sys.argv[3]
LWXDIR    = sys.argv[4]
WXDIR     = sys.argv[5]


# Construct the rsync command with the --files-from flag and the find command to filter files
cmd = f'ssh -p {PORT} {PHYS_USR}@127.0.0.1  \'find {LWXDIR}/*_* -type f -mtime -2 -print0\''
print(cmd)
c = pexpect.spawn(cmd)

# Expect the password prompt and send the password
c.expect('password:')
c.sendline(PHYS_PASS)

files = c.read().decode('UTF-8')
print(files.split('\x00'))
c.close()

for f in files.split('\x00'):
    if '\r\n' in f:
        cmd = f"rsync -qu -e \'ssh -p {PORT}\' {PHYS_USR}@127.0.0.1:{f[3:]} {WXDIR}"
    elif f == '':
        continue
    else:
        cmd = f"rsync -qu -e \'ssh -p {PORT}\' {PHYS_USR}@127.0.0.1:{f} {WXDIR}"
        print(cmd)
    c = pexpect.spawn(cmd)
    # Expect the password prompt and send the password
    c.expect('password:')
    c.sendline(PHYS_PASS)
    print(c.read().decode('UTF-8'))
    c.close()
