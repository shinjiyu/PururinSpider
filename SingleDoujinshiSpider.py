# -*- coding:utf-8 -*-  
import UrlProcessor
import HTTPProcessor
import ImgSaver
def DownloadSimplePageDJS(url_DJS):
    urlprocessor = UrlProcessor.SingleDJS_Processor()
    httpprocessor = HTTPProcessor.HTTPProcessor()
    httpprocessor.UrlOpen(url_DJS)
    if httpprocessor.errorcode == 200:
        urlprocessor.feed(httpprocessor.content.decode( "utf-8"))
        print "find %s pages" % urlprocessor.dwPageCount
        print urlprocessor.PageUrls

    else:
        print "open url failed! errorcode:%u" % httpprocessor.errorcode
       # print httpprocessor.errorreason

    #get pic
    filename = urlprocessor.filename
    pageprocessor =UrlProcessor.SinglePageDJS_Processor()
    imgsaver = ImgSaver.ImgSaver()
    for pageurl in urlprocessor.PageUrls:
        print pageurl
        httpprocessor.UrlOpen(pageurl.decode("utf-8"))
        if httpprocessor.errorcode == 200:
            pageprocessor.feed(httpprocessor.content.decode( "utf-8"))
            imgurl = pageprocessor.img
            print imgurl
            imgsaver.save(imgurl,filename)
            print "save ",imgurl," ok"

        else:
            print "open url failed! errorcode:%u" % httpprocessor.errorcode
