from  pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=oJkR5z50RZU')
video_title = yt.title
video = yt.streams
for i in video.filter(file_extension='mp4',res='720p').all():
    print(i)



