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
    onHold = db["OnHold"]

    #SignUp(userDB,"afkldafdsf@gmail.com","123-456-7890")

except Exception as e:
    print(f"There was an error {e} mongo.py")

def read(collection,query, specific_valuee,searchMethod):
    try:

        if searchMethod == 0:
            a = []
            result = collection.find({f'{specific_valuee}':{'$regex':f'^{query}'}})

            for doc in result:
                a.append(doc)
                
            return a
            
        elif searchMethod == 1:
            a = []
            result = collection.find({specific_valuee : query})
            for doc in result:
                a.append(doc)
            return a

    except Exception as e:
        print(f"There was an error: {e} read")

def rent_A_Book(query):
    try:
        result = read(rentedBooks,query["bookID"],"bookID",1)
        findUser = read(userDB,query['ID'],"ID",1)
            
        a = []
        u = []

        for doc in result:
            a.append(doc)

        for i in findUser:
            u.append(u)

        if len(a) > 0:
            return 2 #This means that the book was already rented

        if len(u) > 0:
            insert_result = rentedBooks.insert_one(query)
            print(f"Inserted doc ID: {insert_result}")
            return 1
        else:
            print("You need to sign up")
            return 3

    except Exception as e:
        print(f"There was an error {e} rentedBook function")

def return_Book(query):
    try:
        rentedBooks.delete_one(query)
    except Exception as e:
        print(f"There was an error: {e} return book function")

def SignUp(email,username):
    try:
        u = userDB.find({"username" : username})

        a = []

        for doc in u:
            a.append(doc)

        if len(a) >0:
            print("You've already signed up here before with this email or number")
        else:
            userID = 1
            userInfo = {"email" : email,"username" : username, "ID" : userID}
            userDB.insert_one(userInfo)
            print("Inserted user info")
            del(userInfo,u,userID)

    except Exception as e:
        print(f"There was an error function SIgn up: {e}")

def OnHold():
    try:
        pass
    except Exception as e:
        print(f"There was an error {e}")

#Make On hold function
# bookID,title,authors,average_rating,isbn,isbn13,language_code,  num_pages,ratings_count,text_reviews_count,publication_date,publisher