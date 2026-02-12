import sqlite3
from flask import Flask, render_template, request
from youtube_search import YoutubeSearch

# For qr code
import qrcode
import base64
import io

import socket

app = Flask(__name__)

Song_queue_indexes = {
    "song_id": 0,
    "song_name": 1,
    "queue_pos": 2,
    "song_urls": 3,
    "singers": 4,
}

##############
## SETTINGS ##
Max_Singers = 10
Max_song_urls = 10


def createDBTables():
    print("Creating missing tables ...")
    with sqlite3.connect("song_queue.db") as conn:
        # creates a table if it doesnt exist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS song_queue(
            song_id INTEGER PRIMARY KEY,
            song_name STRING NOT NULL,
            queue_pos INTEGER NOT NULL,
            song_urls STRING NOT NULL,
            singers STRING NULL
            )
        """)
        conn.commit()
    print("Done")


createDBTables()
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

    song_queue = []
    with sqlite3.connect("song_queue.db") as conn:
        cursor = conn.cursor()
        song_queue = cursor.execute("SELECT * FROM song_queue").fetchall()

    songs = ""
    for song in song_queue:
        singers = str(song[Song_queue_indexes["singers"]])

        songs += f"{song[Song_queue_indexes['song_id']]}$%$%{song[Song_queue_indexes['song_name']]}"  ### $%$% is a separator for song id and song_name

        if singers.strip() == "":
            songs += "*^%"  #### *^% is only a separator to split without the risk of spliting a song name on the queue.html file
        else:
            songs += f" → 🎙️{singers}*^%"
    songs = songs[0:-3]
    return render_template("queue.html", songs=songs)


@app.route("/add_to_queue", methods=["POST"])
def add_to_queue():
    # Handles POST requests to add song to queue db
    song_name = str(request.form.get("song_name"))
    song_urls = []
    song_artist = str(request.form.get("song_artist"))
    vid_option = str(request.form.get("vid_type"))

    results = YoutubeSearch(
        f"Embbedable {vid_option} {song_name} - {song_artist}",
        max_results=Max_song_urls,
    ).to_dict()
    if results:
        for result in results:
            song_urls.append(result["url_suffix"])

    singers = ", ".join(
        x.strip()
        for x in str(request.form.get("singers")).title().split(",")
        if x.strip()
    )

    if song_name and song_urls:
        if add_song_to_db(song_name, song_urls, singers):
            return render_template("succes.html")
        return render_template("error.html")
    return error_message(
        title="Information is missing!",
        message="You need to provide a name and a url for your song",
        redirect_time=10,
        redirect_location="queue",
    )


def add_song_to_db(song_name, song_urls, singers):
    with sqlite3.connect("song_queue.db") as conn:
        cursor = conn.cursor()
        conn.execute("BEGIN")
        song_urls_string = parse_id(song_urls)
        try:
            cursor.execute("SELECT * FROM song_queue")
            rows = cursor.fetchall()
            queue_pos = len(rows)
            cursor.execute(
                "INSERT INTO song_queue(song_name, queue_pos, song_urls, singers) VALUES(?, ?, ?, ?)",
                (song_name, queue_pos, song_urls_string, singers),
            )

            conn.commit()
            return True
        except Exception as e:
            print(f"DB error: {e}")
            conn.rollback()
            return False


@app.route("/add_singer", methods=["POST"])
def add_singer():
    data = request.get_json()

    song_id = str(data.get("song_id"))
    new_singers = str(data.get("new_singer")).strip().split(",")
    print(song_id)
    if song_id and new_singers:
        with sqlite3.connect("song_queue.db") as conn:
            cursor = conn.cursor()
            conn.execute("BEGIN")

            try:
                cursor.execute(
                    "SELECT singers FROM song_queue WHERE song_id=?", (song_id,)
                )

                singers = [
                    s.strip().title()
                    for s in cursor.fetchone()[0].strip().split(",")
                    if s.strip()
                ]
                msg = ""
                should_update = False  # prevent Running if nothing changes
                for new_singer in new_singers:
                    if new_singer.title() not in singers:
                        if (len(singers) + 1) <= Max_Singers:
                            singers.append(new_singer)
                            should_update = True
                            msg += f"{new_singer} Added Succesfully!\n"
                        else:
                            msg += f"{new_singer} can't be added, Song is full!\n"
                    else:
                        msg += f"{new_singer} can't be added, Already in List!\n"

                if should_update:
                    cursor.execute(
                        "UPDATE song_queue SET singers=? WHERE song_id=?",
                        (", ".join(str(x) for x in singers), song_id),
                    )
                    conn.commit()

                return msg, 200
            except Exception as e:
                conn.rollback()
                return f"DB error: {e}", 500
    return "Singers is empty or there is no song id", 500


@app.route("/visualizer")
def visualizer():
    with sqlite3.connect("song_queue.db") as conn:
        cursor = conn.cursor()
        row = cursor.execute("SELECT * FROM song_queue WHERE queue_pos=0;").fetchone()
        row2 = cursor.execute("SELECT * FROM song_queue WHERE queue_pos=1;").fetchone()
        if not row2:
            row2 = [""] * len(
                Song_queue_indexes.keys()
            )  # if row2 is empty create a empty list to prevent errors
        if row:
            vid_ids = row[Song_queue_indexes["song_urls"]]
            name = row[Song_queue_indexes["song_name"]]
            if vid_ids:
                return render_template(
                    "visualizer.html",
                    vid_ids=vid_ids,
                    song_id=row[Song_queue_indexes["song_id"]],
                    song_name=name,
                    singers=row[Song_queue_indexes["singers"]],
                    next_song_name=row2[Song_queue_indexes["song_name"]],
                    next_singers=row2[Song_queue_indexes["singers"]],
                )
            else:
                advance_queue(row[Song_queue_indexes["song_id"]])
                return error_message(
                    title="BAD url for song: " + name,
                    message="removing it from Queue, please add it again with the correct Yotube Link",
                    redirect_time=60,
                    redirect_location="visualizer",
                )
    # TODO: Change this to a proper template
    return "<h1>No Songs on Queue</h1> <meta http-equiv='refresh' content='2;url=/'>"


def error_message(title="", message="", redirect_time=1, redirect_location="queue"):
    return render_template(
        "error.html",
        title=title,
        message=message,
        redirect_time=redirect_time,
        redirect_location=app.url_for(redirect_location),
    )


def parse_id(urls):
    ids = ""
    for url in urls:
        if "(" in urls and ")" in urls:
            url = url.split("(")[-1].split(")")[0]

        if "youtu.be/" in url:
            ids += url.split("youtu.be/")[1].split("?")[0] + ","

        if "v=" in url:
            ids += url.split("v=")[1].split("&")[0] + ","

        if "embed/" in url:
            ids += url.split("embed/")[1].split("?")[0] + ","

    if ids:
        return ids[0:-1]

    print("Couldnt parse")
    return None


def advance_queue(song_id):
    with sqlite3.connect("song_queue.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM song_queue WHERE queue_pos=0 AND song_id= ?", (song_id,)
        )
        cursor.execute(
            "UPDATE song_queue SET queue_pos = queue_pos - 1 WHERE queue_pos > 0;"
        )
        conn.commit()


@app.route("/advance_queue", methods=["POST"])
def advance_queue_helper():
    data = request.get_json()
    song_id = data.get("song_id")

    advance_queue(song_id)

    return "", 200
