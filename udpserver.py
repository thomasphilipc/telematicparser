import logging
import socket
import struct
from time import gmtime, strftime



# not required - was used to send an ack to calamp by building the ack packet
def send_ack(param):

    mobileid,seqno,mtype,lmu = param
    print(mobileid)
    print("seqno")
    print(seqno)
    s = struct.pack('>H', seqno)
    seqnob1,seqnob2= struct.unpack('>BB', s)
    print("mtype")
    print(mtype)
    mobileid1 = int(mobileid[:2],16)
    mobileid2 = int(mobileid[2:4],16)
    mobileid3 = int(mobileid[4:6],16)
    mobileid4 = int(mobileid[6:8],16)
    mobileid5 = int(mobileid[8:],16)
    PACKETDATA = struct.pack('19B', 131, 5, mobileid1,mobileid2,mobileid3,mobileid4,mobileid5,1,1,2,1,seqnob1,seqnob2,mtype,0,0,0,0,0)
    #PACKETDATA = '83 05 01 02 03 04 05 01 01 02 01 00 01 00 00 00 00 00 00'
    print(PACKETDATA.hex())
    print("sending ack to {}".format(lmu))
    host=lmu
    port=20510
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((host,port))
    s.send(PACKETDATA)


    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))


#functions to assist in parsing.
def pop_string(data,length):
    popped = data[:length]
    return popped

def parse_string(data,length,content):
    result=pop_string(str(data),length)
    val = result
    new_data = data[length:]
    ret1 = (new_data,val)
    return ret1

# actual parser
def process_data(data):

    data= str(data.hex())
    if (len(data)>10):
        data,value = parse_string(data,2,"Options Byte")
        print("optionsByte {}".format(value))
        data,value = parse_string(data,2,"Mobile ID Field Length")
        print("MobileID field length {}".format(value))
        data,mobileid = parse_string(data,10,"Mobile ID")
        print("Mobile ID {}".format(value))
        data,value = parse_string(data,2,"Mobile ID Type Length")
        print("Mobile IT type {}".format(value))
        data,value = parse_string(data,2,"Mobile ID Type")
        print("Mobile ID type {}".format(value))
        data,value = parse_string(data,2,"Service Type")
        print("Service Type {}".format(value))
        data,msgtype = parse_string(data,2,"Message Type")
        print("Message TYpe {}".format(msgtype))
        data,seqno = parse_string(data,4,"Sequence Number")
        print("SequenceNum {}".format(seqno))
        print(data)

        if (msgtype == '02'):
            ret= 0
        else:
            print("No ack will be send")
            ret=1

        retval =(ret,mobileid,seqno,msgtype)

        return retval


# put the ip and socket below
host='192.168.168.11'
port=9220
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
while True:
    (data, addr) = s.recvfrom(128*1024)
    lmu=addr[0]
    print(addr[0])
    # actual data in hex printed below
    print(data.hex())
    # calling the parser to process the data
    retval = process_data(data)
    ret, esn, seqno, msgtype = retval
    if (ret == 0):
        print("Sending ack")
        # should be obtin
        mobileid = str(esn)
        param = (mobileid, int(seqno), int(msgtype), lmu)
        print( "Mobile id {} | Sequence {} | mtype {} | lmu {}".format(mobileid, seqno, msgtype, lmu))
        # calling function to build ack
        send_ack(param)


