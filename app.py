import streamlit as st
import requests
from recommender import recommend, df

st.set_page_config(page_title="🎬 Movie Recommender", page_icon="🎬", layout="wide")

st.markdown("""
    <style>
        body { background-color: #0e0e0e; }
        .main { background-color: #141414; }
        h1 { color: #E50914; font-size: 3em; text-align: center; }
        .subtitle { text-align: center; color: #aaaaaa; font-size: 1.1em; margin-top: -15px; margin-bottom: 30px; }
        .movie-card { background-color: #1f1f1f; border-radius: 12px; padding: 10px; text-align: center; }
        .movie-title { color: #ffffff; font-weight: bold; font-size: 0.95em; margin-top: 8px; }
        .movie-rating { color: #f5c518; font-size: 0.85em; }
        .overview { color: #cccccc; font-size: 0.8em; margin-top: 5px; }
        .stButton button { background-color: #E50914; color: white; border: none; border-radius: 8px; padding: 10px 30px; font-size: 1em; width: 100%; }
    </style>
""", unsafe_allow_html=True)

API_KEY = "e129a1f986ff87ebea29a4535e8b1d87"  

def fetch_poster(movie_title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
        data = requests.get(url).json()
        poster_path = data['results'][0]['poster_path']
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"

def fetch_details(movie_title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
        data = requests.get(url).json()
        result = data['results'][0]
        return {
            "rating": round(result.get('vote_average', 0), 1),
            "overview": result.get('overview', 'No overview available.')[:150] + "..."
        }
    except:
        return {"rating": "N/A", "overview": "No overview available."}

st.markdown("<h1>🎬 Movie Recommender</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Find movies you\'ll love based on what you already like</p>', unsafe_allow_html=True)

search = st.text_input("", placeholder="🔍  Type a movie name e.g. Inception, Avatar...")

if search:
    filtered = df[df['title'].str.contains(search, case=False, na=False)]['title'].values
else:
    filtered = df['title'].values

movie = st.selectbox("Select a movie:", filtered if len(filtered) > 0 else ["No matches found"])

if st.button("🎬 Recommend Movies"):
    if movie and movie != "No matches found":
        results = recommend(movie)
        st.markdown("---")
        st.markdown("### You might also like:")
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                poster = fetch_poster(results[i])
                details = fetch_details(results[i])
                st.markdown(f'''
                    <div class="movie-card">
                        <img src="{poster}" width="100%" style="border-radius:8px;">
                        <p class="movie-title">{results[i]}</p>
                        <p class="movie-rating">⭐ {details["rating"]}</p>
                        <p class="overview">{details["overview"]}</p>
                    </div>
                ''', unsafe_allow_html=True)
