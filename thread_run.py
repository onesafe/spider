#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import urllib2
import threading
import time
import database_options 

reload(sys)
sys.setdefaultencoding('utf-8')

_ROOT_URL = 'http://www.22mm.cc'

def get_html(url):
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request)
        if response.getcode() == 200:
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


def do_page_parse(url, parser):
    real_url = get_real_url(url)
    html_string = get_html(real_url)
    try:
        if html_string:
            print '\n%s is dealing with the %s:' % (threading.currentThread().getName(), real_url)
            parser.feed(html_string)
    except UnicodeDecodeError:
        reload(sys)
        sys.setdefaultencoding('gb2312')
        try:
            parser.feed(html_string)
        except UnicodeDecodeError:
            failed_page += 1

def deal_dir(image_path):
    image_path_list = image_path.split('/')
    current_dir = './'
    current_dir += 'mm_image/'
    header = image_path_list[0].split('.')[0]
    if not os.path.exists(current_dir):
        os.mkdir(current_dir)
    current_dir += 'images/'

    if not os.path.exists(current_dir):
        os.mkdir(current_dir)

    for i, path in enumerate(image_path_list[2:-1]):
        current_dir += path
        if i == 1:
            current_dir += '_'
            current_dir += header
        current_dir += '/'
        if not os.path.exists(current_dir):
            os.mkdir(current_dir)

    return current_dir  + image_path_list[-1]

def get_image(url):
    url_list = list(url)
    order = 1
    conn = database_options.connect_db()
    while order > 0:
        url_list[-5] = str(order)
        url_new = ''.join(url_list)
        image_path_pre = url_new[7:]
        image_path = deal_dir(image_path_pre)
        if database_options.check_repeat(conn, image_path):
            request = urllib2.Request(url_new)
            order += 1
            try:
                response = urllib2.urlopen(request)
            except urllib2.HTTPError, e:
                if e.code == 404:
                    order = -1 
                else:
                    print e.code
            else:
                f = open(image_path, 'wb+')
                f.write(response.read())
                f.close()
                image_info = image_path.split('/')
                image_catagory = image_info[3]
                image_group = image_info[4] + '_' + image_info[5]
                image_upload_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

                database_options.store_image_info(conn, image_path, image_catagory, image_group, 0, 0, image_upload_time)  
                print "saved image successfully: %s" % image_path
        else:
            break
    database_options.close_db(conn)
def do_image_parse(image_link):
    get_image(image_link)
