import requests
from bs4 import BeautifulSoup as bs
import time
import operator

from multiprocessing import Pool

def get_html(url):
   result = ""
   resp = requests.get(url)
   if resp.status_code == 200:
      result = resp.text
   return result

def question_title(soup):
    meta = soup.find("meta",  itemprop="title name")
    if meta is not None:
        return meta["content"]
    else:
        return ""
    
def question_body(soup):
    postcell = soup.find_all("div",{'class':'postcell post-layout--right'})
    for i in postcell:
        div_p = i.find_all("p")
        for name in div_p:
            return str(name.get_text())

def answer(soup):
    answercell = soup.find_all("div",{'class':'answercell post-layout--right'})
    for i in answercell:
        div_p = i.find_all("p")
        for name in div_p:
            return name.get_text()        

def comments(soup):
    comments = soup.find_all("span",{'class':'comment-copy'})
    for comment in comments:
        return comment.get_text()

def crawler(dic, index):
    value = get_html("https://stackoverflow.com/questions/"+str(index))
    soup = bs(value, 'html.parser')

    if soup is not None:
        result = ""
        result += str(question_title(soup))
        result += '\n'
        result += str(question_body(soup))
        result += '\n'
        result += str(answer(soup))
        result += '\n'
        result += str(comments(soup))

        for i in result.split():
            key = i.lower()
            if key in dic:
                dic[key] += 1
            else:
                dic[key] = 1

dic = {}    

start = 7783772
length = 100000

target = range(start, start+length)
for index, val in enumerate(target):    
    print(str(index+1) +"/"+str(len(target)))
    crawler(dic,val)
    time.sleep(1)

with open('result.txt', 'w', encoding='UTF-8') as f:
    for key in dic.keys():
        f.write(key+ "\t"+str(dic[key] )+"\n")
    f.close()

print(dic)