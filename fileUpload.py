# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 19:52:06 2016

@author: strider
"""

from uuid import uuid4
import boto
import os.path
from flask import current_app as app
from werkzeug.utils import secure_filename
from boto.s3.key import Key
import urllib


#source_filename = secure_filename(source_file.data.filename)
#source_extension = os.path.splitext(source_filename)[1]
def storeFileInS3(transcript,filename, filetype):
    #filename = open(filename, 'r+')
    conn = boto.connect_s3('AKIAIEGTSP66KGYIBMOQ', 'MK6dNfWvE/tdNhGIYxU1zs/K1677dt6nyrD80tYT')
    bucket = conn.get_bucket('amgen-student-data')
    k = Key(bucket)
    if filetype == 'Transcript':
        k.key = '/Transcripts/'+filename
    else:
        k.key = '/Referral/'+filename
    sent = k.set_contents_from_string(transcript.read())
#sml.set_acl(acl)

def viewTranscript(filename):
    conn = boto.connect_s3('AKIAIEGTSP66KGYIBMOQ', 'MK6dNfWvE/tdNhGIYxU1zs/K1677dt6nyrD80tYT')
    bucket = conn.get_bucket('amgen-student-data')
    key = bucket.get_key('/Transcripts/'+filename)
    key.content_type = 'application/pdf'
    receive = key.get_contents_as_string()
    #receive = key.get_contents_to_filename(filename)
    #print(receive)
    return receive
    
def viewReferral(filename):
    conn = boto.connect_s3('AKIAIEGTSP66KGYIBMOQ', 'MK6dNfWvE/tdNhGIYxU1zs/K1677dt6nyrD80tYT')
    bucket = conn.get_bucket('amgen-student-data')
    key = bucket.get_key('/Referral/'+filename)
    key.content_type = 'application/pdf'
    receive = key.get_contents_as_string()
    print(receive)
    return receive