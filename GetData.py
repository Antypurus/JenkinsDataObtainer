
python =0
try:
    from urllib.request import Request
    from urllib.request import urlopen
    python = 3
except ImportError:
    from urllib2 import Request
    from urllib2 import urlopen
    python =2

import base64
import sys

def getJenkinsAPIData(url,username,password):
    JENKINS_LOGIN = username
    JENKINS_PASSWD = password

    data = None

    request = Request(url, data)#create request header

    #create the secure authentication section of the request header
    if python == 3:
        base64string = base64.encodebytes(('%s:%s' % (JENKINS_LOGIN, JENKINS_PASSWD)).encode()).decode().replace('\n', '')
    elif python == 2:
        base64string = base64.encodestring('%s:%s' % (JENKINS_LOGIN, JENKINS_PASSWD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)

    #execure the actual request
    response = urlopen(request)
    return response

class connectionInfo:
    
    url = None
    username = None
    password = None

    def __init__(self):
        self.queryURL()
        self.queryUsename()
        self.queryPassword()
        return

    def queryUsename(self):
        name = None
        if python == 3:
            name = input("Username:")
        elif python == 2:
            name = raw_input("Username:")
        if not name is None:
            self.username = name

    def queryPassword(self):
        pasw = None
        if python == 3:
            pasw = input("Password:")
        elif python == 2:
            pasw = raw_input("Password:")
        if not pasw is None:
            self.password = pasw

    def queryURL(self):
        addr = None
        if python == 3:
            addr = input("Server Address:")
        elif python == 2:
            addr = raw_input("Server Address:")

        if addr is not None:
            self.url = addr 


con = connectionInfo()
response = getJenkinsAPIData("http://localhost:8080/api/python?depth=0",con.username,con.password)

resp = eval(response.read())

data = resp["jobs"][0]
print(resp["jobs"][0]["url"])