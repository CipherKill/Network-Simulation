from CRC import CRC16
import os
from log_col import *
os.system("color e")
def MACDecoder(MACFrame,cond):

    FrameType = MACFrame[0:3]
    frame_len = len(MACFrame)
    FCS = MACFrame[frame_len-4:frame_len]
    MHRMSDU_Recv = MACFrame[:frame_len-4]
    FCS_RECV = str('%02x' %CRC16().calculate(MHRMSDU_Recv))
    FCS_RECV = (4-len(FCS_RECV))*('0') + FCS_RECV
    if FCS == FCS_RECV:
        pass
        #print("Valid Frame Recieved")
    else:
        log.error("[!]Bad Frame, Frame Discarded")
        return 0

    if FrameType == '001':

        sequenceNumber = MACFrame[32:40]
        SourceAddress = MACFrame[28:32]
        SourcePANIdentifier = MACFrame[28:32]
        DestinationPANIdentifier = MACFrame[24:28]#32:36 before: 24:28
        DestinationAddress = MACFrame[24:28]#24:28
        Payload = MACFrame[40:frame_len-4]
        #print("DATA FRAME RECIEVED ---------------------------------------------")
        #print("Source Address :", SourceAddress)
        #print("Source PAN Identifier :", SourcePANIdentifier)
        #print("Sequence Number :",sequenceNumber)
        if(cond==1):
            log.say("PAYLOAD : {}".format(Payload))
        return sequenceNumber,Payload

    elif FrameType == '011':

        commandFrameIdentifier = MACFrame[32:33]

        if commandFrameIdentifier == '1':
            #print("ASSOCIATION REQUEST FRAME RECIEVED ---------------------------------------------")
            SourceAddress = MACFrame[28:32]
            SourcePANIdentifier = MACFrame[20:24]
            DestinationPANIdentifier = MACFrame[16:20]
            DestinationAddress = MACFrame[24:28]

            AlternatePANCoordinator = MACFrame[33:34]
            DeviceType = MACFrame[34:35]
            PowerSource = MACFrame[35:36]
            ReceiveronWhenIdle = MACFrame[36:37]
            BatteryInformation = MACFrame[37:39]
            SecurityCapabilty  = MACFrame[39:40]
            AllocateAddress    = MACFrame[40:41]
            #print("Source Address :", SourceAddress)
            #print("Source PAN Identifier :", SourcePANIdentifier)
            if(cond==1):
                if AlternatePANCoordinator=='0':
                    log.special("[!]Source Device as no ability to become coordinator")
                else:
                    log.special("[!]Source Device can act as a coordinator")

                if DeviceType == '0':
                    log.special("[!]DEVICE TYPE : Reduced Functionality Device")
                else:
                    log.special("[!]DEVICE TYPE : Fully Functional Device")

            #print("Allocation of Address - DISABLED")
            return commandFrameIdentifier

        if commandFrameIdentifier == '2':
            #print("ASSOCIATION RESPONSE FRAME RECIEVED ---------------------------------------------")
            SourceAddress = MACFrame[28:32]
            SourcePANIdentifier = MACFrame[20:24]
            DestinationPANIdentifier = MACFrame[16:20]
            DestinationAddress = MACFrame[24:28]

            ShortAddress = MACFrame[33:37]

            AssociationStatus = MACFrame[37:38]

            #print("Source Address :", SourceAddress)
            #print("Source PAN Identifier :", SourcePANIdentifier)
            #print("Short Address :", ShortAddress)
            if(cond==1):
                if AssociationStatus=='0':
                    log.special("[#]Association Successful")
                    return commandFrameIdentifier,AssociationStatus
                else:
                    log.error("[#]Association unsuccessful")
            return commandFrameIdentifier,AssociationStatus

        if commandFrameIdentifier == '3':
            #print("DISASSOCIATION NOTIFICATION FRAME RECIEVED ---------------------------------------------")
            SourceAddress = MACFrame[28:32]
            SourcePANIdentifier = MACFrame[20:24]  
            DestinationPANIdentifier = MACFrame[16:20]
            DestinationAddress = MACFrame[24:28]      
            DisassociationReason = MACFrame[33:34]
            
            #print("Source Address :", SourceAddress)
            #print("Source PAN Identifier :", SourcePANIdentifier)
            if(cond==1):
                print("[!]Dissassociation Reason : Co-ordinator wishes to leave the PAN")
            return commandFrameIdentifier,DisassociationReason
        
        if commandFrameIdentifier == '4':
            #print("DATA REQUEST FRAME RECIEVED -----------------------------------------------------------")
            SourceAddress = MACFrame[28:32]
            SourcePANIdentifier = MACFrame[20:24] 
            DestinationPANIdentifier = MACFrame[16:20]
            DestinationAddress = MACFrame[24:28]
            return commandFrameIdentifier

    elif FrameType=='010':
        #print("ACKNOWLEDGEMENT FRAME RECIEVED ---------------------------------------------")
        
        sequenceNumber = MACFrame[32:40]
        SourceAddress = MACFrame[28:32]
        SourcePANIdentifier = MACFrame[28:32]
        DestinationPANIdentifier = MACFrame[24:28]#32:36 before: 24:28
        DestinationAddress = MACFrame[24:28]

        #print("Source Address :", SourceAddress)
        #print("Source PAN Identifier :", SourcePANIdentifier)  
        #print("Sequence Number :",sequenceNumber)   
        return sequenceNumber
