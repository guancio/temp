import pycurl
import StringIO

class MegaUpload:
    def __init__(self, user, pwd):
        self.__curl = pycurl.Curl()
        self.__curl.setopt(pycurl.FOLLOWLOCATION, 1)
        self.__curl.setopt(pycurl.COOKIEFILE, '')
        self.__user = user
        self.__pwd = pwd

    def login(self):
        self.__curl.setopt(pycurl.URL, "http://www.megaupload.com/")
        b = StringIO.StringIO()
        self.__curl.setopt(pycurl.WRITEFUNCTION, b.write)
        self.__curl.perform()
        self.__curl.setopt(pycurl.URL, "http://www.megaupload.com/?c=login")
        b = StringIO.StringIO()
        self.__curl.setopt(pycurl.WRITEFUNCTION, b.write)
        self.__curl.perform()

        self.__curl.setopt(pycurl.URL, "http://www.megaupload.com/?c=login")
        b = StringIO.StringIO()
        self.__curl.setopt(pycurl.WRITEFUNCTION, b.write)
        self.__curl.setopt(pycurl.POST, 1)
        self.__curl.setopt(pycurl.POSTFIELDS, "login=1&password=%s&redir=1&username=%s" % (self.__pwd, self.__user))
        self.__curl.perform()

    def getFiles(self):
        self.__curl.setopt(pycurl.URL, "http://www.megaupload.com/?ajax=1")
        b = StringIO.StringIO()
        self.__curl.setopt(pycurl.WRITEFUNCTION, b.write)
        self.__curl.setopt(pycurl.POST, 1)
        self.__curl.setopt(pycurl.POSTFIELDS, "mode=modeAll")
        self.__curl.perform()
        items = b.getvalue().split(";")[2]
        items = items.split(" = ")[1]
        return eval(items)
