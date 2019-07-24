import datetime

def log(command):
    
    with open('/home/rg252/setup/log.txt','a') as f:
        f.write('\n{} | {}'.format(str(datetime.datetime.now())[:-7],command))
