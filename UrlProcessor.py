# -*- coding:utf-8 -*-
import string
from HTMLParser import HTMLParser
class UrlProcessor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.sublinks = []
        self.imgurls = []
        self.taglogs = []

    def LogTag(self,tag,atts):
        if not tag in self.taglogs:
            self.taglogs.append(tag)

    def IsValid(self,url):
        InvalidDic =["/","javascript:;"]
        return not url in InvalidDic

    def handle_starttag(self,tag,atts):
        self.LogTag(tag,atts)
        if tag == "a":
            if len(atts) == 0:
                pass
            else:
                for (name,value) in atts:
                    if name == "href" and self.IsValid(value) and not value in self.sublinks:
                        self.sublinks.append(value)

        elif tag == "img":
            if len(atts) ==0:
                pass
            else:
                for(name,value) in atts:
                    if name == "src" and not value in self.imgurls:
                        self.imgurls.append(value)


class SingleDJS_Processor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.dwPageCount = 0
        self.PageUrls = []
        self.bNextAIsUrl = False
        self.bNextDataIsPageCount  = False
        self.filename = ""

    def clear(self):
        self.dwPageCount = 0
        self.PageUrls = []
        self.bNextDataIsPageCount  = False

    def handle_starttag(self,tag,atts):
        if tag == "div":
            for(name,value) in atts:
                if name == "class" and value == "block spacetop preview-thumbnails":
                    self.bNextAIsUrl = True
        elif  tag == "a":
            if self.bNextAIsUrl:
                self.bNextAIsUrl = False
                for(name,value) in atts:
                    if name == "href":
                        #create suffix str
                        suffixstr = value[value.rfind("/"):]
                        tempstring = suffixstr[suffixstr.rfind("_"):]
                        tempstring = tempstring.replace("1","@@@###")
                        suffixstr = suffixstr[:suffixstr.rfind("_")]+tempstring
                        self.filename = suffixstr[1:suffixstr.rfind("_")]

                        #create profix str
                        profixstr = value[:value.rfind("/")]
                        profixstr = profixstr[:profixstr.rfind("/")]


                        hoststr = "http://pururin.com"
                        indexlen = len(str(self.dwPageCount))
                        for i in range(0,self.dwPageCount):
                            #create a indexing with same length
                            indexstr = str(i)
                            indexstr = "0"+indexstr
                            strFileName = suffixstr.replace("@@@###",str(i+1))
                            self.PageUrls.append(hoststr+profixstr+"/"+indexstr+strFileName)

    def handle_data(self, data):
        if data == "Pages":
            self.bNextDataIsPageCount = True
        elif self.bNextDataIsPageCount == True:
            self.dwPageCount = string.atoi(data[:data.find(" ")])
            self.bNextDataIsPageCount =False
            print "find pagecount %u" % self.dwPageCount


    def handle_endtag(self, tag):
        if tag == "li":
            self.bInli = False


class SinglePageDJS_Processor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.img = ""

    def Reset(self):
        self.img = ""

    def handle_startendtag(self, tag, attrs):
        if tag == "img":
            classname =""
            src = ""
            for (name,value) in attrs:
                if name == "class":
                    classname = value
                elif name == "src":
                    src  = value

            if classname == "b":
                self.img = "http://pururin.com"+src

class MainPageDJS_Processor(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.SinglePageUrls = []
        self.NextPageUrl = ""
        self.bInPageJumper = False

    def handle_endtag(self,tag):
        if tag == "div":
            self.bInPageJumper = False
    def handle_starttag(self,tag,attrs):
        if tag == "div":
            for (name,value) in attrs:
                if name =="class" and value =="pager jumper":
                    self.bInPageJumper = True

        if tag == "a" :
            for(name,value) in attrs:
                if name == "href" and value.find(u"gallery") != -1:
                    self.SinglePageUrls.append(value)
                elif name == "href" and self.bInPageJumper and self.NextPageUrl == "":
                    self.NextPageUrl = value

