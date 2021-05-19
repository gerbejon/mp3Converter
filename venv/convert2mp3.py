#!/bin/env python
# Requires: youtube_dl module
# Requires: ffmpeg
# Usage:
#
# python youtubeConverter.py <URL>, ...
#
# Example:
#
# python venv/youtubeConverter.py https://www.youtube.com/watch?v=ileD0jgo_Pc

import youtube_dl
import sys
from mp3_tagger import MP3File
import eyed3

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloaded_files/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


if __name__ == "__main__":
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        filenames = sys.argv[1:]
        meta = ydl.extract_info(filenames[0], download=False)
        ydl.download(filenames)
        filedir = 'downloaded_files/%s'%(meta['title'])+'.mp3'
        audiofile = eyed3.load(filedir)
        try:
            if meta['artist'] != None:
                audiofile.tag.artist = meta['artist']
            else:
                audiofile.tag.artist = meta['uploader']
        except:
            audiofile.tag.artist = meta['uploader']
        audiofile.tag.title = meta['title']
        audiofile.tag.save(filedir)
