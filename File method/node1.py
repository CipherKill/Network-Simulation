#import statements here
import time                                             
import os
import threading
from VLCFrames import *
from MACUnrap import *
from log_col import *
#time.sleep(5)
os.system("color f")
device_address="0101"
device_PAN="FF00"

AssociateRQ="1"
AssociateRSP="2"
Diss="3"
dataRQ="4"
up=u"\u2192"
down=u"\u2190"
access='1'
log.warn("[!]CO-ORDINATOR SETUP:")
log.say("")
access=str(input("\nAllow incoming associations? ['1':reject / '0':accept]:~ ")) #'0' will allow '1' will deny
data_ask=(input("Type DATA to be sent:~ "))
dsplit=int(input("Data slot size (bytes):~ "))
input("[Co-ordinator] Ready? [PRESS RETURN]....")
try:
    data_=[data_ask[i:dsplit+i] for i in range(0,len(data_ask),dsplit)]
    log.warn("\n[!]Formatting data to 8 bytes slots.")
    for i in range(len(data_)):
        dat=data_[i]+'0'*(dsplit-len(data_[i]))
        data_[i]=dat
    time.sleep(0.5)
    log.warn("[!]Format complete")
    print("DATA: {}\n".format(data_))
except:
    log.error("[!!!]ERROR IN FORMATTING!")

    
if(access=='1'):
    log.error("[#]Incoming association will be rejected.\n")
elif(access=='0'):
    log.say("[#]Incoming association will be accepted.\n")
else:
    log.warn("[!]Unknown command.\n")
    time.sleep(3)
    exit()

i=0
print("MARK 6")
log.warn("\n[!]This is the CO-ORDINATOR\n[!]Device Address : 0101\n")
time.sleep(1)
log.notify("[!]Program starts now\n")

def write(data):
    channel0=open("channel.txt","w")
    channel0.write(data)
    channel0.flush()
    time.sleep(0.2)
    #open("channel.txt",'w').close()
def look():
    channel1=open("channel.txt","r")                        
    data=channel1.read()
    channel1.close()
    time.sleep(0.2)
    return data
time_start=time.clock()
#send
def send():
    global i,data_,dsplit
    while(True):
        #open("channel.txt","w").close()
        if(i==1):
            data=FrameGenerator.AssociationResponse(access,"0101")
            write(data)
            log.warn("\n[{}]Sending ASSOCIATION RESPONSE!\n".format(up))
            i=10
        elif(i==2):
            log.say("\n[!]SENDING DATA")
            seq_number=len(data_)-1
            data=FrameGenerator.dataFrame(data_[seq_number],seq_number)
            write(data)
            log.warn("\n[{}]DATA frames sent!\n".format(up))
            i=10
        elif(i==3):
            data=FrameGenerator.DisassociationNotification("1")
            write(data)
            log.warn("\n[{}]Sending DISASSOCIATION frame!\n".format(up))
            i=10
            log.warn("\n[!]CLOSING CONNECTION!\n")
            log.say("[*]Completed in {} seconds.\n[*]{} Byte slots used for data.".format(round((time.clock()-time_start),2),dsplit))
            input()
            
        else:
            data=""

#receive
def recv():
    global i,data
    while(True):
        data=look()
        if(len(data)):
            #print("::::::::::::::::::::",data)
            #decode the data here
            DestinationAddress = data[24:28]
            FrameType = data[0:3]
            if(DestinationAddress==device_address):
                open("channel.txt",'w').close()
                if(FrameType=="011"):#command frame
                    cmdID=MACDecoder(str(data),0)
                    if(cmdID==AssociateRQ):#association req
                        i=1
                        log.notify("\n[{}]Received ASSOCIATION frame!\n".format(down))
                        cmdID=MACDecoder(str(data),1)
                    elif(cmdID==dataRQ):    #data req
                        i=2
                        log.notify("\n[{}]Received DATA REQUEST frame!\n".format(down))
                        cmdID=MACDecoder(str(data),1)
                elif(FrameType=="010"):#ack
                    seq=int(MACDecoder(data,0),2)
                    log.notify("\n[{}]Received ACKNOWLEDGMENT from node!\n".format(down))
                    if(seq!=0):
                        #send extra data
                        log.warn("\n[{}]Sending remaining DATA frame {}!\n".format(up,seq-1))
                        data=FrameGenerator.dataFrame(data_[seq-1],seq-1)
                        write(data)
                    else:
                        i=3                       
                                            
            #if association request received, then i+=1
            #if data request received, then i+=1
            #check the ack and see if any more data to be sent, if no then i+=1
            
#multithreading commands
thread1=threading.Thread(target=send,name=1)                
thread2=threading.Thread(target=recv,name=2)                

thread1.start()
thread2.start()
