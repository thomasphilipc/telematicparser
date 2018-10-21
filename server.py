import datetime
import socket
import struct
import time
import teltonikaparser
import bceparser
import esp32
from pymongo import MongoClient
from pprint import pprint

from time import gmtime,strftime

fmt = "%Y-%m-%d %H:%M:%S"

TCP_IP = '192.168.168.11'
TCP_PORT1 = 6102
BUFFER_SIZE = 2048

myclient = MongoClient("mongodb+srv://admin:W1nd0ws87@cluster0-wkvwq.gcp.mongodb.net/test?retryWrites=true")
mydb = myclient["mydatabase"]
mycol = mydb["bce"]


s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((TCP_IP, TCP_PORT1))


print("server listening on port {} on machine with ip {}".format(TCP_PORT1, TCP_IP))
response=0
while 1:
    s1.listen(1)
    conn, addr = s1.accept()

    while 1:
        data = conn.recv(BUFFER_SIZE)
        if data:

            print(data)

            if data.hex()=="23424345230d0a":
                print("keyword recieved for BCE\n")
                response=None

            elif data.hex() =="0d0a":
                pass
            else:
                    print(data.hex())
                    value = bceparser.process_data(data.hex())
                    response = bceparser.process_ack(data.hex())
                    print(value)
                    insertdict= bceparser.create_dict_fromlist(value)
                    x=mycol.insert_one(insertdict)
                    print("Data inserted in mongodb")
                    print(x.inserted_id)
                    print(response)
                    print("packet send")
                    conn.send(response)
            data=""


        else:
            conn.close()
            print("Connection closed")
            break
