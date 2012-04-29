#! /usr/bin/env python
#coding=utf8
import urllib
import urllib2
import cookielib
import base64
import re
import json
import hashlib


postdata = {
    'entry': 'weibo',
    'gateway': '1',
    'from': '',
    'savestate': '7',
    'userticket': '1',
    'ssosimplelogin': '1',
    'vsnf': '1',
    'vsnval': '',
    'su': '',
    'service': 'miniblog',
    'servertime': '',
    'nonce': '',
    'pwencode': 'wsse',
    'sp': '',
    'encoding': 'UTF-8',
    'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
    'returntype': 'META'
}

def get_servertime():
    url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=dW5kZWZpbmVk&client=ssologin.js(v1.3.22)&_=1335601819416'
    data = urllib2.urlopen(url).read()
    p = re.compile('\((.*)\)')
    try:
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        return servertime, nonce
    except:
        print 'Get severtime error!'
        return None

def get_pwd(pwd, servertime, nonce):
    pwd1 = hashlib.sha1(pwd).hexdigest()
    pwd2 = hashlib.sha1(pwd1).hexdigest()
    pwd3_ = pwd2 + servertime + nonce
    pwd3 = hashlib.sha1(pwd3_).hexdigest()
    return pwd3

def get_user(username):
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username


def login():
    cookiefile='./cookies.txt'
    cookies = cookielib.LWPCookieJar(cookiefile)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies), urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    username = 'flyingjoe2010@gmail.com'
    pwd = 'wonderful1989'
    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.22)'
    try:
        servertime, nonce = get_servertime()
    except:
        return
    global postdata
    postdata['servertime'] = servertime
    postdata['nonce'] = nonce
    postdata['su'] = get_user(username)
    postdata['sp'] = get_pwd(pwd, servertime, nonce)
    postdata = urllib.urlencode(postdata)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'}
    req  = urllib2.Request(
        url = url,
        data = postdata,
        headers = headers
    )
    result = urllib2.urlopen(req)
    text = result.read()
    print text
    p = re.compile('location\.replace\(\'(.*?)\'\)')
    try:
        login_url = p.search(text).group(1)
        print login_url
        openresult = urllib2.urlopen(login_url)
        opentxt =openresult.read()
        print opentxt
        #weiboresult = urllib2.urlopen('http://www.weibo.com/login.php')
        #weibotxt = weiboresult.read()
        #print weibotxt
        cookies.save(cookiefile)
        print "Successful!"
    except:
        print 'Login error!'
def testCookie():
    cookiefile='./cookies.txt'
    cookiejar = cookielib.LWPCookieJar(cookiefile)
    cookiejar.load(cookiefile)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar), urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    content = urllib2.urlopen('http://www.weibo.com/').read()
    print content
    p = re.compile('location\.replace\(\'(.*?)\'\)')
    try:
        login_url = p.search(content).group(1)
        print login_url
        opentxt = urllib2.urlopen(login_url).read()
        print opentxt
        weibotxt = urllib2.urlopen('http://s.weibo.com/user/&keytime=1335657463672&region=custom:11:1000&page=1').read()
        print weibotxt
        print "Test Successful!"
    except Exception:
        print 'Test error!'
        print Exception.message,e

login()
#testCookie()