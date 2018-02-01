# scrape for user profile
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import numpy as np
#import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
#from sklearn.neighbors import KNeighborsClassifier
from sqlalchemy import create_engine
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier

# def user_ratings(username):
#     ratings_count = 0
#     user_ratings = []
#     avail_results = True 
#     while avail_results:
#         # assemble the url, make the request, isolate table
#         url = f"https://www.beeradvocate.com/user/beers/?start={ratings_count}&ba={username}&order=dateD&view=R"
#         html = requests.get(url)
#         print(html.url)
#         soup = BeautifulSoup(html.text, 'html.parser')
        
#         # get the ratings table on the page
#         table = soup.find('table')
#         # get the ratings by row
#         ratings_list = table.find_all('tr')[3:]
        
#         # generate profile table if first go
#         if ratings_count == 0:
#              # grab user info table
#             profile_table = soup.find("div", class_ = "pairsJustified")
    
#             # data-points
#             dls = profile_table.find_all('dl')
    
#             #  dictionary holding user stats
#             profile_dict = {"user_name" : username}
    
#             # loop through table items and make dictionary keys and values
#             for dl in dls:
#                 profile_dict[dl.find('dt').text] = dl.find('dd').text
            
#             # list for top 3
#             top_3 = []

#             #beer_links = []
#             for x in range(3):
#                 text_info = ratings_list[x].find_all('a')
#                 num_info = ratings_list[x].find_all('td')[-3:-1]
#                 base_url_ba = "https://www.beeradvocate.com"
#                 beer_link = base_url_ba + text_info[0]['href'][0:text_info[0]['href'].find("?")]
#                 #beer_links.append(beer_link)
#                 top_3_dict = {"Beer Name": text_info[0].text,
#                              "Brewery": text_info[1].text,
#                              "Beer Style": text_info[2].text,
#                              "ABV": num_info[0].text,
#                              "User Rating": num_info[1].text,
#                              "beer_link": beer_link}
#                 top_3.append(top_3_dict)

            
#         #increase ratings count to get next page
#         ratings_count += 50
        
        
        
#         #####need catch for no user ratings
#         if len(ratings_list) > 0:
        
#             #loop through and sort info
            
#             for tr in ratings_list:
#                 tds = tr.find_all('td')

#                 # isolate some info
#                 user_rating = tds[-2].text
# #                 abv = tds[-3].text
#                 rDev = re.findall(r"([\d.]*\d+)", tds[-1].text)[0]
#                 # further isolate element in list holding 3 features
#                 add_beer_info = tds[2].find_all('a')
                
#                 # extract info
# #                 beer_name = add_beer_info[0].text
#                 beer_link_total = add_beer_info[0]['href']
#                 base_url_ba = "https://www.beeradvocate.com"
#                 beer_link = base_url_ba + beer_link_total[0:beer_link_total.find("?")]
# #                 beer_style = add_beer_info[2].text
# #                 brewery = add_beer_info[1].text

#                 #dump into dict
#                 ratings_dict = {
# #                     "beer_name": beer_name,
# #                     "brewery": brewery,
# #                     "beer_style": beer_style,
# #                     "beer_style_match": re.sub(r'\W+', '', beer_style.lower()),
#                     "beer_link": beer_link,
#                     "user_rating": user_rating,
# #                     "abv": abv,
#                     "rDev": rDev

#                 }

#                 # append link to list
#                 user_ratings.append(ratings_dict)
#         else: 
            
#             avail_results = False
            
#     user_ratings_df = pd.DataFrame(user_ratings).drop_duplicates()
    
#     for beer in top_3:
#         response = requests.get(beer['beer_link'])
#         soup = BeautifulSoup(response.text, 'html.parser')
#         beerimages = soup.find('div', {'id': 'main_pic_norm'}).find_all('img')
#         beerlink = beerimages[0]['src']
#         if (beerlink is not None):
#             beer['image_link'] = beerlink
#         else:
#             beer['image_link'] = ""
    
#     return profile_dict, top_3, user_ratings_df

# def match_styles(username):
#     #create df of user ratings
#     profile_dict, top_3, user_ratings_df = user_ratings(username)
#     print(len(user_ratings_df))

