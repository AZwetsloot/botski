useBNC = False

bncHost = 'kronos.nl.eu.swiftirc.net'
bncPort = 41762
bncPass = "KronosTest:f00barsmells"

#If useBNC = True, ignore the stuff directly below.

serverhost = "kronos.al.cx"
ssl = False
#If ssl = True, port must be 6697 or some other ssl enabled port
port = 6667
nick = "botski"
serverpass = None
ident = "botski"
realname = "botski, loggi's younger brother"
automodes = "+Bps"

#------------------------------------------------#

#operLine = "botski penis"
nickservID = "PRIVMSG NickServ :id mybotpasswin"
channels = "#az"
owners = ["Alex!Alex@staff.swiftirc.net", "Patje!Patrick@staff.swiftirc.net"]

#------------------------------------------------#

#Some logging settings
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

mysql_host = "5.39.77.214"
mysql_user = "mydns"
mysql_password = "MyDnS3572"
mysql_database = "mydns" 
#------------------------------------------------#
joins = 0
internalNickDict = {}
internalStatusDict = {}
internalWhoisDict = {}
optin = []
