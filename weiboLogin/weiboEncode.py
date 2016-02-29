# -*- coding: utf-8 -*-

import urllib
import base64
import rsa
import binascii

def post_encode(user_name, password, server_time, nonce, pubkey, rsakv):
    "Used to generate POST data"

    print 'pubkey: ', pubkey
    print 'rsakv: ', rsakv

    encode_username = get_user_name(user_name)

    encode_password = get_pwd(password, server_time,nonce, pubkey)

    post_data={
        'entry':'weibo',
        'gateway':'1',
        'from':'',
        'savestate':'7',
        'useticket':'1',
        'pagerefer':'http://weibo.com/p/1005052679342531/home?from=page_100505&mod=TAB&pids=plc_main',
        'vsnf':'1',
        'su':encode_username,
        'service':'miniblog',
        'servertime':server_time,
        'nonce':nonce,
        'pwencode':'rsa2',
        'rsakv':rsakv,
        'sp':encode_password,
        'sr':'1366*768',
        'encoding':'UTF-8',
        'prelt':'115',
        'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype':'META'
        }
    return post_data

def get_user_name(user_name):
    "Used to encode user name"

    user_name_temp = urllib.quote(user_name)
    user_name_encoded = base64.encodestring(user_name_temp)[:-1]
    return user_name_encoded


def get_pwd(password, servertime, nonce, pubkey):
    rsa_publickey = int(pubkey, 16)
    key = rsa.PublicKey(rsa_publickey, 65537) #创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password) #拼接明文js加密文件中得到
    encropy_pwd = rsa.encrypt(message, key) #加密
    encropy_pwd = binascii.b2a_hex(encropy_pwd) #将加密信息转换为16进制。
    return encropy_pwd
