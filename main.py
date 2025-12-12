import streamlit as st
import pickle
import pandas as pd

# 🎨 Background Style
st.markdown(
    """
    <style>
    /* ======= Netflix-Style Background ======= */
    .stApp {
        background: linear-gradient(
            to bottom right,
            rgba(0, 0, 0, 0.9),
            rgba(50, 20, 20, 0.95),
            rgba(20, 50, 50, 0.85)
        ),
        url("https://assets.nflxext.com/ffe/siteui/vlv3/0e8e5dc8-7a89-4cc1-9d39-3f9a7e9df39f/9b436b73-fb2f-4b89-a4c7-53a41e3b4589/IN-en-20230925-popsignuptwoweeks-perspective_alpha_website_large.jpg");

        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: white;
    }

    /* ======= Title Styling ======= */
    h1, h2, h3 {
        color: #E50914 !important; /* Netflix red */
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
        font-family: serif;
        font-weight: 800;
    }

    /* ======= Text Styling ======= */
    .stSelectbox label, .stButton button, .stMarkdown, .stText {
        color: white !important;
        font-weight: 500;
    }

    /* ======= Button Styling ======= */
    .stButton>button {
        background-color: #E50914;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5em 1em;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #f40612;
        transform: scale(1.05);
    }

    /* ======= Dropdown Styling ======= */
    .stSelectbox [data-baseweb="select"] {
        background-color: rgba(0, 0, 0, 0.7);
        color: white;
    }

    /* ======= Movie Title Styling ======= */
    .movie-title {
        font-size: 20px;
        color: #fff;
        font-weight: 600;
        text-shadow: 2px 2px 4px #000;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = [movies.iloc[i[0]].title for i in movies_list]
    return recommended_movies

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title("🎬 Movie Recommender System")

selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

if st.button("Recommend"):
    recommendation = recommend(selected_movie_name)
    st.subheader("You might also like:")
    for i in recommendation:
        st.write("🎞️", i)
