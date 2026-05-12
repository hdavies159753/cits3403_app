from flask import Blueprint, render_template, jsonify, request
from app.submitting import submit_and_save
from app.models import Drawing, Prompt
from datetime import date

main = Blueprint('main', __name__)

@main.route('/')
def index():
    today = date.today()
    todays_prompt = Prompt.query.filter_by(date=today).first()
    return render_template('prompt.html', todays_prompt=todays_prompt)

@main.route('/browse')
def browse():
    selected_prompt = request.args.get('prompt', 'all')
    selected_date = request.args.get('date', 'all')

    prompts = Prompt.query.order_by(Prompt.date.desc()).all()

    query = Drawing.query.order_by(Drawing.date.desc())

    if selected_prompt != 'all':
        query = query.join(Prompt).filter(Prompt.text == selected_prompt)

    if selected_date != 'all':
        query = query.filter(Drawing.date >= selected_date)

    drawings = query.all()
    dates = sorted({drawing.date.date() for drawing in drawings if drawing.date}, reverse=True)

    return render_template(
        'browse.html',
        prompts=prompts,
        drawings=drawings,
        dates=dates,
        selected_prompt=selected_prompt,
        selected_date=selected_date
    )


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
