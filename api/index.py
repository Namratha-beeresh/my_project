import os
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__, template_folder='../templates')

# MongoDB Connection
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client.namratha_portfolio  # Updated DB name
collection = db.activity_log

@app.route('/')
def index():
    try:
        posts = list(collection.find().sort("_id", -1))
    except Exception as e:
        print(f"Database Error: {e}")
        posts = []
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['POST'])
def add():
    skill = request.form.get('skill')
    notes = request.form.get('notes')
    if skill:
        try:
            collection.insert_one({
                "skill": skill,
                "notes": notes,
                "date": datetime.now().strftime("%b %d, %Y | %I:%M %p") # Prettier date format
            })
        except Exception as e:
            print(f"Insert Error: {e}")
            
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()