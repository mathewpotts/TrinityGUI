#!/usr/bin/python3

# Import Libs
import tkinter as tk
import glob
import os
import sys
import time
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import datetime
from astropy.io import ascii
import numpy as np
import pickle
import subprocess
import pexpect
from tkinter import messagebox
from widgets.cameras import CameraWidget
from widgets.weather import WeatherWidget
from widgets.outlets import OutletWidget
from widgets.door import DoorWidget
from widgets.runlist import RunlistWidget

#######################################################
################## User File paths ####################

# Linux Machine in lab
LHOMEDIR = "/home/mpotts32/"
LCAMDIR = LHOMEDIR + "cams/" # directory for the camera
LINCAMDIR = LCAMDIR + "IN/" # directory for the inside camera
LOUTCAMDIR = LCAMDIR + "OUT/" # directory for the outside camera
os.environ['LWXDIR'] = LHOMEDIR + "weather/" # director for the path of the weather data # set this as an environmental variable
LWPDIR = LHOMEDIR + 'weather_plots/' # directory for the weather plots

# Linux Machine anywhere
HOMEDIR   = os.path.abspath(os.curdir)
RESDIR    = HOMEDIR + "/resources/"
WIDDIR    = HOMEDIR + "/widgets/"
os.environ['BINDIR']    = RESDIR + "/bg_scripts/" # set this as an environmental variable
os.environ['CAMDIR']    = RESDIR + "cams/" # set this as an environmental variable
os.environ['WXDIR']     = RESDIR + "weather/"# set this as an environmental variable
os.environ['WPDIR']     = RESDIR + "weather_plots/"
########## End of File paths ##########################
#######################################################
########## Login Information ##########################
#######################################################
if os.path.isfile(RESDIR + "/tmp.txt"):
    with open(RESDIR + "/tmp.txt") as f:
        lines = f.readlines()
        os.environ['PORT']      = lines[0].split()[0]    
        GT_HOST   = lines[1].split()[0]
        GT_USR    = lines[1].split()[1]
        GT_PASS   = lines[1].split()[2]
        PHYS_HOST = lines[2].split()[0]
        os.environ['PHYS_USR']  = lines[2].split()[1]
        os.environ['PHYS_PASS'] = lines[2].split()[2]
        CTRL_PASS = lines[3].split()[0]
else:
    GT_HOST   = 'ssh.physics.gatech.edu'
    GT_USR    = input("GT Username: ")
    GT_PASS   = input("GT Password: ")
    PHYS_HOST = 'phys43199.physics.gatech.edu'
    os.environ['PHYS_USR']  = input(f"{PHYS_HOST} Username: ")
    os.environ['PHYS_PASS'] = input(f"{PHYS_HOST} Password: ")
    os.environ['PORT']      = input("Input Tunnel Port: ")
    CTRL_PASS = input("Control PC Password: ")
    print(f"{os.environ['PORT']}\n{GT_HOST} {GT_USR} {GT_PASS}\n{PHYS_HOST} {os.environ['PHYS_USR']} {os.environ['PHYS_PASS']}\n{CTRL_PASS}",file=open(RESDIR + '/tmp.txt','w'))
    
