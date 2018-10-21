import socket
import binascii

TCP_IP = '80.227.131.54'
TCP_PORT = 6102
BUFFER_SIZE = 1024
MESSAGE1 = "#BCE#\r\n"
MESSAGE2 = bytes.fromhex('d11fa1e3fb1603003c02a5823897bf56a28bc0008040800400fda65c42efcac841001800400000000000308400000610a8010275108b3000410000000000000000000000003857c356a28bc0008040800400fda65c42efcac84100180040000000000030840000f60fa8010275108b3000420000000000000000000000003817c756a28bc0008040800400fda65c42efcac84100180040000000000030840000e60fa8010275108b30004300000000000000000000000038d7ca56a28bc0008040800400fda65c42efcac84100190040000000000030840000f10fa8010275108b30004200000000000000000000000038d7cc56a28bc0008040800400fda65c42efcac84100180040000000000020800000e60fa8010275108630003f0000000000000000000000003887d456a28bc00080408004000ba75c42e3c9c841001b00fbff0000000020800000d40fa8010275108b30003f0000000000000000000000003807ee56a28bc0008040800400f4a65c4230cac841002a000f000000000020800000ac0fa8010275108630003c00000000000000000000000038570757a28bc000804080040004a75c420bcac84100190001000000000020800000920fa8010275108b30003f00000000000000000000000038e72057a28bc0008040800400fea65c4219cac841001c0003000000000020800000700fa8010275108630004100000000000000000000000038473a57a28bc000804080040005a75c4210cac841001c0005000000000020800000490fa8010275108b30003f000000000000000000000000ab')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
a=MESSAGE1.encode('utf-8')
print(a)
print(MESSAGE2)
s.send(a)
s.send(MESSAGE2)
data = s.recv(BUFFER_SIZE)
if (data):
    print ("received data:", data)
s.close()

