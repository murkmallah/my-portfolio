import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import ttk

# Loading & Preparing Data
df = pd.read_csv("goodreads_data.csv")
df = df.dropna(subset=["Book", "Author", "Genres", "Description"])
df = df.drop_duplicates(subset=['Book'])

# TF-IDF on Descriptions
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['Description'])

# --- Recommendation Functions ---
def recommend_by_genre(genre):
    genre = genre.lower()
    filtered = df[df['Genres'].str.lower().str.contains(genre, na=False)]
    return filtered[['Book', 'Author', 'Genres']].head(10)

def recommend_by_author(author):
    author = author.lower()
    filtered = df[df['Author'].str.lower().str.contains(author, na=False)]
    return filtered[['Book', 'Author', 'Genres']].head(10)

def recommend_by_past_read(book_title):
    book_title = book_title.lower()
    try:
        idx = df[df['Book'].str.lower() == book_title].index[0]
    except IndexError:
        return pd.DataFrame([{"Book": "Not found", "Author": "", "Genres": ""}])
    
    cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
    similar_indices = cosine_sim.argsort()[::-1][1:11]
    recommendations = df.iloc[similar_indices][['Book', 'Author', 'Genres']]
    return recommendations

# Main Hybrid Recommender
def recommend(mode, user_input):
    if mode == "Genre":
        return recommend_by_genre(user_input)
    elif mode == "Author":
        return recommend_by_author(user_input)
    elif mode == "Past Read":
        return recommend_by_past_read(user_input)
    else:
        return pd.DataFrame([{"Book": "Invalid selection", "Author": "", "Genres": ""}])

# GUI Code
def get_recommendations():
    mode = selected_option.get()
    user_input = input_entry.get()
    result_df = recommend(mode, user_input)

    output_text.delete('1.0', tk.END)  # Clear output area
    for i, row in result_df.iterrows():
        output_text.insert(tk.END, f"{i+1}. {row['Book']} — {row['Author']} [{row['Genres']}]\n\n")

# Creating GUI window
window = tk.Tk()
window.title("Book Recommendation Agent")

# Heading
ttk.Label(window, text="Choose Recommendation Type:").pack(pady=5)

# Radio buttons
selected_option = tk.StringVar(value="Genre")
for option in ["Genre", "Author", "Past Read"]:
    ttk.Radiobutton(window, text=option, variable=selected_option, value=option).pack()

# User input
input_entry = ttk.Entry(window, width=50)
input_entry.pack(pady=10)

# Recommend Button
ttk.Button(window, text="Get Recommendations", command=get_recommendations).pack()

# Output area
output_text = tk.Text(window, height=20, width=70, wrap=tk.WORD)
output_text.pack(pady=10)

# Run GUI
window.mainloop()
