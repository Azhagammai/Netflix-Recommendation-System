from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# ==============================
# Load Deep Learning Model Files
# ==============================

try:
    df = pickle.load(open("models/movies_dl.pkl", "rb"))
    embeddings = pickle.load(open("models/dl_embeddings.pkl", "rb"))
except FileNotFoundError:
    print("❌ Model files not found. Make sure they exist in /models folder.")
    exit()

# Precompute similarity matrix
cosine_sim = cosine_similarity(embeddings)


# ==============================
# Recommendation Function
# ==============================

def recommend_movies_dl(title, top_n=5):
    title = title.strip()

    if title not in df["title"].values:
        return ["Movie not found. Please check spelling."]

    idx = df[df["title"] == title].index[0]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1: top_n + 1]
    movie_indices = [i[0] for i in sim_scores]

    return df["title"].iloc[movie_indices].tolist()


# ==============================
# Flask Routes
# ==============================

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []

    if request.method == "POST":
        movie = request.form.get("movie")

        if movie:
            recommendations = recommend_movies_dl(movie)

    return render_template("index.html", recommendations=recommendations)


# ==============================
# Run App
# ==============================

if __name__ == "__main__":
    app.run(debug=True)
