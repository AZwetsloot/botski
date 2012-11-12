M_HOOKS = ['privmsg']
accessHosts = ('staff.swiftirc.net', 'support.swiftirc.net')

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

def checkAccess(host):
    for hostname in accessHosts:
            if host.lower()[-len(hostname):] == hostname:
                return True
    return False

def run(server, irc, con, event):
    nick = event.source().split("!")[0]
    host = event.source().split("@")[1]
    message = event.arguments()[0]
    arguments = message.split(" ")
    if arguments[0].lower() == server.get_nickname().lower() and checkAccess(host):
        command = arguments[1]
        if command == "remove":
            if len(arguments) == 2:
                server.privmsg(nick, "Syntax: %s remove iptaddress" % (server.get_nickname()))
                server.privmsg(nick, "Example: %s remove 92.158.43.23" % (server.get_nickname()))
            elif len(arguments) > 2:
                ip = arguments[2]
                server.privmsg(nick, "Debug: Removing %s..." % (ip))
                try:
                    import MySQLdb
                except:
                    server.privmsg(nick, "Debug: Error! No MySQLdb module - tell Alex ")
                    return
                global conn, cursor
                try:
                    conn = MySQLdb.connect (host = settings.mysql_host,
                                         user = settings.mysql_user,
                                         passwd = settings.mysql_password,
                                         db = settings.mysql_database)
                    cursor = conn.cursor ()
                    #cursor.execute("insert into rr(zone, name,type,data) values(8,'%s','A','127.0.0.2')" % (reversebit(ip)))
                    cursor.execute('''delete from rr where id=8 and name="%s"''' % (reversebit(ip)))
                    server.privmsg(nick, str(cursor.rowcount))
                    cursor.close()
                    conn.commit()
                    conn.close()
                    server.privmsg(nick, "Removed %s from the DNSbl." % (ip))
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    conn.rollback()
                    conn.close()
                    pass
                
        