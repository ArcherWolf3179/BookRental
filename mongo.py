"""def create(collection): #Trying to add to the collection rentedBooks
    try:
        new_doc = frozenset({'_id': ObjectId('65bc50930a2f3c9a1827dd79'), 
                'bookID': 21, 'title': 'A Short History of Nearly Everything',
                'authors': 'Bill Bryson',
                'average_rating': 4.21,
                'isbn': '076790818X',
                'isbn13': 9780767908184,
                'language_code': 'eng',
                '  num_pages': 544,
                'ratings_count': 248558,
                'text_reviews_count': 9396,
                'publication_date': '9/14/2004',
                'publisher': 'Broadway Books'})
        insert_result = collection.insert_one({new_doc})
        print(f"Inserted document ID: {insert_result.inserted_id}")
    except Exception as e:
         print(f"There was an error: {e}")"""

from pymongo import MongoClient
#from bson import ObjectId

URL = "mongodb://localhost:27017/book"

try:
    client = MongoClient(URL)
    db = client.get_database()
    print("Connection successful!")

except Exception as e:
        print("Connection failed:", e)
    
def read(collection,query,specific_valuee):
    try:
        result = collection.find(query)
        for doc in result:
             specific_value = doc[specific_valuee]

        if type(specific_valuee) == str:

            print(f"{specific_valuee.capitalize()} : {specific_value}")

    except Exception as e:
         print(f"There was an error: {e}")

# bookID,title,authors,average_rating,isbn,isbn13,language_code,  num_pages,ratings_count,text_reviews_count,publication_date,publisher

try:
    allbooks = db["books"]
    rentedBooks = db["rentedBooks"]
    q = {"title" : "A Short History of Nearly Everything"}

    read(allbooks,q,"title")

    client.close()
except Exception as e:
     print(f"There was an error {e}")