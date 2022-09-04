# from pytube import YouTube
# from moviepy.editor import *

# import os


# yt = YouTube('https://youtu.be/FwhnIxAAwxo')

# video = yt.streams.get_by_itag(134) 

# path = 'sdcard/kivy'
# path = os.getcwd()

# name= video.default_filename
# new_name = f'_{name}'
# video.download()

import os
cwd = os.getcwd()
name = os.path.join(cwd,'a.mp4')
new_name = os.path.join(cwd,'_a.mp4')
print(name)
import ffmpeg
ffmpeg.input(name).output(new_name).run()


# clip =VideoFileClip(name)

# clip.write_videofile(new_name)
# clip.close()

# os.remove(os.path.join(path,name))
