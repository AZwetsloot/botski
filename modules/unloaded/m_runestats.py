M_HOOKS = ['pubmsg', 'privmsg']

import re
import urllib

commandRegexString = '[!@.]'
commandRegex = re.compile(commandRegexString)

def init():
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
        if command == 'stats':
            if len(arguments) > 1:
                rsn = arguments[1]
                skills = ("Overall", "Atk", "Def", "Str", "Cons", "Ra", "Pr", "Ma", "Coo", "Wc", "Fletch", "Fish", "FM", "Craft", "Smith", "Mining", "Herb", "Agil", "Thief", "Slay", "Farm", "RC", "Hunt", "Cons", "Sum", "DG", "Duel Tournament", "Bounty Hunters", "Bounty Hunter Rogues", "Fist of Guthix", "Mobilising Armies", "B.A Attackers", "B.A Defenders", "B.A Collectors", "B.A Healers", "Castle Wars Games", "Conquest", "Dominion Tower", "The Crucible", "GG: Athletics", "G:G Resource Race")
                f = urllib.urlopen("http://hiscore.runescape.com/index_lite.ws?player=" + rsn)
                fread = f.read()
                finalOutput = rsn + ":"
                c = 0
                for line in fread.split("\n"):
                    if c > 25:
                        #We're only interested in Skills, not those silly rank thingies
                        break
                    x = 0
                    output = skills[c]
                    for item in line.split(","):
                        if item == "-1":
                            x += 1
                            break
                        elif x == 1:
                            output += " " + item
                        x += 1
                    finalOutput += " " + output
                    c += 1
                server.privmsg(returnRoute, finalOutput)
    return