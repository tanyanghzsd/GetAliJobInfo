#coding:utf-8
import urllib,urllib2
import re,sys
from bs4 import BeautifulSoup
import threading



class Tool:
    removeImg=re.compile('<img.*?>| {7}|')
    removeAddr=re.compile('<a.*?>|</a>')
    replaceLine=re.compile('<tr>|<div>|</div>|</p>')
    replaceTD=re.compile('<td>')
    replacePara=re.compile('<p.*?>')
    replaceBR=re.compile('<br><br>|<br>')
    removeExtraTag=re.compile('<.*?>')
    def replace(self,x):
        x=re.sub(self.removeImg,"",x)
        x=re.sub(self.removeAddr,"",x)
        x=re.sub(self.replaceLine,"\n",x)
        x=re.sub(self.replaceTD,"\t",x)
        x=re.sub(self.replacePara,"\n  ",x)
        x=re.sub(self.replaceBR,"\n",x)
        x=re.sub(self.removeExtraTag,"",x)
        return x.strip()
    
tool=Tool()

url='https://campus.alibaba.com/positionList.htm'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 BIDUBrowser/7.4 Safari/537.36'}
req=urllib2.Request(url,headers=headers)
response=urllib2.urlopen(req)
page=response.read()
soup=BeautifulSoup(page)
regex=re.compile(r'<th>(.*?)</th>',re.S)
items=re.findall(regex,page)
# items=soup.find_all('th')
urls=[]
print len(items)
for item in items:
#     print item
#     print len(item)
#     print type(item)
#     print item[9:60]
    urls.append(item[9:60])
    

    
class getContent(threading.Thread):
    def __init__(self,urls):
        self.urls=urls
        threading.Thread.__init__(self)
    def run(self):
        for url in urls:
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 BIDUBrowser/7.4 Safari/537.36'}
            req=urllib2.Request(url,headers=headers)
            response=urllib2.urlopen(req)
            page=response.read()
            soup=BeautifulSoup(page)
            items=re.findall(re.compile(r'<dl class="w  on"(.*?)</dl>',re.S),page)
            titles=soup.find_all('h5')
            for title in titles:
                filename=title.text
                print filename
            for item in items:
                try: 
                    item=tool.replace(item)
                    open(filename+'.txt','w').write(item)
                except IOError:
                    print 'IOError'
                
                
thread1=getContent(urls[0:10])
thread1.run()
thread2=getContent(urls[10:20])
thread2.run()
thread3=getContent(urls[20:30])
thread3.run()
thread4=getContent(urls[30:-1])
thread4.run()
      


    
    
    
#     url.append(item)
#     links=item.split('')
#     link=links[1]
#     print link
