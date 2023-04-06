from flask import Flask, render_template, request, flash
import pandas as pd
application = Flask(__name__)
application.secret_key = "password"

@application.route('/')
@application.route("/hello")
def index():
    flash("Please enter the names of 3 games separated by backslashes (\)")
    return render_template("index.html")
@application.route("/greet", methods=["POST", "GET"])
def greet():
    flash("Hi " + str(request.form['name_input']) +", great to see you!")
    return render_template("index.html")
