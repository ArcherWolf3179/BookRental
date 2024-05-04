from backend import mongo
from flask import Flask, render_template, request, session
import os

try:
    placeholderimg = r"C:\Users\avyuk\OneDrive\Pictures\Screenshots\placeholderimg"

    app = Flask(__name__)
    allbooks = mongo.allbooks
    rentedBookds = mongo.rentedBooks
    userDB = mongo.userDB
    @app.route('/')

    def home():
        return render_template('index.html')
    
    @app.route('/login', method=['POST'])

    def login():
        if request.method == 'POST':
            pass

    @app.route('/search',methods=['POST','GET'])

    def search():
        try:
            if request.method == 'POST':
                search_data = request.form['search_data']
                readResult = mongo.read(allbooks,search_data,"title",0)
                return render_template('result.html',content=readResult,specific_value="title")
        except KeyError as e:
            print(f"Key Error more info here: {e}")
        
    @app.route('/view_book/<bookID>',methods=['POST'])

    def book(bookID):
        try:
            if request.method =='POST':
                readResult = mongo.read(allbooks,int(bookID),"bookID",1)
                print(readResult) #According to this result we're being returned nothing

                if os.path.exists(placeholderimg):
                    placeholer = placeholderimg
                    print("Found")
                else:
                    print("nothing")
                    placeholer = None

                if readResult == None:
                    return "We couldn't find what you were looking for"
                else:
                    return render_template('book.html',BookName=readResult,placeholder = placeholer)
        except Exception as e:
            print(f"There was an error{e}")

    @app.route('/borrowBook/<bookID>', methods=['POST'])

    def borrowBook(bookID):
        try:
            if request.method == 'POST':
                rentResult = mongo.rent_A_Book(bookID,'bookID')

                if rentResult == 1:
                    return render_template('borrow.html',x="You succesfully borrowed your book")
                elif rentResult == 2:
                    return render_template('borrow.html',x="Someone has already borrowed your book")

        except Exception as e:
            print(f"There was an error {e}")

    if __name__ == "__main__":
        app.run(debug=True)

except TypeError as e:
    print(f"There was a type error please check the {e} for the correct type")

except TimeoutError:
    print("Something timedout")

except Exception as e:
    print(f"There was an error {e}")