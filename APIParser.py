#!/bin/python3.6
import urllib.request
import json
import sys

tags = sys.argv[1]
filename = sys.argv[2]
config = "config/config_derpibooru.txt"

class APIParser:
    def __init__(self, taglist="", filename="", config=""):

        self.tagList = taglist
        self.config = config

        self.imgCounter = 0
        self.fileCounter = 0
        self.filePrefix = filename
        self.fileSuffix = ".txt"

        self.imgList = []
        self.imgPage = 0
        self.dataTrue = True

        with open(self.config) as target:
            config = target.read().replace("\t", "")
        config_dict = {}

        for element in config.split("\n"):
            tmp_dict = {element[:element.find(':')]: element[element.find(':') + 1:]}
            config_dict.update(tmp_dict)

        self.urlStr = str(config_dict['urlStr'])
        self.hereticStr = str(config_dict['hereticStr'])
        self.urlSearchStr = str(config_dict['urlSearchStr'])
        self.pageStr = str(config_dict['pageStr'])
        self.keyStr = str(config_dict['keyStr'])

        self.key = str(config_dict['key'])

        self.fileSize = int(config_dict['fileSize'])

    def run(self):
        while self.dataTrue:
            self.download()
            self.save()
        self.exit()

    def download(self):
        self.imgList = []
        loadlist = ['.  ','.. ','...']
        while True:
            url = self.urlStr + self.pageStr + str(self.imgPage) + self.hereticStr + self.urlSearchStr + self.tagList + self.hereticStr + self.keyStr + self.key
            self.page = urllib.request.urlopen(url).read()
            self.page = self.page.decode("utf-8")
            if len(self.page) <= 100:
                self.dataTrue = False
                break
            data = json.loads(self.page)
            cnt = 0

            while True:
                try:
                    __tmp = data['search'][cnt]['representations']['small']
                    cnt += 1
                    self.imgList.append(__tmp.replace("//derpicdn.net",""))
                except:
                    break
            sys.stderr.write('Running%s\r' % (loadlist[self.imgPage % 3])),
            sys.stderr.flush()
            self.imgPage += 1




    def save(self):
        target = open("data/%s%d%s" % (self.filePrefix, self.fileCounter, self.fileSuffix),'a+')
        __tmp = []
        for line in self.uniq(sorted(self.imgList)):
            __tmp.append(line)

        sys.stderr.write('Done, now saving %d links\r' % (len(__tmp)))
        sys.stderr.flush()

        for img in __tmp:
            if self.imgCounter == self.fileSize:
                self.imgCounter = 0
                self.fileCounter += 1
                target.close()
                target = open("data/%s%d%s" % (self.filePrefix, self.fileCounter, self.fileSuffix),'a+')
            target.write(img + "\n")
            target.flush()
            self.imgCounter += 1
        target.close()

    def uniq(self,iterator):
        previous = float("NaN")  # Not equal to anything
        for value in iterator:
            if previous != value:
                yield value
                previous = value

    def exit(self):
        sys.stderr.write('Done, saved to file(s) \"%sx%s\"\n' % (self.filePrefix,self.fileSuffix))
        sys.stderr.flush()

        exit()


if __name__ == "__main__":

    API = APIParser(tags, filename, config)
    API.run()

    while 42:
        try:
            pass
        except KeyboardInterrupt:
            API.exit()
            break
