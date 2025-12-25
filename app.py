import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/queue")
def queue():
    return render_template("queue.html")

@app.route("/add_to_queue", methods=["POST"])
def add_to_queue():
    song_name = request.form.get("song_name")
    if song_name:
        if add_song_to_db(song_name, "http://127.0.0.1:5000/add_to_queue"):
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
            song_name srting PRIMARY KEY,
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
