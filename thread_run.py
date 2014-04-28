#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import urllib2
import threading

reload(sys)
sys.setdefaultencoding('utf-8')


_ROOT_URL = 'http://www.22mm.cc'

def get_html(url):
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request)
        print response.getcode()
        html_string = response.read()
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print 'get server failed'
        if hasattr(e, 'code'):
            print 'Error code: %d' % e.code
        return None
    else:
        # print 'get response ok!'
        return html_string


def get_real_url(url):
    if url.startswith('/'):
        return _ROOT_URL + url
    if url.startswith('mm'):
        return _ROOT_URL + '/' + url


def do_parse(next_url,page_parser):
    real_url = get_real_url(next_url)
    html_string = get_html(real_url)
    try:
        if html_string:
            print '\n%s is dealing with the %s:' % (threading.currentThread().getName(), real_url) 
            page_parser.feed(html_string)
    except UnicodeDecodeError:
        reload(sys)
        sys.setdefaultencoding('gb2312')
        try:
            self.page_parser.feed(html_string)
        except UnicodeDecodeError:
            failed_page += 1