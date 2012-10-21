M_HOOKS = ['pubmsg', 'privmsg']

from random import choice

def init():
    return

def run(server, irc, con, event):
    arguments = event.arguments()[0].split(" ")
    if event.eventtype() == 'privmsg':
        returnRoute = event.source().split("!")[0]
    else:
        returnRoute = event.target()
    if len(arguments) > 0:
        if arguments[0].lower() in ("hi", "hello", "hiya", "hey") and server.get_nickname().lower() in arguments[1].lower():
            server.privmsg(returnRoute, choice(("Hiya", "Hello", "Hi thar", "G'day", "Hey", "Hi")) + " " + event.source().split("!")[0])
        else:
            return
        