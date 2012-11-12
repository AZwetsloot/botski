import src.irclib as irclib
import modules
import traceback
import os
import imp
import settings
import time
import thread
import gc

gc.enable()
global L_ERROR, L_INFO
L_ERROR = 1
L_INFO = 2

def varexists(variable):
    try:
        eval(variable)
        return True
    except:
        return False

def debug_log(msg, flag=2):
    if settings.log_errors_to_console and flag == 1:
        if settings.log_errors_to_console and not settings.log_everything_to_console:
            print msg
        if settings.log_errors_to_file:
            f = open(settings.logging_file, 'a+')
            f.write(time.strftime('%m-%d->%H:%M:%S: ', time.gmtime()) + msg + "\n")
            f.close()
    if settings.log_info_to_console and flag == 2 and not settings.log_everything_to_console:
        print msg
    if settings.log_everything_to_console:
        print msg
    return
        
def get_hooks(module):
    debug_log("Loading " + module + " hooks.", L_INFO)
    mod = imp.new_module(module)
    fp, pathname, description = imp.find_module(module, ['modules'])
    try:
        mod = imp.load_module(module, fp, pathname, description)
    except:
        debug_log("Failed to load " + module, L_ERROR)
        if fp:
            fp.close()
        return
    debug_log(mod.M_HOOKS)
    return mod.M_HOOKS

def init_modules():
    debug_log("Running init for modules...", L_INFO)
    for module in settings.mod_dict:
        debug_log("Searching for init method in " + module, L_INFO)
        mod = imp.new_module(module)
        fp, pathname, description = imp.find_module(module, ['modules'])
        try:
            mod = imp.load_module(module, fp, pathname, description)
            if mod.init:
                debug_log("Ran an init function for " + module, L_INFO)
                mod.init()
        except:
            debug_log("Failed to load " + module, L_ERROR)
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
    #debug_log("Handled event: %s With source: %s Target: %s Arguments: %s" % (e.eventtype(), e.source(), e.target(), str(e.arguments())))
    if e.eventtype() in settings.target_events:
        #debug_log("An event we want to look at was triggered: %s With source: %s Target: %s Arguments: %s" % (e.eventtype(), e.source(), e.target(), str(e.arguments())))
        target_modules = list()
        for mod in settings.mod_dict:
            if e.eventtype() in settings.mod_dict[mod]:
                target_modules.append(mod)
        #debug_log(str(target_modules) + " are interested in processing this event.")
        for mod in target_modules:
            try:
                fp, pathname, description = imp.find_module(mod, ["modules"])
            except:
                debug_log("Couldn't load module " + mod, L_ERROR)
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
    if varexists('settings.nickservID'):
        debug_log("Sent nickserv ID")
        server.send_raw(settings.nickservID)
    if varexists('settings.channels'):
        debug_log("Tried to join channels.")
        server.join(settings.channels)
    if varexists('settings.realname'):
        debug_log("Sent setname")
        server.send_raw("SETNAME :" + settings.realname)
    if varexists('settings.operLine'):
        debug_log("Sent oper line")
        server.send_raw("OPER " + settings.operLine)
    if varexists('settings.automodes'):
        server.send_raw("UMODE2 " + settings.automodes)
    return
    
def main():
    global irc
    global server
    settings.mod_dict = build_mod_dict()
    settings.target_events = find_target_events()
    init_modules()
    try:
        os.unlink(settings.logging_file)
        debug_log("Deleted file: " + settings.logging_file, L_ERROR)
    except:
        debug_log("Failed to delete logging file: " + settings.logging_file, L_ERROR)
        pass
    debug_log("Module hooks loaded for modules: " + str(settings.mod_dict), L_INFO)
    debug_log("Target events:" + str(settings.target_events), L_INFO)
    debug_log("Connecting...", L_INFO)
    irc = irclib.IRC()
    irc.add_global_handler('all_events', handle_events)
    irc.add_global_handler('disconnect', handle_disconnect)
    irc.add_global_handler('welcome', handle_welcome)
    server = irc.server()
    if settings.useBNC:
        server.connect(settings.bncHost, settings.bncPort, settings.nick, settings.bncPass, settings.ident, ssl=settings.ssl)
    else:
        server.connect(settings.serverhost, settings.port, settings.nick, settings.serverpass, settings.ident, ssl=settings.ssl)
    debug_log("Connected.", L_INFO)
    debug_log("Entered main loop.", L_INFO)
    settings.server = server
    irc.process_forever()
    
try:
    main()
except:
    print traceback.format_exc() 