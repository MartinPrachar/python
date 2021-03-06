import requests
import re
import urllib.parse

target_url = "" # type an url
target_links = []

def extract_links(url):
    response = requests.get(target_url)
    return re.findall('(?:href=")(.*?)"', response.content.decode())

def crawl(url):
    href_links = extract_links(url)
    for link in href_links:
        link = urllib.parse.urljoin(url, link)
        if "#" in link:
            link = link.split("#")[0]
        
        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)

crawl(target_url)