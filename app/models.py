import sqlalchemy as sa 
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True, nullable=False)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), unique=True, nullable=False, index=True)
    password_hash: so.Mapped[str] = so.mapped_column(sa.String(128))
    
    
    #Relationship One to Many
    cards:so.Mapped['Card'] = so.relationship('Card', backref='author', lazy=True)
    
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Card(db.Model):
    __tablename__ = 'cards'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    verb: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, index=True, nullable=False)
    meaning: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, nullable=False)
    example1: so.Mapped[str] = so.mapped_column(sa.String(256), index=True, nullable=False)
    example2: so.Mapped[str] = so.mapped_column(sa.String(256), index=True, nullable=False)
    example3: so.Mapped[str] = so.mapped_column(sa.String(256), index=True, nullable=False)
    image_url: so.Mapped[str]  = so.mapped_column(sa.String(255), nullable=False)
    
    #ForeignKey to create a relationship Card-User
    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('users.id'), nullable=False)
    
    
    # SRS - fields
    next_review: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    interval: so.Mapped[int] = so.mapped_column(sa.Integer, default=1)
    repetitions: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    ease_factor: so.Mapped[float] = so.mapped_column(sa.Float, default=2.5)
    review_count: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    last_reviewed: so.Mapped[datetime] = so.mapped_column(sa.DateTime, nullable=True)
    
    
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))