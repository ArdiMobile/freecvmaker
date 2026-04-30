from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
import uuid
import threading
import time

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def delete_later(path):
    time.sleep(300)
    if os.path.exists(path):
        os.remove(path)

@app.route("/api/download")
def download():
    url = request.args.get("url")

    if not url:
        return jsonify({"status": "error", "message": "No URL provided"})

    try:
        file_id = str(uuid.uuid4())
        output_template = f"{DOWNLOAD_DIR}/{file_id}.%(ext)s"

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': output_template,
            'quiet': True,
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        final_file = f"{DOWNLOAD_DIR}/{file_id}.mp4"

        threading.Thread(target=delete_later, args=(final_file,)).start()

        return jsonify({
            "status": "success",
            "download_url": f"/api/file/{file_id}"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


@app.route("/api/file/<file_id>")
def get_file(file_id):
    file_path = f"{DOWNLOAD_DIR}/{file_id}.mp4"

    if not os.path.exists(file_path):
        return "File not found", 404

    return send_file(file_path, as_attachment=True)


@app.route("/")
def home():
    return "Galmee API running on Render 🚀"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)