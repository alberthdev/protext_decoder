#!/usr/bin/env python3
import os
import re
import urllib.request

from bs4 import BeautifulSoup

PROTEXT_URL="http://protext.herokuapp.com/"
FONTS_RE=r'\"(static\/gen\/.*)\"'

# Returns: ciphertext, font_urls
def decode_page(html_file):
    fh = open(html_file, "r")
    html = fh.read()
    fh.close()
    
    m = re.findall(FONTS_RE, html)
    
    if m:
        soup = BeautifulSoup(html, "html.parser")
        res = soup.find_all("h1")
        if len(res) > 0:
            return res[0].text, m
        else:
            return None
    else:
        return None

def does_it_exist(fn):
    try:
        fh = open(fn, "r")
        fh.close()
        return True
    except IOError:
        return False

def dl_fonts(fonts):
    for font in fonts:
        fn = os.path.basename(font)
        if does_it_exist(fn):
            print(" ** Skipping file because it already exists: %s" % fn)
            continue
        url = PROTEXT_URL + font
        
        req = urllib.request.Request(
            url, 
            data=None, 
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
                'Cookie': 'X-VALID=TRUE'
            },
        )
        
        print(" ** Downloading: %s -> %s" % (url, fn))
        url_fh = urllib.request.urlopen(req)
        dst_fh = open(fn, "wb")
        dst_fh.write(url_fh.read())
        dst_fh.close()
        url_fh.close()

def bn_fonts(fonts):
    return [os.path.basename(font) for font in fonts]
