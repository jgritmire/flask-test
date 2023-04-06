from flask import Flask
import pandas as pd
application = Flask(__name__)

@application.route('/')
def hello_world():
    df = pd.read_csv('./data/recommender_data/product_based_recommender_df.csv')
    return str(df.head())