# #   # creates two data frames, one for user_ratings, the other for possible recommendations
#     engine = create_engine('postgresql://hgzhyrxbjgjnwa:3fe5e38aa493b4337c39b464fee4a6e71b1e4d33b57a60d50cbe0deaf6ff3e50@ec2-50-16-202-213.compute-1.amazonaws.com:5432/dacosp3h3fd1ng')
#     beer_features_df = pd.read_sql("SELECT * FROM beer.beer_feature_all",con=engine)
#     user_ratings_df = user_ratings_df.merge(beer_features_df, left_on = 'beer_link', right_on = 'URL', how = "right")
#     rec_df = user_ratings_df[user_ratings_df['beer_link'].isnull()]
#     user_df = user_ratings_df[user_ratings_df['beer_link'].notnull()]
#     user_df['user_rating'] = pd.to_numeric(user_df['user_rating'], errors = "coerce")
#     user_df.sort_values('user_rating', ascending = False, inplace=True)
#     print(f"Number of user matches to our DB: {len(user_df)}")
#     print(f"Number of possible recomendations {len(rec_df)}")
    
    
#     # decision making for 1 and 0
#     # return top 5% for user
#     user_df['yesno'] = ""
#     user_df['yesno'][0:int(len(user_df)*.05)] = 1
#     user_df['yesno'][int(len(user_df)*.05):] = 0
#     user_df['yesno'].astype('int', inplace=True)
    
#     #check cutoff score
#     cut_off = user_df.iloc[int(len(user_df)*.05) - 1]['Score']
#     if cut_off <= 3.75:
#         print(f"{username} has low scoring beers classfied as yesses")
#         bins = [0, 3.49999999, 6] # I know there is no 6, just to be safe
#         labels = [0, 1]
#         userdf['yesno'] = pd.cut(user_df['user_rating'], bins, labels = labels)
    
#     #check count of yesses
# #     yes_count = list(user_df['yesno']).count(1)
# #     if yes_count < 5:
#         # return the top rated beers of each type, 
#         # maybe find top two rated for user and recommend those types?
    
#     return profile_dict, top_3, user_df, rec_df

# def random_forest(username):
#     profile_dict, top_3, user_df, recs_df = match_styles(username)
#     X_columns = ["Score", "Flavor", "ABV","Hoppiness","Maltiness","Fruitiness","Body", "pDev",
#           "Sweetness","Sour","spicy","bitter", 'Aroma_None', 'Aroma_caramel',
#        'Aroma_floral', 'Aroma_fruit', 'Custom Flavor_None',
#        'Custom Flavor_banana', 'Custom Flavor_brown sugar',
#        'Custom Flavor_burnt', 'Custom Flavor_caramel',
#        'Custom Flavor_chocolate', 'Custom Flavor_earthy',
#        'Custom Flavor_herbal', 'Custom Flavor_pumpkin',
#        'Custom Flavor_roasted', 'Custom Flavor_smoke', 'Custom Flavor_toasted',
#        'Custom Flavor_wheat', 'Color_amber', 'Color_black', 'Color_dark ',
#        'Color_gold', 'Color_pale']
    
#     X = user_df[X_columns]
#     target = user_df['yesno'].astype('int')
    
#     X_train, X_test, y_train, y_test = train_test_split(X, target, random_state = 42)
    
#     # build model and score
#     rf = RandomForestClassifier(n_estimators=200)
#     rf = rf.fit(X_train, y_train)
#     score = rf.score(X_test, y_test)
    
#     # % correct predicts on user set
#     predictions = rf.predict(X)
#     actual = user_df['yesno'].astype('int')
#     df = pd.DataFrame({"Predict": predictions, "actual": actual})
#     df['test'] = (df['Predict'] == df['actual'])
#     num_correct = list(df['test']).count(True)
#     perc_correct = num_correct/len(user_df)
    
#     #print results
#     print(f"Random forest Score: {score}")
#     print(f"Random forest % correct: {perc_correct}")
    
#     #make predictions/recommendations
#     recsX = recs_df[X_columns]
#     recommendations = rf.predict(recsX)
#     num_recs = list(recommendations).count(1)
    
#     recs_df['recommend'] = recommendations
    
#     recommended_df = recs_df[(recs_df['recommend'] == 1) & (recs_df['Availaility'] != 'Limited(brewedonce)')]
#     recommended_df.drop_duplicates(['Name', "Brewer"], inplace = True)
#     recommended_df.sort_values('Score', ascending = False, inplace=True)
    
#     info_columns = ["Name", "Brewer", "Location", "Style", "BrosScore", "Score", 
#                     'ABV', 'Availaility', "Ranking", "num_ratings", "ScoreClass", "ImageLink", "URL"]
    
