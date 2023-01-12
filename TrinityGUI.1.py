#!/usr/bin/env python3

##################################################################
################### Trinity GUI ##################################
#####  Header Info
#####
#####
##################################################################


# imports
import math
import tkinter as tk
from random import random
from tkinter import ttk
from PIL import ImageTk, Image
from astropy.io import ascii
import glob
import os
import matplotlib.pyplot as plt
import datetime
from astropy.io import ascii
import numpy as np
import pickle
import pyscreenshot as ImageGrab
import sys

#######################################################
########## User File paths
'''
HOMEDIR = 'C:/Users/Ginkl/Documents/TrintyWork/'
CAMDIR = HOMEDIR + "Cams/"
INCAMDIR = CAMDIR + "In/"
OUTCAMDIR = CAMDIR + "Out/"
WXDIR = HOMEDIR + 'Weather_data/'
'''

HOMEDIR = "/home/mpotts32/"
CAMDIR = HOMEDIR + "cams/"
INCAMDIR = CAMDIR + "IN/"
OUTCAMDIR = CAMDIR + "OUT/"
WXDIR = HOMEDIR + "weather/"
WPDIR = HOMEDIR + "weather_plots/"

########## End of File paths ##########################
#######################################################
# fonts and font sizes used throughout the gui
LARGEFONT = ("Verdana", 35,)
MedFONT = ("Verdana", 25)
SmFONT = ("Verdana", 15)


# this class creates a pop up window
class popupWindow(object):
    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        self.l = tk.Label(top, text="Hello World")
        self.l.pack()
        self.e = tk.Entry(top)
        self.e.pack()
        self.b = tk.Button(top, text='Ok', command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        self.value = self.e.get()
        self.top.destroy()


# This class holds the structor of the tkinter gui structure allowing for multiple pages
class tkinterApp(tk.Tk):

    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, Page1, Page2):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# This method is used to load in the weather data from the desired file from the trinity weather station
# and put everything to an array for easy access
def weather_data(file):
    array_titles = (
        "Node", "RelativeWindDirection", "RelativeWindSpeed", "CorrectedWindDirection",
        "AverageRelativeWindDirection",
        "AverageRelativeWindSpeed", "RelativeGustDirection", "RelativeGustSpeed",
        "AverageCorrectedWindDirection",
        "WindSensorStatus", "Pressure", "Pressure at Sea level", "Pressure at Station", "Relative Humidity",
        "Temperature",
        "Dewpoint",
        "Absolute Humidity", "compassHeading", "WindChill", "HeatIndex", "AirDensity", "WetBulbTempature",
        "SunRiseTime", "SolarNoonTime", "SunsetTime",
        "Position of the Sun", "Twilight (Civil)",
        "Twilight (Nautical)",
        "Twilight (Astronomical)", "X-Tilt", "Y-Tilt", "Z-Orientation", "User Information Field",
        "System Date and Time",
        "Supply Voltage", "Status", "Checksum")
    print(file)
    weather_data_array = ascii.read(file, format='no_header', data_start=0, delimiter=',', names=array_titles)

    # return weather_data_array
    # print(weather_data_array)

    # converts the data to an numpy array to be able to use standard array access
    output_array = np.array(weather_data_array)
    for i in range(len(output_array)):
        for j in range(len(output_array[0])):
            output_array[i][j] = ''.join(str(output_array[i][j]).split(','))
    return output_array


