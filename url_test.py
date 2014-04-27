#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib2
import sys
from http_parse import MMHtmlParse

_ROOT_URL = 'http://www.22mm.cc'


reload(sys)
sys.setdefaultencoding('utf8')

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
        print 'get response ok!'
        return html_string



def main():
    page_count = 1
    failed_page = 0
    parser = MMHtmlParse()
    print "parsing %s" % _ROOT_URL
    html_string = get_html(_ROOT_URL)
    if html_string:
        print 'The 1th page:\n'
        page_count += 1
        parser.feed(html_string)
    next_url = parser.get_next_href_unvisited()
    while next_url:
        if next_url.startswith('/mm'):
            real_next_url = _ROOT_URL + next_url
        if next_url.startswith('mm'):
            real_next_url = _ROOT_URL + '/' + next_url
        print "parsing %s" % real_next_url
        html_string = get_html(real_next_url)
        try:
            if html_string:
                print 'The %dth page:\n' % page_count
                page_count += 1
                parser.feed(html_string)
        except UnicodeDecodeError:
            reload(sys)
            sys.setdefaultencoding('gb2312')
            try:
                parser.feed(html_string)
            except UnicodeDecodeError:
                failed_page += 1
        
        next_url = parser.get_next_href_unvisited()
    parser.get_info()
    print 'failed_page: %d' % failed_page
if __name__ == '__main__':
    main()



