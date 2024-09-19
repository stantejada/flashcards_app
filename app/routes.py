from flask import redirect, render_template, url_for, flash, current_app, request, abort
from app import app, db, srs
import sqlalchemy as sa
from app.form import CardForm, LoginForm, RegisterForm
from app.models import Card, User
from flask_login import current_user, login_required, login_user, logout_user
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timezone

#
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

### index ###
@app.route('/')
@app.route('/home')
@login_required
def home():
    today = datetime.now(timezone.utc).date()
    
    #fetch 10 new cards
    new_cards = Card.query.filter(
        Card.user_id == current_user.id,
        Card.last_reviewed == None
    ).order_by(Card.id).limit(10).all()
    
    #fetch cards from previews days and reviewed
    accumulated_cards = Card.query.filter(
        Card.user_id == current_user.id,
        Card.next_review <= today
    ).order_by(Card.next_review).limit(90).all()
    
    all_cards = new_cards + accumulated_cards
    all_cards = all_cards[:100]
    
    return render_template('index.html', title='Home', cards = all_cards)
    

###Card###
#add new cards
@app.route('/add', methods=['GET','POST'])
@login_required
def add():
    form = CardForm()
    if form.validate_on_submit():
        print(form.image_url.data)
        #check if any image has been upload
        if form.image_url.data and allowed_file(form.image_url.data.filename):
            #Save img
            image_file = form.image_url.data
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['FILE_UPLOAD'],filename)
            image_file.save(image_path)
            
            normalized_img_url = f'img/{filename}'
            
            card = Card(
                verb = form.verb.data,
                meaning = form.meaning.data,
                example1 = form.example1.data,
                example2 = form.example2.data,
                example3 = form.example3.data,
                image_url = normalized_img_url,
                user_id = current_user.id
            )
            db.session.add(card)
            db.session.commit()
            flash("You have added new phrasal verb")
            return redirect(url_for('home'))
        else:
            flash("Invalid file type")
    return render_template('_add.html', form=form, title='Add card')

#review
@app.route('/review/<int:card_id>', methods=['POST'])
def review(card_id):
    card = Card.query.get_or_404(card_id)
    
    if card.user_id != current_user.id:
        abort(403)

    #get user input (incorrect or correct)
    correct = bool(int(request.form['correct']))
    
    #update SRS
    srs.update_srs_binary(card=card, correct=correct)
    
    card.last_reviewed = datetime.now(timezone.utc)
    db.session.commit()
    
    flash("Review recorded successfully.")
    return redirect(url_for('home')) 


### auth ###
#login
@app.route('/login', methods=['GET', 'POST'])
@login_required
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))

        login_user(user)
        print('login!', user.username)
        return redirect(url_for('home'))
        
    return render_template('login.html', form=form, title='Login')

#signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        
        user = User(username=form.username.data, email=form.email.data)
        user.hash_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulation you have been registered!')
        return redirect(url_for('login'))

    return render_template('register.html', title="Sign Up", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))