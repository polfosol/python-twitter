# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 11:48:30 2020

@author: polfosol
"""

import os
import sys
import time
import mimetypes

MEDIA_ENDPOINT_URL = 'https://upload.twitter.com/1.1/media/upload.json'

import requests
from requests_oauthlib import OAuth1

class twitter_media(object):

  def __init__(self, api_key, api_secret, access_token, token_secret):
    '''
    Defines API credentials
    '''
    self.oauth = OAuth1(api_key, client_secret = api_secret,
                        resource_owner_key = access_token,
                        resource_owner_secret = token_secret)

  def open(self, file_name):
    '''
    Open the file and determine its type and other info
    '''
    self.filename = file_name
    self.total_bytes = os.path.getsize(file_name)
    self.media_type = mimetypes.guess_type(file_name)[0]
    self.media_id = None
    self.processing_info = None
    self.category = 'tweet_video'
    if self.media_type == 'image/gif':
        self.category = 'tweet_gif'
    elif 'image' in self.media_type:
        self.category = 'tweet_image'
    # category values: AMPLIFY_VIDEO, TWEET_GIF, TWEET_IMAGE, TWEET_VIDEO


  def upload_init(self, file_name):
    '''
    Initializes Upload
    '''
    self.open(file_name)
    data = {
        'command': 'INIT',
        'media_type': self.media_type,
        'total_bytes': self.total_bytes,
        'media_category': self.category
    }
    req = requests.post(url = MEDIA_ENDPOINT_URL, data = data, auth = self.oauth)
    media_id = req.json()['media_id']
    self.media_id = media_id
    print('INIT uploading', os.path.split(file_name)[-1])


  def upload_append(self):
    '''
    Uploads media in chunks and appends to chunks uploaded
    '''
    segment_id = 0
    bytes_sent = 0
    file = open(self.filename, 'rb')
    while bytes_sent < self.total_bytes:

        chunk = file.read(4*1024*1024)
        data = {
            'command': 'APPEND',
            'media_id': self.media_id,
            'segment_index': segment_id
        }
        print('APPEND')
        req = requests.post(url = MEDIA_ENDPOINT_URL,
                            data = data,
                            files = { 'media': chunk },
                            auth = self.oauth)
        segment_id = segment_id + 1

        if req.status_code < 200 or req.status_code > 299:
            print(req.status_code)
            print(req.text)
            sys.exit(0)
        bytes_sent = file.tell()
        print('%s of %s bytes uploaded' % (str(bytes_sent), str(self.total_bytes)))

    print('Upload chunks complete.')


  def upload_finalize(self):
    '''
    Finalizes uploads and starts video processing
    '''
    print('FINALIZE')
    data = {
        'command': 'FINALIZE',
        'media_id': self.media_id
    }
    req = requests.post(url = MEDIA_ENDPOINT_URL, data = data, auth = self.oauth)
    print(req.json())
    self.processing_info = req.json().get('processing_info', None)
    self.check_status()


  def check_status(self):
    '''
    Checks video processing status
    '''
    if self.processing_info is None:
        return

    state = self.processing_info['state']
    print('Media processing status is %s ' % state)

    if state == u'succeeded':
        return
    if state == u'failed':
        sys.exit(0)

    check_after_secs = self.processing_info['check_after_secs']    
    print('Checking after %s seconds' % str(check_after_secs))
    time.sleep(check_after_secs)

    print('STATUS')
    params = {
        'command': 'STATUS',
        'media_id': self.media_id
    }
    req = requests.get(url = MEDIA_ENDPOINT_URL, params = params, auth = self.oauth)
    self.processing_info = req.json().get('processing_info', None)
    self.check_status()


FILE_NAME = 'C:/path/to/media/test.gif'
CONSUMER_KEY = 'api consumer key'
CONSUMER_SECRET = 'api consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'token secret'

if __name__ == '__main__':
  tm = twitter_media(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
  tm.upload_init(FILE_NAME)
  tm.upload_append()
  tm.upload_finalize()
  print('media id is:', tm.media_id)
