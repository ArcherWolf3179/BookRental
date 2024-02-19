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
            print(f" {specific_valuee.capitalize()} : {specific_value}")


    except Exception as e:
         print(f"There was an error: {e}")

def rent_A_Book(rentedBooksCollection,newDoc):
    try:

        result = rentedBooksCollection.find(newDoc)

        if result:
            print("Book is already rented")
        else:
            insert_result = rentedBooksCollection.insert_one(newDoc)
            print(f"Inserted doc ID: {insert_result}")
    except Exception as e:
        print(f"There was an error {e}")

# bookID,title,authors,average_rating,isbn,isbn13,language_code,  num_pages,ratings_count,text_reviews_count,publication_date,publisher

try:
    allbooks = db["books"]
    rentedBooks = db["rentedBooks"]
    userDB = db["user"]
    q = {"title" : "A Short History of Nearly Everything"}
    new_Docs = {"title" : "A Short History of Nearly Everything", "author" : "Bill Bryson"}

    read(allbooks,q,"title")
    rent_A_Book(rentedBooks,new_Docs)

    client.close()
except Exception as e:
     print(f"There was an error {e}")
