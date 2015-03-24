#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
为了上这个shodan也是拼了。因为注册用户只能看5页数据。
但是，我发现是否这个链接可以看到某个IP是否有服务。
http://www.shodanhq.com/host/view/116.211.118.233
于是，决定来看看有无这个服务，调用这个借口
'''

import httplib2
from string import replace,find,lower
from urlparse import urlparse,urljoin
from urllib import urlencode
import os
import sys
#同目录下的threadpool.py
import threadpool
#import threading


class listServer(object):
	def __init__(self,ipstart,ipend):
		self.server = ['MySQL','NetBIOS','HTTP','SSH','FTP','RDP','MongoDB','POP3 + SSL','IMAP + SSL','Redis','PostgreSQL','DNS','SMTP','MS-SQL']
		self.ips = ipstart
		self.ipe = ipend
		self.url = 'http://www.shodanhq.com/host/view/'
		self.result = {}
		self.alls = []
		self.threadnum = 5

	#ip地址+1
	def ipadd1(self,ip):
		list = ip.split('.')
		if int(list[0])>254 or int(list[1])>255 or int(list[2])>255 or int(list[3])>255:
			return -1
		if int(list[3]) == 255:
			list[3] = '0'
			if int(list[2]) == 255:
				list[2] = '0'
				if int(list[1]) == 255:
					list[1] = '0'
					t0 = int(list[0]) + 1
					list[0] = str(t0)
				t1 = int(list[1]) + 1
				list[1] = str(t1)
			t2 = int(list[2]) + 1
			list[2] = str(t2)
		t3 = int(list[3]) + 1
		list[3] = str(t3)
		return '.'.join(list)
	#得到地址长度
	def getlength(self):
		list_s = self.ips.split('.')
		list_e = self.ipe.split('.')
		length = (int(list_e[0])-int(list_s[0]))*255*255*255 + (int(list_e[1])-int(list_s[1]))*255*255 + (int(list_e[2])-int(list_s[2]))*255 + int(list_e[3])-int(list_s[3])
		print length
		return length
	#结果:{ip:[server1,server2],ip:[ff,ff]}
	def test(self,ip,i):
		#len = self.getlength()
		#ip = self.ips
		'''
		for i in range(len):
			#第一个IP地址进行访问
			h = httplib2.Http()
			url = self.url + ip
			alls = []
			headers = {'Content-type': 'application/x-www-form-urlencoded','Cookie':'__cfduid=d23895210ada71cba838f86839a9b69881427036412; shodan_main_session=0265250eb53249eaaaa18e1da4258ab3; __utmt=1; __utma=93054943.1262941236.1427036349.1427180690.1427192924.7; __utmb=93054943.63.10.1427192924; __utmc=93054943; __utmz=93054943.1427036349.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=Shodan'}
			response, content = h.request(url, 'GET', headers=headers)
			for each in self.server:
				if content.find(each) != -1:
					alls.append(each)
			self.result.setdefault(ip,alls)
			print 'the %s is OK\n' % i
			#ip + 1
			ip = self.ipadd1(ip)
		'''
		#第一个IP地址进行访问
		h = httplib2.Http()
		url = self.url + ip
		alls = []
		headers = {'Content-type': 'application/x-www-form-urlencoded','Cookie':'__cfduid=d23895210ada71cba838f86839a9b69881427036412; shodan_main_session=0265250eb53249eaaaa18e1da4258ab3; __utmt=1; __utma=93054943.1262941236.1427036349.1427180690.1427192924.7; __utmb=93054943.63.10.1427192924; __utmc=93054943; __utmz=93054943.1427036349.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=Shodan'}
		response, content = h.request(url, 'GET', headers=headers)
		for each in self.server:
			if content.find(each) != -1:
				alls.append(each)
		self.result.setdefault(ip,alls)
		print 'the %s is OK\n' % i

	def gothread(self):
		#建立进程池
		pool = threadpool.ThreadPool(self.threadnum)
		len = self.getlength()
		ip = self.ips
		#print type(self.threadnum)
		#print self.threadnum
		#两个list合并，直接相加就可以
		for i in range(len):
			ip = self.ipadd1(ip)
			pool.add_task(self.test,ip,i)
			
		#join and destroy all threads
		pool.destroy()

	def printr(self):
		fp = open(self.ips+'-'+self.ipe,'w')
		for k,v in self.result.iteritems():
			#print 'IP:'+ k
			fp.writelines('IP:'+ k +'\n')
			for each in v:
				#print each
				fp.writelines(each + '\n')
			#print '-------------------------\n'
			fp.writelines('----------------------------\n')
		fp.close()


if __name__=='__main__':
	ips = raw_input('input the start ip:\n')
	ipe = raw_input('input the end ip:\n')
	test = listServer(ips,ipe)
	test.gothread()
	test.printr()
	raw_input('input anything to end\n')
