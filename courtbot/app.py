from email import message
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = '#####'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = '#####'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Reminder(db.Model):
    __tablename__ = 'reminder'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_number = db.Column(db.String(20), unique=True)
    year_filed = db.Column(db.String(4))
    county = db.Column(db.String(10))
    phone_number = db.Column(db.String(20), nullable=False)
    additional_phone_number = db.Column(db.String(20))
    comments = db.Column(db.Text())

    def __init__(self, case_number, year_filed, county, phone_number, additional_phone_number, comments):
        self.case_number = case_number
        self.year_filed = year_filed
        self.county = county
        self.phone_number = phone_number
        self.additional_phone_number = additional_phone_number
        self.comments = comments

    def serialize(self):
        return {
            'case_number': self.case_number,
            'year_filed': self.year_filed,
            'county': self.county,
            'phone_number': self.phone_number,
            'additional_phone_number': self.additional_phone_number,
            'comments': self.comments,
        }


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        case_number = request.form['case_number']
        year_filed = request.form['year_filed']
        county = request.form['county']
        phone_number = request.form['phone_number']
        additional_phone_number = request.form['additional_phone_number']
        comments = request.form['comments']

        if case_number == '' or year_filed == '' or county == '' or phone_number == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Reminder).filter(Reminder.case_number == case_number).count() == 0:
            data = Reminder(case_number, year_filed, county, phone_number,
                            additional_phone_number, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(case_number, year_filed, county, phone_number,
                      additional_phone_number, comments)

            return render_template('success.html')
        return render_template('index.html', message='You have already submitted your case')


if __name__ == '__main__':
    app.run()
