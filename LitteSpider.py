# -*- coding:utf-8 -*-
import UrlProcessor
import HTTPProcessor
import ImgSaver
import urllib2

if __name__ == "__main__":
    urlList=["http://www.baidu.com"]
    imgList=[]
    httpprocessor = HTTPProcessor.HTTPProcessor()
    urlprocessor = UrlProcessor.UrlProcessor()

    step = 0
    while not len(urlList) == 0:
        print "this is the %uth step" % step
        step = step+1
        url =  urlList.pop(0)
        print "-current url is %s " % url
        httpprocessor.UrlOpen(url)
        if(httpprocessor.errorcode == 200):
            urlprocessor.feed(httpprocessor.content)
            urlList = urlList+urlprocessor.sublinks
            imgList = imgList + urlprocessor.imgurls
            if len(imgList) > 10:
                break
    print urlList
    print imgList
    urlprocessor.close()

    imgSaver = ImgSaver.ImgSaver()
    i = 0
    for file in imgList:
        i  = i+1
        print "save file %u" % i
        imgSaver.save(file)


    print "hello! this is a spider"
    pass