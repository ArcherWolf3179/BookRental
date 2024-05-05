from backend import mongo
from flask import Flask, render_template, request, session, url_for, redirect
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

    @app.route('/login', methods=['POST'])

    def login():
        return render_template('login.html')

    @app.route('/loggin', methods=['POST'])

    def loggin():
        if request.method == 'POST':
            user = request.form["user"]
            email = request.form["email"]

            mongo.SignUp({"email":email}, {"user":user})

            session["user"] = user

            return redirect(url_for("home"))

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
                    placeholder = placeholderimg
                    print("Found")
                else:
                    print("nothing")
                    placeholder = None

                if readResult == None:
                    return "We couldn't find what you were looking for"
                else:
                    return render_template('book.html',BookName=readResult,placeholder = placeholder)
        except Exception as e:
            print(f"There was an error{e}")

    @app.route('/borrowBook/<bookID>', methods=['POST'])

    def borrowBook(bookID):
        try:
            if request.method == 'POST':
                if "user" in session:
                    user = session["user"]
                    print(user)
                    rentResult = mongo.rent_A_Book(bookID,'bookID',{"ID",1})

                    if rentResult == 1:
                        return render_template('borrow.html',x="You succesfully borrowed your book")
                    elif rentResult == 2:
                        return render_template('borrow.html',x="Someone has already borrowed your book")

        except Exception as e:
            print(f"There was an errorr {e}")

    if __name__ == "__main__":
        app.secret_key = os.urandom(12).hex()
        app.run(debug=True)

except TypeError as e:
    print(f"There was a type error please check the {e} for the correct type")

except TimeoutError:
    print("Something timedout")

except Exception as e:
    print(f"There was an error {e}")