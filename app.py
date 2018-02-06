#Import frameworks
from flask import Flask, g, render_template, flash, url_for, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

#Import models.py and forms.py
import models
import forms

#Set the default connections
DEBUG = True
PORT = 8000
HOST = '0.0.0.0'


#Initialise the app as the default flask app to run.
app = Flask(__name__)
app.secret_key = 'yuyesFXYIRe5wsuilv45FGCGU6789dh.09);if6p9o/lj.'


#Create an instance of login manager.
login_manager = LoginManager()
#Initialise the app with the login manager.
login_manager.__init__(app)
#If not logged in - redirect to login.
login_manager.login_view = 'login'

#Attempt to load the user, if the user does not exist do nothing
@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except models.DoesNotExist:
        return None




#Connect to the DB before each request.
#g is a global variable that makes something visible to the whole program.
@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


#Close the DB connection after each request.
@app.after_request
def after_request(response):
    g.db.close()
    return response



#Routes the user to register form, includes GET and
#POST methods as user will need to both retrieve and
#send information to the view.
@app.route('/register', methods = ('GET', 'POST'))
def register():
    form = forms.RegistrationForm()
    #Check if all validation criteria is met upon user pressing submit.
    if form.validate_on_submit():
        #flash success message to user
        flash("Registration Successful!", "success")
        #Create user with validated data from the form.
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        #Redirect user to index.
        return redirect(url_for('index'))
    return render_template('register.html', form=form)

#Routes to the login form, again including GET and POST as above
@app.route('/login', methods = ('GET', 'POST'))
def login():
    form = forms.LoginForm()
    #If the form validates then try and create a user with the username that was input
    #If the user with that username doesn't exist throw an
    #error that says incorrect email or password
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Username or password is incorrect!", "error")
        else:
            #If the user instance was created and the username was correct then
            #check if the password hash stored in the DB is equal to
            #the hash of the password that was entered in the form
            #If these are equal then log the user in and tell them they are logged in
            #Then redirect to the homepage
            if check_password_hash(user.password, form.password.data):
                login_user(user) #Creates a session in a browser with a cookie
                flash("You are now logged in.", "success")
                return redirect(url_for('index'))
            else:
                #If password was incorrect flash that one of the fields was invalid
                flash("Username or password is incorrect!", "error")
    #If all else fails render html template for login.html
    return render_template('login.html', form=form)

#Routes to the logout page
#This cannot work if not logged in so if not logged in first route to 'login'
@app.route('/logout')
@login_required
def logout():
    #Logs the user out
    logout_user() #Deletes the cookie that the browser stored hence deleting the current session
    #Inform the user they successfully logged out
    flash("Logged out.", "success")
    #Return to the homepage
    return redirect(url_for('index'))

