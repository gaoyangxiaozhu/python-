# -*- coding: utf-8 -*-

########################
#author:gyy
#date:2016/2/26
#login weibo
########################

import login

import requests
import re
from lxml import etree
from bs4 import BeautifulSoup
import ConfigParser
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class WeiboListMain(object):

    start_url = ['http://weibo.com/p/1005055021784365/follow?relate=fans&from=100505&wvr=6&mod=headfans',
                 'http://weibo.com/p/1005055021784365/follow?relate=fans&page=%s']
    cookies = None

    sub_url_list = []


    def __init__(self, username, password):
        self.username = username
        self.password = password

        #cf = ConfigParser.ConfigParser()
        #cf.read('config.ini')
        #self.cookies = cf.items('cookies')
        #self.cookies = dict(self.cookies)

        #weiboLogin = login.WeiboLogin()
        #self.cookies, isLogin = weiboLogin.login(username, password)

        self.cookies={'SUHB': '04WvY66ZM2peoH', ' SUE': 'es%3D478ee0343a8d4c3b9d629d0c2c9f1b9a%26ev%3Dv1%26es2%3Db12be4e9a9f806fb78cccce110c0d767%26rs0%3Dc7bEkJt7XayTqobfcllKkZ735os8miUYlWWqdVhMKcUt4cWLEjoKr%252FLPzph4EnZ7oGReL1%252BEsepNLG6PvGb3CkeMqd1sgUhL7DDpHiHUz498W%252Fl%252BP%252FVUfzUT43gF1c%252B%252FcACTvFeDcFWl3Z4z%252Fs1YxNkWXunZr6QIQcpxdMR8Jmw%253D%26rv%3D0', ' SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9WWd_GFoCKyuG4vdxLl8ML-55JpX5K2t', ' SUB': '_2A2570Ey8DeRxGeRN6loQ8ibKzjuIHXVYpDl0rDV8PUNbuNAMLXDjkW9LHet94Im-yuQt9UXVznOwS3oolaHDNg..', ' ALF': '1488285803', ' SUP': 'cv%3D1%26bt%3D1456749804%26et%3D1456836204%26d%3Dc909%26i%3D6de9%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D0%26st%3D0%26uid%3D2318128657%26name%3D1456543560%2540qq.com%26nick%3D%25E9%25AB%2598%25E9%2598%25B3%25E9%2598%25B3%25E9%2598%25B3%25E9%2598%25B3%25E5%2585%25BB%26fmp%3D%26lcp%3D2014-03-16%252015%253A34%253A18', ' SUS': 'SID-2318128657-1456749804-JA-h7xj0-aa7599482f3394ed6544cfebe9d56de9', ' SSOLoginState': '1456749804'}

    def extract_weibo_response(self, response):     # 提取script里的weibo内容,替换response
        #script_set = response.xpath('//script')
        script_set=response.find_all('script')

        script = ''
        for s in script_set:
            try:
                s_text = s.string.encode('utf8').replace(r'\"', r'"').replace(r'\/', r'/')
            except:
                s_text = ''

            if s_text.find('follow_item S_line2') > 0 or s_text.find('WB_cardpage S_line1') > 0:
                regx = re.compile(r'FM\.view\(\{.*,"js":".*",\s*"html":"(.*)"\}\)')
                script = script+re.search(regx, s_text).group(1)
                break
        return script
    def parse_text_to_html(self, url):
        response = requests.get(url, cookies=self.cookies)
        #body = etree.HTML(response.text)
        body = BeautifulSoup(response.text)
        body = self.extract_weibo_response(body)
        page = BeautifulSoup(body)
        return page
    def spider(self):
        COUNT = 1
        PAGE = 1
        def start_spider(url, PAGE, COUNT):
            page = self.parse_text_to_html(url)
            current_followrs = page.find_all('div', class_="info_name W_fb W_f14")
            print 'current page number: ', PAGE
            for follow in current_followrs:
                print '当前序号: ', COUNT
                COUNT += 1
                print '   姓名: ', follow.find('a', class_="S_txt1").string
                sex = follow.find('i')['class'][1]
                if sex:
                    print '   性别: ', sex[5:]
                else:
                    print '   性别: male\n'
            PAGE = PAGE + 1
            if PAGE == 6:
                print 'spider end(only 5 pages content)...'
                return
            start_spider(self.start_url[1] % PAGE, PAGE, COUNT)

        start_spider(self.start_url[0], PAGE, COUNT)

weiboMain = WeiboListMain('1456543560@qq.com', '150247')
weiboMain.spider()
