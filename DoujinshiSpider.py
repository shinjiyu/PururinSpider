# -*- coding:utf-8 -*-
import HTTPProcessor
import UrlProcessor
import SingleDoujinshiSpider

if __name__ == "__main__":
    url ="http://pururin.com"
    while True:
        httppcr = HTTPProcessor.HTTPProcessor()
        httppcr.UrlOpen(url);
        if httppcr.errorcode == 200:
            print "open url "+ url+ " success!"
            urlpcr = UrlProcessor.MainPageDJS_Processor()
            urlpcr.feed(httppcr.content.decode("utf-8"))

            for pageurl in urlpcr.SinglePageUrls:
                print pageurl
                SingleDoujinshiSpider.DownloadSimplePageDJS(url+pageurl.decode("utf-8"))
                url =  urlpcr.NextPageUrl
        else:
            print "open url:" + url+" failed!",httppcr.errorcode,httppcr.errorreason
            break
