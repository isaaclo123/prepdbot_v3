import requests
import json
import base64
import getpass
from eventregistry import *
import time
import sys
import json

#######################################################
'''
username = "PREPD USERNAME GOES HERE"
password = "PREPD PASSWORD GOES HERE"

eventregUser = "EVENT REGISTRY USERNAME GOES HERE"
eventregPass = "EVENT REGISTRY PASSWORD GOES HERE"

#TEAM ID GOES HERE
teamId = 0000
'''
#######################################################

loginCookie = ""
loginInfo = ""
articleNum = 0

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

recentQ = GetRecentArticles(maxArticleCount = 1000)

while True:
    if checkLogin() == False:
        print "Login Failed"
        login()
    articleList = recentQ.getUpdates(er)
    print str(len(articleList)) + " articles were added"
    # do whatever you need to with the articleList
    for article in articleList:
        if article["lang"] == "eng":
            cut(article["url"])

    print "\nsleeping for 10 min...\n"
    time.sleep(600)
