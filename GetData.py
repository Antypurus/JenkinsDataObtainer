import urllib2
import base64
import sys

def getJenkinsAPIData(url,username,password):
    JENKINS_LOGIN = username
    JENKINS_PASSWD = password

    data = None

    request = urllib2.Request(url, data)#create request header

    #create the secure authentication section of the request header
    base64string = base64.encodestring('%s:%s' % (JENKINS_LOGIN, JENKINS_PASSWD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)

    #execure the actual request
    response = urllib2.urlopen(request)
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

    def __init__(self,username,password,url):
        self.url = url
        self.password = password
        self.username = username

    def queryUsename(self):
        name = None
        sys.stdout.write("Username:")
        name = sys.stdin.read()
        if not name is None:
            self.username = name

    def queryPassword(self):
        pasw = None
        sys.stdout.write("Password:")
        pasw = sys.stdin.read()
        if not pasw is None:
            self.password = pasw

    def queryURL(self):
        addr = None
        sys.stdout.write("Server Address:")
        addr = sys.stdin.read()
        if not addr is None:
            self.url = addr 



response = getJenkinsAPIData("http://localhost:8080/api/python?depth=0")

resp = eval(response.read())

data = resp["jobs"][0]
print(resp["jobs"][0]["url"])