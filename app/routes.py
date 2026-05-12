from flask import Blueprint, render_template, jsonify, request
from sqlalchemy import func
from app import db
from app.submitting import submit_and_save
from app.models import Drawing, Vote, Prompt, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('prompt.html')

@main.route('/browse')
def browse():
    return render_template('browse.html')

@main.route('/leaderboard')
def leaderboard():
    prompt_id = request.args.get('prompt_id', type=int)

    query = (
        db.session.query(
            Drawing,
            User.username,
            Prompt.text.label('prompt_text'),
            func.count(Vote.id).label('score')
        )
        .join(User, Drawing.user_id == User.id)
        .join(Prompt, Drawing.prompt_id == Prompt.id)
        .outerjoin(Vote, Vote.drawing_id == Drawing.id)
    )

    if prompt_id:
        query = query.filter(Drawing.prompt_id == prompt_id)

    results = (
        query
        .group_by(Drawing.id, User.username, Prompt.text)
        .order_by(func.count(Vote.id).desc())
        .all()
    )

    rankings = []
    for rank, (drawing, username, prompt_text, score) in enumerate(results, 1):
        rankings.append({
            'rank': rank,
            'drawing_id': drawing.id,
            'username': username,
            'prompt_text': prompt_text,
            'score': score,
            'image': drawing.image,
            'date': drawing.date.strftime('%Y-%m-%d') if drawing.date else '',
        })

    prompts = Prompt.query.order_by(Prompt.date.desc()).all()

    return render_template(
        'leaderboard.html',
        rankings=rankings,
        prompts=prompts,
        selected_prompt_id=prompt_id,
    )

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
