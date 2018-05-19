import sqlite3
from flask import Flask, render_template, request, session, flash, redirect, url_for, g

#datebase configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'hard_to_guess'


app = Flask(__name__)

##pull in app configuration by looking for UPPERCASE variables
app.config.from_object(__name__)

from functools import wraps

def login_required(test):
  @wraps(test)
  def wrap(*args, **kwargs):
    if "logged_in" in session:
      return test(*args, **kwargs)
    else:
      flash("YOu need to log in first")
      return redirect(url_for('login'))
  return wrap

#create function to connect to db
def connect_db():
  return sqlite3.connect(app.config['DATABASE'])


@app.route("/", methods=['GET', 'POST'])
def login():
  error = None
  status_code = 200
  if request.method == 'POST':
    if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
      error = 'Invalid Credentials, please try again'
      status_code = 401
    else:
      session['logged_in'] = True
      return redirect((url_for("main")))

  return render_template('login.html', error=error), status_code

@app.route("/logout")
def logout():
  session.pop('logged_in', None)
  flash('You were logged out')
  return redirect(url_for("login"))

@app.route("/add", methods=['POST'])
@login_required
def add():
  title = request.form['title']
  post = request.form['post']
  if not title or not post:
    flash("All fields are required. Please try again")
    return redirect(url_for('main'))

  else:
    g.db = connect_db()
    g.db.execute("insert into posts (title, post) values(?, ?)", [request.form['title'], request.form['post']])
    g.db.commit()
    g.db.close()
    flash('New entry was successfully posted')
    return redirect(url_for('main'))



@app.route("/main")
@login_required
def main():
  g.db = connect_db()
  cur = g.db.execute("select * from posts")
  posts = [dict(title=row[0], post=row[1]) for row in cur.fetchall()]
  g.db.close()

  return render_template('main.html', posts=posts)



if __name__=='__main__':
  app.run(debug=True)
