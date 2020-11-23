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
def add_tweet_to_thread(text, image, mention):
    parameters = dict(status = text,
                      lat = 48.86, # Paris coordinates!
                      long = 2.35,
                      display_coordinates = True,
                      enable_dmcommands = True)
    if len(image) > 0:
        media = [api.media_upload(m).media_id_string for m in image.split("|")]
        parameters.update(media_ids = media)
    if len(mention) > 3:
        parameters.update(in_reply_to_status_id = mention)
    elif mention != "":
        time.sleep(.5)
        last = dict(screen_name = 'polfosol', count = 1, include_rts = False)
        last_id = api.user_timeline(**last)[0].id_str
        parameters.update(in_reply_to_status_id = last_id)
    api.update_status(**parameters)

mythread = open(path, "r", encoding = "utf8").read()
tweets = mythread.split("`")

for i in range(len(tweets)):
    media = ""
    reply = "" if i == 0 else str(i)
    tweet = tweets[i].strip()
    if i == 0 and tweet.startswith("REPLY<"):
        reply = tweet[:tweet.find('>')].split("<")[1]
        tweet = tweet[tweet.find('\n') + 1:].strip()
    if tweet.endswith(">MEDIA"):
        media = tweet[tweet.rfind('<') + 1:].split(">")[0]
        tweet = tweet[:tweet.rfind('\n')].strip()
    add_tweet_to_thread(tweet, media.strip(), reply)
    print("tweet", i+1, "is sent!")
