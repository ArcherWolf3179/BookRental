from pymongo import MongoClient
import random
#from bson import ObjectId

try:

    URL = "mongodb://localhost:27017/book"

    client = MongoClient(URL)
    db = client.get_database()
    print("Connection successful!")

    allbooks = db["books"]
    rentedBooks = db["rentedBooks"]
    userDB = db["user"]

    #SignUp(userDB,"afkldafdsf@gmail.com","123-456-7890")

except Exception as e:
    print(f"There was an error {e}")

def read(collection,query, specific_valuee):
    try:
        a = []
        result = collection.find({'title':{'$regex':f'^{query}'}})
        for doc in result:
            a.append(doc[specific_valuee])
        
        return a

    except Exception as e:
        print(f"There was an error: {e}")

def rent_A_Book(newDoc,specificvalue):
    try:
        result = rentedBooks.find({specificvalue : newDoc})
        findUser = userDB.find({"ID" : 1})
        findBook = allbooks.find({specificvalue : newDoc})

        if findBook:
            print("Book is already rented")

        elif result:
            print("We don't have your book")

        else:
            
            if findUser:
                insert_result = rentedBooks.insert_one({specificvalue : newDoc,"ID" : 1})
                print(f"Inserted doc ID: {insert_result}")
            else:
                print("You need to sign up")

    except Exception as e:
        print(f"There was an error {e}")

def return_Book(query):
    try:
        rentedBooks.delete_one(query)
    except Exception as e:
        print(f"There was an error: {e}")

def SignUp(email,number):
    try:
        e = userDB.find({"email":email}) 
        n = userDB.find({"number" : number})

        if n == True or e == True:
            print("You've already signed up here before with this email or number")
        else:
            userID = 1
            userInfo = {"email":email,"number" : number, "ID" : userID}
            userDB.insert_one({"email":email,"number" : number, "ID" : userID})
            print("Inserted user info")
            del(userInfo,e,n,userID)

    except Exception as e:
        print(f"There was an error function SIgn up: {e}")

# bookID,title,authors,average_rating,isbn,isbn13,language_code,  num_pages,ratings_count,text_reviews_count,publication_date,publisher