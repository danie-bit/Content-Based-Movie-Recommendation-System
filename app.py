import streamlit as st
import pickle
import requests

df = pickle.load(open("movies.pkl",'rb'))
similarity = pickle.load(open("similarity.pkl","rb"))
movie_names = df["title"].values
st.title("Movie Recommender System")

import time
def get_posters(movie_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=1d52ca1c97485a0f058987718a06c535&language=en-US"

    retries = 3
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status() # Raises an HTTPError for bad status codes
            data = response.json()
            poster_path = data["poster_path"]
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error on attempt {i+1}: {e}")
            time.sleep(2 ** i)  # Exponential backoff
    return None # Return None or a placeholder image on failure

# def get_posters(movie_id):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
#     }
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=1d52ca1c97485a0f058987718a06c535&language=en-US"
#     response = requests.get(url, headers=headers)
#     data = response.json()
#     poster_path = data["poster_path"]
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#
#     return full_path

def recommend(movie):
  movie_index = df[df["title"] == movie].index[0]
  distances = similarity[movie_index]
  movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x : x[1])[1:6]
  recommend_movies = []
  recommended_movie_posters = []

  for i in movies_list :
    recommend_movies.append(df.iloc[i[0]]["title"])
    recommended_movie_posters.append(get_posters(df.iloc[i[0]].movie_id))

  return recommend_movies, recommended_movie_posters


selected_movie = st.selectbox(
    "How would you like to be contacted?",
    movie_names,
)

if st.button("Recommend"):
    movies, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(movies[0])
        st.image(posters[0], width=150)
    with col2:
        st.text(movies[1])
        st.image(posters[1], width=150)
    with col3:
        st.text(movies[2])
        st.image(posters[2])
    with col4:
        st.text(movies[3])
        st.image(posters[3])
    with col5:
        st.text(movies[4])
        st.image(posters[4])