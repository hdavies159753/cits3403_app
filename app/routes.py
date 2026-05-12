from flask import Blueprint, render_template, jsonify, request
from app.submitting import submit_and_save
from app.models import Drawing, Prompt, Vote
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('prompt.html')

@main.route('/browse')
def browse():
    return render_template('browse.html')

@main.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/drawing')
def drawing():
    return render_template('drawing.html')

@main.route('/submit_drawing', methods=['POST'])
def submit_drawing():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request."}), 400

    success, message = submit_and_save(data)
    status_code = 200 if success else 400
    return jsonify({
        "success": success,
        "message": message
    }), status_code

@main.route('/vote', methods = ['POST'])
def vote():
    data = request.get_json()
    drawing_id = data.get("drawing_id")
    voter_id = 1
    existing_vote = Vote.query.filter_by(voter_id = voter_id, drawing_id = drawing_id).first()
    if existing_vote:
           return jsonify({
                "success": False,
                "message": "Already Voted!"}), 400
    vote = Vote(voter_id = voter_id, drawing_id = drawing_id)
    db.session.add(vote)
    db.session.commit()
    vote_count = Vote.query.filter_by(drawing_id = drawing_id).count()
    return jsonify({
        "success": True,
        "message": "Vote submitted!",
        "vote_count": vote_count
    })

@main.route("/drawing/<int:drawing_id>")
def individual_drawing(drawing_id):
    drawing = {

    "id": drawing_id,

    "artist": "Test Artist",

    "prompt": "Test Prompt",

    "image": "https://placehold.co/300x200"

}
    return render_template("individual_drawing.html", drawing=drawing)

