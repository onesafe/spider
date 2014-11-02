#!/usr/bin/env python
# -*- coding:utf-8 -*-

import MySQLdb


def _connect_db():
    """
        connect db
    """
    try:                                # add exception
        conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='shangbo123',db='mm_image',charset='utf8')
        return conn
    except MySQLdb.OperationalError:
        return 0
    
def store_image_info(path, catagory, group, praise, step, upload_date, cover):
    """
         store image info image info into db
    """
    conn = _connect_db()
    if conn:
        try:                        # add exception
            cur = conn.cursor()
            cur.execute("insert into app_explore_image_picture(image_path, image_catagory, image_group, image_praise, image_step, image_upload_date, image_cover)"
                "values('%s', '%s', '%s', %d, %d, '%s', %d) " % (path, catagory, group, praise, step, upload_date, cover))
            conn.commit()
        except MySQLdb.OperationalError:
            print "database error!"            
            return 0
        finally:
            cur.close()
            conn.close()

def check_repeat(_path):
    """
        check image path whether repeat
    """
    conn = _connect_db()
    if conn and _path:                       #add exception
        try:
            cur = _conn.cursor()
            cur.execute("select id from app_explore_image_picture where image_path='%s'" % (_path))
            fetch = cur.fetchall()
            if not fetch:
                return True
            else:
                return False
        except MySQLdb.OperationalError:
            cur.close()
            conn.close()
            return False

def close_db(conn):
    conn.close()
