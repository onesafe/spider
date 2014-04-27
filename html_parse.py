#!/usr/bin/env python
# -*- coding:utf-8 -*-
from HTMLParser import HTMLParser

class MMHtmlParse(HTMLParser):
    href_list = []
    href_visited = []
    image_src = []
    src_vistied = []
   
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                if attr[0] == 'href' and self.href_list.count(attr[1]) == 0:
                    if (attr[1].startswith('/mm') or attr[1].startswith('mm')):
                        self.href_list.append(attr[1])
                        self.href_visited.append(0)
        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src' and self.image_src.count(attr[1]) == 0:
                    url_split = attr[1].split('.')
                    if url_split[1] == 'meimei22' and not (attr[1].endswith('/s0.jpg') and attr[1].endswith('/h0.jpg') and attr[1].endswith('/0.jpg')):
                        self.image_src.append(attr[1])
                        self.src_vistied.append(0)

    def get_info(self):
        print 'total page: %d' % len(self.href_list)
        print 'total image: %d' % len(self.image_src)

    def get_next_href_unvisited(self):
        try:
            unvisited_index = self.href_visited.index(0)  
            self.href_visited[unvisited_index] = 1
            return self.href_list[unvisited_index]
        except ValueError:
            return None

    def get_next_image_unvistied(self):
        try:
            unvisited_index = self.href_visited.index(0)
            self.src_vistied[unvisited_index] = 1
            return self.src_vistied[unvisited_index]
        except ValueError:
            return None