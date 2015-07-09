# -*- coding:utf-8 -*-
import HTTPProcessor
import UrlProcessor
import SingleDoujinshiSpider
import threading
import Queue
import time

#lock the url poor
QueueLock  = threading.Lock()

#max urlqueue
urlQueue = Queue.Queue(100)
#thread container
mythreads = []
exitFlag = False

class MyWorkThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while not exitFlag:
            url =""
            QueueLock.acquire()
            bIsThereAnyJob=not urlQueue.empty()
            if bIsThereAnyJob:
                url = urlQueue.get()
            QueueLock.release()
            if not bIsThereAnyJob:
                time.sleep(10)
            else:
                SingleDoujinshiSpider.DownloadSimplePageDJS(url)




if __name__ == "__main__":
    urlbase ="http://pururin.com"
    url = urlbase
    for i in range(0,10):
        mythread = MyWorkThread()
        mythread.start()
        mythreads.append(mythread)

    while True:
        httppcr = HTTPProcessor.HTTPProcessor()
        httppcr.UrlOpen(url);
        if httppcr.errorcode == 200:
            print "open url "+ url+ " success!"
            urlpcr = UrlProcessor.MainPageDJS_Processor()
            urlpcr.feed(httppcr.content.decode("utf-8"))

            for pageurl in urlpcr.SinglePageUrls:
                QueueLock.acquire()
                bFull = urlQueue.full()
                QueueLock.release()
                while bFull:
                    time.sleep(10)
                    QueueLock.acquire()
                    bFull = urlQueue.full()
                    QueueLock.release()
                QueueLock.acquire()
                urlQueue.put(urlbase+pageurl.decode("utf-8"))
                print "add url"
                QueueLock.release()


            url =urlbase+  urlpcr.NextPageUrl.decode("utf-8")
        else:
            print "open url:" + url+" failed!",httppcr.errorcode,httppcr.errorreason
            break
