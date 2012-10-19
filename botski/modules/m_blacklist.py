M_HOOKS = ['privnotice']
source = "irc.az.gy"
page = "http://dnsbl.patricsdfsasdl/"
import socket
import urllib
import settings
import time

def init():
    return

def run(server, irc, con, event):
    e = event
    if "G:Line" in event.arguments()[0] and event.source() == source and 'bots/clones' in event.arguments()[0].lower():
        arguments = event.arguments()[0].split(" ")
        if arguments[2] == "added":
            reason = event.arguments()[0].split(":")[6]
            reason = reason[0:len(reason)-1]
            reason.replace(" ", "")
            host = event.arguments()[0].split("@")[1].split(" ")[0]
            type = "add"
        elif arguments[1] == "removed":
            reason = event.arguments()[0].split(":")[4]
            reason = reason[0:len(reason)-1]
            reason.replace(" ", "")
            host = event.arguments()[0].split("@")[2].split(" ")[0]
            type = "remove"
        elif arguments[1] == "Expiring":
            reason = event.arguments()[0].split(":")[2].split(")")[0]
            reason.replace(" ", "")
            host = event.arguments()[0].split("@")[1].split(")")[0]
            type = "remove"
        additional = None
        if "-" in reason:
            additional = reason.split("-")[1].split(" ")[0]
        try:
            ip = socket.gethostbyname(host)
        except:
            print "Cannot resolve host " + host + " and therefore cannot add it to the blacklist."
            return
        if additional == None:
            additional = "null"
        server.privmsg("#Kronos", "Type: %s Host: %s IP: %s Additional: %s" % (type, host, ip, str(additional)))
        settings.httprequestQ.append(page + "?action=%s&ip=%s&additional=%s" % (type, ip, additional))
        server.privmsg('#Kronos', "Added %s?action=%s&ip=%s&additional=%s to httpreq list " % (page,type, ip, additional))
        for url in settings.httprequestQ:
            try:
                f = urllib.urlopen(url)
                f.read()
                settings.httprequestQ.remove(url)
                if len(settings.httprequestQ) > 10:
                    time.sleep(1)
            except:
                return
    return