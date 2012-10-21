import time
import re
import settings
M_HOOKS = ['privmsg', 'pubmsg', 'namreply', 'mode']
accessList = ['Alex!Alex@staff.swiftirc.net']
targetChannels = ['#kronos', '#az']
staffModes = re.compile("[vho]")
staffSymbols = re.compile("[+%@]") 
activityDB = 'activity.db'
channelProfiles = {}

def handlePubmsg(con, event):
    return

def handlePrivmsg(con, event):
    return

def handleNameslist(con, event):
    for nickname in event.arguments()[2].split(" "):
        print "Handling " + nickname
        if re.search(staffSymbols, nickname):
            print nickname + " matches regex"
            if not channelProfiles.has_key(event.arguments()[1]):
                channelProfiles[event.arguments()[1]] = list()
            channelProfiles[event.arguments()[1].lower()].append(nickname.replace("@","").replace("%","").replace("+",""))
    print str(channelProfiles)
    return

def buildNamelist(chan):
    print "building name list for " + chan
    settings.server.send_raw("NAMES " + chan)
    return

def executeSQL(str, db=activityDB, autocommit=True):
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute('''%s''' % (str))
        results = c.fetchall()
        conn.commit()
        conn.close()
        return results
    except:
        return traceback.format_exc()
        conn.close()

def init():
    for channel in targetChannels:
        channelProfiles[channel.lower()] = list()
        server.send_raw("NAMES " + channel)
    try:
        conn = sqlite3.connect(activityDB)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS activityLog (time int, nick text, channel text)''')
        #Delete all records older than 365d
        deletetime = int(time.gmttime()) - (365 * 24 * 60 * 60)
        c.execute('''DELETE FROM activitylog WHERE time <= %s''' % (deletetime))
        conn.commit()
        conn.close()
    except:
        print traceback.format_exc()
        conn.rollback()
        conn.close()
    return

def run(server, irc, con, event):
    e = event
    print str(e.eventtype()) + " " +  str(e.source()) + " " + str(e.arguments()[0])
    if event.eventtype() == "pubmsg" and event.target().lower() in targetChannels:
        if event.source().split("!")[0] in channelProfile[event.target().lower()]:
            handlePubmsg(con, event)
    elif event.eventtype() == "privmsg":
        handlePrivmsg(con, event)
    elif event.eventtype() == "namreply":
        if event.arguments()[1] in targetChannels:
            handleNameslist(con, event)
    elif event.eventtype() == "mode":
        print "Oh look, a mode, trying to match against " + event.arguments()[0]
        if re.search(staffModes, event.arguments()[0]):
            print event.arguments()[0] + " matches staffmodes, must rebuild nicklist" 
            buildNamelist(event.target())
        else:
            print event.arguments()[0] + " does not match [vho]"
    return