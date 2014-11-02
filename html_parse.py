#!/usr/bin/env python
# -*- coding:utf-8 -*-

#standard module
from HTMLParser import HTMLParser
import Queue

#custom module
from thread_deal_functions import do_page_parse, do_image_parse

class MMHtmlParse(HTMLParser):
    """
        this is a html parser class,parsed tag 'a' and 'img'
    """
    def __init__(self, queue=None, visited_url=None):
        HTMLParser.__init__(self)
        if isinstance(queue, Queue.Queue):                  # add for robustness and  coupling
            self.queue = queue
        else:
            self.queue = Queue.Queue()                      

        if isinstance(visited_url,list):                    # add for robustness and  coupling
            self.visited_url = visited_url
        else:
            self.visited_url = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href' and self.visited_url.count(attr[1]) == 0:
                    if (attr[1].startswith('/mm') or attr[1].startswith('mm')):
                        self.queue.put((do_page_parse, attr[1]))
        if tag == 'img':
                for attr in attrs:
                    if attr[0] == 'src' and self.visited_url.count(attr[1]) == 0:
                        url_split = attr[1].split('.')
                        if url_split[1] == 'meimei22' and attr[1].endswith('/0.jpg'):
                            self.queue.put((do_image_parse,attr[1]))
