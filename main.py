# parser.py
import requests
from bs4 import BeautifulSoup as bs
import time
import operator

from multiprocessing import Pool # Pool import하기

def get_html(url):
   _html = ""
   resp = requests.get(url)
   if resp.status_code == 200:
      _html = resp.text
   return _html

def question_title(soup):
    all_divs = soup.find("meta",  itemprop="title name")
    return all_divs["content"]
    
def question_body(soup):
    all_divs = soup.find_all("div",{'class':'postcell post-layout--right'})
    for i in all_divs:
        all_divs2 = i.find_all("p")
        for name in all_divs2:
            return name.get_text()

def answer(soup):
    all_divs = soup.find_all("div",{'class':'answercell post-layout--right'})
    for i in all_divs:
        all_divs2 = i.find_all("p")
        for name in all_divs2:
            return name.get_text()        

def comments(soup):
    comments = soup.find_all("span",{'class':'comment-copy'})
    for comment in comments:
        return comment.get_text()


def crawler(dic, index):
    value = get_html("https://stackoverflow.com/questions/"+str(index))
    soup = bs(value, 'html.parser')

    result = ""
    result += question_title(soup)
    result += '\n'
    result += question_body(soup)
    result += '\n'
    result += answer(soup)
    result += '\n'
    result += comments(soup)

    for i in result.split():
        if i in dic:
            dic[i] += 1
        else:
            dic[i] = 1

dic = {}

for i in range(7782772, 7782776):
    crawler(dic,7782772)

 #dic = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)

print(dic)

f = open("result.txt", 'w')

for key in dic.keys():
    f.write(key+ "\t"+str(dic[key] )+"\n")

f.close()
