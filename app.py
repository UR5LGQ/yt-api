from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/")
def home():
    return "YT API OK"

@app.route("/search")
def search():
    query = request.args.get("q", "")

    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(
                f"ytsearch10:{query}",
                download=False
            )

        videos = []

        for entry in result.get("entries", []):
            videos.append({
                "id": entry.get("id"),
                "title": entry.get("title")
            })

        return jsonify(videos)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/geturl")
def geturl():
    video_id = request.args.get("id")

    if not video_id:
        return jsonify({"error": "No video id"}), 400

    url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "quiet": True,
        "format": "best"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                url,
                download=False
            )

        return jsonify({
            "title": info.get("title"),
            "url": info.get("url")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
