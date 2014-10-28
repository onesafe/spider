#!/usr/bin/env python
# -*- coding:utf-8 -*-

#standard lib
import sys
import os
import urllib2
import time

#custom lib
import database_options 

reload(sys)
sys.setdefaultencoding('utf-8')

_ROOT_URL = 'http://www.22mm.cc'

def _get_html(url):
    """
        used urllib2 to get html 
        args:
            a section of url
        return:
            a section of html string
    """
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


def _get_real_url(url):
    """
        transform relative url to absolute url
        args:
            relative url
        return:
            absolute url
    """
    if url.startswith('/'):
        return _ROOT_URL + url
    if url.startswith('mm'):
        return _ROOT_URL + '/' + url




def _deal_dir(url):
    """
        deal directory:create that don't exist directory 
        args:
            url
        return:
            no
    """
    image_path_list = url.split('/')
    header = image_path_list[0].split('.')[0]
    current_dir = './'
    current_dir += 'mm_image/'

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
            print "building dir : %s"  % current_dir
            os.mkdir(current_dir)

def _get_path(url):
    """
        across url to get the images path in the computer
    """
    image_path_list = url.split('/')
    header = image_path_list[0].split('.')[0]
    current_dir = './'
    current_dir += 'mm_image/'
    current_dir += 'images/'
    for i, path in enumerate(image_path_list[2:-1]):
        current_dir += path
        if i == 1:
            current_dir += '_'
            current_dir += header
        current_dir += '/'
    return current_dir


def _get_image(url):
    """
        across url to download images
    """
    url_list = list(url)
    order = 1
    conn = database_options.connect_db()
    while order > 0:
        current_dir = _get_path(url[7:])
        url_list[-5] = str(order)
        url_new = ''.join(url_list)
        image_path = current_dir + str(order) + '.jpg'            
        if database_options.check_repeat(conn, image_path):
            _deal_dir(url[7:])
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
                if image_path.endswith('/1.jpg'):
                    image_cover = 1
                else:
                    image_cover = 0
                database_options.store_image_info(conn, image_path, image_catagory, image_group, 0, 0, image_upload_time, image_cover)  
                print "saved image successfully: %s" % image_path
        else:
            break
    database_options.close_db(conn)


def do_image_parse(image_link):
    _get_image(image_link)


def do_page_parse(url, parser):
    """
        do web page parsed,the function will be packaged into a queue,be called by a parse thread 
        args:
            a absolute url
            a parser: it's a class in file "html_parse.py"
        return:
            no
    """
    real_url = _get_real_url(url)
    html_string = _get_html(real_url)
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
