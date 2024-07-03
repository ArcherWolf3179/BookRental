# NOTE the read function will make the query and specfic value into a dictionary for
# NOTE for the read function's search method parameter 0 is for with the regex and 1 is for without
# NOTE the rent function doesn't put the query into a dictionary for you, so you have to do it yourself
from backend import mongo
from flask import Flask, render_template, request, session, url_for, redirect
import os
from datetime import timedelta, datetime

try:
    placeholderimg = r"C:\Users\avyuk\OneDrive\Pictures\Screenshots\placeholderimg"

    app = Flask(__name__)
    allbooks = mongo.allbooks
    rentedBookds = mongo.rentedBooks
    userDB = mongo.userDB
    onhold = mongo.onHold

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

    def login():# NOTE this is where the login page is generated
        if "user" in session:
            user = session["user"] 
            userId = mongo.read(userDB,{"username":user},"username",1)
            rented = mongo.read(rentedBookds,userId[0]["ID"],"ID",1)
            # TODO have to fix bug
            onHold = mongo.read(onhold,userId[0]["ID"],"ID",1)
            overDue = mongo.Overdue(session['user'])

            if overDue == 0:
                return render_template('profile.html',name=user, content=rented,Hold=onHold,overDue=0)
            else:
                return render_template('profile.html',name=user, content=rented,Hold=onHold,overDue=overDue)
        else:
            return render_template('login.html')

    @app.route('/loggin', methods=['POST'])

    def loggin(): # NOTE this is the login function that actually puts your account details in
        if request.method == 'POST':
            session['user'] = request.form["user"]
            email = request.form["email"]

            mongo.SignUp({"email":email}, {"username":session['user']})

            session.permanent = True

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

                    today = datetime.now()
                    Plus = timedelta(days=30)
                    returnDate = today + Plus

                    rentResult = mongo.rent_A_Book({"bookID":bookID,"title":bookTitle[0]["title"],"author":bookTitle[0]['authors'],"ID": userId[0]["ID"], "BorrowedDate" : datetime.now(), "ReturnDate" : returnDate, "IsOverDue" : False})

                    print(f"This is the rent result {rentResult}")

                    if rentResult == 1:
                        print("Rent result is 1")
                        return render_template('borrow.html',x="You have succesfully borrowed this book")
                    elif rentResult == 2:
                        print("rent result is 2")
                        return render_template('borrow.html',x="It seems someone else has borrowed this book",bookID=bookID)
                    else:
                        return "none"
                    
            else:
                return redirect(url_for('login'))

        except Exception as e:
           print(f"There was an errorr {e} borrow book function")

    @app.route('/hold/<bookID>', methods=['POST'])

    def hold(bookID):
        try:
            if request.method == 'POST':
                if "user" in session:
                    user = session["user"]
                    bookTitle = mongo.read(allbooks,int(bookID),"bookID",1)
                    userId = mongo.read(userDB,{"username":user},"username",1)
                    onHold = mongo.OnHold(bookID,bookTitle[0]["title"],userId[0]["ID"])

                    print(onHold)
                    if onHold == 1:
                        return redirect(url_for("home"))
                    elif onHold == 2:
                        return render_template("borrow.html", x="Something went wrong with the hold")

        except Exception as e:
            print(f"There was an error here is more info {e}")

    if __name__ == "__main__":
        app.run(debug=True)

except TypeError as e:
    print(f"There was a type error please check the {e} for the correct type")

except TimeoutError:
    print("Something timedout")

except Exception as e:
    print(f"There was an error {e} main.py")