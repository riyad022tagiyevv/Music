#!/usr/bin/python2.7
# coding=utf-8
"""
Ok, Google, your decision about removing WL from the API sucks!
"""
import ujson as json
import os
from tornado.httpclient import AsyncHTTPClient, HTTPClient, HTTPError, HTTPRequest
from tornado.ioloop import IOLoop
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import urllib
import random


# FIREFOX
# Will not activate WebDriver plugin unless:
# xpinstall.signatures.required in about:config
# https://stackoverflow.com/questions/37247336/selenium-use-of-firefox-profile
# Doesn't work!
# Alternative: https://github.com/5digits/dactyl/wiki/Disable-extension-signing-requirement-in-Firefox-49-or-later

class DebugDump(object):
    def __init__(self, filename):
        self.fp = open(filename, 'wt')

    def __del__(self):
        self.fp.close()

    def write(self, b):
        self.fp.write(b)

FIREFOX_PROFILE_LOCATION = r'%APPDATA%\Mozilla\Firefox\Profiles\<some_profile>'
FIREFOX_BINARY_LOCATION = r'C:\Program Files (x86)\Mozilla Firefox\firefox.exe'

def downloadWL(filename):
    videolist = DebugDump(filename)
    videolist.write('[')

    http = HTTPClient()
    profile = webdriver.FirefoxProfile(FIREFOX_PROFILE_LOCATION)  # This profile is used as a template, not directly
    binary = FirefoxBinary(FIREFOX_BINARY_LOCATION)
    sDriver = webdriver.Firefox(profile, binary, capabilities={"marionette": False})  # https://selenium2.ru/news/188-firefox-esr-52.html
    sDriver.get('https://www.youtube.com/playlist?list=WL')

    # IMPORTANT! To reuse existing session/cookies, log in using the profile listed as template above! (using your browser, not python)
    pass

    # Prepare headers for Tornado
    uagent = sDriver.execute_script("return navigator.userAgent;")
    cookies = sDriver.get_cookies()
    cookies = filter(lambda x: 'youtube.com' in x['domain'], cookies)
    cookies = u'; '.join([u'{}={}'.format(x[u'name'], x[u'value']) for x in cookies])
    ytcfg = sDriver.execute_script('return ytcfg.data_;')
    headers = {
        'X-YouTube-Client-Name': '1',
        'X-YouTube-Client-Version': str(ytcfg['INNERTUBE_CONTEXT_CLIENT_VERSION']),
        'X-YouTube-Page-CL': str(ytcfg['PAGE_CL']),
        'X-Youtube-Identity-Token': ytcfg['ID_TOKEN'],
        'X-YouTube-Page-Label': ytcfg['PAGE_BUILD_LABEL'],  # responseContext.serviceTrackingParams...key=innertube.build.label,
        'X-YouTube-Variants-Checksum': str(ytcfg['VARIANTS_CHECKSUM']),
        'X-YouTube-Utc-Offset': '180',
        'X-SPF-Referer': 'https://www.youtube.com/playlist?list=WL',
        'X-SPF-Previous': 'https://www.youtube.com/playlist?list=WL',
        'Referer': 'https://www.youtube.com/playlist?list=WL',
        'Cookie': cookies
    }

    def buildContURL(ct):
        return u'https://www.youtube.com/browse_ajax?{}'.format(urllib.urlencode({'ctoken': ct['continuation'], 'continuation': ct['continuation'], 'itct': ct['clickTrackingParams']}))

    moreurl = None
    if 0:
        # Old design
        # Get titles already loaded
        for vid in sDriver.find_elements_by_class_name('pl-video'):
            print(u'{}: {}'.format(vid.get_attribute('data-title'), vid.get_attribute('data-video-id')))

        # Get link for more
        morebtn = sDriver.find_element_by_class_name('load-more-button')
        moreurl = u'https://www.youtube.com' + morebtn.get_attribute('data-uix-load-more-href')
    else:
        # New design
        # JS video list: window["ytInitialData"].contents.twoColumnBrowseResultsRenderer.tabs[0].tabRenderer.content.sectionListRenderer.contents[0].itemSectionRenderer.contents[0].playlistVideoListRenderer.contents
        # JS continuation: window["ytInitialData"].contents.twoColumnBrowseResultsRenderer.tabs[0].tabRenderer.content.sectionListRenderer.contents[0].itemSectionRenderer.contents[0].playlistVideoListRenderer.continuations[0].nextContinuationData
        ct = sDriver.execute_script('return window["ytInitialData"].contents.twoColumnBrowseResultsRenderer.tabs[0].tabRenderer.content.sectionListRenderer.contents[0].itemSectionRenderer.contents[0].playlistVideoListRenderer.continuations[0].nextContinuationData;')
        #moreurl = u'https://www.youtube.com/browse_ajax?ctoken={}&continuation={}&itct={}'.format(ct['continuation'], ct['continuation'], ct['clickTrackingParams'])
        moreurl = buildContURL(ct)

    while moreurl is not None:
        try:
            resp = http.fetch(HTTPRequest(moreurl, user_agent=uagent, headers=headers))
            js = json.loads(resp.body)
            js = js[1]['response']['continuationContents']['playlistVideoListContinuation']
            for vid in js['contents']:
                print(u'{}: {}'.format(vid['playlistVideoRenderer']['videoId'], vid['playlistVideoRenderer']['title']['simpleText']))
            if 'continuations' in js:
                ct = js['continuations'][0]['nextContinuationData']
                moreurl = buildContURL(ct)
                videolist.write(json.dumps(js['contents']))
            else:
                moreurl = None

            if moreurl is None:
                videolist.write(']')
            else:
                videolist.write(', ')
        except HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            print("Error: " + str(e))
            moreurl = None
        except Exception as e:
            # Other errors are possible, such as IOError.
            print("Error: " + str(e))
            moreurl = None

    sDriver.close()


def loadSavedWL(filename):
    with open(filename, 'r') as fp:
        js = json.load(fp)

    videos = []
    for packet in js:
        for vid in packet:
            videos.append((vid['playlistVideoRenderer']['videoId'], vid['playlistVideoRenderer']['title']['simpleText']))

    return videos


if __name__ == '__main__':
    # Load/update the list from Youtube
	# downloadWL('videolist.txt')

	# Load, shuffle and display
    videos = loadSavedWL('videolist.txt')

    # TODO: build html page with videos (and thumbnails)
    random.shuffle(videos)
    for (vid, title) in videos:
        print(u'https://www.youtube.com/watch?v={}'.format(vid))
        print(u'\t{}'.format(title))
