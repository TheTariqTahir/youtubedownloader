from typing import List
from pytube import YouTube
from pytube import Playlist
import os



url = 'https://www.youtube.com/watch?v=yBrMXRhVbRE'

def progress_function(stream, chunk, bytes_remaining):
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
    print(f'Download Progress: {percentage_of_completion}%, Total Size:{totalsz} MB, Downloaded: {dwnd} MB, Remaining:{remain} MB')


yt = YouTube(url)

video_list = {}
video = yt.streams.all()
count = 0
for i in range(len(video)):
    print(i)    
# print(video_list)
# video = yt.streams.get_audio_only()
# video_list.append(video)

# for i in video:
#     video_list.append(i)



# video= YouTube(url,on_progress_callback=progress_function)
# video.streams.filter(progressive=True).last().download()

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