# first window frame startpage
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        canvas = tk.Canvas()
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        ttk.Label(self, text="Trinity GUI", font=LARGEFONT).place(x=25, y=25)

        ########## Door Buttons ##########
        # this defintiion creates random output messages for the door as a place holder

        def random_status():
            Door_message = ttk.Label(self)
            # Door_message.place_forget()
            value = random()
            if value <= .33:
                statement = 'Status All good'
            elif .33 < value <= .66:
                statement = 'small error'

            else:
                statement = 'ERROR Door wont shut'

            Door_message.config(text=statement) # gets the label ready

            Door_message.place(x=25, y=375) # place the button, place is used through out pack and place can not be used together
            Door_message.after(5000, Door_message.destroy) # removed the messages after a set time frame

        # door open label
        def door_open():
            this_b = tk.Label(self, text='Door Opening')
            this_b.place(x=75, y=175)
            this_b.after(5000, this_b.destroy)

        # door close label
        def door_close():
            this_b = tk.Label(self, text='Door Closing')
            this_b.place(x=75, y=275)
            this_b.after(5000, this_b.destroy)

        # created the actual buttons that wil be displayed
        door_o_button = ttk.Button(self, text="Door Open", command=door_open)
        door_o_button.place(x=25, y=125, height=50, width=150)

        door_c_button = ttk.Button(self, text="Door Close", command=door_close)
        door_c_button.place(x=25, y=225, height=50, width=150)

        door_status_button = ttk.Button(self, text="Check Status", command=random_status)
        door_status_button.place(x=25, y=325, height=50, width=150)

        ########## End of Door Buttons ######################

        ########## Webcam images ##########

        # these are fake button that have the images for the outside and inside cameras that will refresh
        # to whatever the last created file is in the folder

        # this is a method that finds the inside camera imaged adn then puts the on to the gui window as a button
        def inside_images(file_path_in):
            # gets the last image in the file based on time
            list_in_files = glob.glob(file_path_in)
            file_in = max(list_in_files, key=os.path.getctime)
            # print(f"hey {file_out}")
            # resize the image
            img_in = Image.open(file_in).resize((550, 350))
            self.image_in = ImageTk.PhotoImage(img_in)
            # create the button holder
            inside_but = tk.Button(self, text='Click Me !', image=self.image_in)
            inside_but.place(x=350, y=25) # set the location
            ttk.Label(self, text=str(os.path.basename(file_in)), font=SmFONT).place(x=350, y=400) # make a label of the file name
            canvas.after(50000, inside_images, file_path_in) # refresh the picture after a set amount of time

        inside_images(INCAMDIR + '*') # runs the image the first time

        # creates a def to open the file path of the inside camera images
        def open_indoor_folder():
            os.startfile(INCAMDIR)

        # created the button to open the indoor camera images file path
        ttk.Button(self, text="Indoor filepath", command=open_indoor_folder).place(x=700, y=400, height=50, width=150)

        # see inside camera images for information same as above
        def outside_images(file_path_out):
            list_out_files = glob.glob(file_path_out)
            file_out = max(list_out_files, key=os.path.getctime)
            # print(f"hey {file_out}")
            img_out = Image.open(file_out)

            img_out = img_out.resize((550, 350))

            self.image_out = ImageTk.PhotoImage(img_out)

            outside_but = tk.Button(self, text='Click Me !', image=self.image_out)
            outside_but.place(x=925, y=25)
            ttk.Label(self, text=str(os.path.basename(file_out)), font=SmFONT).place(x=950, y=400)
            canvas.after(50000, outside_images, file_path_out)

        outside_images(OUTCAMDIR + '*')

        def open_outdoor_folder():
            os.startfile(OUTCAMDIR)

        ttk.Button(self, text="Outdoor filepath", command=open_outdoor_folder).place(x=1325, y=400, height=50,
                                                                                     width=150)
        ##########  End of Camera images ##########


        ##### Weather Section ########
        weather_title = tk.Label(self, text="Weather Data", font=MedFONT)
        weather_title.place(x=925, y=525)

        weather_button = ttk.Button(self, text="More Weather Data", command=lambda: controller.show_frame(Page1))
        weather_button.place(x=1325, y=525, height=50, width=150)

        ##### Labels for the weather section ##########
        tk.Label(self, text="Temperature Current:", font=SmFONT).place(x=925, y=635)
        # tk.Label(self, text="Temperature Avg (1h):", font=SmFONT).place(x=925, y=605)
        tk.Label(self, text="Wind Speed Current:", font=SmFONT).place(x=925, y=665)
        # tk.Label(self, text="Wind Speed Avg (1h):", font=SmFONT).place(x=925, y=665)
        tk.Label(self, text="Humidity Current:", font=SmFONT).place(x=925, y=695)
        tk.Label(self, text="Pressure Current:", font=SmFONT).place(x=925, y=725)
        tk.Label(self, text="Wind Direction:", font=SmFONT).place(x=925, y=755)
        tk.Label(self, text="Dew Point", font=SmFONT).place(x=925, y=785)
        tk.Label(self, text="Sunrise:", font=SmFONT).place(x=925, y=815)
        tk.Label(self, text="Sunset:", font=SmFONT).place(x=925, y=845)
        tk.Label(self, text="Civil Twilight:", font=SmFONT).place(x=925, y=875)
        tk.Label(self, text="Astro Twilight:", font=SmFONT).place(x=925, y=905)

        ####### Updating Labels from the weather station ###############

        list_of_files = glob.glob(WXDIR + '*_*')  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime) # gets the latest weather data file
        weather_data_location = latest_file

        # print(latest_file) # checks which file is being read in

        def make_plots_and_labels(file):

            all_data = weather_data(file) # get the data from file to array

            # print(all_data)
            # makes the plots of the wanted weather data
            def save_plot_png(all_data):
                # creates arrays to hold all the data (blank)
                size = len(all_data)
                wind_direction = [0] * size
                date_n_time = [0] * size
                date = [0] * size
                tempature = [0] * size
                wind_speed = [0] * size
                humidity = [0] * size
                dew_point = [0] * size
                pressure = [0] * size

                # arrays are loaded with data
                for i in range(len(all_data)):
                    tempature[i] = float(all_data[i][14])
                    wind_speed[i] = float(all_data[i][2])
                    humidity[i] = float(all_data[i][13])
                    dew_point[i] = float(all_data[i][15])
                    pressure[i] = float(all_data[i][12])
                    wind_direction[i] = int(all_data[i][1])
                    date_n_time[i] = all_data[i][33]
                    temp = str(date_n_time[i])
                    date[i] = datetime.datetime.strptime(temp[:19], "%Y-%m-%dT%H:%M:%S")

                # print(date)
                # a def to make the plot format for each

                def plot_format(x, y, xlabel, ylabel, title, color, fig, thick=1):

                    plt.plot(x, y, c=color, linewidth=thick)
                    plt.title(title)
                    plt.xlabel(xlabel)
                    plt.ylabel(ylabel)
                    plt.xticks(rotation=25)

                    try:
                        os.mkdir(f'{HOMEDIR}weather_plots') # makes a folder to hold all the weather plots if it is not present
                    except:
                        pass
                    fig.canvas.draw() # create the canvas
                    plt.savefig(f'{HOMEDIR}weather_plots/{title}.png') # save the image as a png
                    pickle.dump(fig, open(f'{HOMEDIR}weather_plots/{title}.pickle', 'wb')) # save the image as a pickle so that it can be view in python again
                    fig.clear() # clear the plot
                    fig.clf() # clear the plot ----- This is import so that only one plot is used and reducind the ram needed to run the program

                # all the of the plots that are wanting to be made
                plot_format(date, wind_direction, 'Date', 'Wind Direction (Degrees)', 'Wind_direction_over_time',
                            'green', fig, thick=0.1)
                plot_format(date, tempature, 'Date', 'Tempature (Degrees)', 'Temperature_over_time', 'red', fig)
                plot_format(date, humidity, 'Date', 'Humidity (Percent)', 'Humidity_over_time', 'blue', fig)
                plot_format(date, wind_speed, 'Date', 'Wind Speed (units)', 'Wind_speed_over_time', 'purple', fig,
                            thick=0.1)
                plot_format(date, dew_point, 'Date', 'Dew Point (Degrees)', 'Dewpoint_over_time', 'orange', fig)
                plot_format(date, pressure, 'Date', 'Pressure (units)', 'Pressure_over_time', 'pink', fig)

            save_plot_png(all_data) # run the plots

            # updating variables to creat the labels

            tempature = float(all_data[-1][14])
            wind_speed = float(all_data[-1][2])
            humidity = float(all_data[-1][13])
            dew_point = float(all_data[-1][15])
            pressure = float(all_data[-1][12])
            wind_direction = int(all_data[-1][1])
            date_n_time = all_data[-1][33]
            sun_rise = str(all_data[-1][22])
            sun_set = str(all_data[-1][24])
            civil_twi = str(all_data[-1][26])
            astro_twi = str(all_data[-1][28])

            # makes the labels
            def create_labels():
                date = datetime.datetime.strptime(date_n_time[:19], "%Y-%m-%dT%H:%M:%S")

                tk.Label(self, text=f'{tempature}', font=SmFONT).place(x=1300, y=635)
                # tk.Label(self, text="Temperature Avg (1h):", font=SmFONT).place(x=925, y=605)
                tk.Label(self, text=f'{wind_speed}', font=SmFONT).place(x=1300, y=665)
                # tk.Label(self, text="Wind Speed Avg (1h):", font=SmFONT).place(x=925, y=665)
                tk.Label(self, text=f'{humidity}', font=SmFONT).place(x=1300, y=695)
                tk.Label(self, text=f'{pressure}', font=SmFONT).place(x=1300, y=725)
                tk.Label(self, text=f'{wind_direction}', font=SmFONT).place(x=1300, y=755)
                tk.Label(self, text=f'{dew_point}', font=SmFONT).place(x=1300, y=785)
                tk.Label(self, text=f'{sun_rise}', font=SmFONT).place(x=1300, y=815)
                tk.Label(self, text=f'{sun_set}', font=SmFONT).place(x=1300, y=845)
                tk.Label(self, text=f'{civil_twi}', font=SmFONT).place(x=1300, y=875)
                tk.Label(self, text=f'{astro_twi}', font=SmFONT).place(x=1300, y=905)

            create_labels()

            ################### Wind direction arrows #################
            # def to make the angle and all the other information on the plot
            def draw_line(x, y, angle):
                plt.xlim(-10, 20) # set the limit so that it can all be seen
                plt.ylim(-10, 20)
                plt.axis('off') # removed axis
                plt.text(4.4, 11, 'N', dict(size=20)) # puts in cardinal directions
                plt.text(4.4, -2.5, 'S', dict(size=20))
                plt.text(-2.5, 4.5, 'W', dict(size=20))
                plt.text(11, 4.5, 'E', dict(size=20))

                # converts angle given to rad
                cartesianAngleRadians = (450 - angle) * math.pi / 180.0
                terminus_x = x * math.cos(cartesianAngleRadians) # creates what is needed for arrow - see plt.arrow support
                terminus_y = y * math.sin(cartesianAngleRadians)

                plt.arrow(5, 5, terminus_x, terminus_y, head_width=0.6, width=0.25, color='black') # plots the arrow
                plt.savefig('wind_direction.png')

            # runs the arrow plotting
            angle = wind_direction
            fig3 = plt.figure()
            plt.axis('equal') # do not remove this makes it work??? .... magic
            draw_line(5, 5, angle) # 5 is the size of the arrow ( astectics)

            # works the same as the camera images to put the image of the arrow onto the gui
            # refresh is still needed as the labels update
            def arrow_image():

                img_arrow = Image.open("wind_direction.png")

                # width, height = img_arrow.size
                # img_arrow = img_arrow.crop([1, 1, 1, 1])
                img_arrow = img_arrow.resize((350, 223))

                self.image_arrow = ImageTk.PhotoImage(img_arrow)

                arrow_but = tk.Button(self, text='Click Me !', image=self.image_arrow)
                arrow_but.place(x=525, y=725)

                canvas.after(50000, arrow_image)

            arrow_image()


            canvas.after(50000, make_plots_and_labels, weather_data_location)

