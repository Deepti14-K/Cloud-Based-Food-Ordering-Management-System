from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<h1>Visit the /menu route to view the items and availability in real time</h1>"

@app.route('/menu')
def menu():
    return render_template('index.html')

app.run(threaded=True,host='0.0.0.0')
