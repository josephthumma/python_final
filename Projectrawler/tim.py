from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
a=[]


import os
import requests
def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)
    URL = 'https://en.wikipedia.org/wiki/File_URI_scheme'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    print(soup)


    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'w+') as f:
            #f.write(str(soup))
           for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(str(chunk))
                    f.flush()
                    os.fsync(f.fileno())
    else:  
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))



def read_url(url):
    url = url.replace(" ","%20")
    req = Request(url)
    a = urlopen(req).read()
    soup = BeautifulSoup(a, 'html.parser')
    x = (soup.find_all('a'))
    for i in x:
        file_name = i.extract().get_text()
        url_new = url + file_name
        url_new = url_new.replace(" ","%20")
        if(file_name[-1]=='/' and file_name[0]!='.'):
            read_url(url_new)
        download(url_new, dest_folder="mydir")
list1=[]
with open(r'C:\Users\19195\Desktop\Projectrawler\crawler\paste.txt', 'r',encoding = 'utf-8') as f:
    
    for i in f:
        list1.append(i)
print(list1)
try:
    read_url("https://www.newhahhhven.edu/")
except:
    for i in list1:
        download(i, dest_folder="mydirs")
    pass

print(a)
