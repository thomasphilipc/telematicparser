import datetime
import socket
import struct
import time
import teltonikaparser
import bceparser


from time import gmtime,strftime

fmt = "%Y-%m-%d %H:%M:%S"

TCP_IP = '192.168.168.11'
TCP_PORT = 6102
BUFFER_SIZE = 2048


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
print("server listening on port {} on machine with ip {}".format(TCP_PORT, TCP_IP))
while 1:
    s.listen(1)
    conn, addr = s.accept()
    print ('Connection address:', addr)
    print (conn)
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if data:

            print(data)
            print(data.hex())
            response = bceparser.process_data(data.decode("utf-8"))
            print(response)
            #handle ack response
            if response == 0:
                #packet = struct.pack('1B', 1)
                #print(packet)
                conn.send("packet recieved".encode())
            else:
                #packet = struct.pack('I',response)
                #print(response.to_bytes(4,byteorder="big"))
                #conn.send(response.to_bytes(4,byteorder="big"))
                conn.send("packet recieved".encode())
        else:
            conn.close()
            print("Connection closed")
            break
