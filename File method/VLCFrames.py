from CRC import CRC16

class FrameGenerator:
    def SeqNum_D2B(SeqNum):
        return ('0'*(8-len(bin(SeqNum).replace("0b","")))+bin(SeqNum).replace("0b",""))
    
    def dataFrame(Payload,SeqNum):
        
        FrameControl        = [None]*16 # FrameControl is 2 octets in size
        
        #PREDEFINING THE FRAME CONTROL VALUES (FCS)
        FrameControl[:3]    = ['0','0','1']  #FRAME TYPE (001 - Data Frame)
        FrameControl[3]     = '0'  #SECURITY ENABLED (0 - No security features)
        FrameControl[4]     = '0'  #FRAME PENDING (Set to 0)
        FrameControl[5:7]   = ['0','1'] #ACK Request set to 1 #if we can implement
        FrameControl[7]     = '0' #PAN ID Compression set to 0
        FrameControl[8:10]  = ['0','0'] #Reserved Set to 0 (For future use)
        FrameControl[10:12] = ['1','0'] #Destination Addressing Mode (Contains 16bit address)
        FrameControl[12:14] = ['0','0'] #Frame Version
        FrameControl[14:]   = ['1','0'] #Source Addressing Mode (Contains 16bit address)

        #ADDRESSING FIELDS:
        DestinationAddress       =  ['1','0','1','0'] 
        DestinationPANIdentifier =  ['F','F','0','0'] 
        SourceAddress            =  ['0','1','0','1']
        SourcePANIdentifier      =  ['0','0','F','F']
        AddressingField          =  DestinationPANIdentifier + SourcePANIdentifier + DestinationAddress + SourceAddress 
        
        SeqNum=FrameGenerator.SeqNum_D2B(SeqNum)
        SequenceNumber = [i for i in SeqNum]  #The sequence number field has a length of 1 octet and specify the sequence number data. We used only for 1 client (user) then the sequence number is set to 0b0

        # AuxillarySecurityHeader is omiited as Security Enabled Field is 0 in FCS

        MACHeader = ''.join(FrameControl + AddressingField + SequenceNumber) 
        MHRMSDU   = MACHeader + Payload # Payload is of variable size
        MFR = str('%02x' %CRC16().calculate(MHRMSDU)) #CRC Calculation
        MFR = (4-len(MFR))*('0') + MFR

        MAC_DataFrame = MHRMSDU+MFR

        return MAC_DataFrame

    def AssociationRequest(DevType,AltPanCoord):

        FrameControl        = [None]*16 # FrameControl is 2 octets in size
        
        #PREDEFINING THE FRAME CONTROL VALUES (FCS)
        FrameControl[:3]    = ['0','1','1']  #FRAME TYPE (011 - Command Frame)
        FrameControl[3]     = '0'  #SECURITY ENABLED (0 - No security features)
        FrameControl[4]     = '0'  #FRAME PENDING (Set to 0)
        FrameControl[5:7]   = ['0','1'] #ACK Request set to 1 #if we can implement
        FrameControl[7]     = '0' #PAN ID Compression set to 0
        FrameControl[8:10]  = ['0','0'] #Reserved Set to 0 (For future use)
        FrameControl[10:12] = ['1','0'] #Destination Addressing Mode (Contains 16bit address)
        FrameControl[12:14] = ['0','0'] #Frame Version
        FrameControl[14:]   = ['1','0'] #Source Addressing Mode (Contains 16bit address)

        #ADDRESSING FIELDS:
        DestinationAddress       =  ['0','1','0','1']
        DestinationPANIdentifier =  ['F','F','0','0']
        SourceAddress            =  ['1','0','1','0']
        SourcePANIdentifier      =  ['0','0','F','F']
        AddressingField          =  DestinationPANIdentifier + SourcePANIdentifier + DestinationAddress + SourceAddress 

        # Sequence Number assumed to be 0 as we are not gonna split data into multiple frames
        MACHeader = ''.join(FrameControl + AddressingField) 

        CommandFrameIdentifier = '1' #For association request it is 1

        #CAPABILITY INFORMATION
        AlternatePANCoordinator = AltPanCoord # set to 1 if device can act as coordinator
        DeviceType = DevType #RFD Device - 0 FFD Device - 1
        PowerSource = '0'
        ReceiveronWhenIdle = '1' #Set to 1 to indicate that device does not disbale when idle
        BatteryInformation = '00' #Battery Status Unknown
        SecurityCapabilty  = '0' #Incapable of Security Feautures
        AllocateAddress    = '0' #Set to 0 as address need not to be allocated

        CapabilityInformation = AlternatePANCoordinator + DeviceType + PowerSource + ReceiveronWhenIdle + BatteryInformation + SecurityCapabilty + AllocateAddress
        
        AssociationRequestFrame_noFCS = MACHeader + CommandFrameIdentifier + CapabilityInformation
        MFR = str('%02x' %CRC16().calculate(AssociationRequestFrame_noFCS))
        MFR = (4-len(MFR))*('0') + MFR
        AssociationRequestFrame = AssociationRequestFrame_noFCS + MFR

        return AssociationRequestFrame

    def AssociationResponse(AssoStatus,ShrtAdd):

        FrameControl        = [None]*16 # FrameControl is 2 octets in size
        
        #PREDEFINING THE FRAME CONTROL VALUES (FCS)
        FrameControl[:3]    = ['0','1','1']  #FRAME TYPE (011 - Command Frame)
        FrameControl[3]     = '0'  #SECURITY ENABLED (0 - No security features)
        FrameControl[4]     = '0'  #FRAME PENDING (Set to 0)
        FrameControl[5:7]   = ['0','1'] #ACK Request set to 1 #if we can implement
        FrameControl[7]     = '0' #PAN ID Compression set to 0
        FrameControl[8:10]  = ['0','0'] #Reserved Set to 0 (For future use)
        FrameControl[10:12] = ['1','0'] #Destination Addressing Mode (Contains 16bit address)
        FrameControl[12:14] = ['0','0'] #Frame Version
        FrameControl[14:]   = ['1','0'] #Source Addressing Mode (Contains 16bit address)

        #ADDRESSING FIELDS:
        DestinationAddress       =  ['1','0','1','0']
        DestinationPANIdentifier =  ['F','F','0','0']
        SourceAddress            =  ['0','1','0','1']
        SourcePANIdentifier      =  ['0','0','F','F']
        AddressingField          =  DestinationPANIdentifier + SourcePANIdentifier + DestinationAddress + SourceAddress 

        MACHeader = ''.join(FrameControl + AddressingField)

        CommandFrameIdentifier = '2'

        ShortAddress =  ShrtAdd  # ['0','1','0','1']

        AssociationStatus = AssoStatus # '0' #Association Status set to 0 if it is successful

        AssociationResponseFrame_noFCS = MACHeader + CommandFrameIdentifier + ShortAddress + AssociationStatus
        MFR = str('%02x' %CRC16().calculate(AssociationResponseFrame_noFCS))  
        MFR = (4-len(MFR))*('0') + MFR
        AssociationResponseFrame = AssociationResponseFrame_noFCS + MFR

        return AssociationResponseFrame

    def DisassociationNotification(DisReason):

        FrameControl        = [None]*16 # FrameControl is 2 octets in size
        
        #PREDEFINING THE FRAME CONTROL VALUES (FCS)
        FrameControl[:3]    = ['0','1','1']  #FRAME TYPE (011 - Command Frame)
        FrameControl[3]     = '0'  #SECURITY ENABLED (0 - No security features)
        FrameControl[4]     = '0'  #FRAME PENDING (Set to 0)
        FrameControl[5:7]   = ['0','1'] #ACK Request set to 1 #if we can implement
        FrameControl[7]     = '0' #PAN ID Compression set to 0
        FrameControl[8:10]  = ['0','0'] #Reserved Set to 0 (For future use)
        FrameControl[10:12] = ['1','0'] #Destination Addressing Mode (Contains 16bit address)
        FrameControl[12:14] = ['0','0'] #Frame Version
        FrameControl[14:]   = ['1','0'] #Source Addressing Mode (Contains 16bit address)

        #ADDRESSING FIELDS:
        DestinationAddress       =  ['1','0','1','0']
        DestinationPANIdentifier =  ['F','F','0','0']
        SourceAddress            =  ['0','1','0','1']
        SourcePANIdentifier      =  ['0','0','F','F']
        AddressingField          =  DestinationPANIdentifier + SourcePANIdentifier + DestinationAddress + SourceAddress 

        MACHeader = ''.join(FrameControl + AddressingField)

        CommandFrameIdentifier = '3'

        DisassociationReason = DisReason

        DisassociationNotificationFrame_noFCS = MACHeader + CommandFrameIdentifier + DisassociationReason
        MFR = str('%02x' %CRC16().calculate(DisassociationNotificationFrame_noFCS))  
        MFR = (4-len(MFR))*('0') + MFR
        DisassociationNotificationFrame = DisassociationNotificationFrame_noFCS + MFR

        return DisassociationNotificationFrame

    def DataRequest():

        FrameControl        = [None]*16 # FrameControl is 2 octets in size
        
        #PREDEFINING THE FRAME CONTROL VALUES (FCS)
        FrameControl[:3]    = ['0','1','1']  #FRAME TYPE (011 - Command Frame)
        FrameControl[3]     = '0'  #SECURITY ENABLED (0 - No security features)
        FrameControl[4]     = '0'  #FRAME PENDING (Set to 0)
        FrameControl[5:7]   = ['0','1'] #ACK Request set to 1 #if we can implement
        FrameControl[7]     = '0' #PAN ID Compression set to 0
        FrameControl[8:10]  = ['0','0'] #Reserved Set to 0 (For future use)
        FrameControl[10:12] = ['1','0'] #Destination Addressing Mode (Contains 16bit address)
        FrameControl[12:14] = ['0','0'] #Frame Version
        FrameControl[14:]   = ['1','0'] #Source Addressing Mode (Contains 16bit address)

        #ADDRESSING FIELDS:
        DestinationAddress       =  ['0','1','0','1']
        DestinationPANIdentifier =  ['F','F','0','0']
        SourceAddress            =  ['1','0','1','0']
        SourcePANIdentifier      =  ['0','0','F','F']
        AddressingField          =  DestinationPANIdentifier + SourcePANIdentifier + DestinationAddress + SourceAddress 

        MACHeader = ''.join(FrameControl + AddressingField)

        CommandFrameIdentifier = '4'

        DataRequestFrame_noFCS = MACHeader + CommandFrameIdentifier
        MFR = str('%02x' %CRC16().calculate(DataRequestFrame_noFCS))  
        MFR = (4-len(MFR))*('0') + MFR
        DataRequestFrame = DataRequestFrame_noFCS + MFR

        return DataRequestFrame


    def Acknowledgement(SeqNum):

        FrameControl        = [None]*16 # FrameControl is 2 octets in size
        
        #PREDEFINING THE FRAME CONTROL VALUES (FCS)
        FrameControl[:3]    = ['0','1','0']  #FRAME TYPE (011 - Acknowledgement Frame)
        FrameControl[3]     = '0'  #SECURITY ENABLED (0 - No security features)
        FrameControl[4]     = '0'  #FRAME PENDING (Set to 0)
        FrameControl[5:7]   = ['0','0'] #ACK Request set to 1 #if we can implement (Here I set it to 1 as we dont need Ack for Ack)
        FrameControl[7]     = '0' #PAN ID Compression set to 0
        FrameControl[8:10]  = ['0','0'] #Reserved Set to 0 (For future use)
        FrameControl[10:12] = ['1','0'] #Destination Addressing Mode (Contains 16bit address)
        FrameControl[12:14] = ['0','0'] #Frame Version
        FrameControl[14:]   = ['1','0'] #Source Addressing Mode (Contains 16bit address)

        #ADDRESSING FIELDS:
        DestinationAddress       =  ['0','1','0','1']
        DestinationPANIdentifier =  ['F','F','0','0']
        SourceAddress            =  ['1','0','1','0']
        SourcePANIdentifier      =  ['0','0','F','F']
        AddressingField          =  DestinationPANIdentifier + SourcePANIdentifier + DestinationAddress + SourceAddress
        SeqNum=FrameGenerator.SeqNum_D2B(SeqNum)
        SequenceNumber = [i for i in SeqNum]

        MACHeader = ''.join(FrameControl + AddressingField + SequenceNumber)

        # Sequence Number = '0000000'  #The sequence number field has a length of 1 octet and specify the sequence number data. We used only for 1 client (user) then the sequence number is set to 0b0

        Acknowledgement_noFCS = MACHeader
        MFR = str('%02x' %CRC16().calculate(Acknowledgement_noFCS))  
        MFR = (4-len(MFR))*('0') + MFR
        AcknowledgementFrame = Acknowledgement_noFCS + MFR

        return AcknowledgementFrame
