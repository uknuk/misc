#!/usr/bin/env python3

import os
import re
import argparse
from pytubefix import Playlist
from pytubefix import YouTube
from moviepy.editor import AudioFileClip
from unidecode import unidecode

DIR = f"{os.environ['HOME']}/mus"
REMOVE = r"[\\/\'\"\-_\.,:!;()…]"

def download(v, title, dest):
    stream = v.streams.filter(only_audio=True).order_by('abr').desc()[0]
    print(stream.abr)  
    print(title)
    fname = f"{title}.webm"
    stream.download(dest, fname)
    wpath = f'{dest}/{fname}'
    clip = AudioFileClip(wpath)
    mpath = wpath.replace(".webm", ".mp3")
    clip.write_audiofile(mpath, bitrate=stream.abr.replace('bps',''))
    os.remove(wpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('dest')
    parser.add_argument('-r', '--remove')
    parser.add_argument('-t', '--title')
    parser.add_argument('-n', '--numbers')

    args = parser.parse_args()
    
    dest = f'{DIR}/{args.dest}'
    if not os.path.exists(dest):
        os.makedirs(dest)

    if "list=" in args.url:
        plist = Playlist(args.url)
        videos = list(plist.videos)
        num = 1

        if args.numbers:
            numbers = args.numbers.split(',')
            # use match from 3.12?
            start = int(numbers[0])
            num = int(numbers[1]) if len(numbers) > 1 else start + 1
            videos = videos[start:] if len(numbers) < 3 else videos[start : int(numbers[2])]

        for v in videos:
            print(v.title)
            title = v.title.replace(args.remove, '') if args.remove else v.title
            title = re.sub(REMOVE, '', unidecode(title))
            title = re.sub(' +', '_', title.strip())
            track = num if num > 9 else f'0{num}'
            title = f"{track}_{title}"
            download(v, title, dest)
            num += 1
    else:
        download(YouTube(args.url), args.title, dest) 


