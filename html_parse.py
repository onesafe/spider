#!/usr/bin/env python
# -*- coding:utf-8 -*-

from HTMLParser import HTMLParser

from thread_run import do_parse

class MMHtmlParse(HTMLParser):

    def __init__(self, queue, visited_url):
        HTMLParser.__init__(self)
        self.queue = queue
        self.visited_url = visited_url
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href' and self.visited_url.count(attr[1]) == 0:
                    if (attr[1].startswith('/mm') or attr[1].startswith('mm')):
                        self.queue.put((do_parse, attr[1]))

class MMImageParse(HTMLParser):

    def __init__(self, queue, visited_image):
        HTMLParser.__init__(self)
        self.queue = queue
        self.visited_image = visited_image
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src' and self.visited_image.count(attr[1]) == 0:
                    url_split = attr[1].split('.')
                    if url_split[1] == 'meimei22' and not (attr[1].endswith('/s0.jpg') or attr[1].endswith('/h0.jpg') or attr[1].endswith('/0.jpg')):
                        # self.queue.put((do_parse,attr[1]))
                        print attr[1]+'\n'


