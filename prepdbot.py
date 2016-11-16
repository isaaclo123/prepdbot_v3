import requests
import json
import base64
import time
import sys
import json
from eventregistry import *

#######################################################

username = "PREPD USERNAME"
password = "PREPD PASSWORD"

eventregUser = "EVENT REGISTRY USERNAME"
eventregPass = "EVENT REGISTRY PASSWORD"

#TEAM ID GOES HERE
teamId = 0000

#place sources here in array form
sources = ["The Economist", "New York Times", "BBC", "Wall Street Journal", "Christian Science Monitor", "Washington Post"]

#place concepts here in array form
concepts = ["Economy", "Politics", "Military"]

#######################################################

loginCookie = ""
loginInfo = ""
articleNum = 0
oldURL = []
URL = []

#checks if person is logged into prepd

def checkLogin():
    global loginCookie
    profileReq = requests.get('https://api-v3.prepd.in/core/profile', cookies=loginCookie)

    if profileReq.status_code == 200:
        return True
    else:
        return False

#logs in to prepd

def login():
    global username
    global password
    global loginInfo
    global loginCookie

    print "Logging in " + username

    setReq = requests.get('https://api-v3.prepd.in/core/cookie/set')
    setCookie = dict(setReq.cookies)

    getReq = requests.get('https://api-v3.prepd.in/core/cookie/get', cookies=setCookie)

    base64auth = base64.b64encode(username + ":" + password)

    loginReq = requests.get('https://api-v3.prepd.in/core/login', headers={"authorization": "Basic " + base64auth})

    loginCookie = dict(loginReq.cookies)

    loginInfo = json.loads(loginReq.text)

#cuts an article based on a URL

def cut(url):
    global loginCookie
    global teamId
    global articleNum

    print url

    fastcatchReq = requests.get("https://api-v3.prepd.in/ws/authorize/fast-catch", cookies=loginCookie)

    diffbotPayload = {'teamId': teamId, 'url': url}
    diffbotReq = requests.post("https://api-v3.prepd.in/core/publications/diffbot", cookies=loginCookie, json=diffbotPayload)

    catchPayload = {"teams":[teamId],"url": url,"content":None}
    catchReq = requests.post("https://api-v3.prepd.in/core/catch", cookies=loginCookie, json=catchPayload)

    extempReq = requests.post("https://api-v3.prepd.in/core/catch", cookies=loginCookie, json=catchPayload)

    if extempReq.status_code != 200:
        print "Article already cut"

    if (fastcatchReq.status_code == 200 and diffbotReq.status_code == 200 and catchReq.status_code == 200 and extempReq.status_code == 200):
        articleNum = articleNum + 1

    print "Articles cut: " + str(articleNum) + "\n"

#relogin

def relogin():
    if checkLogin() == False:
        print "Login Failed"
        login()

#gets source URLs

def getURL(er):
    global sources
    global concepts
    global oldURL
    global URL

    print "\nGetting URLs\n"

    oldURL = list(URL)
    URL = []

    for i in concepts:
        print i
        q = QueryArticles(lang = ["eng"], sourceUri = sources, conceptUri = [er.getConceptUri(i)])
        q.addRequestedResult(RequestArticlesInfo(count = 40))
        res = er.execQuery(q)
        print ""

        for j in res["articles"]["results"]:
            if (j["url"] not in URL) and (j["url"] not in oldURL):
                print j["url"]
                URL.append(j["url"])
        print ""

#main

login()

if checkLogin() :
    print "\nLogin Success\n"
else:
    print "\nLogin Failed\n"
    sys.exit(1)

er = EventRegistry("http://eventregistry.org", verboseOutput = True)
print "logging in to Event registry\n"
er.login(eventregUser,eventregPass)

for i in xrange(0, len(sources)):
    sources[i] = er.getNewsSourceUri(sources[i])

while True:
    relogin()

    getURL(er)
    print str(len(URL)) + " articles were added"

    for i in URL:
        relogin()
        cut(i)

    print "\nsleeping for 30 min...\n"
    time.sleep(1800)
