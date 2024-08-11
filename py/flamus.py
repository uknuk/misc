#!/usr/bin/env python3

from os import environ, path, listdir
import re
from flask import Flask, Response, jsonify

DIR = '.flamus'

def convert(name):
        if name[:2] == 'M0':
            return name.replace('M0', '200')

        if name[:2] == 'Op':
            return name.replace('Op', '')

        if re.compile('^\d{2}[\s+|_|-]').match(name):
            return '20' + name if int(name[:2]) < 30 else '19' + name

        return name

app = Flask(__name__)

@app.route("/play")
def play():
    fname = "/home/bma/Music/Ange/77_Tome_VI.mp3"
    def generate():
        with open(fname, "rb") as f:
            data = f.read(1024)
            while data:
                yield data
                data = f.read(1024)
    resp = Response(generate(), mimetype="audio/mpeg")
    return resp

@app.route("/artists")
def get_artists():
    root = path.join(environ['HOME'], DIR, 'media')
    arts = {}
    for dir in listdir(root):
        for name in listdir(path.join(root,dir)):
            arts[name] = path.join(dir, name)

    return jsonify(arts)

@app.route("/artists/<location>/<artist>")
def get_artist(location, artist):
    art_path = path.join(environ['HOME'], DIR, 'media', location, artist)
    albs = sorted(listdir(art_path), key = lambda d: convert(d))
    return jsonify(albs)






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1927)