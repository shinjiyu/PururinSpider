# -*- coding:utf-8 -*-
import sys
import os
import shutil
import HTTPProcessor
class FilePathProducer:
    def __init__(self):
        self.filePaths = []
        self.index = 0

    #不会产生后缀
    def GeneratePath(self,rootpath = ""):
        if rootpath == "":
            rootpath = sys.argv[0]
            rootpath = rootpath[:rootpath.rfind('/')]

        if not os.path.isdir(rootpath):
            os.mkdir(rootpath)


        prefix = "__temp"
        filename = prefix + str(self.index)
        self.index = self.index +1
        return os.path.join(rootpath,filename)

class ImgSaver:
    def __init__(self):
        self.FPP = FilePathProducer()
        pass

    def save(self,url,filename):
        rootpath = sys.argv[0]
        rootpath = rootpath[:rootpath.rfind('/')]

        suffix = url[url.rfind('.'):]
        if suffix.find("?") != -1:
            suffix = suffix[:suffix.find('?')]
        filepath = self.FPP.GeneratePath(os.path.join(rootpath,filename))+suffix

        if os.path.exists(filepath):
            os.remove(filepath)
        downloader = HTTPProcessor.HTTPProcessor()

        downloader.UrlOpen(url)
        if downloader.errorcode == 200:
            file = open(filepath,'wb')
            file.write(downloader.content)
            file.flush()
            file.close()
        else:
            filepath = ""

        del downloader
        return ""



