import urllib2
import base64

def getJenkinsAPIData(url):
    JENKINS_LOGIN = "admin"
    JENKINS_PASSWD = "siroco3ds112"

    data = None

    request = urllib2.Request(url, data)#create request header

    #create the secure authentication section of the request header
    base64string = base64.encodestring('%s:%s' % (JENKINS_LOGIN, JENKINS_PASSWD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)

    #execure the actual request
    response = urllib2.urlopen(request)
    return response


url="http://localhost:8080/api/python?depth=0"
response = getJenkinsAPIData(url)

resp = eval(response.read())

'''
for key in resp:
    print(key)
'''
data = resp["jobs"][0]
print(resp["jobs"][0]["url"])