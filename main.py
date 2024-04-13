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
            titleResult = mongo.read(allbooks,search_data,"title",1)

            return render_template('result.html',content=titleResult)
        
    @app.route("/book",methods=['POST'])

    def book():
        pass

    if __name__ == "__main__":
        app.run(debug=True)

except TypeError as e:
    print(f"There was a type error please check the {e} for the correct type")

except TimeoutError:
    print("Something timedout")

except Exception as e:
    print(f"There was an error {e}")