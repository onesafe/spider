#!/usr/bin/env python
# -*- coding:utf-8 -*-

#stardard module
import threading
import Queue
import sys
import urllib2

from html_parse import MMHtmlParse
from thread_run import do_page_parse

#set coding
reload(sys)
sys.setdefaultencoding('utf8')

MUTEX = threading.Lock()                         

# EVENT = threading.Event()

# COUNT = 0


class ThreadPool(object):
    """
        handout and recyle the threads
    """
    def __init__(self, threads_num, root_url, image_group_num):
        self.root_url = root_url
        self.threads = []
        self.events = []
        self.queue = Queue.Queue()
        self.max_threads_num = threads_num
        self.image_group_num = image_group_num
        self.visited_url = []
        self.visited_url_length = len(self.visited_url)
        self._create_event()
        self._create_threads()
        self._init_queue()
        self.count = [0, ]                                       # add
    def _create_threads(self):
        for i in range(self.max_threads_num):
            event = self.events[i]
            thread = PageParseThread(self.queue, i+1, event, self.visited_url, self.count)          # modified
            self.threads.append(thread)
            thread.start()

    def _create_event(self):
        for i in range(self.max_threads_num):
            event = threading.Event()
            self.events.append(event)

    def _init_queue(self):
        self.queue.put((do_page_parse, self.root_url))

    def get_thread(self):
        # global EVENT
        for i, event in enumerate(self.events):
            if not event.isSet():
        #        EVENT.clear()
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

    def check_image_count(self):
        if self.image_group_num == -2:
            return True
        else:
            if self.count[0] < self.image_group_num - 1:
                return True
            else:
                return False


class PageParseThread(threading.Thread):
    """
        define a thread for parse the <a> tag
    """
    def __init__(self, queue, i, event, visited_url, count):                         # modified
        threading.Thread.__init__(self,name='page_parser_thread_%d' % i)
        self.queue = queue
        self.event = event
        self.visited_url = visited_url
        self.parser = MMHtmlParse(self.queue, self.visited_url)
        self.image_count = count
    def run(self):
        # global EVENT
        while True:
            self.event.wait()
            if not self.queue.empty():
                func, url = self.queue.get()
                if self.visited_url.count(url) == 0:
                    self.visited_url.append(url)
          #      EVENT.set()
                if self.queue.empty():
                    MUTEX.acquire()
                    if url.startswith("http:"):
                        func(url)
                        self.image_count[0] += 1                          # modified
                    else:
                        func(url, self.parser)
                    if not self.queue.empty():
                        MUTEX.release()
                else:
                    if url.startswith("http:"):
                        func(url)
                        self.image_count[0] += 1                           # modified
                        print "test: %d " % COUNT
                    else:
                        func(url, self.parser)
                self.queue.task_done()
                self.event.clear() 


def run_main():
    root_url = "/"
    image_group_num = deal_argv()
    if not image_group_num == -1:
        pool = ThreadPool(5,root_url, image_group_num)
        # EVENT.set()
        while pool.check_queue():
        #    EVENT.wait()
            pool.get_thread()
            if not pool.check_image_count():
                print "finished"
                break

def deal_argv():
    if len(sys.argv) <= 2 :
        try:
            image_group_num = int(sys.argv[1])
            if image_group_num > 0:
                return image_group_num
            else:
                print "arguments error,only one and integer(>0)"
                return -1
        except IndexError:
            image_group_num = -2

            return image_group_num
        except ValueError:
            print "arguments type error,please input integer!"
        
    else:
        print "arguments error,only one and integer"
        return -1

if __name__ == '__main__':
     run_main()

    

