import settings
import functions as f

M_HOOKS = ['privmsg']
accessHosts = ('staff.swiftirc.net')

def init():
    return

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
                server.privmsg(nick, "Syntax: %s remove ipaddress" % (server.get_nickname()))
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
                    #cursor.execute("insert into rr(zone, name,type,data) values(8,'%s','A','127.0.0.2')" % (f.reversebit(ip)))
                    cursor.execute('''delete from rr where zone=8 and name="%s"''' % (f.reversebit(ip)))
                    if cursor.rowcount > 1:
                        conn.rollback()
                        server.privmsg(nick, "Something went wrong, and the syntax affected more than one line in the database. Please report this to Alex.")
                    elif cursor.rowcount == 0:
                        server.privmsg(nick, "There was no record for %s in the database." % (ip))
                    else:
                        server.privmsg(nick, "The IP was successfully removed from the database.")
                        server.privmsg(nick, "Please take note that DNS results may be cached in the BOPM for up to 5 minutes.")
                    cursor.close()
                    conn.commit()
                    conn.close()
                except MySQLdb.Error, e:
                    if "exists" in e.args[1]:
                        conn.close()
                        pass
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    conn.rollback()
                    conn.close()
                    pass
        elif command == "check":
            if len(arguments) > 2:
                try:
                        import MySQLdb
                except:
                    server.privmsg(nick, "Debug: Error! No MySQLdb module - tell Alex ")
                    return
                ip = arguments[2]
                try:
                    conn = MySQLdb.connect (host = settings.mysql_host,
                                             user = settings.mysql_user,
                                             passwd = settings.mysql_password,
                                             db = settings.mysql_database)
                    cursor = conn.cursor ()
                     #cursor.execute("insert into rr(zone, name,type,data) values(8,'%s','A','127.0.0.2')" % (f.reversebit(ip)))
                    cursor.execute('''select * from rr where zone=8 and name="%s"''' % (f.reversebit(ip)))
                    if cursor.rowcount >= 1:
                        server.privmsg(nick, "The IP exists in the database.")
                    else:
                        server.privmsg(nick, "The IP does not exist in the database.")
                    cursor.close()
                    conn.close()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    server.privmsg(nick, "Error %d: %s" % (e.args[0], e.args[1]))
        