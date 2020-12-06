#import statements here
import time                                             
import os
import threading
from VLCFrames import *
from MACUnrap import *
from log_col import *
#time.sleep(3.5)
log.say("")
input("[Node] Ready? [PRESS RETURN]....")
device_address="1010"
device_PAN="00FF"
dat=[]
AssociateRQ="1"
AssociateRSP="2"
Diss="3"
dataRQ="4"
status="1"
down=u"\u2192"
up=u"\u2190"
i=1
device_type="0" #choose "1" if can act as coordinator

print("\nMARK 6")
log.special("\n[!]This is the NODE\n[!]Device Address : 1010\n")
time.sleep(1)
log.notify("[!]Program starts now\n")

def write(data):
    channel0=open("channel.txt","w")
    channel0.write(data)
    channel0.close()
    time.sleep(0.2)
    #open("channel.txt","w").close()

def look():
    channel1=open("channel.txt","r")                        
    data=channel1.read()
    channel1.close()
    time.sleep(0.2)
    return data
time_start=time.clock()
#send
def send():
    global i,status   
    while(True):
        #open("channel.txt","w").close()
        if(i==1):
            #send association request
            #print("cooking")
            data=FrameGenerator.AssociationRequest('1','1')
            write(data)
            log.warn("\n[{}]Sending ASSOCIATION Request.\n".format(up))
            i=10
        elif(i==2 and status=="0"):
            data=FrameGenerator.DataRequest()
            write(data)
            log.warn("\n[{}]Sending DATA Request.\n".format(up))
            i=10
        #elif(i==369):
        #    exit()
        else:
            data=""
        #time.sleep(1)
        #print("{}[SEND]:~ ".format(i),end="")
        #data=str(input())
        #time.sleep(0.2)
        #write(data)
        #print("Writting frame :>{}".format(data))
        #disassociate(below)
        if(data[1:]=='close'):                                         
            print("[*]Closing Channel :)")              
            channel0.close()                                    
            os.system('del channel.txt')                
            break
#receive
def recv():
    global i,status,dat
    d=""
    while(True):
        data=look()
        #print("::::::::::::::::",data)
        #open("channel.txt","w").close()
        if(len(data)):
            #decode the data here
            DestinationAddress = data[24:28]
            FrameType = data[0:3]
            #print("Checking address...")
            if(DestinationAddress==device_address):
                open("channel.txt",'w').close()
                if(FrameType=="011"): #command frame
                    cmdID,status=MACDecoder(str(data),0)
                    if(cmdID==AssociateRSP):
                        if(status=="0"):
                            log.notify("\n[{}]Received ASSOCIATION Response, Access granted.\n".format(down))
                            cmdID,status=MACDecoder(str(data),1)
                            i=2
                        else:
                            log.error("[!]Co-ordinator has rejected access\n")
                            cmdID,status=MACDecoder(str(data),1)
                            log.error("\n[!]CONNECTION CLOSED : due to rejection.\n")
                    if(cmdID==Diss):
                        log.notify("\n[{}]Received DISASSOCIATION Response\n".format(down))
                        cmdID,status=MACDecoder(str(data),1)
                        log.warn("[!]CLOSING CONENCTION!\n")
                        log.say("[*]Completed in {} seconds.".format(round((time.clock()-time_start),2)))
                        i=369
                        time.sleep(2)
                        input()
                elif(FrameType=="001"):
                    seqID,payload=MACDecoder(str(data),0)
                    log.notify("\n[{}]Received DATA frame.\n".format(down))
                    seqID,payload=MACDecoder(str(data),1)
                    #d=d+payload
                    #d=d.replace("0","")
                    payload=payload.replace("0","")
                    dat.append(payload)
                    #send ack
                    if(seqID=="00000000"):
                        log.special("\n[!]DATA RETRIEVED: {}\n".format("".join(dat[::-1])))
                    open("channel.txt",'w').close()
                    data=FrameGenerator.Acknowledgement(int(seqID,2))
                    write(data)
                    log.warn("\n[{}]Sending ACKNOWLEDGEMENT\n".format(up))

                    
            else:
                pass
                #print("Address do not match")
            #if association response received, then i+=1
            #if data frames received, then...
                    #check sequence number and send ack back
            #if dissassocation frame received then close channel
            if(data=='close'):                  
                print("Disconnecting Channel")
                break

#asociation and stuff like that(code here)
            
#multithreading commands
thread1=threading.Thread(target=send,name=3)                #activate send thread                 
thread2=threading.Thread(target=recv,name=4)                #activates receive thread

thread1.start()
thread2.start()
