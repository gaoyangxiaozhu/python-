#-*- coding: UTF-8 -*-
'''
网络爬虫之用户名密码以及验证码登录：爬取知乎网站
'''

import requests
import ConfigParser
import json

def create_session():
    cf = ConfigParser.ConfigParser()
    cf.read('config.ini')
    cookies = cf.items('cookies')
    cookies = dict(cookies)
    #from pprint import pprint
    #pprint(cookies)
    email = cf.get('info', 'email')
    password = cf.get('info', 'password')

    session = requests.session()
    login_data = {'email': email, 'password': password}
#    header = {
#        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 Chrome/48.0.2564.82 Safari/537.36',
#        'Host': 'www.zhihu.com',
#        'Referer': 'http://www.zhihu.com/'
#        }
    r = session.post('http://www.zhihu.com/login/email', data=login_data)
    print r.json()['msg']
    

    if r.json()['r'] == 1:
        print 'Login Failed, reason is:',
        for m in r.json()['data']:
            print r.json()['data'][m]
        print 'So we use cookies to login in ....'
        has_cookies = False 
        for key in cookies:
            if key!= '__name__' and cookies[key] != '':
                has_cookies = True
                break
        if has_cookies is False:
            raise ValueError('请填写config.ini文件中的cookies项')
        else:
            r = session.get('http://www.zhihhu.com/login/email', cookies=cookies) #实现验证码登录

    with open('login.html', 'w') as fp:
        fp.write(r.content)

    return session, cookies    

if __name__ == '__main__':
    requests_session, requests_cookies = create_session()

    url = 'http://www.zhihu.com/topic/19552832'

    content = requests_session.get(url, verify=False).content
    with open('url.html', 'w') as fp:
        fp.write(content)



