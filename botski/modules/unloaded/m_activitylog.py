import time
import re
global channelProfiles
M_HOOKS = ['privmsg', 'pubmsg', 'namreply', 'mode']
accessList = ['Alex!Alex@staff.swiftirc.net']
targetChannels = ['#kronos', '#az']
staffModes = re.compile("[vho]")
staffSymbols = re.compile("[+%@]") 
activityDB = 'activity.db'
channelProfiles = {}

def executeSQL(str, db=activityDB, autocommit=True):
    print "Ex Q: " + str
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
        
def handlePubmsg(con, event):
    executeSQL('''INSERT INTO activitylog values(%s, "%s", "%s")''' % (int(time.gmttime()), event.source().split("!").lower(), event.target().lower()))
    return

def handlePrivmsg(con, event):
    return

def handleNameslist(con, event):
    for nickname in event.arguments()[2].split(" "):
        if re.search(staffSymbols, nickname):
            if not channelProfiles.has_key(event.arguments()[1].lower()):
                channelProfiles[event.arguments()[1]] = list()
            channelProfiles[event.arguments()[1].lower()].append(nickname.replace("@","").replace("%","").replace("+","").lower())
    print str(channelProfiles)
    return

def buildNamelist(chan):
    server.send_raw("NAMES " + chan)
    return

def init():
    for channel in targetChannels:
        channelProfiles[channel.lower()] = list()
        server.send_raw("NAMES " + channel)
        print "Init run"
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
    if event.eventtype() == "pubmsg" and event.target().lower() in targetChannels:
        print str(channelProfiles)
        if event.source().split("!")[0].lower() in channelProfiles[event.target().lower()]:
            handlePubmsg(con, event)
    elif event.eventtype() == "privmsg":
        handlePrivmsg(con, event)
    elif event.eventtype() == "namreply":
        if event.arguments()[1] in targetChannels:
            handleNameslist(con, event)
    elif event.eventtype() == "mode":
        if re.search(staffModes, event.arguments()[0]):
            buildNamelist(event.target())
    return