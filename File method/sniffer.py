from CRC import CRC16
import os
#os.system("mode con cols=100 lines=25")
os.system("color b")

def MACDecoder(MACFrame):

    FrameType = MACFrame[0:3]
    frame_len = len(MACFrame)
    FCS = MACFrame[frame_len-4:frame_len]
    MHRMSDU_Recv = MACFrame[:frame_len-4]
    FCS_RECV = str('%02x' %CRC16().calculate(MHRMSDU_Recv))
    FCS_RECV = (4-len(FCS_RECV))*('0') + FCS_RECV
    if FCS == FCS_RECV:
        print("Valid Frame Recieved")
    else:
        #print("[!]Bad Frame, Frame Discarded")
        return 0

    if FrameType == '001':

        sequenceNumber = MACFrame[32:40]
        SourceAddress = MACFrame[28:32]
        SourcePANIdentifier = MACFrame[28:32]
        DestinationPANIdentifier = MACFrame[24:28]#32:36 before: 24:28
        DestinationAddress = MACFrame[24:28]#24:28
        Payload = MACFrame[40:frame_len-4]
        print("\n\nDATA FRAME RECIEVED ---------------------------------------------")
        print("Source Address :", SourceAddress)
        print("Destination Adddress :", DestinationAddress)
        #print("Source PAN Identifier :", SourcePANIdentifier)
        print("Sequence Number :",sequenceNumber)
        print("-----------------------------------------------------------------")
        print("PAYLOAD : {}".format(Payload))
        print("-----------------------------------------------------------------\n\n")
        

    elif FrameType == '011':

        commandFrameIdentifier = MACFrame[32:33]

        if commandFrameIdentifier == '1':
            print("\n\nASSOCIATION REQUEST FRAME RECIEVED ---------------------------------------------")
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
            print("Source Address :", SourceAddress)
            print("Destination Adddress :", DestinationAddress)
            
            #print("Source PAN Identifier :", SourcePANIdentifier)
            if AlternatePANCoordinator=='0':
                print("[!]Source Device as no ability to become coordinator")
            else:
                print("[!]Source Device can act as a coordinator")

            if DeviceType == '0':
                print("[!]DEVICE TYPE : Reduced Functionality Device")
            else:
                print("[!]DEVICE TYPE : Fully Functional Device")

            #print("Allocation of Address - DISABLED")
            print("--------------------------------------------------------------------------------\n\n")

        if commandFrameIdentifier == '2':
            print("\n\nASSOCIATION RESPONSE FRAME RECIEVED ---------------------------------------------")
            SourceAddress = MACFrame[28:32]
            SourcePANIdentifier = MACFrame[20:24]
            DestinationPANIdentifier = MACFrame[16:20]
            DestinationAddress = MACFrame[24:28]

            ShortAddress = MACFrame[33:37]

            AssociationStatus = MACFrame[37:38]

            print("Source Address :", SourceAddress)
            print("Destination Adddress :", DestinationAddress)
            #print("Source PAN Identifier :", SourcePANIdentifier)
            #print("Short Address :", ShortAddress)
            if AssociationStatus=='0':
                print("[#]Association Successful")
            else:
                print("[#]Association unsuccessful")
            print("----------------------------------------------------------------------------------\n\n")

        if commandFrameIdentifier == '3':
            print("\n\nDISASSOCIATION NOTIFICATION FRAME RECIEVED ---------------------------------------------")
            SourceAddress = MACFrame[28:32]
            SourcePANIdentifier = MACFrame[20:24]  
            DestinationPANIdentifier = MACFrame[16:20]
            DestinationAddress = MACFrame[24:28]      
            DisassociationReason = MACFrame[33:34]
            
            print("Source Address :", SourceAddress)
            print("Destination Adddress :", DestinationAddress)
            #print("Source PAN Identifier :", SourcePANIdentifier)
            print("[!]Dissassociation Reason : Co-ordinator wishes to leave the PAN")
            print("----------------------------------------------------------------------------------\n\n")
            return 1
        if commandFrameIdentifier == '4':
            print("\n\nDATA REQUEST FRAME RECIEVED -----------------------------------------------------------")
            SourceAddress = MACFrame[28:32]
            SourcePANIdentifier = MACFrame[20:24] 
            DestinationPANIdentifier = MACFrame[16:20]
            DestinationAddress = MACFrame[24:28]
            print("Source Address :", SourceAddress)
            print("Destination Adddress :", DestinationAddress)
            print("----------------------------------------------------------------------------------\n\n")
    elif FrameType=='010':
        print("\n\nACKNOWLEDGEMENT FRAME RECIEVED ---------------------------------------------")
        
        sequenceNumber = MACFrame[32:40]
        SourceAddress = MACFrame[28:32]
        SourcePANIdentifier = MACFrame[28:32]
        DestinationPANIdentifier = MACFrame[24:28]#32:36 before: 24:28
        DestinationAddress = MACFrame[24:28]
        print("Source Address :", SourceAddress)
        print("Destination Adddress :", DestinationAddress)
        #print("Source Address :", SourceAddress)
        #print("Source PAN Identifier :", SourcePANIdentifier)  
        #print("Sequence Number :",sequenceNumber)   
        print("----------------------------------------------------------------------------------\n\n")
input("Sniffer Ready? [PRESS RETURN]...")
cache="0x0000"
while(True):
    f=open("channel.txt","r")
    data=f.read()
    if(data==cache):
        continue
    print("Scan results....")
    cache=data
    flag=0
    flag=MACDecoder(data)
    if(flag==1):
        print("[!]Transmission has ended...")
        break
input("Program has ended....[RETURN TO CLOSE]")
