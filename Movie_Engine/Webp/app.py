import pickle

import requests
import streamlit as st
from st_aggrid import AgGrid
from streamlit_option_menu import option_menu

similarity = pickle.load(open('sim.pkl', 'rb'))
movies = pickle.load(open('database.pkl', 'rb'))
top = pickle.load(open('qua.pkl', 'rb'))


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

    return movie_name, movies_poster


with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Top Movies", "Recommender", "About"],
        icons=["triangle", "book", "house door"],
        menu_icon="cast",
        default_index=0,
        orientation="right"
    )

htmlcode = '''<h4><marquee behavior='alternate', style='italics'>MOVIES RECOMMENDATION ENGINE</marquee><h4>'''
st.markdown(htmlcode, unsafe_allow_html=True)


# streamlit/stapp.py
def set_bg_hack_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url("https://repository-images.githubusercontent.com/275336521/20d38e00-6634-11eb-9d1f-6a5232d0f84f");
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


set_bg_hack_url()

# loading bar
import time

if selected == "Top Movies":
    st.subheader("Top Movies")
    #st.dataframe(top.head(20))
    AgGrid(top.head(20), theme='dark')

if selected == "Recommender":
    movies_list = movies['title'].values
    selected_movie_name = st.selectbox(' Search Your Movie Here : : - ', movies_list)
    names = []
    poster = []
    if st.button('Recommend !!'):
        with st.spinner('Search Engine Running...'):
            time.sleep(10)
        names, poster = get_recommendations(selected_movie_name)
        st.markdown("<h5 style='text-align: center; color: white;'> ----> Recommended Movies <---- </h5>",
                    unsafe_allow_html=True)

       
        a = 0
        for i in range(1, 4):
            cols = st.columns(3)
            with cols[0]:
                with st.container():
                    st.text(names[a])
                    st.image(poster[a])
            with cols[1]:
                with st.container():
                    st.text(names[a + 1])
                    st.image(poster[a + 1])
            with cols[2]:
                with st.container():
                    st.text(names[a + 2])
                    st.image(poster[a + 2])
                    a = a + 3
        

if selected == "About":
    st.text("Recommender System is a system that seeks to predict or filter preferences according")
    st.text(" to the user’s choices. ")
    st.text("Recommender systems are utilized in a variety of areas including movies, music, news, books,")
    st.text(" research articles, search queries, social tags, and products in general.")


