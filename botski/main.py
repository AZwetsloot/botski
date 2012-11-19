import src.irclib as irclib
import modules
import traceback
import os
import imp
import settings
import time
import thread
import gc
import re
import functions as f 
gc.enable()
global L_ERROR, L_INFO
L_ERROR = 1
L_INFO = 2
import sys
_old_excepthook = sys.excepthook

def myexcepthook(exctype, value, traceback):
    print "[ERROR] -> '%s'" % (str(value))
    print str(traceback)
    _old_excepthook(exctype, value, traceback)

sys.excepthook = myexcepthook

class Logger(object):
    def __init__(self, filename="botski.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "w")
        self.log.close()
        self.cr_pattern = re.compile("^.*\r", re.M)
        self.bs_pattern = re.compile(".\b")

    def write(self, message):
        self.terminal.write(message)
        self.log = open('botski.log', 'a')
        message = self.bs_pattern.sub('', self.cr_pattern.sub('', message))
        self.log.write(message)
        self.log.close()
                
sys.stdout = Logger("botski.log")
        
def get_hooks(module):
    f.debug_log("Loading " + module + " hooks.", L_INFO)
    mod = imp.new_module(module)
    fp, pathname, description = imp.find_module(module, ['modules'])
    try:
        mod = imp.load_module(module, fp, pathname, description)
    except:
        f.debug_log("Failed to load " + module, L_ERROR)
        if fp:
            fp.close()
        return
    f.debug_log(mod.M_HOOKS)
    return mod.M_HOOKS

def init_modules():
    f.debug_log("Running init for modules...", L_INFO)
    for module in settings.mod_dict:
        f.debug_log("Searching for init method in " + module, L_INFO)
        mod = imp.new_module(module)
        fp, pathname, description = imp.find_module(module, ['modules'])
        try:
            mod = imp.load_module(module, fp, pathname, description)
            if mod.init:
                f.debug_log("Ran an init function for " + module, L_INFO)
                mod.init()
        except:
            f.debug_log("Failed to load " + module, L_ERROR)
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
    #f.debug_log("Handled event: %s With source: %s Target: %s Arguments: %s" % (e.eventtype(), e.source(), e.target(), str(e.arguments())))
    if e.eventtype() in settings.target_events:
        #f.debug_log("An event we want to look at was triggered: %s With source: %s Target: %s Arguments: %s" % (e.eventtype(), e.source(), e.target(), str(e.arguments())))
        target_modules = list()
        for mod in settings.mod_dict:
            if e.eventtype() in settings.mod_dict[mod]:
                target_modules.append(mod)
        #f.debug_log(str(target_modules) + " are interested in processing this event.")
        for mod in target_modules:
            try:
                fp, pathname, description = imp.find_module(mod, ["modules"])
            except:
                f.debug_log("Couldn't load module " + mod, L_ERROR)
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
        f.debug_log("Sent nickserv ID")
        server.send_raw(settings.nickservID)
    if f.varexists('settings.channels'):
        f.debug_log("Tried to join channels.")
        server.join(settings.channels)
    if f.varexists('settings.realname'):
        f.debug_log("Sent setname")
        server.send_raw("SETNAME :" + settings.realname)
    if f.varexists('settings.operLine'):
        f.debug_log("Sent oper line")
        server.send_raw("OPER " + settings.operLine)
    if f.varexists('settings.automodes'):
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
        f.debug_log("Deleted file: " + settings.logging_file, L_ERROR)
    except:
        f.debug_log("Failed to delete logging file: " + settings.logging_file, L_ERROR)
        pass
    f.debug_log("Module hooks loaded for modules: " + str(settings.mod_dict), L_INFO)
    f.debug_log("Target events:" + str(settings.target_events), L_INFO)
    f.debug_log("Connecting...", L_INFO)
    irc = irclib.IRC()
    irc.add_global_handler('all_events', handle_events)
    irc.add_global_handler('disconnect', handle_disconnect)
    irc.add_global_handler('welcome', handle_welcome)
    server = irc.server()
    if settings.useBNC:
        server.connect(settings.bncHost, settings.bncPort, settings.nick, settings.bncPass, settings.ident, ssl=settings.ssl)
    else:
        server.connect(settings.serverhost, settings.port, settings.nick, settings.serverpass, settings.ident, ssl=settings.ssl)
    f.debug_log("Connected.", L_INFO)
    f.debug_log("Entered main loop.", L_INFO)
    settings.server = server
    irc.process_forever()
    
try:
    main()
except:
    print traceback.format_exc() 