from backend import mongo
from flask import Flask, render_template, request, session, url_for, redirect
import os
from datetime import timedelta

try:
    placeholderimg = r"C:\Users\avyuk\OneDrive\Pictures\Screenshots\placeholderimg"

    app = Flask(__name__)
    allbooks = mongo.allbooks
    rentedBookds = mongo.rentedBooks
    userDB = mongo.userDB

    app.secret_key = os.urandom(12).hex()
    app.permanent_session_lifetime = timedelta(days=30)

    @app.route('/')

    def home():
        if "user" in session:
            user = session['user']
            return render_template('index.html',x=user)
        else:
            return render_template('index.html',x="Log in")
    
    @app.route('/back')

    def back():
        return redirect(url_for('home'))

    @app.route('/login', methods=['POST'])

    def login():
        if "user" in session:
            return "Your already logged in"
        else:
            return render_template('login.html')

    @app.route('/loggin', methods=['POST'])

    def loggin():
        if request.method == 'POST':
            session.permanent = True
            user = request.form["user"]
            email = request.form["email"]

            mongo.SignUp({"email":email}, {"username":user})
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
            print(f"There was an error {e} book function")

    @app.route('/borrowBook/<bookID>', methods=['POST'])

    def borrowBook(bookID):
        try:
            if request.method == 'POST':
                if "user" in session:
                    user = session["user"]
                    userId = mongo.read(userDB,{"username":user},"username",1)
                    bookTitle = mongo.read(allbooks,int(bookID),"bookID",1)
                    #print(f"This is the book title {bookTitle}")
                    rentResult = mongo.rent_A_Book({"bookID":bookID,"title":bookTitle[0]["title"],"ID": userId[0]["ID"]})

                    print(f"This is the rent result {rentResult}")

                    if rentResult == 1:
                        print("Rent result is 1")
                        return render_template('borrow.html',x="You have succesfully borrowed this book")
                    elif rentResult == 2:
                        print("rent result is 2")
                        return render_template('borrow.html',x="It seems someone else has borrowed this book")
                    else:
                        return "none"
                    
            else:
                return redirect(url_for('login'))

        except Exception as e:
           print(f"There was an errorr {e} borrow book function")

    @app.route('/hold')

    def hold():
        pass

    if __name__ == "__main__":
        app.run(debug=True)

except TypeError as e:
    print(f"There was a type error please check the {e} for the correct type")

except TimeoutError:
    print("Something timedout")

except Exception as e:
    print(f"There was an error {e} main.py")