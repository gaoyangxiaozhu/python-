# -*- coding: utf-8 -*-

import requests

import weiboEncode
import weiboSearch
import json

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class WeiboLogin:
    def __init__(self, user, pwd):
        print 'Initializing WeiboLogin....'
        self.username = user
        self.password = pwd
        self.server_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)&_=1379834957683"
        self.login_url = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
        self.headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}

    def Login(self):
        "登陆程序"

        server_time, nonce, pubkey, rsakv = self.get_server_time()#登陆的第一步
        post_data = weiboEncode.post_encode(self.username, self.password, server_time, nonce, pubkey, rsakv)#加密用户和密码
        print "Post data length:\n", len(post_data)

        req = requests.post(self.login_url, data=post_data, headers=self.headers) #登陆的第二步——解析新浪微博的登录过程中
        print "Posting request..."
        text = req.text
        cookies = dict()
        try:
            login_url = weiboSearch.sRedirectData(text)#解析重定位结果
            req = requests.get(login_url)
            cookies_str= req.request.headers['Cookie']

            cookies_array = cookies_str.split(';')



            for item in cookies_array:
                key, value = item.split('=')
                cookies[key] = value
            print cookies
        except:
            print 'Login Error'
            return False

        #访问主页，把主页写入到文件中
        url = 'http://weibo.com/p/1005055021784365/follow?relate=fans&from=100505&wvr=6&mod=headfans#place'
        request = requests.get(url, cookies=cookies)
        text = request.text
        
        fp_raw = open("./weibo.html", "w+")
        fp_raw.write(text)
        fp_raw.close()
        #print text

        print 'Login Success'




        return True
    def get_server_time(self):
        "Get server time and nonce, which are used to encode the password"
        print "Getting server time and nonce..."
        r = requests.get(self.server_url) #得到网页内容
        server_data = r.text
        try:
            server_time, nonce, pubkey, rsakv = weiboSearch.sServerData(server_data)#解析得到serverTime，nonce等
            return server_time, nonce, pubkey, rsakv
        except:
            print 'Get server time & nonce error!'
            return None


if __name__ == '__main__':
    weiboLogin = WeiboLogin('example@163.com', 'password')

    if weiboLogin.Login() == True:
        print '登录成功'
