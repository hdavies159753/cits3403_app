from flask import Blueprint, render_template, jsonify, request
from sqlalchemy import func
from app import db
from app.submitting import submit_and_save
from app.models import Drawing, Vote, Prompt, User
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User
from app.forms import LoginForm, RegisterForm
from app.submitting import submit_and_save
from datetime import date

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    today = date.today()
    todays_prompt = Prompt.query.filter_by(date=today).first()
    return render_template('prompt.html', todays_prompt=todays_prompt)


@main.route('/browse')
@login_required
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
        return redirect(next_page or url_for('main.index'))

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


@main.route('/drawing')
@login_required
def drawing():
    return render_template('drawing.html')


@main.route('/submit_drawing', methods=['POST'])
@login_required
def submit_drawing():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid request."}), 400

    success, message = submit_and_save(current_user.id, data)
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

