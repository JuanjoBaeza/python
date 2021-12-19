from pytube import YouTube

# Install this pytube version -> pip install git+https://github.com/nficano/pytube
# To extract the audio track -> apt-get install ffmpeg -> ffmpeg -i /PATH/INPUT.mp4 /PATH/OUTPUT.mp3

link = input ("Enter the link of YouTube video you want to download: ")
yt = YouTube(link)

print("Title: ",yt.title)
print("Number of views: ",yt.views)
print("Length of video: ",yt.length)
print("Rating of video: ",yt.rating)

ys = yt.streams.get_highest_resolution()

print("Downloading...")
ys.download()
print("Download completed!!")