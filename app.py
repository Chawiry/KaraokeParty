import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    # Landing page
    return render_template("index.html")

@app.route("/queue")
def queue():
    # Add songs to queue page
    return render_template("queue.html")

@app.route("/add_to_queue", methods=["POST"])
def add_to_queue():
    # Handles POST requests to add song to queue db 
    song_name = request.form.get("song_name")
    if song_name:
        if add_song_to_db(song_name, "https://test.com"):    ##### CHANGE TEMP URL
            return render_template('succes.html')
        return render_template('error.html')
    return render_template('error.html')


def add_song_to_db(song_name, song_url):
 with sqlite3.connect('song_queue.db') as conn:
        cursor = conn.cursor()
        conn.execute("BEGIN")
        
        # creates a table if it doesnt exist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS song_queue(
            song_name STRING PRIMARY KEY,
            queue_pos INTEGER NOT NULL,
            song_url STRING NOT NULL
            )
        """)
        
        try:
            cursor.execute("SELECT * FROM song_queue")
            rows = cursor.fetchall()
            queue_pos = len(rows)
            cursor.execute("INSERT INTO song_queue(song_name, queue_pos, song_url) VALUES(?, ?, ?)", (song_name, queue_pos, song_url))

            conn.commit()
            return True
        except:
            conn.rollback()
            return False
