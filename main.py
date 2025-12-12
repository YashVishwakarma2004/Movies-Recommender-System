import os
import gdown
import pickle
import pandas as pd
import streamlit as st

# -------------------------------
# MODEL DOWNLOAD & LOADING
# -------------------------------

MODEL_FILENAME = "similarity.pkl"

# Google Drive File ID
DRIVE_FILE_ID = os.environ.get("MODEL_DRIVE_ID", "16brzhMb_UWb_pzNpx5TUkp6ZXr9mhH_K")


def download_model_if_missing():
    if os.path.exists(MODEL_FILENAME):
        print("Model already exists, skipping download.")
        return

    if not DRIVE_FILE_ID:
        raise RuntimeError("MODEL_DRIVE_ID environment variable is missing.")

    url = f"https://drive.google.com/uc?id={DRIVE_FILE_ID}"
    print(f"Downloading model from {url} ...")
    if not os.path.exists("similarity.pkl"):
        url = "https://drive.google.com/uc?id=YOUR_ID"
        gdown.download(url, "similarity.pkl", quiet=False)


def load_similarity_model():
    download_model_if_missing()
    with open(MODEL_FILENAME, "rb") as f:
        return pickle.load(f)


# Load model once
similarity = load_similarity_model()

# Load movies dictionary (this must be in your repo)
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)

# -------------------------------
# STREAMLIT UI
# -------------------------------

# Background styling
st.markdown(
    """
    <style>
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
    h1, h2, h3 {
        color: #E50914 !important;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.8);
        font-family: serif;
        font-weight: 800;
    }
    .stButton>button {
        background-color: #E50914;
        color: white;
        border-radius: 8px;
        padding: 0.6em 1.2em;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #f40612;
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎬 Netflix-Style Movie Recommender System")

# Recommendation Function
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]
    return [movies.iloc[i[0]].title for i in movies_list]


selected_movie = st.selectbox(
    "Select a movie:",
    movies["title"].values
)

if st.button("Recommend"):
    st.subheader("You may also like:")
    for rec in recommend(selected_movie):
        st.write("🎞️", rec)

