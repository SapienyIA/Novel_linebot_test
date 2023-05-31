import requests
from bs4 import BeautifulSoup
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context
headers = {'User-Agent': 'Mozilla/5.0'}
filename = "url"

def check_update():
    cu = read_file()
    msg = ""
    for url in cu.keys():
        response = requests.get(url,headers = headers)
        html = BeautifulSoup(response.text,features="html.parser")
        chapter = html.find_all("dl",class_="novel_sublist2")
        title = html.find("title").text
        update = {}
        li = []
        li.append(nformat(title))
        li.append(nformat(chapter[-1].a.text))
        update[url]= li
        if (update[url][1] == cu[url][1]):
            msg +="沒更新\n"+str(title)+"\n最新章是:"+update[url][1]+"\n連結:"+url[0:25]+str(chapter[-1].a["href"])
        else:
            msg +="有更新\n"+str(title)+"\n最新章是:"+update[url][1]+"\n連結:"+url[0:25]+str(chapter[-1].a["href"])
            cu[url] = update[url]
            with open(filename,'w') as file:
                for k,v in cu.items():
                    file.write(str(k)+' '+str(v[0])+' '+str(v[1])+'\n')
        msg += '\n\n'
    return msg


def check_update2():
    cu = read_file()
    for url in cu.keys():
        response = requests.get(url,headers = headers)
        html = BeautifulSoup(response.text,features="html.parser")
        chapter = html.find_all("dl",class_="novel_sublist2")
        title = html.find("title").text
        update = {}
        li = []
        li.append(nformat(title))
        li.append(nformat(chapter[-1].a.text))
        update[url]= li
        if (update[url][1] == cu[url][1]):
            msg ="沒更新\n"+str(title)+"\n最新章是:"+update[url][1]+"\n連結:"+url[0:25]+str(chapter[-1].a["href"])
            print(msg)
        else:
            msg ="有更新\n"+str(title)+"\n最新章是:"+update[url][1]+"\n連結:"+url[0:25]+str(chapter[-1].a["href"])
            print(msg)
            cu[url] = update[url]
            with open(filename,'w') as file:
                for k,v in cu.items():
                    file.write(str(k)+' '+str(v[0])+' '+str(v[1])+'\n')
            send_message(msg)

def make_book(url):
    response = requests.get(url,headers = headers)
    html = BeautifulSoup(response.text,features="html.parser")
    name = html.find("title").text
    chapter = html.find_all("dl",class_="novel_sublist2")
    for ch in chapter:
        u = url[0:25] + str(ch.a["href"])
        print("處理中:"+u)
        with open(name,'a') as file:
            file.write(return_chapter(u))
    print("完成")

def return_chapter(url): 
    response = requests.get(url,headers = headers)
    html = BeautifulSoup(response.text,features="html.parser")
    titles = html.find("div",id="novel_honbun")
    ch =""
    for p in titles:
        if p != "\n":
            ch += p.text+"\n"
    return ch

def nformat(title):
    not_allowed = ["*","|","\\",":",'""',"<",">","?","/","〜","【",
                   "】","\u3000"," "]
    for na in not_allowed:
        title = title.replace(na,"")
    return title


def read_file():
    rb = {}
    with open("./url", 'r') as file:
        for line in file.readlines():
            line = line.strip()
            key =line.split(' ')[0]
            value=[]
            value.append(line.split(' ')[1])
            value.append(line.split(' ')[2])
            rb[key]=value
    return rb

def list_query():
    rb = read_file()
    index = ""
    for key in rb.values():
        index += key[0]+"\n\n"
    return index

def book_add(name):
    tag= "https://ncode.syosetu.com/"
    msg = "已新增"
    if (name[0:26]==tag):
        if (requests.get(name,headers = headers).status_code==200):
            url = read_file()
            if name not in url.keys():
                response = requests.get(name,headers = headers)
                html = BeautifulSoup(response.text,features="html.parser")
                chapter = html.find_all("dl",class_="novel_sublist2")
                title = html.find("title").text
                name+= ' '+   nformat(title) +' '+ nformat(chapter[-1].a.text) +'\n'
                with open("./url",'a') as file:
                    file.write(name)
            else:
                msg = "已在清單內"
        else:
            msg = "網址可能有誤"
    else:
        msg = "不支援的網站"
    return msg

def book_remove(name):
    url = read_file()
    msg = "不在清單內"
    for k,v in url.items():
        if name == str(v[0]):
            del url[k]
            with open("./url",'w') as file:
                for k,v in url.items():
                    file.write(str(k)+' '+str(v[0])+' '+str(v[1])+'\n')
            msg = "已移除"
            return msg
    if name in url.keys():
        del url[name]
        with open("./url",'w') as file:
            for k,v in url.items():
                file.write(str(k)+' '+str(v[0])+' '+str(v[1])+'\n')
        msg = "已移除"
    return msg

def send_message(msg):
    try:
        requests.get("http://127.0.0.1:5000/?msg="+msg,headers=headers)
    except:
        print("發送訊息時出現問題")
