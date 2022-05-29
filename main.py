from turtle import title, width
from urllib import response
import streamlit as st
import pickle
import pandas as pd
import requests
import json

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read}</style>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: red;'>Movies Recommendation System</h1>", unsafe_allow_html=True)

# function to fetch poster and details of recommended movies from tmdb website using API
def fetch_details(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=2277317c22be6028e61a76356b211f09&language=en-US'.format(movie_id)) 
    data = response.json() 
    poster_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    overview = data['overview']
    homepage = data['homepage']
    vote_count = data['vote_count']
    rating = data['vote_average']
    # genre = data['genres']
    # genres_data = json.load(genre)
    # genres = genres_data['name']
    return poster_path,overview,homepage,vote_count,rating

# main function for selecting top similar movies
def recommend(movie,k):
    index = movieslist[movieslist['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
     
    for i in distances[1:k]:
        movie_id = movieslist.iloc[i[0]].movie_id
        movie_title = movieslist.iloc[i[0]].title
        movie_director = movieslist.iloc[i[0]].crew
        movie_cast = movieslist.iloc[i[0]].cast

        movie_poster,movie_overview,movie_homepage,movie_votes,movie_rating = fetch_details(movie_id)

        st.markdown(f"[ {movie_title}]({movie_homepage})")
        st.image(movie_poster, width=250)
        st.markdown('Director : ' + str(movie_director))
        st.markdown('Cast : ' + str(movie_cast))
        st.markdown(movie_overview)
        st.markdown('Total votes : ' + str(movie_votes))
        st.markdown('Rating : ' + str(movie_rating) + '⭐')


movies_list = pickle.load(open('movies_list.pkl','rb'))         # loads movies_list.pkl(contains movies dataframe) file in read binary mode
movieslist = pd.DataFrame(movies_list)
similarity = pickle.load(open('similarity.pkl','rb'))           # loads similarity.pkl(contains similarity matrix) file in read binary mode
movies = movieslist['title'].values

selected_movie = st.selectbox('Type or select a movie from the dropdown',movies)
no_of_recommendations = st.number_input('Number of movies to be Recommended', 2, 20)

if st.button('Recommend'):
    recommend(selected_movie,no_of_recommendations+1)



