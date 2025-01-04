# Highlight Reel

This spaghetti code is my first ever project that I completed. I did not know how to split code into different files yet

# Reason?
A game I was playing at the time was Rocket League and I was looking for a reason to use my basic python abilities and continue to learn by doing I decided to attempt to create an automated highlight reel. 

# Okay but this still makes no sense...
At the time there was something going on in E-sports and youtube was getting a lot of views - I figured if I could automate this maybe I could make a little bit of money making a youtube videos passively and since I enjoyed the game at the time It was fun.

# Plan
- OBS is running - Using OBS START Button located in GUI, this was made for ease of use
- Planned but never implemented was the OpenCV monitoring the game state

This would work by creating a gui, then while watching (later to thought to use OpenCV in order to complete the following) when a goal was scored a button would be pressed this would create a timestamp in json. When the goal was timestamped to the game we then by creating a specific time window from when the goal was scored to include the previous 10 seconds for context of the goal and then a following 5 seconds as there are specific celebrations, This would add up for a total of 15 second clips. This would compound over the entire match often adding up to less than a few minutes. Rocket League matches are 5 minutes in length.

## Tkinter GUI
I initially used Tkinter as it was a lightweight gui, I merely needed a list of buttons in vertical column that would give functionality to the code.


