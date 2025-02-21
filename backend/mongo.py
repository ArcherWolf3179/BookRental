from pymongo import MongoClient
from datetime import datetime

try:

    URL = "mongodb://localhost:27017/book"

    client = MongoClient(URL)
    db = client.get_database()

    allbooks = db["books"]
    rentedBooks = db["rentedBooks"]
    userDB = db["user"]
    onHold = db["OnHold"]

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
            print({specific_valuee : query})
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
            u.append(i)

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
            userInfo = {"email" : email,"username" : username, "ID" : userID," overdue ": False}
            userDB.insert_one(userInfo)
            print("Inserted user info")
            del(userInfo,u,userID)

    except Exception as e:
        print(f"There was an error function SIgn up: {e}")

def OnHold(bookID,title,userID):
    try:
        print("On hold function activated") 
        Isuser = onHold.find({"ID" : userID})# Ok so what we're doing here is we're looking at the onHold collection and checking to see if the user is there
        user = userDB.find({"ID" : userID})# this does the same thing but with the user collection

        b = []
        a = []
        for doc in Isuser:#goes through the results in Isuser and adding that to list a
            a.append(doc)

        print(a)

        for doc in user:#same thing here but is for user and goes to list b
            b.append(doc)

        print(b)

        # This is making sure list A is 0 because if a is zero then the user will not already have put anything on hold list
        # List b is making sure the user exists
        if len(a) == 0 and len(b) > 0:
            userOnHoldInfo = {"title" : title, "bookID" : bookID, "ID" : userID} # Just making this into a dictionary to insert into the onHold collection
            onHold.insert_one(userOnHoldInfo)
            del(userID)
            print("Insertion succesfull")
            return 1
        else:
            return 2

    except Exception as e:
        print(f"There was an error {e}")
        return 2
    
def Overdue(user):
    try:

        userID = read(userDB,{"username":user},"username",1)
        returnDate = read(rentedBooks,userID[0]['ID'],"ID",1)
        
        if returnDate[0]["ReturnDate"] < datetime.now():

            filter = {"ID" : userID[0]["ID"]}
            update = {"$set" : {"IsOverDue" : True}}

            userUpdate = {"$set" : {"overdue" : True}}

            result = rentedBooks.update_one(filter,update)
            userDB.update_one(filter,userUpdate)
            print(f"The result is {result}")

            title = read(rentedBooks,userID,'ID',1)

            return title
        
        else:
            return 0

    except Exception as e:
        print(f"There was an error this is the overdue function {e}")
Overdue("Avyukta Dinesh")
#Make On hold function
# bookID,title,authors,average_rating,isbn,isbn13,language_code, num_pages,ratings_count,text_reviews_count,publication_date,publisher