import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

from tqdm import tqdm

# data scraper initial code
headers = {"Accept-Language": "en-US, en; q=0.5"}

url = "https://www.imdb.com/search/title/?genres=horror&languages=en&sort=user_rating,desc&title_type=feature&num_votes=10000,&explore=genres"
results = requests.get(url, headers=headers)

soup = BeautifulSoup(results.text, "html.parser")

# intialize empty lists where you'll store your data
titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

movie_div = soup.find_all('div', class_='lister-item mode-advanced')


# initiate the for loop
# this tells your scraper to iterate through
# every div container we stored in movie_div
for container in tqdm(movie_div):

    # name
        name = container.h3.a.text
        titles.append(name)

    # year
        year = container.h3.find('span', class_='lister-item-year').text
        years.append(year)

    # length
        runtime = container.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else '-'
        time.append(runtime)

    # rating
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

    # metascore
        m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
        metascores.append(m_score)

    # votes
        nv = container.find_all('span', attrs={'name': 'nv'})

        vote = nv[0].text
        votes.append(vote)

        grosses = nv[1].text if len(nv) > 1 else '-'
        us_gross.append(grosses)

print (titles)
print (years)
print (time)
print (imdb_ratings)
print (metascores)
print (votes)
print (us_gross)

# building a dataframe with pandas
movies = pd.DataFrame({
    'movie': titles,
    'year': years,
    'timeMin': time,
    'imdb': imdb_ratings,
    'metascore': metascores,
    'votes': votes,
    'us_grossMillions': us_gross,
})

# checks for data types (debug)
# print(movies.dtypes)

# cleaning data with pandas
movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)
movies['metascore'] = pd.to_numeric(movies['metascore'], errors='coerce')
movies['votes'] = movies['votes'].str.replace(',', '').astype(int)
movies['us_grossMillions'] = movies['us_grossMillions'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['us_grossMillions'] = pd.to_numeric(movies['us_grossMillions'], errors='coerce')

print(movies)

movies.to_csv('movies.csv')

# progress bar
# https://stackoverflow.com/questions/43259717/progress-bar-for-a-for-loop-in-python-script