M_HOOKS = ['pubmsg', 'privmsg']

import re
import sqlite3
import traceback
import time
import thread
import settings

commandRegexString = '[!@.]'
commandRegex = re.compile(commandRegexString)
scaling = {
   'years': 365.25 * 24 * 3600, 
   'year': 365.25 * 24 * 3600, 
   'yrs': 365.25 * 24 * 3600, 
   'y': 365.25 * 24 * 3600, 

   'months': 29.53059 * 24 * 3600, 
   'month': 29.53059 * 24 * 3600, 
   'mo': 29.53059 * 24 * 3600, 

   'weeks': 7 * 24 * 3600, 
   'week': 7 * 24 * 3600, 
   'wks': 7 * 24 * 3600, 
   'wk': 7 * 24 * 3600, 
   'w': 7 * 24 * 3600, 

   'days': 24 * 3600, 
   'day': 24 * 3600, 
   'd': 24 * 3600, 

   'hours': 3600, 
   'hour': 3600, 
   'hrs': 3600, 
   'hr': 3600, 
   'h': 3600, 

   'minutes': 60, 
   'minute': 60, 
   'mins': 60, 
   'min': 60, 
   'm': 60, 

   'seconds': 1, 
   'second': 1, 
   'secs': 1, 
   'sec': 1, 
   's': 1
}
periods = '|'.join(scaling.keys())
p_command = r'\.in ([0-9]+(?:\.[0-9]+)?)\s?((?:%s)\b)?:?\s?(.*)' % periods
r_command = re.compile(p_command)


def start_messagecheck_daemon():
    #Give the IRC connection time to establish first!
    time.sleep(10)
    while True:
        time.sleep(3)
        try:
            conn = sqlite3.connect('reminders.db')
            c = conn.cursor()
            c.execute('''SELECT * FROM reminders WHERE time <= %s''' % (int(time.time())))
            results = c.fetchall()
            for row in results:
                settings.server.send_raw(row[1])
            c.execute('''DELETE FROM reminders WHERE time <= %s''' % (int(time.time())))
            conn.commit()
            conn.close()
        except:
            print traceback.format_exc()
            conn.close()
    return

def init():
    #Start the reminder checker. This is a separate thread that checks every 5 seconds if a message should've been shown.
    thread.start_new(start_messagecheck_daemon, ())
    try:
        conn = sqlite3.connect('reminders.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS reminders (time int, message text)''')
        conn.commit()
        conn.close()
    except:
        print traceback.format_exc()
        conn.rollback()
        conn.close()
    return

def run(server, irc, con, event):
    if event.eventtype() == 'privmsg':
        returnRoute = event.source().split("!")[0]
    else:
        returnRoute = event.target()
    arguments = event.arguments()[0].split(" ")
    if re.match(commandRegex, arguments[0][0]):
        command = arguments[0][1:len(arguments[0])]
        command = command.lower()
        if command == 'in':
            if len(arguments) > 1:
                m = r_command.match(event.arguments()[0])
                if not m: 
                    return
                length, scale, message = m.groups()
                length = float(length)
                factor = scaling.get(scale, 60)
                duration = length * factor
                if duration % 1: 
                    duration = int(duration) + 1
                else: 
                    duration = int(duration)
                now = int(time.time())
                reminderTime = now + duration
                reminderDate = time.asctime(time.gmtime(reminderTime)) + "GMT"
                try:
                    conn = sqlite3.connect('reminders.db')
                    c = conn.cursor()
                    c.execute('''INSERT INTO reminders values(%s, '%s')''' % (reminderTime, "PRIVMSG " + returnRoute + " :" + event.source().split("!")[0] + ": " + message))
                    conn.commit()
                    conn.close()
                    server.privmsg(returnRoute, "OK, I will remind you at " + reminderDate)
                except:
                    server.privmsg(returnRoute, "Database error: Your reminder was not added.")
                    print traceback.format_exc()
                    conn.close()
                return
            else:
                server.privmsg(returnRoute, "[ Syntax: " + commandRegexString + "in (Xd|Xm|Xs) MSG | Example: .in 22h Tell Alex that he is beautiful. ]")
            return
        elif command == "reminders":
            try:
                conn = sqlite3.connect('reminders.db')
                c = conn.cursor()
                c.execute("SELECT * from reminders")
                results = c.fetchall()
                server.privmsg(returnRoute, "I currently have " + str(len(results)) + " reminder(s) in the queue.")
                conn.commit()
                conn.close()
            except:
                conn.close()
                server.privmsg(returnRoute, "Database connection failed.")
                traceback.print_exc()
            return
    return