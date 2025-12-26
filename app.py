import sqlite3
from flask import Flask, render_template, request, redirect

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
    song_url = request.form.get("song_url")

    if song_name and song_url:
        if add_song_to_db(song_name, song_url):
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


@app.route("/visualizer")
def visualizer():
    with sqlite3.connect("song_queue.db") as conn:
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM song_queue WHERE queue_pos=0;").fetchone()
        if row:
            url = row[2]  # index 2 of the tuple should be song url
            name = row[0] # index 0 should be song name
            remove_played_song()
            url = parse_url(url)
            return render_template("visualizer.html", song_id=url, song_name=name)
    return "No Songs on Queue"


def parse_url(url):
    str_to_remove = ["https://", "youtu.be/", "www.youtube.com", "/watch?v=", "/embed/"]
    video_id = url
    for to_remove in str_to_remove:
        video_id = video_id.replace(to_remove, "")
    return video_id

def remove_played_song():
    with sqlite3.connect("song_queue.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM song_queue WHERE queue_pos=0;")
        cursor.execute("UPDATE song_queue SET queue_pos = queue_pos - 1 WHERE queue_pos > 0;")
        conn.commit()
    return "Deleted"
