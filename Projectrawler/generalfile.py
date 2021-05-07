import os
from urllib.request import urlopen
from finderfile import FinderLink
import string
import json


def project_dir_create(directory):
    if not os.path.exists(directory):
        print('Creating directory ' + directory)
        os.makedirs(directory)


def data_files_create(project_name, base_url):
    queue = os.path.join(project_name , 'queue.txt')
    crawled = os.path.join(project_name,"crawled.txt")
    if not os.path.isfile(queue):
        filewrite(queue, base_url)
    if not os.path.isfile(crawled):
        filewrite(crawled, '')


def filewrite(path, data):
    with open(path, 'w') as f:
        f.write(data)


def appendfile(path, data):
    with open(path, 'a') as file:
        file.write(data + '\n')

def searche(word):
    dict1={'URLS':[]}
    with open("C:/Users/19195/Desktop/Projectrawler/crawler/crawled.txt", 'rt',encoding='utf8') as openfile:
        for line in openfile:
            for part in line.split():
                #print(part)
                #part = changer(part)
                #print(part)
                if word in part.lower():
                    a=line.split('*')[0]
                    dict1["URLS"].append(a)
        
        json_object = json.dumps(dict1, indent = 4)  
        print(json_object) 

def changer(word):
    translationTable = str.maketrans("ıİüÜöÖçÇşŞğĞ", "iIuUoOcCsSgG")
    word = word.translate(translationTable)
    return word


def delete_file_contents(path):
    open(path, 'w').close()


def fileset(file_name):
    results = set()
    with open(file_name, 'rt',encoding='utf8') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results


def setfile(links, file_name):
    with open(file_name,"w",encoding='utf8') as f:
        for l in sorted(links):
            f.write(l+"\n")

