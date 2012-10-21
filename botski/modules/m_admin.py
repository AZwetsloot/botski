M_HOOKS = ['pubmsg', 'privmsg']

import settings
import re
import sys
if not sys.platform == "win32":
    import resource
import os
import imp

commandRegexString = '[!@.]'
commandRegex = re.compile(commandRegexString)

def find_target_events():
    target_events = list()
    for mod in settings.mod_dict:
        for event in settings.mod_dict[mod]:
            target_events.append(event)
    return target_events

def varexists(variable):
    try:
        eval(variable)
        return True
    except:
        return False
    
def get_hooks(module):
    debug_log("Loading " + module + " hooks.")
    mod = imp.new_module(module)
    fp, pathname, description = imp.find_module(module, ['modules'])
    try:
        mod = imp.load_module(module, fp, pathname, description)
    except:
        debug_log("Failed to load " + module)
        if fp:
            fp.close()
        return
    debug_log(mod.M_HOOKS)
    return mod.M_HOOKS

def init_modules():
    debug_log("Running init for modules...")
    for module in settings.mod_dict:
        debug_log("Searching for init method in " + module)
        mod = imp.new_module(module)
        fp, pathname, description = imp.find_module(module, ['modules'])
        try:
            mod = imp.load_module(module, fp, pathname, description)
            if mod.init:
                debug_log("Ran an init function for " + module)
                mod.init()
        except:
            debug_log("Failed to load " + module)
        if fp:
            fp.close()
    return 
      
def build_mod_dict():
    mod_dict = dict()
    #modulename:module_hooks#
    #We'll make our own list, with blackjack and hookers!     
    for filename in os.listdir('./modules'):
        if "." in filename:
            if filename.split(".")[1] == "py" and not filename == "__init__.py":
                module =  filename.split(".")[0]
                mod_dict[module] =  get_hooks(module)
    return mod_dict

def reloadEverything():
    del settings.mod_dict
    settings.mod_dict = build_mod_dict()
    del settings.target_events
    settings.target_events = find_target_events()
    return

def showLoadedModules(server, event, returnRoute):
    output = "Loaded Modules: "
    for mod in settings.mod_dict:
        output += mod + " "
    server.privmsg(returnRoute, output)
    return

def init():
    print "m_admin init was run"
    return

def run(server, irc, con, event): 
    if not event.source() in settings.owners:
        return
    else:
        if event.eventtype() == "privmsg":
            returnRoute = event.source().split("!")[0]
        else:
            returnRoute = event.target()
        arguments = event.arguments()[0].split(" ")
        if re.match(commandRegex, arguments[0][0]):
            command = arguments[0][1:len(arguments[0])]
            command = command.lower()
            if command == "modules":
                showLoadedModules(server,event, returnRoute)
                return
            elif command == "meminfo":
                if not sys.platform == "win32":
                    server.privmsg(returnRoute, "Meminfo: " + str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) + " kB")
                else:
                    server.privmsg(returnRoute, "Meminfo: Meminfo not available on Win32.")
                return  
            elif command == 'reload':
                reloadEverything()
                server.privmsg(returnRoute, "Reloaded all modules including previously unloaded modules. To unload them permenantly, move them to the ./unloaded directory.")
                showLoadedModules(server,event, returnRoute)
                return
            elif command == 'printdict':
                server.privmsg(returnRoute, str(settings.mod_dict))
                server.privmsg(returnRoute, str(settings.target_events))
                return
            elif command == 'unload':
                if len(arguments) > 1:
                    if settings.mod_dict.has_key(arguments[1]):
                        del settings.mod_dict[arguments[1]]
                        server.privmsg(returnRoute, arguments[1] + ' unloaded...')
                        showLoadedModules(server, event, returnRoute)
                    else:
                        server.privmsg(returnRoute, 'Can\'t find any module named \'' + arguments[1] + '\'')
                else:
                    server.privmsg(returnRoute, 'Syntax: ' + str(commandRegexString) + 'unload m_modulename')
                return
            elif command == 'raw':
                commandLen = len(arguments[0]) + 1
                server.send_raw( event.arguments()[0][commandLen:len(event.arguments()[0])])
            elif command == 'var':
                if len(arguments) > 1:
                    if varexists(arguments[1]):
                        server.privmsg(returnRoute, "Contents of %s = %s" % (arguments[1], str(eval(arguments[1]))))
                    else:
                        server.privmsg(returnRoute, "Var %s doesn't exist." % (arguments[1]))
                
    return