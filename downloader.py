from typing import List
from pytube import YouTube
from pytube import Playlist
from moviepy.editor import *
import os



url = 'https://www.youtube.com/watch?v=0TWIT1Q264c'

def progress_function(stream, chunk, bytes_remaining,text):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    totalsz = (total_size/1024)/1024
    totalsz = round(totalsz,1)
    remain = (bytes_remaining / 1024) / 1024
    remain = round(remain, 1)
    dwnd = (bytes_downloaded / 1024) / 1024
    dwnd = round(dwnd, 1)
    percentage_of_completion = round(percentage_of_completion,2)
    print(text)
    # print(f'Download Progress: {percentage_of_completion}%, Total Size:{totalsz} MB, Downloaded: {dwnd} MB, Remaining:{remain} MB')

text='asdf'
# video= YouTube(url,on_progress_callback=(lambda text = text :progress_function(text)))
video= YouTube(url,on_progress_callback=progress_function(**kwargs,text))
video.streams.filter(progressive=True).first().download()

# yt = YouTube(url)

# video_list = {}
# video = yt.streams.first().default_filename

# name = (video.split('.'))
# print(f'{name[0]}.{name[1]}')

# for i in range(len(video)):
#     print(i)    
# print(video_list)
# video = yt.streams.get_audio_only()
# video_list.append(video)

# for i in video:
#     video_list.append(i)




# for playlist

# from pathlib import Path
# downloads_path = str(Path.home() / "YoutubeDownloads")
# print(downloads_path)

# playlist_= Playlist(url)
# path = os.getcwd()
# for v in playlist_.videos:
#     # v.streams.filter(file_extension='mp3').first().download()
#     name = v.title[:round(len(v.title)/2)]
#     try:
#         v.streams.get_audio_only().download(filename=f'{name}.mp4')
#         mp4_without_frames = AudioFileClip(f'{name}.mp4')
#         mp4_without_frames.write_audiofile(f'{name}__.mp3')
#         mp4_without_frames.close() # function call mp4_to_mp3("my_mp4_path.mp4", "audio.mp3")
#         os.remove(os.path.join(path,f'{name}.mp4'))
#         print('done==========')
        
#     except Exception as e:
#         print(e)