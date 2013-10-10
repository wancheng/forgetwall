#!/usr/bin/python  
#coding=utf-8  

import time,urllib,urllib2
import hashlib

TPL_EVENT = '''
<xml>
    <ToUserName><![CDATA[%(to)s]]></ToUserName>
    <FromUserName><![CDATA[%(from)s]]></FromUserName>
    <CreateTime>%(time)d</CreateTime>
    <MsgType><![CDATA[event]]></MsgType>
    <Event><![CDATA[%(event)s]]></Event>
    <EventKey><![CDATA[%(key)s]]></EventKey>
</xml>'''

def post(url, data):  
	print url
	print data
	# data = urllib.urlencode(data)  
	req = urllib2.Request(url,data)  
	req.add_header("Content-Type","text/xml")
	response = urllib2.urlopen(req)  
	return response.read()  
  
def follow(url):
	msg = {
			"to":"123456",
			"from":"654321",
			"time":time.time(),
			"event":"subscribe",
			"key":""
			}
#	qs = "?signature=%s&timestamp=%s&nonce=%s" % int(msg["time"]),str(random.random())[-10:]

	suburl = "?signature=%s&timestamp=%s&nonce=%s&token=%s&echostr=%s" % (getSignature(msg["time"]),msg["time"],"wancheng","wancheng","wancheng")
	print post(url+suburl,TPL_EVENT % msg)

def getSignature(t):
	nonce = "wancheng"
	token = "wancheng"
	echostr = "wancheng"
	tmplist = [token, str(t), nonce]
	tmplist.sort()
	tmpstr = ''.join(tmplist)
	signature = hashlib.sha1(tmpstr).hexdigest()
	return signature

def main():  
		posturl = "http://127.0.0.1/weixin"  
		follow(posturl)
  
if __name__ == '__main__':  
		main()  
