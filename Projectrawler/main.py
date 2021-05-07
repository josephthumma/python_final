import threading
from queue import Queue
from spiderfile import Spiders
from domainfile import *
from generalfile import *
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
PROJECT_NAME = 'crawler'
HOMEPAGE = 'https://www.newhaven.edu/'
DOMAIN_NAME = domain_name_get(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Spiders(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

def createworkers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        url = queue.get()
        Spiders.crawl_page(threading.current_thread().name, url)
        queue.task_done()


def jobs_create():
    for link in fileset(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawls()


def crawls():
    queued_links = fileset(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + ' links in the queue')
        jobs_create()


createworkers()
crawls()
