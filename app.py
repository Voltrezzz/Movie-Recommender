import streamlit as st
from recommender import recommend, df

st.title(" Movie Recommender")

movie = st.selectbox("Pick a movie you like:", df['title'].values)

if st.button("Recommend"):
    results = recommend(movie)
    st.subheader("You might also like:")
    for r in results:
        st.write("🎥 " + r)