#Routes to the new booking page
@app.route('/new_booking', methods = ('GET', 'POST'))
@login_required
def book():
    form = forms.BookingForm()
    #Declare instances in query var
    instances_in_query = 0
    if form.validate_on_submit():
        #If the form validates then check to see which room was
        #selected so that number of computers can be checked
        if form.room.data == 'lib_ground':
            #If the room is the downstairs lib then perform a query that selects
            #all of the bookings in the DB that have the same date, period and room as the input
            query = models.Booking.select().where(
                models.Booking.date == form.date.data,
                models.Booking.period == form.period.data,
                models.Booking.room == form.room.data
            )
            #For each instance inside the query, add one to the instances var
            #so I know how many bookings have been made for the particular date and time
            for instance in query:
                instances_in_query = instances_in_query + 1
            #If instances are less than the number of computers, there are more
            #computers left and therefore booking can be created
            if instances_in_query < 6:
                models.Booking.create(user=g.user._get_current_object(),
                                      room=form.room.data,
                                      date=form.date.data,
                                      period=form.period.data,
                                      purpose=form.purpose.data)
                flash("Booking Created!", 'success')
                return redirect(url_for('index'))
            else:
                flash("Room fully booked!", 'error')
        elif form.room.data == 'lib_first':
            query = models.Booking.select().where(
                models.Booking.date == form.date.data,
                models.Booking.period == form.period.data,
                models.Booking.room == form.room.data
            )
            for instance in query:
                instances_in_query = instances_in_query + 1
            if instances_in_query < 3:
                models.Booking.create(user=g.user._get_current_object(),
                                      room=form.room.data,
                                      date=form.date.data,
                                      period=form.period.data,
                                      purpose=form.purpose.data)
                flash("Booking Created!", 'success')
                return redirect(url_for('index'))
            else:
                flash("Room fully booked!", 'error')
        elif form.room.data == 'social_first':
            query = models.Booking.select().where(
                models.Booking.date == form.date.data,
                models.Booking.period == form.period.data,
                models.Booking.room == form.room.data
            )
            for instance in query:
                instances_in_query = instances_in_query + 1
            if instances_in_query < 12:
                models.Booking.create(user=g.user._get_current_object(),
                                      room=form.room.data,
                                      date=form.date.data,
                                      period=form.period.data,
                                      purpose=form.purpose.data)
                flash("Booking Created!", 'success')
                return redirect(url_for('index'))
            else:
                flash("Room fully booked!", 'error')
        elif form.room.data == 'f16':
            query = models.Booking.select().where(
                models.Booking.date == form.date.data,
                models.Booking.period == form.period.data,
                models.Booking.room == form.room.data
            )
            for instance in query:
                instances_in_query = instances_in_query + 1
            if instances_in_query < 9:
                models.Booking.create(user=g.user._get_current_object(),
                                      room=form.room.data,
                                      date=form.date.data,
                                      period=form.period.data,
                                      purpose=form.purpose.data)
                flash("Booking Created!", 'success')
                return redirect(url_for('index'))
            else:
                flash("Room fully booked!", 'error')
        elif form.room.data == 'f19':
            query = models.Booking.select().where(
                models.Booking.date == form.date.data,
                models.Booking.period == form.period.data,
                models.Booking.room == form.room.data
            )
            for instance in query:
                instances_in_query = instances_in_query + 1
            if instances_in_query < 12:
                models.Booking.create(user=g.user._get_current_object(),
                                      room=form.room.data,
                                      date=form.date.data,
                                      period=form.period.data,
                                      purpose=form.purpose.data)
                flash("Booking Created!", 'success')
                return redirect(url_for('index'))
            else:
                flash("Room fully booked!", 'error')
        elif form.room.data == 'f22':
            query = models.Booking.select().where(
                models.Booking.date == form.date.data,
                models.Booking.period == form.period.data,
                models.Booking.room == form.room.data
            )
            for instance in query:
                instances_in_query = instances_in_query + 1
            if instances_in_query < 12:
                models.Booking.create(user=g.user._get_current_object(),
                                      room=form.room.data,
                                      date=form.date.data,
                                      period=form.period.data,
                                      purpose=form.purpose.data)
                flash("Booking Created!", 'success')
                return redirect(url_for('index'))
            else:
                flash("Room fully booked!", 'error')
        elif form.room.data == 'f23':
            query = models.Booking.select().where(
                models.Booking.date == form.date.data,
                models.Booking.period == form.period.data,
                models.Booking.room == form.room.data
            )
            for instance in query:
                instances_in_query = instances_in_query + 1
            if instances_in_query < 12:
                models.Booking.create(user=g.user._get_current_object(),
                                      room=form.room.data,
                                      date=form.date.data,
                                      period=form.period.data,
                                      purpose=form.purpose.data)
                flash("Booking Created!", 'success')
                return redirect(url_for('index'))
            else:
                flash("Room fully booked!", 'error')
        elif form.room.data == 'f30':
            query = models.Booking.select().where(
                models.Booking.date == form.date.data,
                models.Booking.period == form.period.data,
                models.Booking.room == form.room.data
            )
            for instance in query:
                instances_in_query = instances_in_query + 1
            if instances_in_query < 8:
                models.Booking.create(user=g.user._get_current_object(),
                                      room=form.room.data,
                                      date=form.date.data,
                                      period=form.period.data,
                                      purpose=form.purpose.data)
                flash("Booking Created!", 'success')
                return redirect(url_for('index'))
            else:
                flash("Room fully booked!", 'error')
        elif form.room.data == 'f59':
            query = models.Booking.select().where(
                models.Booking.date == form.date.data,
                models.Booking.period == form.period.data,
                models.Booking.room == form.room.data
            )
            for instance in query:
                instances_in_query = instances_in_query + 1
            if instances_in_query < 18:
                models.Booking.create(user=g.user._get_current_object(),
                                      room=form.room.data,
                                      date=form.date.data,
                                      period=form.period.data,
                                      purpose=form.purpose.data)
                flash("Booking Created!", 'success')
                return redirect(url_for('index'))
            else:
                flash("Room fully booked!", 'error')
        elif form.room.data == 'f62':
            query = models.Booking.select().where(
                models.Booking.date == form.date.data,
                models.Booking.period == form.period.data,
                models.Booking.room == form.room.data
            )
            for instance in query:
                instances_in_query = instances_in_query + 1
            if instances_in_query < 16:
                models.Booking.create(user=g.user._get_current_object(),
                                      room=form.room.data,
                                      date=form.date.data,
                                      period=form.period.data,
                                      purpose=form.purpose.data)
                flash("Booking Created!", 'success')
                return redirect(url_for('index'))
            else:
                flash("Room fully booked!", 'error')
        elif form.room.data == 'f76':
            query = models.Booking.select().where(
                models.Booking.date == form.date.data,
                models.Booking.period == form.period.data,
                models.Booking.room == form.room.data
            )
            for instance in query:
                instances_in_query = instances_in_query + 1
            if instances_in_query < 4:
                models.Booking.create(user=g.user._get_current_object(),
                                      room=form.room.data,
                                      date=form.date.data,
                                      period=form.period.data,
                                      purpose=form.purpose.data)
                flash("Booking Created!", 'success')
                return redirect(url_for('index'))
            else:
                flash("Room fully booked!", 'error')
    return render_template('booking.html', form=form)


@app.route('/')
@login_required
def index():
    return render_template('home.html')



#__name__ was applied to 'app' therefore it will equal __main__
#and will run with the connections defined at the beginning of the file.
#Initialise the User model and create a user for myself if it doesn't already exist.
#Use a try-except for this as my user will exist after the first launch and I do not wish to
#create multiple instances, therefore pass on the error
if __name__ == '__main__':
    models.initialise()
    try:
        models.User.create_user(
            username="declan.clark",
            email="declan.clark@ridgewoodschool.co.uk",
            password="secret",
            admin=True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, port=PORT, host=HOST)

