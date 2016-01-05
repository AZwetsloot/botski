M_HOOKS = ['privmsg', 'pubmsg']
import re
import socket
import traceback

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
        if command == "host":
            if len(arguments) > 0:
                try:
                    if re.match("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", arguments[1]) or ":" in arguments[1]:
                        addrinfo = socket.gethostbyaddr(arguments[1])
                        server.privmsg(returnRoute, arguments[1] + " has the reverse address " +  addrinfo[0])                  
                    else:
                        addrinfo = socket.getaddrinfo(arguments[1], 80)
                        c = len(addrinfo)
                        x = 0
                        output = ""
                        if c > 1:
                            for addr in addrinfo:
                                x +=1
                                if not addr[4][0] in output:
                                    if not x == c: 
                                        output += addr[4][0] + ", "
                                    else:
                                        output += addr[4][0]
                            server.privmsg(returnRoute, arguments[1] + " has the addresses " + output)
                        else:
                            server.privmsg(returnRoute, arguments[1] + " has the address " + addrinfo[0][4][0])

                except:
                    server.privmsg(returnRoute, "No record found.")
                    print traceback.format_exc()
            
    return

    