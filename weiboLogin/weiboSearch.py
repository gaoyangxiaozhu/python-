import re
import json

def sServerData(serverData):
    "Search the server time & nonce from server data"
    p = re.compile('\((.*)\)')
    json_data = p.search(serverData).group(1)
    data = json.loads(json_data)
    server_time = str(data['servertime'])
    nonce = data['nonce']
    pubkey = data['pubkey']
    rsakv = data['rsakv']
    print "Server time is:", server_time
    print "Nonce is:", nonce
    return server_time, nonce, pubkey, rsakv
def sRedirectData(text):
    p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')
    login_url = p.search(text).group(1)
    print 'login_url:', login_url
    return login_url
