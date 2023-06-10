# Import the Tkinter module
import tkinter as tk
import subprocess
import pyautogui as pag
import datetime
from datetime import timedelta, datetime
import os
import pydirectinput as pdi
import time
import json
import shutil
import moviepy.editor as mpy
import psutil

timestamps = {}
clicks = {'click':0}
goal_time_edit = list()
goal_time_edit_seconds = list()

# Create a new Tkinter window
window = tk.Tk()

# Change the title of the window
window.title("Mike's Project Version: 2")

# Set the window size to 200x400 pixels
window.geometry("375x400+0+0")

button_names = [
    "Open OBS",
    "Start",
    "Goal",
    "Stop",
    "Convert Timestamps to JSON",
    "Make New Video"#,
    #" "
]

# Open OBS application
def open_obs():
    obsapp_path = "C:\\Users\\Micha\\Desktop\\OneDrive\\Project_Twitch\\obs64.lnk"
    obs_app = subprocess.Popen([r'C:\\Users\\Micha\\Desktop\\OneDrive\\Project_Twitch\\obs64.lnk'], shell=True)
    print()

# Get current time and format it as a string
def get_time(): 
    current_time = datetime.now()
    formatted_time = "{:%Y-%b-%d %H-%M-%S}".format(datetime.now())
    return current_time, formatted_time

# Records timestamp when start button clicked
def start():
    pdi.press('up')
    timestamps.update({'Name': get_time()[1]})
    timestamps.update({'Start': get_time()[0]})
    os.startfile('C:\\Users\\Micha\\Desktop\\OneDrive\\Twitch')
    print("Start")

# Record timestamp when goal button clicked
def goal():
    clicks['click'] += 1
    output = "Goal {}"
    for click_number in clicks.values():
        goal = output.format(click_number)
        timestamps.update({goal: get_time()[0]})
        print(goal)

# Record timestamp when stop button clicked
def stop():
    pdi.press('down')
    timestamps.update({'Stop': get_time()[0]})
    print("Stop")

# Convert timestamps to JSON format
def converted_timestamps():
    start = timestamps['Start']
    goal_timestamps = timestamps.copy()
    goal_timestamps.pop('Name')
    goal_timestamps.pop('Start')
    goal_timestamps.pop('Stop')
    #print(goal_timestamps)
    for goal_number, goal in goal_timestamps.items():
        goal_time = str(goal - start)
        goal_timestamps[goal_number] = goal_time
    print(goal_timestamps)
    time.sleep(2)  
    timestamp = timestamps['Name']
    source = 'C:\\Users\\Micha\\Desktop\\OneDrive\\Twitch'
    destination = 'C:\\Users\\Micha\\Desktop\\OneDrive\\Twitch\\' + timestamp
    twitch_dir = os.listdir(source)
    os.mkdir(destination)
    mp4_file = timestamp + '.mp4'
    mp4_exist = os.path.exists(source + "\\" + 'RENAME.mp4')
    json_object = timestamp + '.json'
    try:
        if os.path.exists(destination) == True:
            os.chdir(destination)
            with open(json_object, 'w') as outfile:
                json.dump(goal_timestamps, outfile)
    finally: 
        os.chdir(source)
        if mp4_exist == True:
            time.sleep(0.5)
            old_name = 'RENAME.mp4'
            os.rename(old_name, mp4_file)
            shutil.move(mp4_file, destination)

def json_edit():  
    #timestamp = '2022-Dec-07 16-29-52.json'
    timestamp = timestamps['Name']
    source = 'C:\\Users\\Micha\\Desktop\\OneDrive\\Twitch'
    #destination = source + '\\' + '2022-Dec-07 16-29-52'
    destination = source + '\\' + timestamp
    
    os.chdir(destination)
    #with open(timestamp + '.json', 'r') as openfile:
        #json_object = json.load(openfile)
    with open(timestamp + '.json', 'r') as openfile:
        json_object = json.load(openfile)
        print(json_object)
    
    for goal_number, goal_time in json_object.items():
        semicolon_remove = goal_time.replace(':', '')
        goal_time_edit.append(semicolon_remove[1:5])

    print(goal_time_edit)
   
    for i in goal_time_edit:
        min = i[0:2]
        sec = i[2:4]
        multiply = int(min) * 60
        full_time = multiply + int(sec)
        goal_time_edit_seconds.append(full_time)
        #print(min, sec, full_time)
        print(full_time)
  
    clip_max_list = list()
    clip_min_list = list()
    
    for full_time in goal_time_edit_seconds:
        clip_range_max = full_time + 10
        clip_range_min = full_time - 10
        
        clip_min_list.append(clip_range_min)
        clip_max_list.append(clip_range_max)
    
    #print(clip_min_list, clip_max_list)
    

    for i in range(len(clip_min_list)):
        if clip_min_list[i] < 0:
            clip_min_list[i] = 0

    # Not necessary when manual
    #clip_max_list[-1] = clip_max_list[-1] - 5
    
    #print(clip_min_list, clip_max_list)

    clip_max_list_errors = list()
    
    for x in clip_max_list:
        
        if x > clip_max_list[-1]:
            errors = x - 10
            clip_max_list_errors.append(errors)
            #print(errors)
    
    delete_until = len(clip_max_list_errors) - 1
    
    print(clip_max_list_errors, "went over time")
    
    for i in clip_max_list_errors:
        clip_max_list[delete_until:-1] = clip_max_list_errors
    
    #print(clip_max_list)    
    
    clip_range = dict()
    
    for key in clip_min_list:
        for value in clip_max_list:
            clip_range[key] = value
            clip_max_list.remove(value)
            break
    print(clip_range)

    video_mp4 = timestamps['Name'] + '.mp4'
    print(video_mp4)
    video = mpy.VideoFileClip(video_mp4)
    
    unfinished_clips = list()
        
    for i in clip_range:
        clip = video.subclip(i, clip_range[i])
        unfinished_clips.append(clip)


    finished_clip = mpy.concatenate_videoclips(unfinished_clips)
    finished_clip.write_videofile(timestamps['Name'] + '_clipped.mp4', threads=8, fps=60, preset='ultrafast')
    video.close()

# Create the buttons and add them to the window
for button_name in button_names:
    button = tk.Button(window, text=button_name)

    # Set the button's command to the corresponding function
    if button_name == "Open OBS":
        button.configure(command= open_obs)
    elif button_name == "Start":
        button.configure(command= start)
    elif button_name == "Goal":
        button.configure(command= goal)
    elif button_name == "Stop":
        button.configure(command= stop)
    elif button_name == "Convert Timestamps to JSON":
        button.configure(command= converted_timestamps)
    elif button_name == "Make New Video":
        button.configure(command=json_edit)

    # Set the button's background color to black and text color to white
    button.configure(bg="black", fg="white")

    # Set the button's font size to 20 pixels
    button.configure(font=("Arial", 20))
    
    # Add the button to the window
    button.pack(fill=tk.BOTH, expand=True)

# Start Tkinter loop
window.mainloop()
