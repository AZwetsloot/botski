M_HOOKS = ['join', 'ctcpreply', 'privnotice']
joinsInFivSeconds = 5
targetChannel = '#irchelp'
import time
import settings
import thread


def d():
    while True:
        time.sleep(5)
        settings.joins = 0
    print "What? True is no longer True, question all reality and start preparing for interplanetenary destruction."
    return
        
def init():
    #Set up the daemon to reset variables.
    thread.start_new_thread(d, ())
    return

def evalHasK(nick):
    if settings.internalNickDict.has_key(nick):
        return settings.internalNickDict[nick]
    else:
        return "None given in timeframe"


def watMeans(status):
    if status == "0":
        return "Unregistered"
    elif status == "1":
        return "Registered but not Identified"
    elif status == "2":
        return "Unidentified but host in /ns access list"
    elif status == "3":
        return "Identified"
    else:
        return "Unknown"
def runJoin(server,irc, con, event):
    settings.joins += 1
    nick = event.source().split("!")[0]
    server.ctcp("VERSION", nick)
    time.sleep(2)
    server.privmsg("NickServ", "status " + nick)
    return

def runPrivnotice(server, irc, con, event):
    nick = event.source().split("!")[0]
    arguments = event.arguments()[0].split(" ")
    if nick.lower() == "nickserv":
        if arguments[0] == "STATUS":
            settings.internalStatusDict[arguments[1]] = arguments[2]
            server.notice("+" + targetChannel, "[IRCHELP] Nick: " + arguments[1] + " | NickServ status: " + watMeans(settings.internalStatusDict[arguments[1]]) + " | Client: " + evalHasK(arguments[1]))
            del settings.internalNickDict[arguments[1]]
            del settings.internalStatusDict[arguments[1]]
            return

def run(server, irc, con, event):
    if event.eventtype() == "join" and event.target().lower() == targetChannel and settings.joins <= joinsInFivSeconds:
        #thread.start_new_thread(runJoin, (server, irc, con, event))
        runJoin(server, irc, con, event)
    elif event.eventtype() == "ctcpreply":
        settings.internalNickDict[event.source().split("!")[0]] = event.arguments()[1]
    elif event.eventtype() == "privnotice":
        #thread.start_new_thread(runPrivnotice, (server,irc,con,event))
        runPrivnotice(server, irc, con, event)
    return