#     recommended_yearround = recommended_df[recommended_df['Availaility'] == "Year-round"]
#     recommended_other = recommended_df[recommended_df['Availaility'] != "Year-round"]
    
#     def findrecs(df, num):
#         for x in range(1,11):
#             recs = df.groupby('Style')[info_columns].head(x)

#             if len(recs) < num:
#                 continue

#             if len(recs) >= num:
#                 recs = recs.iloc[0:num]
#                 break
            
#         return recs
    
#     top_yearround = findrecs(recommended_yearround, 6)
#     top_other = findrecs(recommended_other, 4)
    
#     frames = [top_yearround, top_other]
#     top_recs = pd.concat(frames, ignore_index = True)
    
#     top_recs.sort_values(['Score', 'Ranking'], inplace = True, ascending = False)
    
#     recs_dict = top_recs.to_dict(orient = 'records')
    
#     API_dict = {
#         "userProfile": profile_dict,
#         "top3UserBeers": top_3,
#         "recommendations": recs_dict,
#         "R2Score": score,
#         "percCorrect": perc_correct
#     }

#     return API_dict

# function for ratings scrape

def user_ratings(username):
    ratings_count = 0
    user_ratings = []
    avail_results = True 
    while avail_results:
        # assemble the url, make the request, isolate table
        url = f"https://www.beeradvocate.com/user/beers/?start={ratings_count}&ba={username}&order=dateD&view=R"
        html = requests.get(url)
        print(html.url)
        soup = BeautifulSoup(html.text, 'html.parser')
        
        # get the ratings table on the page
        table = soup.find('table')
        # get the ratings by row
        if table:
            ratings_list = table.find_all('tr')[3:]
        else: 
            ratings_list = []
        
        # generate profile table if first go
        if ratings_count == 0:
             # grab user info table
            profile_table = soup.find("div", class_ = "pairsJustified")
    
            # data-points
            dls = profile_table.find_all('dl')
    
            #  dictionary holding user stats
            profile_dict = {"user_name" : username}
    
            # loop through table items and make dictionary keys and values
            for dl in dls:
                profile_dict[dl.find('dt').text] = dl.find('dd').text
            
            # list for top 3
            top_3 = []

            # isolate first 3 or less for rop 3 beers from profile
            if len(ratings_list) >=3:
                top_ratings = ratings_list[0:3]
                #beer_links = []
            else: 
                top_ratings = ratings_list[0:len(ratings_list)]
            
            for x in range(len(top_ratings)):
                text_info = top_ratings[x].find_all('a')
                num_info = top_ratings[x].find_all('td')[-3:-1]
                base_url_ba = "https://www.beeradvocate.com"
                beer_link = base_url_ba + text_info[0]['href'][0:text_info[0]['href'].find("?")]
                #beer_links.append(beer_link)
                top_3_dict = {"Beer Name": text_info[0].text,
                             "Brewery": text_info[1].text,
                             "Beer Style": text_info[2].text,
                             "ABV": num_info[0].text,
                             "User Rating": num_info[1].text,
                             "beer_link": beer_link}
                top_3.append(top_3_dict)

            
        #increase ratings count to get next page
        ratings_count += 50
        
        
        #####need catch for no user ratings
        if len(ratings_list) > 0:

            #loop through and sort info

            for tr in ratings_list:
                tds = tr.find_all('td')

                # isolate some info
                user_rating = tds[-2].text
#                 abv = tds[-3].text
                rDev = re.findall(r"([\d.]*\d+)", tds[-1].text)[0]
                # further isolate element in list holding 3 features
                add_beer_info = tds[2].find_all('a')

                # extract info
#                 beer_name = add_beer_info[0].text
                beer_link_total = add_beer_info[0]['href']
                base_url_ba = "https://www.beeradvocate.com"
                beer_link = base_url_ba + beer_link_total[0:beer_link_total.find("?")]
#                 beer_style = add_beer_info[2].text
#                 brewery = add_beer_info[1].text

                #dump into dict
                ratings_dict = {
#                     "beer_name": beer_name,
#                     "brewery": brewery,
#                     "beer_style": beer_style,
#                     "beer_style_match": re.sub(r'\W+', '', beer_style.lower()),
                    "beer_link": beer_link,
                    "user_rating": user_rating,
#                     "abv": abv,
                    "rDev": rDev
                }

                # append link to list
                user_ratings.append(ratings_dict)

        else: 

            avail_results = False

    if len(user_ratings) > 0:

        user_ratings_df = pd.DataFrame(user_ratings).drop_duplicates()

    else: 

        user_ratings_df = pd.DataFrame()

    if len(top_3) > 0:
        for beer in top_3:
                response = requests.get(beer['beer_link'])
                soup = BeautifulSoup(response.text, 'html.parser')
                beerimages = soup.find('div', {'id': 'main_pic_norm'}).find_all('img')
                beerlink = beerimages[0]['src']
                if (beerlink is not None):
                    beer['image_link'] = beerlink
                else:
                    beer['image_link'] = ""
                    
    return profile_dict, top_3, user_ratings_df

