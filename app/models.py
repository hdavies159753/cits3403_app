from app import db
from datetime import datetime

class Drawing(db.Model):
    __tablename__ = "drawings"
    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    prompt_id = db.Column(db.Integer, db.ForeignKey("prompts.id"), nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint("user_id", "prompt_id", name = "One_user_one_prompt_for_drawing"),
    )

    user = db.relationship("User", back_populates = "Drawings")
    prompt = db.relationship("Prompt", back_populates = "Drawings")
    votes = db.relationship("Vote", back_populates = "drawing")



class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64),nullable = False)
    email = db.Column(db.String(64), nullable = True)
    password_hashed = db.Column(db.String(64), nullable = True)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    Drawings = db.relationship("Drawing", back_populates = "user")
    vote_drawing = db.relationship("Vote", back_populates = "voter")


class Prompt(db.Model):
    __tablename__ = "prompts"
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.Date, nullable = False, unique = True)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    Drawings = db.relationship("Drawing", back_populates = "prompt")

class Vote(db.Model):
    __tablename__ = "votes"
    id = db.Column(db.Integer, primary_key = True)
    voter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    drawing_id = db.Column(db.Integer, db.ForeignKey("drawings.id"), nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("voter_id","drawing_id", name = "one_user_one_drawing_voted" ),
    )

    voter = db.relationship("User", back_populates = "vote_drawing")
    drawing = db.relationship("Drawing", back_populates = "votes")