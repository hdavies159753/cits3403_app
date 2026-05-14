from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from sqlalchemy import func
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date

from app import db
from app.models import Drawing, Vote, Prompt, User
from app.forms import LoginForm, RegisterForm
from app.submitting import submit_and_save
from app.browse_logic import get_browsepage_data

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    today = date.today()
    todays_prompt = Prompt.query.filter_by(date=today).first()
    has_submitted = False
    if todays_prompt:
        has_submitted = Drawing.query.filter_by(
            user_id=current_user.id, prompt_id=todays_prompt.id
        ).first() is not None
    return render_template('prompt.html', todays_prompt=todays_prompt, has_submitted=has_submitted)


@main.route('/browse')
@login_required
def browse():
    selected_prompt = request.args.get('prompt', 'all')
    selected_date = request.args.get('date', 'all')

    page_data = get_browsepage_data(selected_prompt, selected_date)
    return render_template('browse.html', **page_data)



@main.route('/leaderboard')
@login_required
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


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('main.login'))

        login_user(user)
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/') or next_page.startswith('//'):
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('login.html', form=form)


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data or None
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/submit_drawing', methods=['POST'])
@login_required
def submit_drawing():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request."}), 400
    
    today = date.today()
    todays_prompt = Prompt.query.filter_by(date=today).first()

    existing_drawing = Drawing.query.filter_by(user_id=current_user.id,prompt_id=todays_prompt.id).first()

    if existing_drawing:
        return jsonify({"success": False,"message": "You have already submitted a drawing for this prompt."}), 400

    success, message, drawing_id = submit_and_save(current_user.id, data)
    status_code = 200 if success else 400
    response = {"success": success, "message": message}
    if drawing_id:
        response["drawing_id"] = drawing_id
    return jsonify(response), status_code

@main.route('/vote', methods=['POST'])
@login_required
def vote():
    data = request.get_json()
    drawing_id = data.get("drawing_id")

    drawing_obj = Drawing.query.get(drawing_id)
    if not drawing_obj:
        return jsonify({"success": False, "message": "Drawing not found."}), 404
    if drawing_obj.user_id == current_user.id:
        return jsonify({"success": False, "message": "You cannot vote on your own drawing."}), 400

    existing_vote = Vote.query.filter_by(voter_id=current_user.id, drawing_id=drawing_id).first()
    if existing_vote:
        return jsonify({"success": False, "message": "Already voted!"}), 400

    new_vote = Vote(voter_id=current_user.id, drawing_id=drawing_id)
    db.session.add(new_vote)
    db.session.commit()
    vote_count = Vote.query.filter_by(drawing_id=drawing_id).count()
    return jsonify({"success": True, "message": "Vote submitted!", "vote_count": vote_count})

@main.route("/drawing/<int:drawing_id>")
@login_required
def individual_drawing(drawing_id):
    drawing = Drawing.query.get_or_404(drawing_id)
    vote_count = Vote.query.filter_by(drawing_id=drawing_id).count()
    has_voted = Vote.query.filter_by(voter_id=current_user.id, drawing_id=drawing_id).first() is not None
    is_own_drawing = drawing.user_id == current_user.id
    return render_template("individual_drawing.html", drawing=drawing, vote_count=vote_count, has_voted=has_voted, is_own_drawing=is_own_drawing)

@main.route("/success/<int:drawing_id>")
@login_required
def submission_success(drawing_id):
    drawing = Drawing.query.get_or_404(drawing_id)
    if drawing.user_id != current_user.id:
        return redirect(url_for('main.browse'))
    return render_template("success.html", drawing=drawing)


@main.route("/profile/<int:user_id>")
@login_required
def user_profile(user_id):
    user = User.query.get_or_404(user_id)

    drawings = (
        Drawing.query
        .filter_by(user_id=user.id)
        .order_by(Drawing.date.desc())
        .all()
    )

    return render_template("userprofile.html", user=user, drawings=drawings)

