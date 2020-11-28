# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 19:33:11 2020

@author: polfosol
"""

APIkey = "Enter your API key here"
APIConsumerSecret = "then set the API secret key"
AccessToken = "here is your access token..."
AccessTokenSecret = "and, access token secret"
# >> Location is Paris, France (Yeah bitch!):
latitude = 48.86  # 29.98   -12.046
longitude = 2.35  # 31.134  -77.043 which is Cairo and Lima

import tweepy
auth = tweepy.OAuthHandler(APIkey, APIConsumerSecret)
auth.set_access_token(AccessToken, AccessTokenSecret)
api = tweepy.API(auth)

from large_media import twitter_media as uploader
med = uploader(APIkey, APIConsumerSecret, AccessToken, AccessTokenSecret)

import os
def upload_the_media(file):
    text = 'error'
    for j in [1, 2, 3]:
        try:
            if os.path.getsize(file) > 4000000:
                med.upload_init(file)
                med.upload_append()
                med.upload_finalize()
                text = str(med.media_id)
            else:
                text = api.media_upload(file).media_id_string
            break
        except:
            if j == 3:
                print("Error: failed to upload", file)
            pass
    return text

def upload_all_media(allfiles, backup):
    allmedia_ids = dict()
    for file in allfiles:
        if not os.path.isfile(file):
            allmedia_ids[file] = 'error' if ':' in file else file
            continue
        allmedia_ids[file] = upload_the_media(file)
        if allmedia_ids[file] != 'error':
            backup = backup.replace(file, allmedia_ids[file])
    # verify:
    if 'error' in allmedia_ids.values():
        with open('backup', 'w', encoding = 'utf8') as backup_file:
            backup_file.write(backup)
        sys.exit("process is terminated due to these errors.")
    return allmedia_ids

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

# import tkinter as tk
# from tkinter import filedialog as dialog
import easygui
import sys
def load_thread():
    # root = tk.Tk()
    # root.withdraw()
    # f = dialog.askopenfile(mode = "r", filetypes = [('Text', ['.txt'])]).name
    # return os.path.realpath(f)
    return easygui.fileopenbox(default = '*.txt')

tweets = []
if __name__ == '__main__':
    file = ''
    try:
        file = sys.argv[1]
        latitude = float(sys.argv[2])
        longitude = float(sys.argv[3])
    except:
        pass
    if len(file) == 0:
        file = load_thread()
    tweets = open(file, "r", encoding = "utf8").read().split("`")
    print("processing content...")
    if len(tweets) == 0 or tweets[0] == '':
        sys.exit("Error: thread is empty!")

thread = [['', [], '', ''] for t in tweets]
last = ''

for i, tweet in enumerate(thread):
    text = tweets[i].strip()
    if i == 0 and text.startswith("REPLY<"):
        last = text[:text.find('>')][text.find('<') + 1:].split('/')[-1]
        text = text[text.find('\n') + 1:]
    if text.endswith(">MEDIA"):
        tweet[1] = text[:text.rfind('>')][text.rfind('<') + 1:].split('|')
        text = text[:text.rfind('\n')]
    if text.endswith(">ATTACH"):
        tweet[2] = text[:text.rfind('>')][text.rfind('<') + 1:]
        text = text[:text.rfind('\n')]
    tweet[0] = text.strip()

media_files = (m for tweet in thread for m in tweet[1])
uploaded = upload_all_media(media_files, "`".join(tweets))

for i, tweet in enumerate(thread, start = 1):
    tweet[3] = last
    tweet[1] = [uploaded[m] for m in tweet[1]]
    last = add_tweet_to_thread(*tweet)
    print("tweet", i, "is sent!")
