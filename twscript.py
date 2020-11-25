# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 19:33:11 2020

@author: polfosol
"""

# import easygui
# path = easygui.fileopenbox(default = '*.txt')

import os
import tkinter as tk
from tkinter import filedialog as dialog
root = tk.Tk()
root.withdraw()
file = dialog.askopenfile(mode = "r", filetypes = [('Text', ['.txt'])]).name
path = os.path.realpath(file)

import tweepy
auth = tweepy.OAuthHandler(
    "placeholder for: API key",
    "placeholder for: API secret key")
auth.set_access_token(
    "placeholder for: Access token",
    "placeholder for: Access token secret")
api = tweepy.API(auth)

import time
def add_tweet_to_thread(text, media, attach, reply):
    parameters = dict(status = text,
                      lat = 48.86,
                      long = 2.35,
                      display_coordinates = True)
    if len(attach) > 0:
        parameters.update(attachment_url = attach.strip())
    if len(reply) > 0:
        parameters.update(in_reply_to_status_id = reply.strip())
        parameters.update(auto_populate_reply_metadata = True)
    if len(media) > 0:
        images = [api.media_upload(m).media_id_string for m in media]
        parameters.update(media_ids = images)
    else:
        time.sleep(.5)
    return api.update_status(**parameters).id_str

content = open(path, "r", encoding = "utf8").read()
tweets = content.split("`")
thread = [['', [], '', ''] for t in tweets]
twlast = ''

for i in range(len(thread)):
    text = tweets[i].strip()
    if i == 0 and text.startswith("REPLY<"):
        twlast = text[:text.find('>')].split('<')[1]
        text = text[text.find('\n') + 1:]
    if text.endswith(">MEDIA"):
        thread[i][1] = text[text.rfind('<') + 1:].split('>')[0].split('|')
        text = text[:text.rfind('\n')].strip()
    if text.endswith(">ATTACH"):
        thread[i][2] = text[text.rfind('<') + 1:].split('>')[0]
        text = text[:text.rfind('\n')].strip()
    thread[i][0] = text

for tweet in thread:
    tweet[3] = twlast
    twlast = add_tweet_to_thread(*tweet)
    print("tweet", i+1, "is sent!")
