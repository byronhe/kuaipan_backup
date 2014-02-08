#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

__author__ = 'byronhe (lh2008999@gmail.com)'

import Kuaipan
import pprint
from pprint import pprint
import time
import sys
import os
import urllib
import hashlib

def sha1(file_path):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open(file_path, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()

def download_file(file_path,to_dir):
    local_filepath=to_dir+'/'+file_path
    if not os.path.isdir(os.path.dirname(local_filepath)):
        os.makedirs(os.path.dirname(local_filepath))
    if os.path.isfile(local_filepath):
        meta_info=kuaipan_file.metadata(file_path) 
        if meta_info['sha1']==sha1(local_filepath):
            print 'skip file '+file_path + " sha1:",meta_info['sha1']
            return 

    t=time.time()
    r = kuaipan_file.download_file(file_path, local_filepath=local_filepath)
    t=time.time()-t
    sz=os.stat(local_filepath).st_size
    print 'Downdloading file ',file_path,' to ',local_filepath,' size=',sz,'speed='+str( sz / t / 1024),'KB/S'

def download_dir(dir,local_dir):
    content=kuaipan_file.metadata(dir) 
    if content['type'] != "folder":
        download_file(dir,local_dir)
    if 'files' in content:
        for child in content['files']:
            download_dir(dir+"/"+child['name'],local_dir)

#local_path:/a/b/c/d.txt 
#   to_path:/backup/2014/
def upload_file(local_path,to_path):
    remote_path=to_path+'/'+os.path.basename(local_path)
    to_dir=os.path.dirname(remote_path)

    r=kuaipan_file.fileops_create_folder(to_dir)
    #print 'Create directory ',r['path']," ",r['msg']

    #meta_info=kuaipan_file.metadata(remote_path) 
    #if meta_info['sha1']==sha1(local_path):
    #    print 'skip file '+local_path + " remote:" +remote_path+ " sha1:",meta_info['sha1']
    #    return 

    t=time.time()
    print 'Upload file ',local_path,' to ',remote_path
    r = kuaipan_file.upload_file(local_path, remote_path ,ForceOverwrite=True)
    t=time.time()-t
    #print 'Upload file ',local_path,' to ',remote_path,' size='+r['size']
    print 'Upload file ',local_path,' to ',remote_path,' size='+r['size'],'speed='+str(int(r['size']) / t / 1024),'KB/S'

def walk_upload(to_path,dir,files):
    for f in files:
        p=dir+"/"+f
        if os.path.isfile(p):
            upload_file(p,to_path)

def upload_dir(local_path,to_path):
    if os.path.isdir(local_path):
        os.path.walk(local_path,walk_upload,to_path)
    else:
        upload_file(local_path,to_path)



def ls_dir(dir,indent=0):
    meta_info=kuaipan_file.metadata(dir)
        #pprint.pprint(meta_info)
    if 'type' in meta_info and meta_info['type'] != "folder":
        print ' '*indent,meta_info['path'],'\t',meta_info['size'],'\t',meta_info['type'],'\t',meta_info['sha1'],'\t',meta_info['modify_time']
    else:
        print ' '*indent,'\t',meta_info['path']
        if 'files' in meta_info:
            for child in meta_info['files']:
                ls_dir(dir+'/'+child['name'],indent+4)



consumer_key = 'consumer_key here'
consumer_secret = 'consumer_secret here'
oauth_token        = 'oauth_token here'
oauth_token_secret = 'oauth_token_secret here'

kuaipan_file = Kuaipan.KuaipanFile(consumer_key, consumer_secret, oauth_token, oauth_token_secret)



print " "*20,"Your Account Information:"
pprint( kuaipan_file.account_info() )
print "\n"

if len(sys.argv) < 2:
    print "usage example:"
    print sys.argv[0],"ls /backup/"
    print sys.argv[0],"upload /tmp/ /backup/2014_2_5/"
    print sys.argv[0],"download /backup/2014_2_5/ /tmp/restore/"
    sys.exit(0)

if sys.argv[1] == "ls":
    if len(sys.argv) == 3:
        ls_dir(sys.argv[2])
    else:
        ls_dir("/")

if sys.argv[1] == "upload":
    if len(sys.argv) == 4:
        upload_dir(sys.argv[2],sys.argv[3])

if sys.argv[1] == "download":
    if len(sys.argv) == 4:
        download_dir(sys.argv[2],sys.argv[3])
