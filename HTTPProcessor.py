# -*- coding:utf-8 -*-
import urllib2
import urllib
from urllib2 import Request, urlopen, URLError,HTTPError
class HTTPProcessor:
    def __init__(self):
        self.errorcode = 0
        self.errorreason = ""
        self.content = ""

    def UrlOpen(self,url):
        self.errorcode = 0
        self.errorreason = ""
        self.content = ""

        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'


        headers = { 'User-Agent' : user_agent }
        request= urllib2.Request(url,None,headers);
        trytimes = 0
        while self.errorcode != 200:
            try:
                trytimes  =  trytimes+1
                print "try %uth time to open "% trytimes,url
                response = urllib2.urlopen(request,timeout= 3000)
            except HTTPError, e:
                self.errorcode = e.code
            except URLError, e:
                self.errocode = 0
                self.errorreason = e.reason
            except ValueError, e:
                self.errorcode = 0
                self.errorreason  = e
            else:
                self.errorcode = 200
                self.content = response.read()
                response.close()
            if trytimes>=10:
                break





