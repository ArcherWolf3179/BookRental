from pymongo import MongoClient

URL = "mongodb://localhost:27017/book"

try:
    client = MongoClient(URL)
    db = client.get_database()
    print("Connection successful!")

except Exception as e:
    print("Connection failed:", e)
    
def read(collection,query):
    result = collection.find(query)
    for doc in result:
        print(doc)

mycollection = db["books"]
q = {"authors" : "Bill Bryson"}

read(mycollection,q)
