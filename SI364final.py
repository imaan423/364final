## Imaan Munir - SI 364 Final

## Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError, RadioField, IntegerField
from wtforms.validators import Required, Length, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
import requests
import json

# Imports for login management
from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash


# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/SI364projectplanimunir"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['HEROKU_ON'] = os.environ.get('HEROKU')


# App addition setups
manager = Manager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

# Login configurations setup
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app) 


## Association tables
# Association Table between Director and Movies 
director_movies= db.Table('director_movies', db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')), db.Column('director_id', db.Integer, db.ForeignKey('director.id')))


##################
##### MODELS #####
##################

class User(UserMixin, db.Model):
		__tablename__ = "user"
		id = db.Column(db.Integer, primary_key=True)
		username = db.Column(db.String(255), unique=True, index=True)
		email = db.Column(db.String(64), unique=True, index=True)
		password_hash = db.Column(db.String(128))
		#movie = db.relationship('Search',backref='User')

		@property
		def password(self):
				raise AttributeError('password is not a readable attribute')

		@password.setter
		def password(self, password):
				self.password_hash = generate_password_hash(password)

		def verify_password(self, password):
				return check_password_hash(self.password_hash, password)


## DB load function
@login_manager.user_loader
def load_user(user_id):
		return User.query.get(int(user_id))


class Actor(db.Model):
		__tablename__ = "Actor"
		id = db.Column(db.Integer,primary_key=True)
		name = db.Column(db.String(64))
		#one-to-many relationship (one user id, saved list of fav celebrity names)
		user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

		def __repr__(self):
				return "{}".format(self.name, self.id)


class Movie(db.Model):
		__tablename__ = "movie"
		id = db.Column(db.Integer,primary_key=True)
		title = db.Column(db.String(200))
		rating = db.Column(db.String(200))
		year = db.Column(db.String(200))
		#many to many relationship (multiple directors with multiple movies)
		director = db.relationship("Director", secondary = director_movies, backref=db.backref('movie', lazy='dynamic'), lazy='dynamic')


		def __repr__(self):
			return "{} has a rating of: {}, filmed in:{}".format(self.title, self.rating, self.year)        


class Director(db.Model):
		__tablename__ = "director"
		id = db.Column(db.Integer,primary_key=True)
		title = db.Column(db.String(128))



###################
###### FORMS ######
###################

class FavoriteActorForm(FlaskForm):
		name = StringField("Enter your favorite movie celebrity name:", validators=[Required()])
		submit = SubmitField()


class RegistrationForm(FlaskForm):
		email = StringField('Enter Email:', validators=[Required(),Length(1,64),Email()])
		username = StringField('Enter Username:',validators=[Required(),Length(1,64)])
		password = PasswordField('Enter Password:',validators=[Required(),Length(1,200),EqualTo('password2',message="Passwords must match")])
		password2 = PasswordField("Confirm Password:",validators=[Required()])
		submit = SubmitField('Register User')

		def validate_email(self,field):
			if User.query.filter_by(email=field.data).first():
				raise ValidationError('It looks like this email address has already been registered.')

class LoginForm(FlaskForm):
		email = StringField('Email', validators=[Required(), Length(1,64), Email()])
		password = PasswordField('Password', validators=[Required()])
		remember_me = BooleanField('Keep me logged in')
		submit = SubmitField('Log In')


class MovieForm(FlaskForm):
	movietitle = StringField("Enter the title of the movie", validators=[Required()])
	director = StringField("Enter the directors of the movie (as a comma separated list)", validators=[Required()])
	rating = IntegerField("Enter the rating of this movie", validators=[Required()])
	year = IntegerField("Enter what year this movie was filmed in", validators=[Required()])
	submit = SubmitField('Submit')

class FindMovies(FlaskForm):
		see = StringField("What movie would you like to look up?", validators=[Required()])
		submit = SubmitField() 


class UpdateButtonForm(FlaskForm):
	newtitle = StringField("Enter the updated title of the movie", validators=[Required()])
	newrating = StringField("Enter the updated rating of the movie", validators=[Required()])
	newyear = StringField("Enter the updated year of the movie", validators=[Required()])
	submit = SubmitField('Update')


class DeleteButtonForm(FlaskForm):
	submit = SubmitField('Delete')


####################
#### HELPER FXNS ###
####################

def get_or_create_celebname(celeb_name):
		get_user = db.session.query(User).filter_by(username=current_user.username).first()
		celebrity = db.session.query(Actor).filter_by(name= celeb_name, user_id=get_user.id).first()
		if celebrity:
			return celebrity
		else:
			 new_celebrity = Actor(name=celeb_name, user_id=get_user.id)
			 db.session.add(new_celebrity)
			 db.session.commit()
			 return new_celebrity


def get_or_create_director(director_name):
	director = db.session.query(Director).filter_by(title= director_name).first()
	if director:
		return director
	else:
		director = Director(title = director_name)
		db.session.add(director)
		db.session.commit()
		return director


def get_or_create_movie(title, year, rating, current_user, director_list = []):
	movie = db.session.query(Movie).filter_by(title = title).first()
	if movie:  
		return movie
	else:
		movie = Movie(title = title, year = year, rating = rating)
		for d in director_list:
			d = d.strip()
			d = get_or_create_director(d)
			movie.director.append(d)
		db.session.add(movie)
		db.session.commit()
		return movie


def find_movie(query, params={}):
	result = requests.get('https://api.themoviedb.org/3/search/movie?api_key=01f21469bee1f9c1dae9b24273441f0c&language=en-US&query='+query+'&page=1&include_adult=false', params = params)
	json_result = json.loads(result.text)
	if json_result['results']==[]:
		return "",""
	return json_result['results'][0]['title'], json_result['results'][0]['overview']




########################
#### View functions ####
########################

## Error handling routes
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


@app.route('/login',methods=["GET","POST"])
def login():
	#should render Login Form to see if user is not database. If not in database, the user gets invalid username / password and redirected to login.html
		form = LoginForm()
		if form.validate_on_submit():
				user = User.query.filter_by(email=form.email.data).first()
				if user is not None and user.verify_password(form.password.data):
						login_user(user, form.remember_me.data)
						return redirect(request.args.get('next') or url_for('home'))
				flash('Invalid username or password.')
		return render_template('login.html',form=form)


@app.route('/logout')
@login_required
def logout():
	#should flash screen "You have been logged out" and render index.html
		logout_user()
		flash('You have been logged out')
		return redirect(url_for('home'))


@app.route('/register',methods=["GET","POST"])
def register():
	#should render RegistrationForm and process the data (username, email, password) and add /commit it to database. When form is submitted, it should redirect to login.html. if not, should just the form again.
		form = RegistrationForm()
		if form.validate_on_submit():
				user = User(email=form.email.data,username=form.username.data,password=form.password.data)
				db.session.add(user)
				db.session.commit()
				flash('You can now log in!')
				return redirect(url_for('login'))
		return render_template('register.html',form=form)


@app.route('/', methods=['GET', 'POST'])
def home():
		form = MovieForm() 
		form2 = FavoriteActorForm() 
		if form.validate_on_submit():
				movietitle = form.movietitle.data
				director = form.director.data.split(",")
				rating = form.rating.data
				year = form.year.data
				get_or_create_movie(movietitle, year, rating, current_user, director)
				return redirect(url_for('all_movies'))
		if form2.validate_on_submit():
				name = form2.name.data
				get_or_create_celebname(name)
				return redirect(url_for('see_favorite'))
		return render_template('index.html',form=form, form2=form2)


	#should be home page. it should have a search form to enter movie data (title, director, rating, year) you have recently watched. the data from form should be processed and get redirected to see_favorites.html where the a saved list of movies the user has watched is shown; if not, should just show form again.


@app.route('/all_movies', methods=["GET","POST"])
def all_movies():
	form = DeleteButtonForm()
	form2= UpdateButtonForm()
	all_movies = []
	movie = db.session.query(Movie).all()
	return render_template('all_movies.html', allmovies = movie, form=form, form2=form2)
	#should query all movies and return template that shows all movies saved


@app.route('/delete/<movielst>',methods=["GET","POST"])
def delete(movielst):
		l = Movie.query.filter_by(title=movielst).first()
		for item in l.director:
			if len(Movie.query.join(Director.movie).filter(Director.title==item.title).all()) < 2:
				db.session.delete(item)
				db.session.commit()
		db.session.delete(l)
		db.session.commit()
		flash("Deleted movie "+movielst)
		return redirect(url_for('all_movies'))



@app.route('/movie/<info>',methods=["GET","POST"])
def single_movie(info):
	form = UpdateButtonForm()
	lst = Movie.query.filter_by(title=info).first()
	return render_template('single_movie.html',item=lst,form=form)


@app.route('/update/<item>',methods=["GET","POST"])
def update(item):
	form = UpdateButtonForm()
	if form.validate_on_submit():
		new_title = form.newtitle.data
		new_rating = form.newrating.data
		new_year = form.newyear.data
		m = Movie.query.filter_by(title=item).first()
		m.title = new_title
		m.rating = new_rating
		m.year = new_year
		db.session.commit()
		flash("Updated movie information: " + "Updated title is " + m.title + " with a rating of " + m.rating + " filmed in " + m.year)
		return redirect(url_for('all_movies'))
	return render_template('update.html',item = item, form = form)



@app.route('/all_directors')
def all_directors():
		directornames = Director.query.all()
		directors = []
		for item in directornames:
				name = item.title
				movie = Movie.query.join(Director.movie).filter(Director.title==name).all()
				empty = []
				for i in movie:
					empty.append(i.title)
				directors.append((name, empty))
		return render_template('all_directors.html', directors = directors)
	#should query all directors and return template that shows all directors saved


@app.route('/see_favorite')
@login_required
def see_favorite():
		if current_user.is_authenticated:
			names = User.query.filter_by(username=current_user.username).first()
			actors = Actor.query.filter_by(user_id= names.id).all()
			return render_template('favorite.html',names=actors)
		else:
			flash("You're not logged in! Try again.")
			return redirect(url_for('index'))
#should first make sure the user is logged in to access the page. if user is logged in, then it will query all favorite celebrities names and match the names with the user ID to only display the names entered by the specific user. it will then render favorite.html where it is a page with all the saved celebrity names by that given user. if not, should just show form again.

@app.route('/search_movie', methods=["GET","POST"])
@login_required
def search_movie():
		form = FindMovies() 
		if form.validate_on_submit():
				term = form.see.data
				title, overview = find_movie(term)
				return render_template('search_movie.html',title=title, overview=overview, form=form)
		return render_template('search_movie.html',form=form, title=" ")
	#should render a form where a user can input a movie and then from TheMovieDB API get movie title and movie overview about the particular movie




if __name__ == '__main__':
		db.create_all()
		manager.run()





