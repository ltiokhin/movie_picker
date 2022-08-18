
#import modules
import pandas as pd
import numpy as np

#load csv file
df_movies = pd.read_csv("movies.csv")

#define movie selection function
def get_me_a_movie():

    # tracker to keep track of whether there was a valid movie recommendation
    error_tracker = 0

    while error_tracker < 4:
        try:
            #extract the column names, which tells the user all the features that they can use to search the movie
            col_names = list(df_movies.columns)
            #tells the user the attributes that they can use to select a movie
            print(f"You can select a movie based on the following attributes:\n{col_names}")

            ## begin user input section ##

            #for those inputs that should be numbers, have the user continue to enter input until the input can be converted to an integer
            while True:
                try:
                    max_length_minutes = int(input("What's the maximum amount of minutes that you want to spend watching this movie? Please enter only a number."))
                    min_year = int(input("What's the oldest possible year of the movie that you want to watch?"))
                    max_year = int(input("What's the most recent possible year of the movie that you want to watch?"))
                    min_rating = int(input("What's the minimum IMDB rating that you'd be willing to watch? (Enter a number between 0 and 10)"))
                    break
                except ValueError:
                    print("Your input wasn't number :/ Please try again ...")

            #remove nas from each genre and store non-na values in new objects. Combine these objects together and store the unique values in the unique_genres object
            #this then produces a numpy array of unique genres
            genre1_clean = df_movies['genre1'][~df_movies['genre1'].isna()]
            genre2_clean = df_movies['genre2'][~df_movies['genre2'].isna()]
            genre3_clean = df_movies['genre3'][~df_movies['genre3'].isna()]
            unique_genres = pd.concat([genre1_clean, genre2_clean, genre3_clean], axis=0).unique()

            # do the same thing, but for the unique languages
            unique_languages = df_movies['language']
            unique_languages = unique_languages[~unique_languages.isna()].unique() #check where values are not nan and return only non-null values, then filter for unique values

            # have the user input their preferences for genres and languages. If doesn't provide input that matches the possible options for genre and language, then throw an error and have them try again
            while True:
                try:
                    print(f"You can pick from the following movie genres:\n{unique_genres}") # print the values on a new line (\n)
                    genre = str(input("What is your preferred genre for this movie? (please enter one of the above genres exactly as written above)")).lower()
                    print(f"You can pick from the following movie languages:\n{unique_languages}") # print the values on a new line (\n)
                    language = str(input("What is your preferred language for this movie? (please enter one of the above languages exactly as they are written)")).lower()
                    #check if they entered a genre and language that is in the list of available ones. If so, break out of the while loop. If not, go back to start.
                    if (genre in unique_genres) and (language in unique_languages):
                        break
                    else:
                        print("You either didn't enter a proper genre or language. Please try again :)\n")
                except:
                    print("There was an unknown error in your input of genres and languages. Please try again :)\n")
                    error_tracker += 1

            ## end user input section ##

            #filter the original data frame based on all the conditions specified by the user
            #makes sure the variables are integers or strings, as appropriate
            df_movies_usersubset = df_movies[(df_movies['length_minutes'] < int(max_length_minutes)) &
                                         (df_movies['year_released'] > int(min_year)) &
                                         (df_movies['year_released'] < int(max_year)) &
                                         (df_movies['rating_imdb'] > int(min_rating)) &
                                         (df_movies['language'] == str(language))]

            #also filter by genre, then drop duplicate rows
            df_movies_usersubset = df_movies_usersubset[(df_movies_usersubset['genre1'] == str(genre)) |
                                             (df_movies_usersubset['genre2'] == str(genre)) |
                                             (df_movies_usersubset['genre3'] == str(genre))].drop_duplicates()

            #if there is no movie that fits this criteria, tell this to the user.
            #otherwise randomly sample a movie from the subset of movies that fits the user's preferences and return this movie
            if len(df_movies_usersubset) > 0:
                with pd.option_context("display.max_columns", None): #show all of the columns in the data frame
                    print(f"Here is your movie :) \n {df_movies_usersubset.sample()}")

                #ask user if they are happy with the movie
                happy = input("Are you happy with this movie? Enter 'yes' or 'no' without parentheses")

                #check if they entered something that, when converted to lower case, starts with "ye".
                #Upsides is that it covers any case input + words like "yep". Downside is that it also covers "yellow, yesterday" and so on...
                if happy.lower().startswith("ye"):
                    break
                else:
                    print("OK — let's pick another movie for you!")
                    with pd.option_context("display.max_columns", None):  # show all of the columns in the data frame
                        print(f"Here is your second option :) \n {df_movies_usersubset.sample()}") #can potentially sample the same movie
                    break
            else:
                print("There are no movies that fit your criteria :/ \nTry again\n")
                #adds 1 to the error tracker
                error_tracker += 1
        except:
            print("There was an error somewhere and we're not sure what it is. \n"
                  "Could you please try again, and check your input carefully? \n" 
                  "P.S. I'm sorry for this uninformative error message :////// \n")
            error_tracker += 1

#Now get me a movie!
get_me_a_movie()


