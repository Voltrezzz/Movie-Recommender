import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('movies.csv')
print(df.columns)
print(df.head())

df['tags'] = df['overview'] + " " + df['genres'] + " " + df['keywords']
df['tags'] = df['tags'].fillna("").str.lower()

tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
matrix = tfidf.fit_transform(df['tags'])

similarity = cosine_similarity(matrix)

def recommend(movie_title):
    idx = df[df['title'] == movie_title].index[0]
    distances = list(enumerate(similarity[idx]))
    movies = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
    return [df.iloc[i[0]]['title'] for i in movies]