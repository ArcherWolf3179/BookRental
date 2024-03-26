from backend import mongo
from flask import Flask, redirect, url_for, render_template

try:
    app = Flask(__name__)
    @app.route("/")

    def home():
        try:
            r = mongo.read(mongo.allbooks,"A Short","title")
            return render_template('index.html')
        
        except FileNotFoundError as e:
            print(f"The file wasn't found more info can be found here {e}")

        except Exception as e:
            print(f"There was an error: {e}")

    @app.route("/admin")

    def admin():
        return redirect(url_for("home"))

    if __name__ == "__main__":
        app.run()

except TypeError as e:
    print(f"There was a type error please check the {e} for the correct type")

except TimeoutError:
    print("Something timedout")

except Exception as e:
    print(f"There was an error {e}")