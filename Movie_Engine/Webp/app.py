import streamlit as st
import pickle
import requests

st.markdown("<h1 style='text-align: center; color: white;'>{ Movie Recommender System }</h1>", unsafe_allow_html=True)

similarity = pickle.load(open('sim.pkl','rb'))
movies = pickle.load(open('database.pkl','rb'))
top10 = pickle.load(open('qua.pkl','rb'))

def fetch_poster(movie_id):
     response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
     data = response.json()
     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def get_recommendations(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    movie_name = []
    movies_poster = []
    for i in distances[1:10]:
        movie_id = movies.iloc[i[0]].id
        movies_poster.append(fetch_poster(movie_id))
        movie_name.append(movies.iloc[i[0]].title)

    return movie_name,movies_poster


st.sidebar.markdown("<p style='text-align: center; color: white;'> ----> Top 10 Movies <---- </p>", unsafe_allow_html=True)
top_movies = top10['title'].values
for i in top_movies:
    st.sidebar.text(i)
    print("\n")


movies_list = movies['title'].values
selected_movie_name = st.selectbox(' Search Your Movie Here : : - ', movies_list)
names = []
poster = []
if st.button('Recommend !!'):
    names,poster = get_recommendations(selected_movie_name)
    st.markdown("<p style='text-align: center; color: white;'> ----> Recommenden Movies <---- </p>", unsafe_allow_html=True)

    a = 0
    for i in range(1, 4):
        cols = st.columns(3)
        with cols[0]:
            st.header(names[a])
            st.image(poster[a])
        with cols[1]:
            st.header(names[a+1])
            st.image(poster[a+1])
        with cols[2]:
            st.header(names[a+2])
            st.image(poster[a+2])

        a = a + 3