def match_styles(username):
    flag = 0
    #create df of user ratings
    profile_dict, top_3, user_ratings_df = user_ratings(username)
    print(len(user_ratings_df))

#   # creates two data frames, one for user_ratings, the other for possible recommendations
    engine = create_engine('postgresql://hgzhyrxbjgjnwa:3fe5e38aa493b4337c39b464fee4a6e71b1e4d33b57a60d50cbe0deaf6ff3e50@ec2-50-16-202-213.compute-1.amazonaws.com:5432/dacosp3h3fd1ng')
    beer_features_df = pd.read_sql("SELECT * FROM beer.beer_feature_all",con=engine)
    if len(user_ratings_df) > 0:
        user_ratings_df = user_ratings_df.merge(beer_features_df, left_on = 'beer_link', right_on = 'URL', how = "right")
        rec_df = user_ratings_df[user_ratings_df['beer_link'].isnull()]
        user_df = user_ratings_df[user_ratings_df['beer_link'].notnull()]
        user_df['user_rating'] = pd.to_numeric(user_df['user_rating'], errors = "coerce")
        user_df.sort_values('user_rating', ascending = False, inplace=True)
        print(f"Number of user matches to our DB: {len(user_df)}")
        print(f"Number of possible recomendations {len(rec_df)}")

        # decision making for 1 and 0
        # return top 5% for user
        user_df['yesno5'] = ""
        user_df['yesno5'][0:int(len(user_df)*.05)] = 1
        user_df['yesno5'][int(len(user_df)*.05):] = 0
        user_df['yesno5'].astype('int', inplace=True)

        user_df['yesno10'] = ""
        user_df['yesno10'][0:int(len(user_df)*.1)] = 1
        user_df['yesno10'][int(len(user_df)*.1):] = 0
        user_df['yesno10'].astype('int', inplace=True)

        #check cutoff score
        cut_off = user_df.iloc[int(len(user_df)*.05) - 1]['user_rating']
        if cut_off <= 3.75:
            print(f"{username} has low scoring beers classfied as yesses")
            bins = [0, 3.49999999, 6] # I know there is no 6, just to be safe
            labels = [0, 1]
            user_df['yesno5'] = pd.cut(user_df['user_rating'], bins, labels = labels)

        # check count of yesses
        yes_count = list(user_df['yesno5']).count(1)
        if yes_count < 5:
            bins = [0, 4.75, 6] # I know there is no 6, just to be safe
            labels = [0, 1]
            user_df['yesno5'] = pd.cut(user_df['user_rating'], bins, labels = labels)
            yes_count = list(user_df['yesno5']).count(1)
            if yes_count < 5:
    #             yes_count = list(user_df['yesno10']).count(1)
                cut_off = user_df.iloc[int(len(user_df)*.10) - 1]['user_rating']
                if cut_off <= 3.75:
                    print(f"{username} has low scoring beers classfied as yesses")
                    bins = [0, 3.49999999, 6] # I know there is no 6, just to be safe
                    labels = [0, 1]
                    user_df['yesno10'] = pd.cut(user_df['user_rating'], bins, labels = labels)
                    yes_count = list(user_df['yesno10']).count(1)
                    flag = 2
        if yes_count < 5: 
            flag = 1
    else:
        rec_df = beer_features_df
        flag = 1
        user_df = user_ratings_df
    
    return profile_dict, top_3, user_df, rec_df, flag

