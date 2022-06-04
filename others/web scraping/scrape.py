import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get("https://news.ycombinator.com/news")
res2 = requests.get("https://news.ycombinator.com/news?p=2")
soup = BeautifulSoup(res.text, "html.parser")
soup2 = BeautifulSoup(res2.text, "html.parser")
# soup.body soup.head soup.content soup.find_all("a/div...") soup.find("a") - firt
# print(soup.find(id="score_22873298"))
# .something - class tag
links = soup.select(".storylink")
# CSS selectors
subtext = soup.select(".subtext")
links2 = soup2.select(".storylink")
subtext2 = soup2.select(".subtext")
print(links)

mega_links = links+links2
mega_subtext = subtext+subtext2

def sort_stories(hnlist):
    return sorted(hnlist, key=lambda x: x["votes"], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get("href", None)
        vote = subtext[idx].select(".score")
        if len(vote):
            points = int(vote[0].getText().replace(" points", ""))
            if points>99:
                hn.append({"title": title, "link": href, "votes": points})
    return sort_stories(hn)


pprint.pprint(create_custom_hn(mega_links, mega_subtext))