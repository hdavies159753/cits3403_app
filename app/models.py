from datetime import datetime, timezone
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    drawings = db.relationship('Drawing', backref='author', lazy='dynamic')
    votes = db.relationship('Vote', backref='voter', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'


class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256), nullable=False)
    date = db.Column(db.Date, unique=True, nullable=False, index=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    drawings = db.relationship('Drawing', backref='prompt', lazy='dynamic')

    def __repr__(self):
        return f'<Prompt {self.date}: {self.text}>'


class Drawing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prompt_id = db.Column(db.Integer, db.ForeignKey('prompt.id'), nullable=False)
    image_data = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    votes = db.relationship('Vote', backref='drawing', lazy='dynamic')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'prompt_id', name='uq_one_drawing_per_user_per_prompt'),
    )

    def vote_count(self):
        return self.votes.count()

    def __repr__(self):
        return f'<Drawing {self.id} by User {self.user_id}>'


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    drawing_id = db.Column(db.Integer, db.ForeignKey('drawing.id'), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    # Self-vote prevention is enforced at the application level since
    # SQLite does not support subqueries in CHECK constraints.
    __table_args__ = (
        db.UniqueConstraint('voter_id', 'drawing_id', name='uq_one_vote_per_user_per_drawing'),
    )

    def __repr__(self):
        return f'<Vote by User {self.voter_id} on Drawing {self.drawing_id}>'
