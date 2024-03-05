from backend import mongo
import flask

app = flask.Flask(__name__)
@app.route("/")

def home():
    r = mongo.read(mongo.allbooks,"A Short","title")
    return flask.render_template("index.html", context=r)

@app.route("/admin")

def admin():
    return flask.redirect(flask.url_for("home"))

if __name__ == "__main__":
    app.run()