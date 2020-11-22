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
    reply = mention
    images = []
    if len(image) > 0:
        images = [api.media_upload(m).media_id_string for m in image.split("|")]
    if reply != "" and len(reply) < 4:
        time.sleep(.5)
        reply = api.user_timeline(screen_name = 'polfosol',
                                  count = 1,
                                  include_rts = False)[0].id_str
    api.update_status(status = text, media_ids = images, in_reply_to_status_id = reply)

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
