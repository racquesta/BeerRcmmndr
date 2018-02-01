
# coding: utf-8

# In[2]:

import pandas as pd
from bs4 import BeautifulSoup
import requests
import re


# In[16]:

# read in beerstyles csv
df = pd.read_csv('allbeerLinksRonessa.csv', encoding = "ISO-8859-1")


# In[17]:

df.head()


# In[ ]:




# In[18]:

# dfKristine = df.iloc[0:5000]
# dfRonessa = df.iloc[5000:10000]
# dfPaul = df.iloc[10000:15000]
# dfJing = df.iloc[15000:]


# In[19]:

# dfJing.to_csv("JingBeer.csv")


# In[20]:

# urls = [row['url'] for index,row in df.iterrows()]


# In[21]:

# urls

#  beer_dict = {
#                     "beer_name": beer_list[i],
#                     "beer_style": style_names[x],
#                     "beer_url": "https://www.beeradvocate.com" + beer_links[i],
#                     "csv_name": csv_names[x],
#                     "match_name": match_names[x],
#                     "style_url": style_urls[x],
#                     "num_ratings": ratings_list[i],
#                     'score': scores[i],
#                     'abv': abv[i],
#                     'brewery': brewery[i]
#                 }


# In[ ]:

Name = []
Style = []
Url = []
Score = [] #<span class="ba-ravg">2.36</span>
ScoreClass = []
RatingCount = []
Ranking = []
ReviewCount = []
pDev = [] #percent deviation
BrosScore = []
Brewer = []
Location = []
ABV = []
Availability = []
imageLink = []
csv_name = []
match_name = []
num_ratings = []

beerCount = 1

for index, row in df.iterrows():
    print(row['beer_name'], row['beer_style'])
    name = row['beer_name']
    style = row["beer_style"]
    url = row["beer_url"]
    
    Name.append(name)
    Style.append(style)
    Url.append(url)
    csv_name.append(row['csv_name'])
    match_name.append(row['match_name'])
    num_ratings.append(row['num_ratings'])
    Brewer.append(row['brewery'])
    ABV.append(row['abv'])
    Score.append(row['score'])
    
# test 1 url first
# url = "https://www.beeradvocate.com/beer/profile/29/65/"
# urls = [row['url'] for row in df.iterrows()]

# use this to test 2 urls in a row
# urls = ['https://www.beeradvocate.com/beer/profile/29/65/','https://www.beeradvocate.com/beer/profile/285/39766/']
# for url in urls:
    # go to each beer style page and get the top 50 beers (by count of ratings)
    # response from site
    try:
        print(beerCount)
        response = requests.get(url)

        # Create BeautifulSoup object; parse with 'html.parser'
        soup = BeautifulSoup(response.text, 'html.parser')

#         beerScore = soup.find('span', class_='ba-ravg')
#         if (beerScore.text is not None):
#             Score.append(beerScore.text)
#         else:
#             Score.append('')

        scoreclass = soup.find('div', {'id':'score_box'}).find_all('b')
        if (scoreclass[1] is not None):
            ScoreClass.append(scoreclass[1].text)
        else:
            ScoreClass.append('')

#         rating = soup.find('span', class_='ba-ratings')
#         if (rating.text is not None):
#             RatingCount.append(rating.text)
#         else:
#             RatingCount.append('')

        itemstats = soup.find('div', {'id': 'item_stats'}).find_all('dd')
        ranking = itemstats[0].text.replace("#", "").replace(",", "")
        if (ranking is not None):
            Ranking.append(ranking)
        else:
            Ranking.append('')

        reviews = itemstats[1].text.replace(",", "")
        if (reviews is not None):
            ReviewCount.append(reviews)
        else:
            ReviewCount('')

        pdev = re.sub('\s','',itemstats[3].text).replace("%", "")
        if (pdev is not None):
            pDev.append(pdev)
        else:
            pDev.append('')

        brosdiv = soup.find('span', {'class': 'ba-bro_score'})
        #print(brosdiv)
        bros = brosdiv.text.strip()
        if (bros is not None):
            BrosScore.append(bros)
        else:
            BrosScore.append('')

        # get brewer and brewery from infobox    
        infobox = soup.find('div', {'id': 'info_box'}).find_all('a')

#         brewer = infobox[0].find('b').text

#         if (brewer is not None):
#             Brewer.append(brewer)
#         else:
#             Brewer.append('')

        # what needs to be checked for empty here?
        # do i need to empty the list when i'm done using it for next time?
        location = []
        for ahref in infobox:
            if ('/place/' in ahref['href']):
                location.append(ahref.text)

                
        if (len(location) > 1):
            place = ', '.join(location)
        elif (len(location) == 1):
            place = location[0]
        else:
            place = ''
#         print(place)
        Location.append(place)

        # get ABV and availability from infoboxHeadings
        infoboxHeadings = soup.find('div', {'id': 'info_box'}).find_all('b')
#         abv = re.sub('\s','',infoboxHeadings[5].next_sibling).replace("%", "")
#         if (abv is not None):
#             ABV.append(abv)
#         else:
#             ABV.append('')

        availability = re.sub('\s','',infoboxHeadings[6].next_sibling)
        if (availability is not None):
            Availability.append(availability)
        else:
            Availability.append('')

        beerimages = soup.find('div', {'id': 'main_pic_norm'}).find_all('img')
        beerlink = beerimages[0]['src']
        if (beerlink is not None):
            imageLink.append(beerlink)
        else:
            imageLink.append('')

        beerCount += 1
    except:
        print('error!', beerCount, url)
        beerCount += 1 #move to the next one
    


# In[ ]:

# scoreclass = soup.find('div', {'id':'score_box'}).find_all('b')
# sc = scoreclass[1].text
# print (sc)
# print(imageLink)


# In[13]:

num_ratings


# In[ ]:

featuredf = pd.DataFrame({"Name": Name, "URL": Url, "Style": Style, "Score":Score,"ScoreClass":ScoreClass,
                          "Ranking":Ranking,"ReviewCount":ReviewCount,"pDev":pDev,
                         "BrosScore":BrosScore,"Brewer":Brewer,"Location":Location,"ABV":ABV,
                         "Availaility":Availability,"ImageLink":imageLink, "csv_name": csv_name, "match_name": match_name,
                         "num_ratings": num_ratings})


# In[ ]:

featuredf


# In[ ]:

# featuredf['Ranking'] = featuredf['Ranking'].str.replace(",", "")
# featuredf['RatingCount'] = featuredf['RatingCount'].str.replace(",", "")
# featuredf['ReviewCount'] = featuredf['ReviewCount'].str.replace(",", "")


# In[ ]:

# save to csv
featuredf.to_csv('AllScrapedBeerFeatures.csv', index=False)


# In[26]:

# read in beerstyles csv
test = pd.read_csv('AllBeersEachStyle.csv', encoding = "ISO-8859-1")


# In[29]:

test['urlHack'] = test['url'] + ' '


# In[30]:

test.to_csv('AllBeersEachStyleHack.csv')


# In[34]:

featuredf['beerid'] = featuredf['ImageLink'].replace(['https://cdn.beeradvocate.com/im/beers/',',jpg'],'', inplace=True)
featuredf


# In[ ]:



