
import base64
import ast
import getpass
import time
import sqlite3

PYTHON =0
try:
    from urllib.request import Request
    from urllib.request import urlopen
    from urllib.error import HTTPError
    from urllib.error import URLError 
    PYTHON = 3
except ImportError:
    from urllib2 import Request
    from urllib2 import urlopen
    from urllib2 import HTTPError
    from urllib2 import URLError
    PYTHON =2

dbCON = None
dbCUR = None

def getJenkinsAPIData(url,username,password):
    JENKINS_LOGIN = username
    JENKINS_PASSWD = password

    DATA = None

    request = Request(url, DATA)#create request header

    #create the secure authentication section of the request header
    if PYTHON == 3:
        base64string = base64.encodebytes(('%s:%s' % (JENKINS_LOGIN, JENKINS_PASSWD)).encode()).decode().replace('\n', '')
    elif PYTHON == 2:
        base64string = base64.encodestring('%s:%s' % (JENKINS_LOGIN, JENKINS_PASSWD)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)

    #execure the actual request
    try:
        ANS = urlopen(request)
        return ANS
    except HTTPError as e:
        print(e.reason)
        return None
    except URLError as e:
        print(e.reason)
        return None

def openDB(dbName):
    dbCON = sqlite3.connect(dbName)
    dbCUR = dbCON.cursor()

    dbCUR.execute("""CREATE TABLE IF NOT EXISTS JOB(URL TEXT,NAME TEXT,STATUS TEXT,LAST_CHECKED TEXT)""")
    dbCON.commit()
    return

def insertJobIntoDB(jURL,Name,Status,Date):
    dbCUR.execute("""INSERT INTO JOB(URL,NAME,STATUS,LAST_CHECLED) VALUES (?,?,?,?)""",jURL,Name,Status,Date)
    dbCON.commit()
    return

def closeDB():
    if dbCUR is not None:
        dbCUR.close()
        dbCUR = None
    if dbCON is not None:
        dbCON.close()
        dbCON = None
    return


class connectionInfo:

    api_append = "/api/python?depth=0"
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
        if PYTHON == 3:
            name = input("Username:")
        elif PYTHON == 2:
            name = raw_input("Username:")
        if not name is None:
            self.username = name

    def queryPassword(self):
        pasw = None
        
        if PYTHON == 3:
            pasw = input("Password:")
        elif PYTHON == 2:
            pasw = raw_input("Password:")
        
        #the following line works fine on CLI however seems to have IDE compatibility issues
        #the line is also a substitute for the if block above it and serves as a safer way to 
        #input passwords into the script
        #pasw = getpass.getpass("Password:")
        if not pasw is None:
            self.password = pasw

    def queryURL(self):
        addr = None
        if PYTHON == 3:
            addr = input("Server Address:")
        elif PYTHON == 2:
            addr = raw_input("Server Address:")

        if addr is not None:
            self.url = addr 

openDB("test.db")

CON = connectionInfo()
RESPONSE = getJenkinsAPIData("http://localhost:8080/api/python?depth=0",CON.username,CON.password)

if RESPONSE is None:
    print("Connection Issue Exiting")
    exit(1)

RESP = eval(RESPONSE.read())#ast.literal_eval(RESPONSE.read()) seems to not work with pycharm as well however it should be used over eval

DATA = RESP["jobs"][0]
for i in RESP["jobs"]:
    print(i["url"])
    RESPONSE = getJenkinsAPIData(i["url"]+CON.api_append,CON.username,CON.password)
    if RESPONSE is None:
        print("Connection Issue Exiting")
        exit(1)
    
    JOB = eval(RESPONSE.read())

    RESPONSE = getJenkinsAPIData(JOB["lastBuild"]["url"]+CON.api_append,CON.username,CON.password)
    if RESPONSE is None:
        print("Connection Issue Exiting")
        exit(1)

    lastBuild = eval(RESPONSE.read())

    now = time.ctime(int(time.time()))

    insertJobIntoDB(i["url"],JOB["displayName"],lastBuild["result"],now)

    print("\tJob Display Name:{}".format(JOB["displayName"]))
    print("\tLast Build Time Checked At:{}".format(now))
    print("\tLast Build Status:{}".format(lastBuild["result"]))

closeDB()