from flask import Flask, render_template, request, flash
import pandas as pd
import numpy as np
import fuzzyset
application = Flask(__name__)
application.secret_key = "password"

product = pd.read_csv('./data/recommender_data/product_based_recommender_df.csv'
                     ).set_index('Name')
review = pd.read_csv('./data/recommender_data/review_based_recommender_df.csv'
                    ).set_index('Name')
game_names = fuzzyset.FuzzySet(list(product.columns))
def intersection(list1, list2):
    return [item for item in list1 if item in list2]

def new_user_recommender(user_input):
    if len(user_input.split('/')) != 3:
        return 'ERROR PLEASE TRY AGAIN'
    else:
        liked_games = []
        liked_games.append(game_names.get(user_input.split('/')[0])[0][1])
        liked_games.append(game_names.get(user_input.split('/')[1])[0][1])
        liked_games.append(game_names.get(user_input.split('/')[2])[0][1])

        review_recs_1 = list(review[liked_games[0]])
        review_recs_2 = list(review[liked_games[1]])
        review_recs_3 = list(review[liked_games[2]])

        product_recs_1 = list(product[liked_games[0]])
        product_recs_2 = list(product[liked_games[1]])
        product_recs_3 = list(product[liked_games[2]])

        in_both_1 = intersection(review_recs_1, product_recs_1)
        in_both_2 = intersection(review_recs_2, product_recs_2)
        in_both_3 = intersection(review_recs_3, product_recs_3)

        final_recs = []
        for i in range(0, 10):
            if in_both_1[i] not in final_recs:
                if in_both_1[i] not in liked_games:
                    final_recs.append(in_both_1[i])
            if in_both_2[i] not in final_recs:
                if in_both_2[i] not in liked_games:
                    final_recs.append(in_both_2[i])
            if in_both_3[i] not in final_recs:
                if in_both_3[i] not in liked_games:
                    final_recs.append(in_both_3[i])

        return("My recommendations for you based on " +str(liked_games)+ \
        " are:" + str(final_recs[:10]))


@application.route('/')
@application.route("/hello")
def index():
    flash("Please enter the names of 3 games separated by backslashes (\)")
    return render_template("index.html")

@application.route("/greet", methods=["POST", "GET"])
def greet():
    flash(new_user_recommender(str(request.form['name_input'])))
    return render_template("index.html")
