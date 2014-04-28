#!/usr/bin/env python
# -*- coding:utf-8 -*-

#stardard module
import threading
import Queue
import sys
import urllib2

from html_parse import MMHtmlParse
from thread_run import do_parse

#set coding
reload(sys)
sys.setdefaultencoding('utf8')

MUTEX = threading.Lock()

EVENT = threading.Event()

COUNT = 0

class ThreadPool(object):
    """
        handout and recyle the threads
    """
    def __init__(self, threads_num, root_url):
        self.root_url = root_url
        self.threads = []
        self.events = []
        self.queue = Queue.Queue()
        self.max_threads_num = threads_num
        self.visited_url = []
        self._create_event()
        self._create_threads()
        self._init_queue()

    def _create_threads(self):
        for i in range(self.max_threads_num):
            event = self.events[i]
            thread = PageParseThread(self.queue, i+1, event, self.visited_url)
            self.threads.append(thread)
            thread.start()

    def _create_event(self):
        for i in range(self.max_threads_num):
            event = threading.Event()
            self.events.append(event)

    def _init_queue(self):
        self.queue.put((do_parse, self.root_url))

    def get_thread(self):
        global EVENT
        for i, event in enumerate(self.events):
            if not event.isSet():
                EVENT.clear()
                event.set()
                return i
        return False

    def check_queue(self):
        un_deal = 0
        for event in self.events:
            if event.isSet():
                un_deal += 1
        if self.queue.empty() and un_deal == 0:
            return False
        else:
            return True

    def get_visited(self):
        print "fuckfuckfuckfuckfuck %d" % len(self.visited_url)



class PageParseThread(threading.Thread):
    """
        define a thread for parse the html
    """
    def __init__(self, queue, i, event, visited_url):
        threading.Thread.__init__(self,name='page_parser_thread_%d' % i)
        self.queue = queue
        self.event = event
        self.visited_url = visited_url
        self.parser = MMHtmlParse(self.queue, self.visited_url)
        
    def run(self):
        global EVENT
        global COUNT
        while True:
            self.event.wait()
            if not self.queue.empty():
                func, url = self.queue.get()
                self.visited_url.append(url)            
                EVENT.set()
                if self.queue.empty():
                    MUTEX.acquire()
                    func(url, self.parser)
                    if not self.queue.empty():
                        MUTEX.release()
                else:
                    func(url, self.parser)
                self.queue.task_done()
                self.event.clear() 


if __name__ == '__main__':
    root_url = "/"
    pool = ThreadPool(5,root_url)
    EVENT.set()
    while pool.check_queue():
        EVENT.wait()
        pool.get_thread()
        # pool.get_visited()







