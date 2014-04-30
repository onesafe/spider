#!/usr/bin/env python
# -*- coding:utf-8 -*-

from HTMLParser import HTMLParser

from thread_run import do_page_parse, do_image_parse

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
                        self.queue.put((do_page_parse, attr[1]))
        if tag == 'img':
                for attr in attrs:
                    if attr[0] == 'src':
                        url_split = attr[1].split('.')
                        if url_split[1] == 'meimei22' and attr[1].endswith('/0.jpg'):
                            self.queue.put((do_image_parse,attr[1]))
                            # print "image_url: %s \n" % attr[1]