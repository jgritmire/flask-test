#importing relevant packages
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

cover_art = pd.read_csv('./data/recommender_data/cover_art.csv')

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

        #reordering our cover art dataframe based on our recommendation list
        final_recs_image_paths = []
        for i in range(0, 10):
            final_recs_image_paths.append(\
                list(cover_art[cover_art['Name']==final_recs[i]]['ImagePath'])[0])


        # final_recs_image_paths = list(\
        #         cover_art.loc[cover_art['Name'].isin(final_recs[:10])==True]['ImagePath'])


        return([final_recs[:10], final_recs_image_paths])


@application.route('/')
@application.route("/hello")
def index():
    flash("Please enter the names of 3 games separated by foward slashes (/)")
    return render_template("index.html")

@application.route("/greet", methods=["POST", "GET"])
def greet():
    return render_template("index.html",
#game rec 1 and cover art 1
        game_1 = new_user_recommender(request.form['name_input'])[0][0],
        cover_art_1 = new_user_recommender(request.form['name_input'])[1][0],
#game rec 2 and cover art 2
        game_2 = new_user_recommender(request.form['name_input'])[0][1],
        cover_art_2 = new_user_recommender(request.form['name_input'])[1][1],
#game rec 3 and cover art 3
        game_3 = new_user_recommender(request.form['name_input'])[0][2],
        cover_art_3 = new_user_recommender(request.form['name_input'])[1][2],
#game rec 4 and cover art 4
        game_4 = new_user_recommender(request.form['name_input'])[0][3],
        cover_art_4 = new_user_recommender(request.form['name_input'])[1][3],
#game rec 5 and cover art 5
        game_5 = new_user_recommender(request.form['name_input'])[0][4],
        cover_art_5 = new_user_recommender(request.form['name_input'])[1][4],
#game rec 6 and cover art 6
        game_6 = new_user_recommender(request.form['name_input'])[0][5],
        cover_art_6 = new_user_recommender(request.form['name_input'])[1][5],
#game rec 7 and cover art 7
        game_7 = new_user_recommender(request.form['name_input'])[0][6],
        cover_art_7 = new_user_recommender(request.form['name_input'])[1][6],
#game rec 8 and cover art 8
        game_8 = new_user_recommender(request.form['name_input'])[0][7],
        cover_art_8 = new_user_recommender(request.form['name_input'])[1][7],
#game rec 9 and cover art 9
        game_9 = new_user_recommender(request.form['name_input'])[0][8],
        cover_art_9 = new_user_recommender(request.form['name_input'])[1][8],
#game rec 10 and cover art 10
        game_10 = new_user_recommender(request.form['name_input'])[0][9],
        cover_art_10 = new_user_recommender(request.form['name_input'])[1][9]
        )
