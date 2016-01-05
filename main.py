import src.irclib as irclib
import traceback
import os
import imp
import settings
import thread
import gc
import functions as f
import sys
_old_excepthook = sys.excepthook

def myexcepthook(exctype, value, traceback):
    print "[ERROR] -> '%s'" % (str(value))
    print str(traceback)
    _old_excepthook(exctype, value, traceback)

sys.excepthook = myexcepthook

def get_hooks(module):
    f.internalDebug("Loading " + module + " hooks.")
    mod = imp.new_module(module)
    fp, pathname, description = imp.find_module(module, ['modules'])
    try:
        mod = imp.load_module(module, fp, pathname, description)
    except:
        f.internalDebug("Failed to load " + module)
        if fp:
            fp.close()
        return
    f.internalDebug(mod.M_HOOKS)
    return mod.M_HOOKS

def init_modules():
    f.internalDebug("Running init for modules...")
    for module in settings.mod_dict:
        f.internalDebug("Searching for init method in " + module)
        mod = imp.new_module(module)
        fp, pathname, description = imp.find_module(module, ['modules'])
        try:
            mod = imp.load_module(module, fp, pathname, description)
            if mod.init:
                f.internalDebug("Ran an init function for " + module)
                mod.init()
        except:
            f.internalDebug("Failed to load " + module)
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

def find_target_events():
    target_events = list()
    for mod in settings.mod_dict:
        for event in settings.mod_dict[mod]:
            target_events.append(event)
    return target_events
                
def handle_events(c, e):
    #print str(e.eventtype()) + " " +  str(e.source()) + " " + str(e.arguments()[0])
    #f.internalDebug("Handled event: %s With source: %s Target: %s Arguments: %s" % (e.eventtype(), e.source(), e.target(), str(e.arguments())))
    if e.eventtype() in settings.target_events:
        #f.internalDebug("An event we want to look at was triggered: %s With source: %s Target: %s Arguments: %s" % (e.eventtype(), e.source(), e.target(), str(e.arguments())))
        target_modules = list()
        for mod in settings.mod_dict:
            if e.eventtype() in settings.mod_dict[mod]:
                target_modules.append(mod)
        #f.internalDebug(str(target_modules) + " are interested in processing this event.")
        for mod in target_modules:
            try:
                fp, pathname, description = imp.find_module(mod, ["modules"])
            except:
                f.internalDebug("Couldn't load module " + mod)
                print traceback.format_exc()
                return
            try:
                module = imp.load_module(mod, fp, pathname, description)
                thread.start_new_thread(module.run,(settings.server, irc, c, e))
            except:
                print traceback.format_exc()
    else: 
        #We're not interested in this event.
        return

def handle_disconnect(c, e):
    main()
    return

def handle_welcome(c, e):
    if f.varexists('settings.nickservID'):
        f.internalDebug("Sent nickserv ID")
        server.send_raw(settings.nickservID)
    if f.varexists('settings.channels'):
        f.internalDebug("Tried to join channels.")
        server.join(settings.channels)
    if f.varexists('settings.realname'):
        f.internalDebug("Sent setname")
        server.send_raw("SETNAME :" + settings.realname)
    if f.varexists('settings.operLine'):
        f.internalDebug("Sent oper line")
        server.send_raw("OPER " + settings.operLine)
    if f.varexists('settings.automodes'):
        server.send_raw("UMODE2 " + settings.automodes)
    return
    
def main():
    #Write a pidfile.
    pidfile = file("botski.pid", "w")
    pidfile.write(str(os.getpid()))
    pidfile.close()
    #Enable Garbage Collector
    gc.enable()
    global irc
    global server
    settings.mod_dict = build_mod_dict()
    settings.target_events = find_target_events()
    init_modules()
    try:
        os.unlink(settings.logging_file)
        f.internalDebug("Deleted file: " + settings.logging_file)
    except:
        f.internalDebug("Failed to delete logging file: " + settings.logging_file)
        pass
    f.internalDebug("Module hooks loaded for modules: " + str(settings.mod_dict))
    f.internalDebug("Target events:" + str(settings.target_events))
    f.internalDebug("Connecting...")
    irc = irclib.IRC()
    irc.add_global_handler('all_events', handle_events)
    irc.add_global_handler('disconnect', handle_disconnect)
    irc.add_global_handler('welcome', handle_welcome)
    server = irc.server()
    if settings.useBNC:
        server.connect(settings.bncHost, settings.bncPort, settings.nick, settings.bncPass, settings.ident, ssl=settings.ssl)
    else:
        server.connect(settings.serverhost, settings.port, settings.nick, settings.serverpass, settings.ident, ssl=settings.ssl)
    f.internalDebug("Connected.")
    f.internalDebug("Entered main loop.")
    settings.server = server
    irc.process_forever()
    f.internalDebug("irc.process_forever did not go forever")
    
try:
    main()
except:
    print traceback.format_exc() 