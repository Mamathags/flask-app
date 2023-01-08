import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Registration {self.firstname}>'



@app.route('/')
def index():
    registrations = Registration.query.all()
    return render_template('index.html', registrations=registrations)



@app.route('/<int:register_id>/')
def register(register_id):
    register = Registration.query.get_or_404(register_id)
    return render_template('register.html', register=register)




@app.route('/create/', methods=('GET', 'POST'))
def create():
      if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']
        register = Registration(firstname=firstname,
                          lastname=lastname,
                          email=email,
                          age=age,
                          bio=bio)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for('index'))

      return render_template('create.html')



@app.route('/<int:register_id>/edit/', methods=('GET', 'POST'))
def edit(register_id):
    register = Registration.query.get_or_404(register_id)

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        age = int(request.form['age'])
        bio = request.form['bio']

        register.firstname = firstname
        register.lastname = lastname
        register.email = email
        register.age = age
        register.bio = bio

        db.session.add(register)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('edit.html', register=register)

@app.post('/<int:register_id>/delete/')
def delete(register_id):
    register = Registration.query.get_or_404(register_id)
    db.session.delete(register)
    db.session.commit()
    return redirect(url_for('index'))
