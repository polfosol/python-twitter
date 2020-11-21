# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 19:33:11 2020

@author: polfosol
"""

import easygui
path = easygui.fileopenbox(default = '*.txt')

# import os as win
# import tkinter as tk
# from tkinter import filedialog
# root = tk.Tk()
# root.withdraw()
# thr = filedialog.askopenfile(mode="r", filetypes=[('Thread', ['.txt'])]).name
# path = win.path.realpath(thr)

import tweepy
auth = tweepy.OAuthHandler(
    "strlen=25",
    "strlen=50")
auth.set_access_token(
    "strlrn=50",
    "strlen=45")
api = tweepy.API(auth)

import time as clock
def add_tweet_to_thread(text, image, j, mention):
    reply = mention
    images = []
    if len(image) > 0:
        images = [api.media_upload(m).media_id_string for m in image.split("|")]
    if j > 0:
        clock.sleep(.5)
        reply = api.user_timeline(screen_name = 'polfosol',
                                  count = 1, include_rts = False)[0].id_str
    if len(reply) > 0:
        api.update_status(status = text, media_ids = images,
                          in_reply_to_status_id = reply)
    else:
        api.update_status(status = text, media_ids = images)

mythread = open(path, "r", encoding = "utf8").read()
tweets = mythread.split("`")

for i in range(len(tweets)):
    media = ""
    reply = ""
    tweet = tweets[i].strip()
    if i == 0 and tweet.startswith("REPLY<"):
        reply = tweet.split("<")[1].split(">")[0]
        tweet = tweet[tweet.find('\n') + 1:].strip()
    if tweet.endswith(">MEDIA"):
        media = tweet[tweet.rfind('\n') + 1:].split("<")[1].split(">")[0]
        tweet = tweet[:tweet.rfind('\n')].strip()
    add_tweet_to_thread(tweet, media.strip(), i, reply)
    print("tweet", i+1, "is sent!")
