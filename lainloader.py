#!/usr/bin/env python3
import base64
import hashlib
import json
import os
import sys
import urllib.request

# directory is a string containing the directory path to download into
# base is the base url that the attachment name gets appended on to
# object is a json object that contains filename, ext, md5, and tim
# returns nothing
def dl_attatchment_from_object(directory, base, object):
    if object['ext'] == 'deleted':
        return
    filename = object['filename'] + object['ext']
    print(filename)
    f = open(directory + filename, 'wb+')
    f.write(urllib.request.urlopen(base + object['tim'] + object['ext']).read())
    f.seek(0)
    m = base64.b64encode(hashlib.md5(f.read()).digest())
    f.close()
    if m.decode('utf8') != object['md5']:
        print("ERROR: Incorrect md5 hash on file ", filename, ". Deleting ", filename, sep = '')
        os.remove(directory + filename)

# directory is a string containing the directory path to download into
# base is the base url that the attachment name gets appended on to
# post is a json object from the posts list
# returns nothing
def dl_all_attatchments_from_post(directory, base, post):
    if('filename' not in post):
        return

    dl_attatchment_from_object(directory, base, post)

    if('extra_files' in post):
        for file in post['extra_files']:
            dl_attatchment_from_object(directory, base, file)


def main():
    if(len(sys.argv) not in [3,4]):
        print(sys.argv)
        print("Usage: lainloader threadurl directorypath [startpost]")
        exit()

    startpost = 0
    if(len(sys.argv) == 4):
        startpost = int(sys.argv[3])

    directory = sys.argv[2]
    if directory[-1] != '/':
        directory = directory + '/'

    url = sys.argv[1]
    if url[-5:] == ".html":
        url = url[:-5]
    url += ".json"
    base = url.rsplit('/', 2)[0] + '/src/'

    page = json.load(urllib.request.urlopen(url))
    for post in page["posts"]:
        if(int(post['no']) >= startpost):
            dl_all_attatchments_from_post(directory, base, post)

if __name__ == "__main__":
    main()