def random_forest(username):
    
    profile_dict, top_3, user_df, recs_df, flag = match_styles(username)
    
    if flag != 1:
        X_columns = ["Score", "pDev", "ABV", "Flavor", "Hoppiness","Maltiness","Fruitiness","Body",
              "Sweetness","Sour","spicy","bitter", 'Aroma_None', 'Aroma_caramel',
           'Aroma_floral', 'Aroma_fruit', 'Custom Flavor_None',
           'Custom Flavor_banana', 'Custom Flavor_brown sugar',
           'Custom Flavor_burnt', 'Custom Flavor_caramel',
           'Custom Flavor_chocolate', 'Custom Flavor_earthy',
           'Custom Flavor_herbal', 'Custom Flavor_pumpkin',
           'Custom Flavor_roasted', 'Custom Flavor_smoke', 'Custom Flavor_toasted',
           'Custom Flavor_wheat', 'Color_amber', 'Color_black', 'Color_dark ',
           'Color_gold', 'Color_pale']

        X = user_df[X_columns]
    
    num_recs = ""
    
    if flag == 0:
        target5 = user_df['yesno5'].astype('int')
        X_train5, X_test5, y_train5, y_test5 = train_test_split(X, target5, random_state = 42)

        # build model and score for 5%
        rf5 = RandomForestClassifier(n_estimators=200)
        rf5 = rf5.fit(X_train5, y_train5)
        score = rf5.score(X_test5, y_test5)
        #oob_score = rf5.oob_score_
        
        #make predictions/recommendations
        recsX = recs_df[X_columns]
        recommendations = rf5.predict(recsX)
        num_recs = list(recommendations).count(1)
        
        #print results
        print(f"Random forest top 5% R2 Score: {score}")
        #print(f"Random forest top 5% oob: {oob_score}")
        
    if flag == 2 or num_recs == 0:
        
        target10 = user_df['yesno10'].astype('int')
        X_train10, X_test10, y_train10, y_test10 = train_test_split(X, target10, random_state = 42)

        # build model and score for 10%
        rf10 = RandomForestClassifier(n_estimators=200, oob_score = True)
        rf10 = rf10.fit(X_train10, y_train10)
        score = rf10.score(X_test10, y_test10)
       # oob_score = rf10.oob_score_
        
        #make predictions/recommendations
        recsX = recs_df[X_columns]
        recommendations = rf10.predict(recsX)
        num_recs = list(recommendations).count(1)
        
        #print results
        print(f"Random forest top 10% R2 Score: {score}")
        #print(f"Random forest top 10% oob: {oob_score}")
        
    if flag == 1 or num_recs == 0:
        
        recommended_df = recs_df[(recs_df['Availaility'] != 'Limited(brewedonce)')]
        
        score = "Not enough user ratings to perform prediction.  Generic recommendations provided."
        
    else:
        
        
        recs_df['recommend'] = recommendations
    
        recommended_df = recs_df[(recs_df['recommend'] == 1) & (recs_df['Availaility'] != 'Limited(brewedonce)')]
    
    recommended_df.drop_duplicates(['Name', "Brewer"], inplace = True)
    recommended_df.sort_values('Score', ascending = False, inplace=True)

    info_columns = ["Name", "Brewer", "Location", "Style", "BrosScore", "Score", 
                        'ABV', 'Availaility', "Ranking", "num_ratings", "ScoreClass", "ImageLink", "URL"]

    recommended_yearround = recommended_df[recommended_df['Availaility'] == "Year-round"]
    recommended_other = recommended_df[recommended_df['Availaility'] != "Year-round"]
        
    def findrecs(df, num):
        for x in range(1,11):
            recs = df.groupby('Style')[info_columns].head(x)

            if len(recs) < num:
                continue

            if len(recs) >= num:
                recs = recs.iloc[0:num]
                break
            
        return recs
    
    top_yearround = findrecs(recommended_yearround, 6)
    top_other = findrecs(recommended_other, 4)
    
    frames = [top_yearround, top_other]
    top_recs = pd.concat(frames, ignore_index = True)
    
    top_recs.sort_values(['Score', 'Ranking'], inplace = True, ascending = False)
    
    recs_dict = top_recs.to_dict(orient = 'records')
    
    
    # % correct predicts on user set
#     predictions = rf.predict(X)
#     actual = user_df['yesno'].astype('int')
#     df = pd.DataFrame({"Predict": predictions, "actual": actual})
#     df['test'] = (df['Predict'] == df['actual'])
#     num_correct = list(df['test']).count(True)
#     perc_correct = num_correct/len(user_df)
    
    #print results
#     print(f"Random forest Score: {score}")
#     print(f"Random forest % correct: {perc_correct}")
    
    #make predictions/recommendations
#     recsX = recs_df[X_columns]
#     recommendations = rf.predict(recsX)
#     num_recs = list(recommendations).count(1)
    
    
    
    API_dict = {
        "userProfile": profile_dict,
        "top3UserBeers": top_3,
        "recommendations": recs_dict,
        "R2Score": score
#         "percCorrect": perc_correct
    }

    return API_dict