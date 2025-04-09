from flask import Flask,request,render_template
import numpy as np
import pandas as pd
import pickle
import requests

# laoding models
df = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))


def recommendation(song_df):
    if song_df not in df['song'].values:
        return ["Song not found in dataset. Please try another song."]
    
    idx = df.index[df['song'] == song_df].tolist()
    
    if not idx:  # If index is empty, return an error message
        return ["Error: Unable to find song index."]
    
    idx = idx[0]  # Extract first index
    distances = sorted(enumerate(similarity[idx]), reverse=True, key=lambda x: x[1])
    
    songs = [df.iloc[m_id[0]].song for m_id in distances[1:21]]
    return songs if songs else ["No recommendations found."]




# flask app
app = Flask(__name__)
# paths
@app.route('/')
def index():
    names = list(df['song'].values)
    return render_template('index.html',name = names)


@app.route('/recom', methods=['POST'])
def mysong():
    try:
        user_song = request.form['names']
        songs = recommendation(user_song)

        # Generate online image URLs
        # song_images = {song: f"https://source.unsplash.com/300x200/?music,{song.replace(' ', '+')}" for song in songs}

        return render_template('index.html', songs=songs, name=list(df['song'].values), selected_song=user_song)
    except Exception as e:
        return render_template('index.html', songs=["Error: " + str(e)], name=list(df['song'].values))



# python
if __name__ == "__main__":
    app.run(debug=True)
    
    