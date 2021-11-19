from  urllib import  parse
import random
import requests
from bs4 import BeautifulSoup
import re
def sendPicture(target):
        texturl = parse.quote(target)
        # header = {      
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        #     # 'Cookie': 'wluuid=66;  ',
        #     # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        #     # 'Accept-encoding': 'gzip, deflate, br',
        #     # 'Accept-language': 'zh-CN,zh;q=0.9',
        #     # 'Cache-Control': 'max-age=0',
        #     # 'connection': 'keep-alive'
        #     # , 'Host': 'stock.tuchong.com',
        #     # 'Upgrade-Insecure-Requests': '1'
        #     }
        url="https://stock.tuchong.com/search?term={}".format(texturl)
        req=requests.get(url)
        soup=BeautifulSoup(req.text,'html.parser')
        js=soup.select('script')
        pattern = re.compile(r'(image_id\":(\"\d+\"))')
        va = pattern.findall(str(js))
        url_list=[]
        for i in range(len(va)):
            url = 'https://weiliicimg9.pstatp.com/weili/l/'+va[i][1].strip('\"')+'.webp'
            url_list.append(url)
        url = random.choice(url_list)
        # url = url_list[random.randint(0,len(url_list)-1)]
        return url