#################### End of Wind direction arrows ###################################
        fig = plt.figure() # the one figure used to make all the weather data plots
        make_plots_and_labels(weather_data_location)

        # takes a screenshot of part of the screen NO SET CORRECTLY AS IT WILL BE DIFFERENT ON THE GATECH COMPUTER
        # JUST NEEDS TO BE PLAYEd WITH
        def take_screen_capture():
            im = ImageGrab.grab(bbox=(400, 200, 1000, 1000))
        
            im.save('Weather_readout_screenshot.png')

        take_screen_capture()
        canvas.after(50000, take_screen_capture)


# second window frame page1
class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        canvas = tk.Canvas()

        label = ttk.Label(self, text="Weather Data Plots", font=LARGEFONT)
        label.place(x=25, y=25)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="StartPage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place
        # by using grid
        button1.place(x=100, y=450, height=50, width=150)

        # button to show frame 2 with text
        # layout2
        button2 = ttk.Button(self, text=" More Weather Plots",
                             command=lambda: controller.show_frame(Page2))

        # putting the button in its place by
        # using grid
        button2.place(x=100, y=500, height=50, width=150)

        #################### Searching weather data files ###################################
        #### There is still a major bug with this where after the older plots are made the new plots get messed up
        # do not know how to fix


        # creates the pop up window for searching past weather data files
        def open_popup():
            top = tk.Toplevel(self)
            top.geometry("750x250")
            top.title("Weather Data Search")
            tk.Label(top, text="Please enter a date for the weather graphs you want to look at").place(x=25, y=25)
            tk.Label(top, text="Ex. YxxxMxDx").place(x=25, y=50)

            e = tk.Entry(top)
            e.place(x=25, y=75)

            def get_info():
                v = e.get() # take input from the text box
                string_to_update = tk.StringVar()
                input_label = tk.Label(top, textvariable=string_to_update, fg='red').place(x=25, y=125)

                # if len(v) == 8 and v.isdigit() == True:
                if os.path.exists(f'{WXDIR}weather_{v}') == True: # makes the date if the file exists
                    string_to_update.set("Beginning Data Processing")

                    # print(f'{WXDIR}weather_{v}')
                    old_data = weather_data(f'{WXDIR}weather_{v}') # gets the old data in arrays
                    DATEDIR = f'{HOMEDIR}weather_plots/{v}/' # creates a variable for the dir

                    # make the plots

                    def save_plot_png(all_data):
                        size = len(all_data)
                        wind_direction = [0] * size
                        date_n_time = [0] * size
                        date = [0] * size
                        tempature = [0] * size
                        wind_speed = [0] * size
                        humidity = [0] * size
                        dew_point = [0] * size
                        pressure = [0] * size

                        for i in range(len(all_data)):
                            tempature[i] = float(all_data[i][14])
                            wind_speed[i] = float(all_data[i][2])
                            humidity[i] = float(all_data[i][13])
                            dew_point[i] = float(all_data[i][15])
                            pressure[i] = float(all_data[i][12])
                            wind_direction[i] = int(all_data[i][1])
                            date_n_time[i] = all_data[i][33]
                            temp = str(date_n_time[i])
                            date[i] = datetime.datetime.strptime(temp[:19], "%Y-%m-%dT%H:%M:%S")

                        # print(date)
                        # plot format for old just changed the save location and what the title is
                        def plot_format2(x, y, xlabel, ylabel, title, color, fig2, thick=1):

                            plt.plot(x, y, c=color, linewidth=thick)
                            plt.title(title)
                            plt.xlabel(xlabel)
                            plt.ylabel(ylabel)
                            plt.xticks(rotation=25)

                            try:
                                os.mkdir(DATEDIR)
                            except Exception as e:
                                pass
                                # print("AAHHH",e)
                            fig2.canvas.draw()
                            plt.savefig(f'{DATEDIR}{title}.png')
                            pickle.dump(fig2, open(f'{DATEDIR}/{title}.pickle', 'wb'))
                            fig2.clear()
                            # FIx so not to many figures will be made

                        plot_format2(date, wind_direction, 'Date', 'Wind Direction (Degrees)',
                                     f'Wind_direction_over_time_{v}',
                                     'green', fig2, thick=0.1)
                        plot_format2(date, tempature, 'Date', 'Tempature (Degrees)', f'Temperature_over_time_{v}',
                                     'red', fig2)
                        plot_format2(date, humidity, 'Date', 'Humidity (Percent)', f'Humidity_over_time_{v}', 'blue',
                                     fig2)
                        plot_format2(date, wind_speed, 'Date', 'Wind Speed (units)', f'Wind_speed_over_time_{v}',
                                     'purple',
                                     fig2,
                                     thick=0.1)
                        plot_format2(date, dew_point, 'Date', 'Dew Point (Degrees)', f'Dewpoint_over_time_{v}',
                                     'orange', fig2)
                        plot_format2(date, pressure, 'Date', 'Pressure (units)', f'Pressure_over_time_{v}', 'pink',
                                     fig2)

                    # a second figure is used to make all these plots
                    fig2 = plt.figure()
                    save_plot_png(old_data)
                    fig2.clear()

                    string_to_update.set("Graphs Complete")
                    os.startfile(DATEDIR)
                    # -update how the save location is determined
                    # make a folder in the weather plots folder
                    # call function to make the same plots to a folder and open the folder so it can be viewed

                # elif len(v) == 8 and v[0] != 2 or v[2] > 2 or v[4] > 3:
                # string_to_update.set("Not a valid date")

                else:
                    string_to_update.set("Not a valid input or no file with that date is found") # displays to the user when the file is not found
                    # tk.Label(top, text="Please make a valid input",fg='red').place(x=25, y=125)

            tk.Button(top, text='Ok', command=get_info).place(x=25, y=100) # makes the ok button to run everythong


        button3 = ttk.Button(self, text="Weather Data Search", command=open_popup)
        button3.place(x=100, y=550, height=50, width=150)

        #################### End of Weather data search ###################################

        # places the weather plots on the weather plots page
        def weather_plots(file_path_in):

            # list_in_files = glob.glob(file_path_in)
            # file_in = max(list_in_files, key=os.path.getctime)
            # print(f"hey {file_out}")
            # ttk.Label(self, text=str(os.path.basename(file_in)), font=SmFONT).place(x=350, y=400)
            plot_1 = Image.open(f'{file_path_in}Dewpoint_over_time.png').resize((550, 350))
            self.plot_1 = ImageTk.PhotoImage(plot_1)
            tk.Button(self, text='Click Me !', image=self.plot_1).place(x=325, y=125)

            plot_2 = Image.open(f'{file_path_in}Temperature_over_time.png').resize((550, 350))
            self.plot_2 = ImageTk.PhotoImage(plot_2)
            tk.Button(self, text='Click Me !', image=self.plot_2).place(x=325, y=500)

            plot_3 = Image.open(f'{file_path_in}Pressure_over_time.png').resize((550, 350))
            self.plot_3 = ImageTk.PhotoImage(plot_3)
            tk.Button(self, text='Click Me !', image=self.plot_3).place(x=925, y=125)

            plot_4 = Image.open(f'{file_path_in}Wind_direction_over_time.png').resize((550, 350))
            self.plot_4 = ImageTk.PhotoImage(plot_4)
            tk.Button(self, text='Click Me !', image=self.plot_4).place(x=925, y=500)

            # plot_5 = Image.open(f'{file_path_in}Wind_speed_over_time.png').resize((550, 350))
            # self.plot_5 = ImageTk.PhotoImage(plot_5)
            # tk.Button(self, text='Click Me !', image=self.plot_5).place(x=950, y=775)

            canvas.after(50000, weather_plots, file_path_in) # refreshes after some time

        weather_plots(WPDIR) # runs the weather plots

        def weather_plots_folder():
            os.startfile(WPDIR)

        ttk.Button(self, text="Weather Plots File Path", command=weather_plots_folder).place(x=100, y=400, height=50,
                                                                                             width=150)
        # button to the weather plots path

