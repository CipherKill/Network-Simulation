import os
import time
def log(data):
    n=len(data)+7
    print('\n\n\n'+'-'*n+'\n')
    print('::: '+str(data)+' :::')
    print('\n'+'-'*n)
    
os.system('mode con cols=100 lines=8')
cache="0000"
print('\n'+'*'*60+'\n')
print("LiFi Channel")
print('\n'+'*'*60)
input("Ready [RETURN]....")
while(True):
    channel1=open("channel.txt","r")
    file=open("data_log.txt",'a')
    #time.sleep(1)
    data=channel1.read()
    channel1.close()
    time.sleep(0.2)
    #response(deformat)
    if(len(data)):
        log(data)
        if(data!=cache):
            file.write(data+"\n")
            file.close()
        if(data=='close'):                  
             print("Disconnecting Channel")
             break
