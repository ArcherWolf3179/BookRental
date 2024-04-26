from backend import mongo
from flask import Flask, render_template, request

try:
    app = Flask(__name__)
    allbooks = mongo.allbooks
    rentedBookds = mongo.rentedBooks
    userDB = mongo.userDB
    @app.route("/")

    def home():
        return render_template('index.html')

    @app.route('/search',methods=['POST','GET'])

    def search():
        try:
            if request.method == 'POST':
                search_data = request.form['search_data']
                readResult = mongo.read(allbooks,search_data,"title")
                return render_template('result.html',content=readResult,specific_value="title")
        except KeyError as e:
            print(f"Key Error more info here: {e}")
        
    @app.route('/view_book/<bookID>',methods=['POST'])

    def book(bookID):
        try:
            if request.method =='POST':
                readResult = mongo.read(allbooks,bookID,"bookID")
                print(readResult) #According to this result we're being returned nothing
                return render_template('book.html',BookName=readResult)
        except Exception as e:
            print(f"There was an error{e}")

    if __name__ == "__main__":
        app.run(debug=True)

except TypeError as e:
    print(f"There was a type error please check the {e} for the correct type")

except TimeoutError:
    print("Something timedout")

except Exception as e:
    print(f"There was an error {e}")