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

    @app.route('/search',methods=['POST'])

    def search():
        if request.method == 'POST':
            search_data = request.form['search_data']
            readResult = mongo.read(allbooks,search_data,"title")
            return render_template('result.html',content=readResult)

    @app.route("/book",methods=['POST'])

    def goToBook():
        print(request.method)
        if request.method == 'POST':
            book_data = request.form.get('book_data')
            title = mongo.read(allbooks,book_data,"title")
            print(book_data)
            return render_template('book.html',BookName=title)

    if __name__ == "__main__":
        app.run(debug=True)

except TypeError as e:
    print(f"There was a type error please check the {e} for the correct type")

except TimeoutError:
    print("Something timedout")

except Exception as e:
    print(f"There was an error {e}")