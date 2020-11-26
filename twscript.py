# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 19:33:11 2020

@author: polfosol
"""

APIkey = "Enter your API key here"
APIsecret = "then set the API secret key"
AccessToken = "here is your access token..."
AccessTokenSecret = "and, access token secret"
# >> Location is Paris, France (Yeah bitch!):
latitude = 48.86
longitude = 2.35

import tweepy
auth = tweepy.OAuthHandler(APIkey, APIsecret)
auth.set_access_token(AccessToken, AccessTokenSecret)
api = tweepy.API(auth)

import time
def add_tweet_to_thread(text, media, attach, reply):
    parameters = dict(status = text,
                      lat = latitude,
                      long = longitude,
                      display_coordinates = True,
                      enable_dmcommands = True)
    if len(attach) > 0:
        parameters.update(attachment_url = attach.strip())
    if len(reply) > 0:
        parameters.update(in_reply_to_status_id = reply.strip(' -'))
    if reply.endswith('-'):
        parameters.update(auto_populate_reply_metadata = True)
    if len(media) > 0:
        parameters.update(media_ids = media)
    time.sleep(.5)
    return api.update_status(**parameters).id_str

import sys
# import os
# import tkinter as tk
# from tkinter import filedialog as dialog
import easygui
def load_thread(textfile):
    if len(textfile) > 0:
        return open(textfile, "r", encoding = "utf8").read()
    # root = tk.Tk()
    # root.withdraw()
    # f = dialog.askopenfile(mode = "r", filetypes = [('Text', ['.txt'])]).name
    # path = os.path.realpath(f)
    path = easygui.fileopenbox(default = '*.txt')
    return open(path, "r", encoding = "utf8").read()

tweets = []
if __name__ == '__main__':
    file = ''
    try:
        file = sys.argv[1]
        latitude = float(sys.argv[2])
        longitude = float(sys.argv[3])
    except:
        pass
    tweets = load_thread(file).split("`")
    if len(tweets) == 0 or tweets[0] == '':
        sys.exit("Error: thread is empty!")

thread = [['', [], '', ''] for t in tweets]
last = ''
for i in range(len(thread)):
    media = []
    text = tweets[i].strip()
    if i == 0 and text.startswith("REPLY<"):
        last = text[:text.find('>')].split('<')[1]
        text = text[text.find('\n') + 1:]
    if text.endswith(">MEDIA"):
        media = text[text.rfind('<') + 1:].split('>')[0].split('|')
        text = text[:text.rfind('\n')].strip()
    if text.endswith(">ATTACH"):
        thread[i][2] = text[text.rfind('<') + 1:].split('>')[0]
        text = text[:text.rfind('\n')].strip()
    thread[i][0] = text
    thread[i][1] = [api.media_upload(m).media_id_string for m in media]

for tweet in thread:
    tweet[3] = last
    for j in [1, 2, 3]:
        try:
            last = add_tweet_to_thread(*tweet)
        except:
            last = 'error'
            pass
        if last != 'error':
            print("tweet", i+1, "is sent! id:", last)
            break;
        elif j < 3:
            print("an error occurred. retrying...")
        else:
            raise SystemExit("Connection error or whatever!")
