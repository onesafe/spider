#!/usr/bin/env python
# -*- coding:utf-8 -*-

import MySQLdb


def connect_db():
    """
        connect db
    """
    conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='shangbo123',db='mm_image',charset='utf8')
    return conn

def store_image_info(conn, path, catagory, group, praise, step, upload_date, cover):
    """
         store image info image info into db
    """
    cur = conn.cursor()
    cur.execute("insert into app_explore_image_picture(image_path, image_catagory, image_group, image_praise, image_step, image_upload_date, image_cover)"
        "values('%s', '%s', '%s', %d, %d, '%s', %d) " % (path, catagory, group, praise, step, upload_date, cover))
    conn.commit()
    cur.close()

def check_repeat(_conn ,_path):
    """
        check image path whether repeat
    """
    cur = _conn.cursor()
    cur.execute("select id from app_explore_image_picture where image_path='%s'" % (_path))
    fetch = cur.fetchall()
    cur.close()
    if not fetch:
        return True
    else:
        return False

def close_db(conn):
    conn.close()
