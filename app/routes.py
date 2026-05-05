from flask import Blueprint, render_template, jsonify, request
from app.submitting import submit_and_save

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
    success, message = submit_and_save(data)
    return jsonify({
        "success": success, 
        "message" : message
    })
