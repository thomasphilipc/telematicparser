import datetime
from struct import pack,unpack

from time import gmtime,strftime
from ctypes import *
fmt = "%Y-%m-%d %H:%M:%S"



mask1 = {'0':17,
         '1': 2,
         '2': 2,
         '3': 2,
         '4': 2,
         '5': 2,
         '6': 2,
         '7': 2,
         '8': 2,
         '9': 2,
         '10': 4,
         '11': 4,
         '12': 2,
         '13': 2,
         '14': 9,
         '15': 1,
         }
mask2 = {'0':2,
         '1': 2,
         '2': 2,
         '3': 2,
         '4': 2,
         '5': 2,
         '6': 2,
         '7': 2,
         '8': 2,
         '9': 2,
         '10': 4,
         '11': 4,
         '12': 2,
         '13': 2,
         '14': 9,
         '15': 1,
         }
# function POP_STRING
# description : the function here pops a string and returns the popped value and the string after pop
# input :  data (string) and the length (int )that has to be popped
# output :  popped value (string) and the data(string) after pop operation

def pop_string(data,length):
    popped = data[:length]
    data = data[length:]
    return popped,data




def convert(s):
    i = int(s, 16)                   # convert from hex to a Python int
    cp = pointer(c_int(i))           # make this into a c integer
    fp = cast(cp, POINTER(c_float))  # cast the int pointer to a float pointer
    return fp.contents.value         # dereference the pointer, get the float

# function reorder_hexstring
# description : the function reorders the string to have it in reverse byte order
# input :  value (string)
# output :  reversed value (string)
def reorder_hexstring(value):
    result= value.encode('utf-8')
    resultnew=[]
    for i in range(0,len(result),2):
        resultnew.append(result[-2:].decode('utf-8'))
        result=result[:-2]
    result=(''.join(resultnew))
    return result

# function parse_string
# description : the function does the logic to cover bytes into data
# input :  data (string) , lengthinbytes(int) , content (string) to do logic
# output :  data (string) , val (result) , content (what the content was)
def parse_string(data,lengthinbytes,content):
    length=2*lengthinbytes
    result,data=pop_string(data,length)
    if content == 'imei':
        result=reorder_hexstring(result)
        val=int(result, 16)
    elif content == 'len':
        result=reorder_hexstring(result)
        val=int(result,16)
    elif content == 'serviceid':
        val=int(result,16)
    elif content == 'confirmationkey':
        val=int(result,16)
    elif content == 'structurelength':
        val=int(result,16)
    elif content == 'checksum':
        val=int(result,16)
    elif content == 'data_time':
        result=reorder_hexstring(result)
        result=result[:-1]
        print(int(result,16))
        val=(int(result,16))*2
        print((int('47798280',16)))
        val=val+(int('47798280',16))
        epochtime =val
        t = datetime.datetime.fromtimestamp(epochtime)
        line=("Epoch is {} Timestamp is  {}".format(epochtime,t.strftime(fmt))) # prints 2012-08-28 02:45:17
        #print(line)
        val=line
    elif content == 'data_mask1':
        result=reorder_hexstring(result)
        print(result.zfill(16))
        val="{0:b}".format(int(result,16))
        print(val)
        val=val[-1:]
    elif content == 'data_mask2':
        result=reorder_hexstring(result)
        print(result)
        val="{0:b}".format(int(result,16))
        print(val.zfill(16))
        val=val[-1:]
    elif content == 'data_coord':

        print(result)
        print("longitude")
        print(convert(reorder_hexstring(result[:8])))
        print("latitude")
        print(convert(reorder_hexstring(result[8:16])))
        print("speed")
        print(result[16:18])
        print("Hdop")
        print(int(result[18])*5)
        print("satellites")
        print(int(result[19])*1)
        print("Course")
        print(int(result[20:22],16))
        print("altitude")
        print(int(reorder_hexstring(result[22:26]),16))
        print("odoemeter")
        print(result[26:])
        val=result
    elif content == 'data_di':
        print(result)
        val="{0:b}".format(int(result,16))
        print(val)
        for i in range(0,16):
            print("IN{} = {}".format(i+1,val[i]))
    else:
        val = result
    print(val)
    ret = (data,val,content)
    return ret



# function parse_string
# description : the function does the logic to cover bytes into data
# input :  data (string)
# output :  result (list)
def parsed_data(data):
    print("in parsed data")

    parsed=process_data(data)
    print(parsed)
    return parsed

def process_data(data):
    print("In process data")
    print(data)
    result = []
    print("IMEI")
    data,val,content=parse_string(data,8,'imei')
    result.append("{} is {} ".format(content,val))
    print(data)
    print("Length")
    data,val,content=parse_string(data,2,'len')
    result.append("{} is {} ".format(content,val))
    print(data)
    print("ServiceID")
    data,val,content=parse_string(data,1,'serviceid')
    result.append("{} is {} ".format(content,val))
    print(data)
    print("CONFIRMATION KEY")
    data,val,content=parse_string(data,1,'confirmationkey')
    result.append("{} is {} ".format(content,val))
    print(data)
    print("STRUCTURE LENGTH")
    data,val,content=parse_string(data,1,'structurelength')
    result.append("{} is {} ".format(content,val))
    data_length=val
    print(data)
    print("Data Time")
    data,val,content=parse_string(data,4,'data_time')
    result.append("{} is {} ".format(content,val))
    print(data)
    print("Data Mask 1")
    data,val,content=parse_string(data,2,'data_mask1')
    result.append("{} is {} ".format(content,val))
    print(data)
    print("Data Mask 2")
    data,val,content=parse_string(data,2,'data_mask2')
    result.append("{} is {} ".format(content,val))
    print(data)
    print("Data Co ordinates")
    data,val,content=parse_string(data,17,'data_coord')
    result.append("{} is {} ".format(content,val))
    print(data)
    print("Data Digital Inputs")
    data,val,content=parse_string(data,2,'data_di')
    result.append("{} is {} ".format(content,val))
    print(data)
    print("Data")
    data,val,content=parse_string(data,data_length-33,'data')
    result.append("{} is {} ".format(content,val))
    print(data)
    print("Check Sum")
    data,val,content=parse_string(data,1,'checksum')
    result.append("{} is {} ".format(content,val))

    return result

if __name__ == '__main__':
    # print_a() is only executed when the module is run directly.
    parsed_data("B00848D9044101002300A5E420A7B7E354038048000F7CAB419BF827420027590E010000000080000710506C01A1")
