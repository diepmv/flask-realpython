import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
#USERNAME = 'admin'
#PASSWORD = 'admin'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'myprecious'

#define full path for database
DATABASE_PATH = os.path.join(basedir, DATABASE)

#the database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ DATABASE_PATH
