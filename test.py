# -*- coding:utf-8 -*-
import HTTPProcessor
import UrlProcessor
if __name__ == "__main__":
    url ="http://pururin.com"
    httppcr = HTTPProcessor.HTTPProcessor()
    httppcr.UrlOpen(url);
    urlpcr = UrlProcessor.MainPageDJS_Processor()
    urlpcr.feed(httppcr.content.decode("utf-8"))
    print urlpcr.SinglePageUrls
    print urlpcr.NextPageUrl