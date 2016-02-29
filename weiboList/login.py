# -*- coding: utf-8 -*-

########################
#author:gyy
#date:2016/2/26
#login weibo
########################

import sys
import base64
import re
import json
import rsa
import binascii
import requests
import urllib

#from bs4 import BeautifulSoup

#新浪微博的模拟登陆
class WeiboLogin:
    #预登陆获得 servertime, nonce, pubkey, rsakv
    def getServerData(self):
        url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)&_=1379834957683"
        print "Getting server time and nonce..."
        data = requests.get(url).text
        p = re.compile('\((.*)\)')
        try:
                json_data = p.search(data).group(1)
                print json_data
                data = json.loads(json_data)
                print 'data: '
                print data
                server_time = str(data['servertime'])
                nonce = data['nonce']
                pubkey = data['pubkey']
                rsakv = data['rsakv']
                print "Server time is:", server_time
                print "Nonce is:", nonce
                return server_time, nonce, pubkey, rsakv
        except:
                print 'Get severtime error!'
                return None


    #获取加密的密码
    def getPassword(self, password, servertime, nonce, pubkey):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537) #创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password) #拼接明文js加密文件中得到
        passwd = rsa.encrypt(message, key) #加密
        passwd = binascii.b2a_hex(passwd) #将加密信息转换为16进制。
        return passwd

    #获取加密的用户名
    def getUsername(self, username):
        username_ = urllib.quote(username)
        username = base64.encodestring(username_)[:-1]
        return username

     #获取需要提交的表单数据
    def getFormData(self,userName,password,servertime,nonce,pubkey,rsakv):
        userName = self.getUsername(userName)
        psw = self.getPassword(password,servertime,nonce,pubkey)

        form_data = {
            'entry':'weibo',
            'gateway':'1',
            'from':'',
            'savestate':'7',
            'useticket':'1',
            'pagerefer':'http://weibo.com/p/1005052679342531/home?from=page_100505&mod=TAB&pids=plc_main',
            'vsnf':'1',
            'su':userName,
            'service':'miniblog',
            'servertime':servertime,
            'nonce':nonce,
            'pwencode':'rsa2',
            'rsakv':rsakv,
            'sp':psw,
            'sr':'1366*768',
            'encoding':'UTF-8',
            'prelt':'115',
            'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype':'META'
            }
        return form_data

    #登陆函数
    def login(self,username, psw):
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        servertime,nonce,pubkey,rsakv = self.getServerData()
        formData = self.getFormData(username, psw, servertime, nonce, pubkey, rsakv)
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'}
        req  = requests.post(url, data = formData, headers = headers)
        print "Posting request..."
        text = req.text
        print text
        p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')
        cookies = dict()

        try:
            login_url = p.search(text).group(1)
            print 'login_url:', login_url
            req =requests.get(login_url)
            cookies_str= req.request.headers['Cookie']
            cookies_array = cookies_str.split(';')

            for item in cookies_array:
                key, value = item.split('=')
                cookies[key] = value
            print "Login success!"
            return cookies, True
        except:
            print 'Login error!'
            return None, False
