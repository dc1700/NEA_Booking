#Import frameworks
from peewee import *
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash

#Create DB with name booking.db
DATABASE = SqliteDatabase('booking.db')


#Create a class called User that models all user info to be collected and maintained
#Inherits from 'Model' and 'UserMixin'
#Username must be unique
#Email addresses must be unique
#Password has max length of 100, hashing algorithm has length 60 but I have included 'wiggle room'
#Admin field to determine which interface elements to show, false by default

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    is_admin = BooleanField(default=False)

    #Metadata
    #create a database variable and assign it to the DB above
    #set the 'order by' feature to order by username when DB is searched

    class Meta:
        database = DATABASE
        order_by = ('username',)


    def get_booking(self):
        return Booking.select().where(Booking.user == self)

    #This method must be a class method and call upon cls instead of self as the latter would
    #require that when a user is created an instance of the user model is created for the method
    #to act on and that is nto such a great approach. This class method allows the method itself
    #to create the instance to act upon.
    #
    #The method will try to create the user with the given fields and if the required unique fields
    #are in fact unique then the user will be created however if not this will result in an integrity
    #error which should throw a value error that states a user already exists.
    #
    #When storing the password of a new user it will be hashed using the method below so that a plain
    #text password is never stored as that would make for bad security.
    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin = admin)
        except IntegrityError:
            raise ValueError("User with these details already exists.")

#Data model for users' bookings
class Booking(Model):
    room = CharField()
    period = CharField()
    date = DateField()
    purpose = CharField()
    #User is a foreign key to the bookings
    user = ForeignKeyField(
        rel_model=User,
        related_name='bookings'
    )

    class Meta:
        database = DATABASE
        order_by = ('-date',)


#Initialise the connection to the DB and create a table called User, then close the DB
#Set safe to true so that data isn't overwritten with a blank table on each launch
def initialise():
    DATABASE.connect()
    DATABASE.create_tables([User, Booking], safe=True)
    DATABASE.close()