from urllib.parse import urlparse


def domain_name_get(url):
    try:
        results = sub_domain_name_get(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''

def sub_domain_name_get(url):
    try:
        return urlparse(url).netloc
    except:
        return ''
