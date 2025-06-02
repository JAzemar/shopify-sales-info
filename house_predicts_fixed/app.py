From flask import flask, render_template

App = Flask(__name__)

@app.route('/')
Def home ():
    Return render_template("index.html")

If __name__ == '__main__':
     app.run()