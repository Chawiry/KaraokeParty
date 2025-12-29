import sqlite3
from flask import Flask, render_template, request

# For qr code
import qrcode
import base64
import io

import socket

app = Flask(__name__)


if __name__ == "__main__":
    app.run(host=socket.gethostname())
    print("Running on: https://" + socket.gethostname() + ":5000/")


@app.route("/")
def index():
    # Landing page

    full_url = request.url_root.rstrip("/") + app.url_for("queue")
    qr = qrcode.make(full_url)
    img_buffer = io.BytesIO()
    qr.save(img_buffer)
    img_str = base64.b64encode(img_buffer.getvalue()).decode()

    return render_template("index.html", qr_data=img_str)


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
            return render_template("succes.html")
        return render_template("error.html")
    return render_template("error.html")


def add_song_to_db(song_name, song_url):
    with sqlite3.connect("song_queue.db") as conn:
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
            cursor.execute(
                "INSERT INTO song_queue(song_name, queue_pos, song_url) VALUES(?, ?, ?)",
                (song_name, queue_pos, song_url),
            )

            conn.commit()
            return True
        except:
            conn.rollback()
            return False


@app.route("/visualizer")
def visualizer():
    with sqlite3.connect("song_queue.db") as conn:
        cursor = conn.cursor()

        conn.execute("""
            CREATE TABLE IF NOT EXISTS song_queue(
            song_name STRING PRIMARY KEY,
            queue_pos INTEGER NOT NULL,
            song_url STRING NOT NULL
            )
        """)

        row = cursor.execute("SELECT * FROM song_queue WHERE queue_pos=0;").fetchone()
        if row:
            id = parse_id(row[2])  # index 2 of the tuple should be song url
            name = row[0]  # index 0 should be song name
            if id:
                return render_template("visualizer.html", song_id=id, song_name=name)
            else:
                return "BAD url for song " + name
    return "<h1>No Songs on Queue</h1> <meta http-equiv='refresh' content='2;url=/'>"


def parse_id(url):
    if "(" in url and ")" in url:
        url = url.split("(")[-1].split(")")[0]

    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]

    if "v=" in url:
        return url.split("v=")[1].split("&")[0]

    if "embed/" in url:
        return url.split("embed/")[1].split("?")[0]

    return None


@app.route("/advance_queue", methods=["POST"])
def advance_queue():
    data = request.get_json()
    song_name = data.get("song_name")

    with sqlite3.connect("song_queue.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM song_queue WHERE queue_pos=0 AND song_name= ?", (song_name,)
        )
        cursor.execute(
            "UPDATE song_queue SET queue_pos = queue_pos - 1 WHERE queue_pos > 0;"
        )
        conn.commit()
    return "", 200
