# python-system-info
A port of my old Bash system info script to Python. Python has a lot more cool things I wanted to try, so I started porting it over. Will be updating it over time as I make changes.

Important Info:
  1) Requires Python 3.x
  2) Requires psutil
  3) Requires curses
  4) Requires pyalsaaudio
  0) [More to come]
  
To Do:
  1) ~~Add colours~~ DONE!
  2) ~~Make conditional colour formatting~~ DONE!
  3) _Split some of the longer functions_ UPDATED!
  4) ~~Make application use curses~~ DONE!
  5) _Create new modules/libraries to separate functions_ UPDATED!
  6) ~~Add audio monitoring and controls~~ DONE!
  7) Add command-line arguments capabilities
  0) [More to come]
  
Controls:
  1) Mute volume (M/m)
  2) Reset volume (R/r) -- default is 50, but you can change it
  3) Raise volume (A/a) -- default step is 2, but you can change it
  4) Lower volume (Z/z) -- same as above
  5) Quit (ESC/Q/q)

<img src='https://i.imgur.com/qzVMX87.png'/>
<img src='https://i.imgur.com/UlDMNek.png'/>
<img src='https://i.imgur.com/YCeNOGH.png'/>
