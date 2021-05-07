import urllib
from urllib.request import urlopen
from finderfile import FinderLink
from domainfile import *
from generalfile import *
import  requests
from bs4 import BeautifulSoup



class Spiders:

    project_name = ''
    base_url = ''
    domain_name = ''
    queue_file = ''
    crawled_file = ''
    queue = set()
    crawled = set()

    def __init__(self, project_name, base_url, domain_name):
        Spiders.project_name = project_name
        Spiders.base_url = base_url
        Spiders.domain_name = domain_name
        Spiders.queue_file = Spiders.project_name + '/queue.txt'
        Spiders.crawled_file = Spiders.project_name + '/crawled.txt'
        self.boot()
        self.crawl_page('First spider', Spiders.base_url)

    @staticmethod
    def boot():
        project_dir_create(Spiders.project_name)
        data_files_create(Spiders.project_name, Spiders.base_url)
        Spiders.queue = fileset(Spiders.queue_file)
        Spiders.crawled = fileset(Spiders.crawled_file)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spiders.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spiders.queue)) + ' | Crawled  ' + str(len(Spiders.crawled)))
            Spiders.add_links_to_queue(Spiders.gather_links(page_url))
            Spiders.queue.remove(page_url)
            a= Spiders.get_title(page_url)
            b=Spiders.get_title2(page_url)
            #print(a)
            Spiders.crawled.add(page_url + "*" + str(b) + "*" + str(a))
            Spiders.update_files()

    @staticmethod
    def get_title(page_url):
        r = requests.get(page_url)
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        for i in soup.find_all("meta", {"name": "keywords"}):
            data = i
            return data

    @staticmethod
    def get_title2(page_url):
        r = urllib.request.urlopen(page_url)
        soup = BeautifulSoup(r, 'html.parser')
        return (soup.title.text)



    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = FinderLink(Spiders.base_url, page_url)
            finder.feed(html_string)
        except Exception as e:
            print(str(e))
            return set()
        return finder.page_links()

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spiders.queue) or (url in Spiders.crawled):
                continue
            if Spiders.domain_name != domain_name_get(url):
                continue
            Spiders.queue.add(url)

    @staticmethod
    def update_files():
        setfile(Spiders.queue, Spiders.queue_file)
        setfile(Spiders.crawled, Spiders.crawled_file)
