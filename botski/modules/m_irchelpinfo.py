M_HOOKS = ['join', 'ctcpreply', 'privnotice', 'privmsg', 'whoischannels']
joinsInFivSeconds = 5
targetChannel = '#irchelp'
import time
import settings
import thread
import pickle
import re
import traceback
import os.path
commandRegexString = '[!@.]'
commandRegex = re.compile(commandRegexString)


def d():
    while True:
        time.sleep(5)
        settings.joins = 0
    print "What? True is no longer True, question all reality and start preparing for interplanetary destruction."
    return
        
def init():
    #Set up the daemon to reset variables.
    thread.start_new_thread(d, ())
    if os.path.isfile('store.pckl'):
        f = open('store.pckl')
        settings.optin = pickle.load(f)
        f.close()
    return

def evalHasK(nick):
    if settings.internalNickDict.has_key(nick):
        return settings.internalNickDict[nick]
    else:
        return "None given in timeframe"

def delEntry(user):
    f = open('store.pckl', 'w')
    try:
        n = 0
        for item in settings.optin:
            if item.lower() == user.lower():
                del settings.optin[n]
                return
            n += 1
    except:
        print "failed to delete user from settings.optin"
        print traceback.format_exc()
        return
    pickle.dump(settings.optin, f)
    f.close()
    return

def addEntry(user):
    f = open('store.pckl', 'w')
    try:
        settings.optin.append(user)
    except:
        return
    pickle.dump(settings.optin, f)
    f.close()
    return

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
    time.sleep(2.5)
    server.privmsg("NickServ", "status " + nick)
    return

def runPrivnotice(server, irc, con, event):
    nick = event.source().split("!")[0]
    arguments = event.arguments()[0].split(" ")
    if nick.lower() == "nickserv":
        if arguments[0] == "STATUS":
            settings.internalStatusDict[arguments[1]] = arguments[2]
            noticenicks = ""
            for nick in settings.optin:
                noticenicks += nick + ","
                if len(noticenicks.split(",")) == 5:
                    server.notice(noticenicks,  "[IRCHELP] Nick: " + arguments[1] + " | NickServ status: " + watMeans(settings.internalStatusDict[arguments[1]]) + " | Client: " + evalHasK(arguments[1]))
                    noticenicks = ""
            server.notice(noticenicks,  "[IRCHELP] Nick: " + arguments[1] + " | NickServ status: " + watMeans(settings.internalStatusDict[arguments[1]]) + " | Client: " + evalHasK(arguments[1]))
            #server.notice("+" + targetChannel, "[IRCHELP] Nick: " + arguments[1] + " | NickServ status: " + watMeans(settings.internalStatusDict[arguments[1]]) + " | Client: " + evalHasK(arguments[1]))
            del settings.internalNickDict[arguments[1]]
            del settings.internalStatusDict[arguments[1]]
            return
        
def runPrivmsg(server, irc, con, event):
    arguments = event.arguments()[0].split(" ")
    if re.match(commandRegex, arguments[0][0]):
        command = arguments[0][1:len(arguments[0])]
        command = command.lower()
        nick = event.source().split("!")[0]
        if command == "optin":
            server.send_raw("WHOIS " + nick)
            time.sleep(1)
            channels = settings.internalWhoisDict[nick].split(" ")
            for channel in channels:
                if "#" in channel:
                    name = "#" + channel.split("#")[1]
                    if name.lower() == targetChannel.lower():
                        if re.match("[+%@]", channel.split("#")[0]):
                        #if "@" in channel.split('#')[0]:
                            if not nick in settings.optin:
                                addEntry(nick)
                                server.privmsg(nick, "Successfully added you to the opt-in list.")
                            else:
                                server.privmsg(nick, "You're already in the optin list for this nickname.")
                            del settings.internalWhoisDict[nick]
                        else:
                            server.privmsg(nick, "You're not voice, halfop or op in the target channel, and cannot receive these notices.")
                    else:
                        pass
        elif command == "optout":
            delEntry(nick)
            server.privmsg(nick, "Even if you weren't on the list, you definitely aren't now!")
        else:
            return
    return

def runWhois(server, irc, con, event):
    if settings.internalWhoisDict.has_key(event.arguments()[0]):
        settings.internalWhoisDict[event.arguments()[0]] += " " + event.arguments()[1]
    else:
        settings.internalWhoisDict[event.arguments()[0]] = event.arguments()[1]
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
    elif event.eventtype() == "privmsg":
        runPrivmsg(server, irc, con, event)
    elif event.eventtype() == "whoischannels":
        runWhois(server, irc, con, event)
    return
