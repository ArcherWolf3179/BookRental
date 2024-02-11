from pymongo import MongoClient

URL = "mongodb://localhost:27017/book"

def checkUrl(url):
    try:
        client = MongoClient(url)
        db = client.get_database()
        print("Connection successful!")
        client.close()
        return True
    except Exception as e:
        print("Connection failed:", e)
        return False