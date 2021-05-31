from pytube import YouTube

class getVideo:
    streams=[]

    def search(self,url):
        self.streams.clear()
        yt = YouTube(url)
        for i in yt.streams.filter(file_extension='mp4').all():
            self.streams.append(i)
        return self.streams
    
    def down(self,index,path):
        self.streams[index].download(path)

    
        