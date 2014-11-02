#!/usr/bin/env python
# -*- coding:utf-8 -*-

#standard module
import sys
import os
import urllib2
import time

#custom module
import database_options 

reload(sys)
sys.setdefaultencoding('utf-8')

_ROOT_URL = 'http://www.22mm.cc'


def _http_request(url):        #add for coupling
    """send a http request,and get relevant resource"""
    request = urllib2.Request(url)
    try:                       #add for robustness
        response = urllib2.urlopen(request)
        if response.getcode() == 200:
            content = response.read()
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print 'get server failed'
        if hasattr(e, 'code'):
            print 'Error code: %d' % e.code
        return None
    except urllib2.HTTPError, e:
        if e.code == 404:
            order = -1 
        else:
            print e.code
        return None
    else:
        # print 'get response ok!'
        return content

            

def _get_html(url):
    """
        used urllib2 to get html 
        args:
            a section of url
        return:
            a section of html string
    """
    return _http_request(url)


def _get_real_url(url):
    """
        transform relative url to absolute url
        args:
            relative url
        return:
            absolute url
    """
    if isinstance(url,str) and url:   #modified for robustness
        if url.startswith('/'):
            return _ROOT_URL + url
        if url.startswith('mm'):
            return _ROOT_URL + '/' + url
    else:
        return None




def _deal_dir(url):
    """
        deal directory:create that don't exist directory 
        args:
            url
        return:
            no
    """
    if isinstance(url,str) and url:  #modified for robustness
        image_path_list = url.split('/')
        header = image_path_list[0].split('.')[0]
        current_dir = './mm_image/'
    else:
        current_dir = ""

    if current_dir and not os.path.exists(current_dir):    #modified for robustness
        os.mkdir(current_dir)

    if current_dir:                   #modified for robustness
        current_dir += 'images/'

    if current_dir and not os.path.exists(current_dir): #modified for robustness
        os.mkdir(current_dir)

    if current_dir:
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
    if isinstance(url,str) and url:  #modified for robustness
        image_path_list = url.split('/')
        header = image_path_list[0].split('.')[0]
        current_dir = './mm_image/images/'
        try:                        #modified for robustness
            for i, path in enumerate(image_path_list[2:-1]):
                current_dir += path
                if i == 1:
                    current_dir += '_'
                    current_dir += header
                current_dir += '/'
        except IndexError:
            current_dir = None
    else:
        current_dir = None
    return current_dir


def _get_image_path(url):                #add for  coupling
    """get image path for divers image"""
    current_dir = _get_path(url[7:])
    if current_dir:
        try:                             #add for robustness
            url_list[-5] = str(order)
            url_new = ''.join(url_list)
            image_path = current_dir + str(order) + '.jpg'
            return image_path
        except IndexError:
            return None
    else:
        return None
        
def _store_image(image_path, content):     #add for  coupling
    """ store image"""
    with open(image_path, 'wb+') as f:     #add for robustness
        f.write(content)

def _set_image_info(image_path):           #add for  coupling
    """set image info into database"""
    if isinstance(url,str) and url:        #add for robustness
        image_info = image_path.split('/')
        try:                               #add for robustness
            image_catagory = image_info[3]
            image_group = image_info[4] + '_' + image_info[5]
        except IndexError:
            image_catagory = ""
            image_group = ""
        image_upload_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        if image_path.endswith('/1.jpg'):
            image_cover = 1
        else:
            image_cover = 0
        database_options.store_image_info(image_path, image_catagory, image_group, 0, 0, image_upload_time, image_cover)  
        print "saved image successfully: %s" % image_path

    
def _get_image(url):   #improve coupling
    """
        across url to download images
    """
    url_list = list(url)
    order = 1
    while order > 0:
        image_path = _get_image_path(url)
        if database_options.check_repeat(image_path):
            _deal_dir(url[7:])
            order += 1
            content = _http_request(url_new)
            if content:
                _store_image(image_path, content)            
                _set_image_info(image_path)
        else:
            break


def do_image_parse(image_link):
    """download image and save it into current directory"""
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
