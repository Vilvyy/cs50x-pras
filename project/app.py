import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import requests

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///manga.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST" :
        if not request.form.get("name"):
            return redirect("/")
        else:
            value = request.form.get("name")
            value = value.replace(" ", "%20")
            response = requests.get(f"https://api.mangadex.org/author?limit=32&name=%22{value}%22&order%5Bname%5D=asc") # https://www.geeksforgeeks.org/how-to-get-data-from-api-in-python-flask/
            response_manga = requests.get(f"https://api.mangadex.org/manga?limit=10&title={value}&includedTagsMode=AND&excludedTagsMode=OR&contentRating%5B%5D=safe&contentRating%5B%5D=suggestive&contentRating%5B%5D=erotica&order%5BlatestUploadedChapter%5D=desc")
            if response.status_code == 200 and response_manga.status_code == 200:
                author_search = response.json()
                manga_search = response_manga.json()
                for row in author_search['data']:
                    biography = row['attributes']['biography']

                    # Check if 'biography' is a dictionary and has the 'en' key
                    if isinstance(biography, dict) and 'en' in biography:
                        bio_text = biography['en']
                        if len(bio_text) > 100:
                            # Slice the string and append '...'
                            shortened_biography = bio_text[:100] + "..."
                            # Insert it back into the JSON
                            row['attributes']['biography']['en'] = shortened_biography

                for row in manga_search['data']:
                    desc = row['attributes']['description']

                    # Check if 'biography' is a dictionary and has the 'en' key
                    if isinstance(desc, dict) and 'en' in desc:
                        desc_text = desc['en']
                        if len(desc_text) > 100:
                            # Slice the string and append '...'
                            shortened_desc = desc_text[:100] + "..."
                            # Insert it back into the JSON
                            row['attributes']['description']['en'] = shortened_desc

                return render_template("index.html", author=author_search, manga=manga_search)
            elif response.status_code == 200:
                author_search = response.json()
                return render_template("index.html", author=author_search)
            elif response_manga.status_code == 200:
                manga_search = response_manga.json()
                return render_template("index.html", author=manga_search)
            else:
                author_search = {"data": []} # ChatGPT SUGGESTED
                return render_template("index.html", author=author_search)
    else:
        return render_template("index.html")
