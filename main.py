import requests                         #allows us to download HTML from site
from bs4 import BeautifulSoup           #allows us to use HTML and grab data from site
import pandas as pd                     #frame data in rows and columns
import numpy as np                      #used to handle large datasets
from time import sleep                  #control the loops rate 
from random import randint              # vary the amount of waiting time


title = []
year = []
time = []
genre = []
score = []
director = []
stars = []


#creating an array of values and passing it in the url for dynamic webpages. (start, stop, step.)
pages = np.arange(1,1001,50)

for page in pages:

    page = requests.get("https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start="+str(page)+"&ref_=adv_nxt")
    soup = BeautifulSoup(page.content, 'html.parser')     # parsing/modifying out the data that we actually want


    data = soup.findAll('div', attrs = {'class': 'lister-item mode-advanced'})
    sleep(randint(2,10))                #vary amount of waiting time and can help avoid getting IP address banned due to a ton of requests
    for store in data:
        name = store.h3.a.text
        title.append(name)

        year_of = store.h3.find('span', class_ = 'lister-item-year text-muted unbold').text.replace('(', '').replace(')', '')
        year.append(year_of)

        runtime = store.p.find('span', class_ = 'runtime').text
        time.append(runtime)

        movie_genre = store.p.find('span', class_ = 'genre').text.replace('\n', '').strip()
        genre.append(movie_genre)

        imdbscore =  store.find('div', class_ = 'inline-block ratings-imdb-rating').text.replace('\n\n', '').replace('\n', '')
        score.append(imdbscore)


        dir = store.find('p', class_='').find_all('a')[0].text
        director.append(dir)

        stars.append([actor.text for actor in store.find('p',class_='').find_all('a')[1:]])

        dataframe = pd.DataFrame({'Title': title, 'Year': year, 'Runtime': time, 'Genre': genre, 'IMDB Rating': score, 'Director': director, 'Actors': stars})


dataframe.to_csv('Top 1000 IMDB movies.csv')