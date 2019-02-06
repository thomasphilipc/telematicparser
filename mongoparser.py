from pymongo import MongoClient
import bceparser


client = MongoClient()
client = MongoClient("mongodb+srv://admin:W1nd0ws87@cluster0-wkvwq.gcp.mongodb.net/test?retryWrites=true")
mydb = client["mydatabase"]
myclient = MongoClient("mongodb+srv://admin:W1nd0ws87@cluster0-wkvwq.gcp.mongodb.net/test?retryWrites=true")
mydb = myclient["mydatabase"]
mycol = mydb["bceparsedall"]

raw =mydb["bceraw"]

with client:

    docs = client.mydatabase.bceraw.find()
    print(client.mydatabase.bceraw.count_documents({}))

    for doc in docs:
        if doc:
            try:
                print (" Raw data : {}".format(doc['0']))
                print("Length of Raw data : {}".format(len(doc['0'])))
                value= []
                value.append(doc['0'])
                value1 = bceparser.process_data(doc['0'])
                value.append(value1)
                print(value)
                insertdict= bceparser.create_dict_fromlist(value)
                x=mycol.insert_one(insertdict)
                print("Data inserted in mongodb")
                print(x.inserted_id)
            except:
                print("Error")
        else:
            print("Dont know")

