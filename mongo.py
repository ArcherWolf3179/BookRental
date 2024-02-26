from pymongo import MongoClient
import random
#from bson import ObjectId

URL = "mongodb://localhost:27017/book"

try:
    client = MongoClient(URL)
    db = client.get_database()
    print("Connection successful!")

except Exception as e:
    print("Connection failed:", e)
    
def read(allbookscollection,query,specific_valuee):
    try:
        specific_value = None
        result = allbookscollection.find(query)
        for doc in result:
            specific_value = doc.get(specific_valuee)

        if type(specific_valuee) == str:
            print(f" {specific_valuee.capitalize()} : {specific_value}")
            return specific_value, True

    except Exception as e:
         print(f"There was an error read function: {e}")

def rent_A_Book(rentedBooksCollection,newDoc,userEmail,userDB,specificvalue):
    try:
        result = rentedBooksCollection.find({specificvalue : newDoc})
        findUser = userDB.find({"email" :userEmail})

        if result == False:
            print("Book is already rented")
            return False,1
        else:
            insert_result = rentedBooksCollection.insert_one({specificvalue : newDoc,"email" : userEmail})
            print(f"Inserted doc ID: {insert_result}")

    except Exception as e:
        print(f"There was an error {e}")

def return_Book(rentedbooksCollection,query):
    try:
        rentedbooksCollection.delete_one(query)
    except Exception as e:
        print(f"There was an error: {e}")

def generate_UserID(userCollection):
    try:
        
        num1 = random.randint(0,9)
        num2 = random.randint(0,9)
        num3 = random.randint(0,9)
        num4 = random.randint(0,9)
        num5 = random.randint(0,9)
        num6 = random.randint(0,9)

        numbers = [num1,num2,num3,num4,num5,num6]

        ud = [str(num) for num in numbers]

        userID = ud[0] + ud[1] + ud[2] + ud[3] + ud[4] + ud[5]

        #findUserID = userCollection.find({"ID": userID})

        return userID
    except Exception as e:
        print(f"There was an error {e}")

def SignUp(userCollection,email,number):
    try:
        e = userCollection.find({"email":email}) 
        n = userCollection.find({"number" : number})

        if n == True or e == True:
            print("You've already signed up here before with this email or number")
        else:
            userID = generate_UserID(userCollection)
            userInfo = {"email":email,"number" : number, "ID" : userID}
            userCollection.insert_one({"email":email,"number" : number, "ID" : userID})
            print("Inserted user info")
            del(userInfo,e,n,userID)

    except Exception as e:
        print(f"There was an error function SIgn up: {e}")

# bookID,title,authors,average_rating,isbn,isbn13,language_code,  num_pages,ratings_count,text_reviews_count,publication_date,publisher

try:
    allbooks = db["books"]
    rentedBooks = db["rentedBooks"]
    userDB = db["user"]

    e = rent_A_Book(rentedBooks,"A Short History of Nearly Everything","adkflafkdsf@gmail.com",userDB,"title")

    client.close()
except Exception as e:
    print(f"There was an error {e}")