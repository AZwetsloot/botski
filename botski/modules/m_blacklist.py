M_HOOKS = ['privnotice']
source = ["kronos.nl.eu.SwiftIRC.net", "irc.swiftirc.net"]
page = "http://dnsbl.patricsdfsasdl/"

import socket
import urllib
import settings
import time

def init():
    return

def reversebit(str):
    str = str.split(".")[::-1]
    out = ""
    c = 0
    for s in str:
        c += 1
        if (c < len(str)):
            out += s + "."
        else:
            out += s
    return out

def run(server, irc, con, event):
    e = event
    if "G:Line" in event.arguments()[0] and event.source() in source and 'bots/clones' in event.arguments()[0].lower():
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
        '''
        if additional == None:
            additional = "null"
        settings.httprequestQ.append(page + "?action=%s&ip=%s&additional=%s" % (type, ip, additional))
        for url in settings.httprequestQ:
            try:
                f = urllib.urlopen(url)
                f.read()
                settings.httprequestQ.remove(url)
                if len(settings.httprequestQ) > 10:
                    time.sleep(1)
            except:
                return
        '''
        #server.privmsg("#Home", "%s record %s%s (%s)" % (type, reversebit(ip), dnsbldomain, additional))
        if type == "add":
            try:
                import MySQLdb
            except:
                print "No MySQLdb, no DNSbl."
                return
            global conn, cursor
            try:
                conn = MySQLdb.connect (host = settings.mysql_host,
                                     user = settings.mysql_user,
                                     passwd = settings.mysql_password,
                                     db = settings.mysql_database)
                cursor = conn.cursor ()
                cursor.execute("insert into rr(zone, name,type,data) values(8,'%s','A','127.0.0.2')" % (reversebit(ip)))
                cursor.close()
                conn.commit()
                conn.close()
                print "Added " + ip + " to dnsbl."
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                conn.rollback()
                conn.close()
                pass
            
            return

    return