########## End of Login Information ###################

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")

        logo_path = RESDIR + "/trinity-logo.png"
        global logo
        logo = ImageTk.PhotoImage(Image.open(logo_path).resize((75, 75))) # get the image import into tkinter
        logo_label = tk.Label(root, image = logo)
        logo_label.pack()
        
        main_label = tk.Label(root, text="Trinity GUI")
        main_label.pack(padx=20, pady=20)
        
        page1_button = tk.Button(root, text="Cameras", command=self.open_cameras)
        page1_button.pack(pady=10)
        
        page2_button = tk.Button(root, text="Weather", command=self.open_weather)
        page2_button.pack(pady=10)

        outlets_button = tk.Button(root, text="Outlets", command=self.open_outlets)
        outlets_button.pack(pady=10)

        door_button = tk.Button(root, text="Door", command=self.open_doors)
        door_button.pack(pady=10)

        runlist_button = tk.Button(root, text="Observation Run", command=self.open_runlist)
        runlist_button.pack(pady=10)

        SAM_button = tk.Button(root, text="SAM", command=self.open_SAM)
        SAM_button.pack(pady=10)
        
        quit_button = tk.Button(root, text="Quit", command=self.root.quit)
        quit_button.pack(pady=20)
    
    def open_cameras(self):
        CameraWidget(self.root)
    
    def open_weather(self):
        WeatherWidget(self.root)

    def open_outlets(self):
        OutletWidget(self.root)

    def open_doors(self):
        DoorWidget(self.root)

    def open_runlist(self):
        RunlistWidget(self.root)

    def open_SAM(self):
        SAM = WIDDIR + "/SAM"
        cmd = f"python3 {SAM}/SPB2Obs.py -loc {SAM}/gpsLocation.txt -obj {SAM}/input0.txt -elv 2000"
        print(cmd)
        return subprocess.Popen(cmd.split())
        
        
def main():
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

# This function is used to read an SSH tunnel to the lab computer.
# This way the GUI can be used anywhere provided you have GT creds.
def create_tunnel():
    print(f"Creating SSH Tunnel to {PHYS_HOST} on port {os.environ['PORT']}")
   

    # SSH into the first computer and establish an SSH tunnel
    ssh_cmd = f"ssh -o StrictHostKeyChecking=no {GT_USR}@{GT_HOST} -L {os.environ['PORT']}:{PHYS_HOST}:22"
    print(ssh_cmd)
    try:
        ssh = pexpect.spawn(ssh_cmd)
        # Expect the password prompt and send the password
        ssh.expect('password:')
        ssh.sendline(GT_PASS)
    except:
        print("ssh: connect to host ssh.physics.gatech.edu port 22: Connection refused")
        print("Please try again in a couple minutes.")
        sys.exit(1)
    return ssh

def update_images():
    CAMS = ['IN','OUT']
    proc_ls = []
    for cam in CAMS:
        cmd = f'python3 {os.environ["BINDIR"]}/update_cam.py {cam}CAM {os.environ["CAMDIR"]}'
        #print(cmd)
        proc_ls.append(subprocess.Popen(cmd.split()))
    return proc_ls

def update_wx():
    cmd = f"python3 {os.environ['BINDIR']}/update_wx.py {os.environ['PORT']} {os.environ['PHYS_USR']} {os.environ['PHYS_PASS']} {os.environ['LWXDIR']} {os.environ['WXDIR']}"
    #print(cmd)
    return subprocess.Popen(cmd.split())

def update_pdu_status():
    cmd = f"python3 {os.environ['BINDIR']}/update_pdu_status.py {os.environ['PORT']} {os.environ['PHYS_USR']} {os.environ['PHYS_PASS']}"
    #print(cmd)
    return subprocess.Popen(cmd.split())

def update_wx_plots():
    cmd = f"python3 {os.environ['BINDIR']}/weather_plots.py {os.environ['WXDIR']} {os.environ['WPDIR']}"
    #print(cmd)
    return subprocess.Popen(cmd.split())

if __name__ == "__main__":
    tunnel = create_tunnel()

    # Allow time for tunnel to open
    print("Allowing the tunnel time to establish... Sleeping 5 seconds")
    time.sleep(5)

    # Enable the background scripts that update the weather and cameras
    cam_procs = update_images()
    print(cam_procs)
    wx_proc = update_wx()
    print(wx_proc)
    pdu_proc = update_pdu_status()
    print(pdu_proc)
    wx2_proc = update_wx_plots()
    print(wx2_proc)

    # Allow time for bg_scripts to execute fully
    print("Starting up background scripts... Sleeping 20 seconds")
    time.sleep(20)

    # Start GUI
    main()

    # End background scripts
    for proc in cam_procs:
        print(proc)
        proc.kill()
    print(wx_proc)
    wx_proc.kill()
    print(pdu_proc)
    pdu_proc.kill()
    print(wx2_proc)
    wx2_proc.kill()
    
    tunnel.close()
