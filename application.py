#importing relevant packages
from flask import Flask, render_template, request, flash
import pandas as pd
import numpy as np
import fuzzyset

#instantiating the application
application = Flask(__name__)
application.secret_key = "password"

#reading in the relevant dataframes
product = pd.read_csv('./data/recommender_data/product_based_recommender_df.csv'
                     ).set_index('Name')
review = pd.read_csv('./data/recommender_data/review_based_recommender_df.csv'
                    ).set_index('Name')
cover_art = pd.read_csv('./data/recommender_data/cover_art.csv')
#creating a set of board game names for fuzzy matching the user input
game_names = fuzzyset.FuzzySet(list(product.columns))

#creating a function that retuns the intersection of two lists
def intersection(list1, list2):
    return [item for item in list1 if item in list2]
#creating a function for partial matching
def partial_match(subs):
    game_names = [item.lower() for item in list(product.columns)]
    partials = [i for i in game_names if subs in i]
    partials = [i.title() for i in partials]
    return partials

#defining the function that will return our board game recs
def new_user_recommender(user_input):
#confirming that the user has enetered 3 game titles correctly
    if len(user_input.split('/')) != 3:
        return 'ERROR PLEASE TRY AGAIN'
    else:
#creating a blank list to add the user inputs to
        liked_games = []
#splitting the list and adding each title to the liked games list
        liked_games.append(game_names.get(user_input.split('/')[0])[0][1])
        liked_games.append(game_names.get(user_input.split('/')[1])[0][1])
        liked_games.append(game_names.get(user_input.split('/')[2])[0][1])

#getting the list of game recs based on review score similarites for each title
        review_recs_1 = list(review[liked_games[0]])
        review_recs_2 = list(review[liked_games[1]])
        review_recs_3 = list(review[liked_games[2]])

#getting the list of game recs based on product similarity for each title
        product_recs_1 = list(product[liked_games[0]])
        product_recs_2 = list(product[liked_games[1]])
        product_recs_3 = list(product[liked_games[2]])

#we want games that similar users like, but also that have similar mechanics
#as such, we will get the intersection of the review recs and product recs
        in_both_1 = intersection(review_recs_1, product_recs_1)
        in_both_2 = intersection(review_recs_2, product_recs_2)
        in_both_3 = intersection(review_recs_3, product_recs_3)

#creating an empty list for our final recs
        final_recs = []
#checking that we have enough recs for product 1
        if len(in_both_1) < 4:
            in_both_1=in_both_1 + product_recs_1
#checking that we have enough recs for product 2
        if len(in_both_2) < 4:
            in_both_2=in_both_2 + product_recs_2
#checking that we have enough recs for product 3
        if len(in_both_3) < 4:
            in_both_3=in_both_3 + product_recs_3
#getting a list of 10 final recs, adding one rec at a time based on each of the
#3 games the user initially input
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

#returning the final rec list, and the associated cover art for each game
        return([final_recs[:10], final_recs_image_paths])

#setting up the flask app to return the appropriate information based on user input
@application.route('/')
# @application.route("/greet")
def index():
    # flash("Please enter the names of 3 games separated by foward slashes (/)")
    return render_template("index.html")

@application.route("/greet", methods=["POST", "GET"])
def greet():
    try:
        return render_template("index2.html",
        games_fuzzy_1 = game_names.get(request.form['name_input'].split('/')[0])[0][1],
        games_fuzzy_2 = game_names.get(request.form['name_input'].split('/')[1])[0][1],
        games_fuzzy_3 = game_names.get(request.form['name_input'].split('/')[2])[0][1],

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
    except:
        return render_template("error.html",
        wrong_game_name = request.form['name_input'],
        wrong_game_suggestions = partial_match(request.form['name_input'])
        )
