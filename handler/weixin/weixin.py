#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import time
import xml.etree.ElementTree as ET
import logging
from handler.base import BaseHandler

class WeixinHandler(BaseHandler):
	def get(self):
		signature = self.get_argument("signature")
		timestamp = self.get_argument("timestamp")
		nonce = self.get_argument("nonce")
		echostr = self.get_argument("echostr")
		if verification(self) and echostr is not None:
			logging.info(echostr)
			self.write(echostr)
		else:
			self.write("access fail")

	def post(self):
		if verification(self):
			data = self.request.body
			logging.error("==data=:\n"+data)
			msg = parse_msg(data)
			if user_subscribe_event(msg):
				# save user's infomation
				weixinid = msg["FromUserName"]
				sql = "SELECT weixinid,employeeid,state  FROM weixin_user WHERE weixinid = %s" % weixinid
				print sql
				weixin_user = self.db.get(sql)
				print weixin_user['weixinid']
				if not weixin_user:
					self.db.execute(
						"INSERT INTO weixin_user (weixinid,state) values (%s,%s)",weixinid,1)
				else:
					sql = "UPDATE weixin_user SET state = 1 WHERE weixinid = %s" % weixinid
					self.db.execute(sql)

				helpinfo = help_info(msg)
				logging.error("help:\n"+helpinfo)
				self.write(help_info(msg))
			elif user_unsubscribe_event(msg):
				self.db.execute(
						"UPDATE weixin_user SET state = 10"
						"WHERE weixinid = %s",weixinid)
			elif is_text_msg(msg):
				content = msg['Content']
				if content == u'?' or content == u'？':
					self.write(help_info(msg))
				else:
					# books = search_book(content)
					# return rmsg
					self.write(response_text_msg(msg,"I'm sorry!"))
		self.write('message processing fail')

def verification(self):
    signature = self.get_argument('signature')
    timestamp = self.get_argument('timestamp')
    nonce = self.get_argument('nonce')
    token = "wancheng"
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = ''.join(tmplist)
    hashstr = hashlib.sha1(tmpstr).hexdigest()
    if hashstr == signature:
        return True
    return False

def user_subscribe_event(msg):
    return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'

def user_unsubscribe_event(msg):
	return msg['MsgType'] == 'event' and msg['Event'] == 'unsubscribe'

HELP_TPL = \
u"""
<item>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
<PicUrl><![CDATA[%s]]></PicUrl>
<Url><![CDATA[%s]]></Url>
</item>
</Articles>
</xml>
"""
NEWSHEAD_TPL = \
u"""
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[news]]></MsgType>
<ArticleCount>%d</ArticleCount>
<Articles>
"""

NEWSITEM_TPL = \
u"""
<item>
<Title><![CDATA[%s]]></Title> 
<Description><![CDATA[%s]]></Description>
<PicUrl><![CDATA[%s]]></PicUrl>
<Url><![CDATA[%s]]></Url>
</item>
"""

NEWSFOOT_TPL = \
u"""
</Articles>
</xml> 
"""
def help_info(msg):
    newshead = NEWSHEAD_TPL % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),6)
    item1 = NEWSITEM_TPL % (u"点击进入...","t","http://www.forgetwall.com/static/img/index.png","http://www.forgetwall.com/bh?page=1")   
    item2 = NEWSITEM_TPL % (u"回复\"b\"进行员工身份绑定","","http://www.forgetwall.com/static/img/a.png","hhttp://www.forgetwall.com/wx/page?page=1")
    item3 = NEWSITEM_TPL % (u"成就卓越 卓越成就","","http://www.forgetwall.com/static/img/3.png","hhttp://www.forgetwall.com/bh?page=1")
    item4 = NEWSITEM_TPL % (u"无限成长 成长无限","","http://www.forgetwall.com/static/img/4.png","http://www.forgetwall.com/bh?page=1")
    item5 = NEWSITEM_TPL % (u"至真信赖 信赖至真","","http://www.forgetwall.com/static/img/5.png","http://www.forgetwall.com/bh?page=1")
    item6 = NEWSITEM_TPL % (u"欢迎加入我们","","http://www.forgetwall.com/static/img/a.png","http://www.forgetwall.com/bh?page=1")
    return newshead+item1+item2+item3+item4+item5+item6+NEWSFOOT_TPL

TEXT_MSG_TPL = \
u"""
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<FuncFlag>0</FuncFlag>
</xml>
"""

def response_text_msg(msg, content):
    s = TEXT_MSG_TPL % (msg['FromUserName'], msg['ToUserName'], 
        str(int(time.time())), content)
    return s

def parse_msg(rawmsgstr):
    root = ET.fromstring(rawmsgstr)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg

def is_text_msg(msg):
    return msg['MsgType'] == 'text'