# third window frame page2
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        canvas = tk.Canvas()
        label = ttk.Label(self, text="More Weather Data", font=LARGEFONT)
        label.grid(row=0, column=4, padx=10, pady=10)

        # button to show frame 2 with text
        # layout2
        button1 = ttk.Button(self, text="Weather Data Plot 1",
                             command=lambda: controller.show_frame(Page1))

        # putting the button in its place by
        # using grid
        button1.place(x=100, y=450, height=50, width=150)

        # button to show frame 3 with text
        # layout3
        button2 = ttk.Button(self, text="Startpage",
                             command=lambda: controller.show_frame(StartPage))

        # putting the button in its place by
        # using grid
        button2.place(x=100, y=400, height=50, width=150)

        # puts the weather plots on the extra weather plots page
        def weather_plots(file_path_in):
            # list_in_files = glob.glob(file_path_in)
            # file_in = max(list_in_files, key=os.path.getctime)
            # print(f"hey {file_out}")
            # ttk.Label(self, text=str(os.path.basename(file_in)), font=SmFONT).place(x=350, y=400)

            plot_1 = Image.open(f'{file_path_in}Wind_speed_over_time.png').resize((550, 350))
            self.plot_1 = ImageTk.PhotoImage(plot_1)
            tk.Button(self, text='Click Me !', image=self.plot_1).place(x=325, y=125)
            '''
            plot_2 = Image.open(f'{file_path_in}Temperature_over_time.png').resize((550, 350))
            self.plot_2 = ImageTk.PhotoImage(plot_2)
            tk.Button(self, text='Click Me !', image=self.plot_2).place(x=325, y=500)

            plot_3 = Image.open(f'{file_path_in}Pressure_over_time.png').resize((550, 350))
            self.plot_3 = ImageTk.PhotoImage(plot_3)
            tk.Button(self, text='Click Me !', image=self.plot_3).place(x=925, y=125)

            plot_4 = Image.open(f'{file_path_in}Wind_direction_over_time.png').resize((550, 350))
            self.plot_4 = ImageTk.PhotoImage(plot_4)
            tk.Button(self, text='Click Me !', image=self.plot_4).place(x=925, y=500)
            '''
            canvas.after(50000, weather_plots, file_path_in)

        weather_plots(WPDIR)

        def weather_plots_folder():
            os.startfile(WPDIR)


# Driver Code
app = tkinterApp()
app.geometry('1500x1000')
app.title("Trinity GUI")
app.mainloop()
