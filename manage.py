import requests
import re
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
with open('output.csv', 'a') as file:
    file.write('name,content,time,url,\n')

url_list = []


def html_get(c_url):
    #父html内容获取
    try:
        r = requests.get(c_url,headers=headers)
        if r.status_code == 200:
            html_parser(r)
        else:
            print("ERROR:"+c_url)
    except:
        RequestException

def html_parser(r):
    #父htl中url正则匹配
    r.encoding='utf-8'
    html = r.text
    res = re.findall(r'\./2018.*htm',html)
    for u in res:
        url_list.append(u)

def content_get(url):
    content = requests.get(url,headers=headers)
    content.encoding='utf-8'
    content_text = content.text
    #解析文章内容
    soup = BeautifulSoup(content_text)
    name = soup.find("h2", class_="tc").get_text()
    content_data = soup.find("div", class_="vF_detail_content").get_text()
    time = soup.find(id="pubTime").get_text()
    res_write(name,content_data,time,url)
    print("Done:" + str(count_url) + url)



def res_write(name,content_data,time,url):
    with open('output.csv', 'a') as file:
        file.write('\"' + name + '\"' + ',')
        file.write('\"' + content_data + '\"' + ',')
        file.write('\"' + time + '\"' + ',')
        file.write('\"' + url + '\"' + ',')
        file.write('\n')
URL_ROOT = "http://www.ccgp.gov.cn/cggg/zygg/gkzb/index.htm"
url_next = "http://www.ccgp.gov.cn/cggg/zygg/gkzb/index_{}.htm"


if __name__ == '__main__':
    count_url = 1
    for count in range(25):
        if count == 0:
            c_url = URL_ROOT
        else:
            c_url = url_next.format(count)
        c_url = URL_ROOT
        html_get(c_url)
    for i in url_list:
        #构造url
        res_url = "http://www.ccgp.gov.cn/cggg/zygg/gkzb/"+i[1:]
        content_get(res_url)
        count_url = count_url + 1
