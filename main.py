import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *


PROJECT_NAME = 'cnodejs'
HOMEPAGE = 'http://118.31.19.120:3000/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8

queue = Queue()
Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

# Create workwe threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do the next job in the queue
def work():
    while True:
        url = queue.get()
        print("work-------url:",url)
        Spider.crawl_page(threading.current_thread().name,url)
        queue.task_done()



# Each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()



# check if there are items in the queue, if so crawl time
def crawl():
    queue_links = file_to_set(QUEUE_FILE)
    print("queue_links: ",queue_links)
    if len(queue_links) > 0:
        print(str(len(queue_links)) + " links in the queue")
        create_jobs()

create_workers()
crawl()