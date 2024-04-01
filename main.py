from backend import mongo
from flask import Flask, redirect, url_for, render_template, request

try:
    app = Flask(__name__)
    allbooks = mongo.allbooks
    rentedBookds = mongo.rentedBooks
    userDB = mongo.userDB
    @app.route("/")

    def home():
        try:
            r = mongo.read(allbooks,"A Short","title")
            return render_template('index.html')
        
        except FileNotFoundError as e:
            print(f"The file wasn't found more info can be found here {e}")

        except Exception as e:
            print(f"There was an error: {e}")

    @app.route('/search',methods=['POST'])

    def search():
        search_data = request.form['search_data']

        readResult = mongo.read(allbooks,search_data,"title")
        print(readResult)

        return render_template('result.html',content=readResult)

    @app.route("/admin")

    def admin():
        return redirect(url_for("home"))

    @app.route("/book",methods=['GET'])

    def goToBook():
        nameData = request.form['book']
        title = mongo.read(allbooks,nameData,"title")
        return render_template('book.html',BookName=nameData,bookTitle=title)

    if __name__ == "__main__":
        app.run(debug=True)

except TypeError as e:
    print(f"There was a type error please check the {e} for the correct type")

except TimeoutError:
    print("Something timedout")

except Exception as e:
    print(f"There was an error {e}")