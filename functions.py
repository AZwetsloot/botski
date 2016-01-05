'''Functions or variables used everywhere go here'''
import settings

def reversebit(str):
    str = str.split(".")[::-1]
    out = ""
    c = 0
    for s in str:
        c += 1
        if (c < len(str)):
            out += s + "."
        else:
            out += s
    return out

def debug_log(msg, flag=2):
    '''
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
    '''
    print msg
    return

def varexists(variable):
    try:
        eval(variable)
        return True
    except:
        return False
    
