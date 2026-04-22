from flask import Blueprint, render_template

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
