useBNC = False
bncHost = 'foo.bar.net'
bncPort = 1234
bncPass = "Foo:Bar"

#If useBNC = True, ignore the stuff directly below.
serverhost = "irc.swiftirc.net"
ssl = False
#If ssl = True, port must be 6697 or some other ssl enabled port
port = 6667
nick = "notski"
serverpass = None
ident = "botski"
realname = "botski"
automodes = "+Bps"

#------------------------------------------------#

#operLine = "botski myO:LinePwd"
nickservID = "PRIVMSG NickServ :id aPassword"
channels = "#az"
owners = ["Alex!~alex@Swift-822F6A28.al.cx"]

#------------------------------------------------#

#Some logging settings - these probably don't work yet.
log_everything_to_console = False
log_errors_to_console = True
log_errors_to_file = True
log_info_to_console = True
logging_file = "./botski.log"

#------------------------------------------------#

#Some Global Variables
mod_dict = dict()
stage = dict()
user_settings = dict()
target_events = list()
server = None
httprequestQ = list()
#------------------------------------------------#

#Put module specific globals below.
m_bncapp_bncchan = "#az"
m_bncapp_bncadminchan = "#az"
m_bncapp_adminhosts = ["Alex!Alex@Alex.support.swiftirc.net"]

#------------------------------------------------#
#This is for a module. Maybe it should just be in the module.
mysql_host = "1.2.3.4"
mysql_user = "foo"
mysql_password = "bar"
mysql_database = "mydns" 
#------------------------------------------------#
#This is for a module. Maybe it should just be in the module.
joins = 0
internalNickDict = {}
internalStatusDict = {}
internalWhoisDict = {}
optin = []
