from flask import *
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
from flask.helpers import url_for
from flask_bootstrap import Bootstrap
from flask_login.utils import login_required, logout_user
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, current_user
from flask_login.mixins import UserMixin
from wtforms import StringField, PasswordField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import Length, Email
from wtforms.validators import InputRequired, ValidationError
import phonenumbers
from sqlalchemy import select
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.debug = False
app.config.from_pyfile('config.cfg')
app.config["SECRET_KEY"] = "THIS IS A SECRET"
Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager()
login.init_app(app)
login.login_view = 'login'


@login.user_loader
def user_loader(user_id):
    return Users.query.filter_by(id=user_id).first()


class DiseaseType(db.Model):
    __tablename__ = 'diseasetype'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    description = db.Column(db.String(140))


class Country(db.Model):
    __tablename__ = 'country'

    cname = db.Column(db.String(50), primary_key=True)
    population = db.Column(db.BigInteger)


class Disease(db.Model):
    __tablename__ = 'disease'

    dis_id = db.Column(db.Integer, db.Identity(start=1, cycle=True))
    disease_code = db.Column(db.String(50), primary_key=True)
    disease_name = db.Column(db.String(50), unique=True)
    pathogen = db.Column(db.String(20))
    description = db.Column(db.String(140))
    id = db.Column(db.Integer, db.ForeignKey(
        'diseasetype.id', ondelete="CASCADE"), nullable=False)
    creator = db.Column(db.String(60), db.ForeignKey(
        'doctor.email', ondelete="CASCADE"), nullable=False)


class Discover(db.Model):
    __tablename__ = 'discover'

    id = db.Column(db.Integer, db.Identity(start=1, cycle=True))
    cname = db.Column(db.String(50), db.ForeignKey(
        'country.cname', ondelete="CASCADE"), primary_key=True)
    disease_code = db.Column(db.String(50), db.ForeignKey(
        'disease.disease_code', ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    first_enc_date = db.Column(db.Date)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, db.Identity(start=1, cycle=True))
    email = db.Column(db.String(60), primary_key=True)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(30))
    surname = db.Column(db.String(40))
    salary = db.Column(db.Integer)
    phone = db.Column(db.String(20), unique=True)
    cname = db.Column(db.String(50), db.ForeignKey(
        'country.cname', ondelete="CASCADE"))

    @property
    def is_doctor(self):
        dr = Doctor.query.filter_by(email=self.email).first()
        if dr is None:
            return False
        else:
            return True


class PublicServant(db.Model):
    __tablename__ = 'publicservant'

    email = db.Column(db.String(60), db.ForeignKey(
        'users.email', ondelete="CASCADE"), primary_key=True)
    department = db.Column(db.String(50))


class Doctor(db.Model):
    __tablename__ = 'doctor'

    email = db.Column(db.String(60), db.ForeignKey(
        'users.email', ondelete="CASCADE"), primary_key=True)
    degree = db.Column(db.String(20))


class Specialize(db.Model):
    __tablename__ = 'specialize'

    spec_id = db.Column(db.Integer, db.Identity(start=1, cycle=True))
    id = db.Column(db.Integer, db.ForeignKey(
        'diseasetype.id', ondelete="CASCADE"), primary_key=True)
    email = db.Column(db.String(60), db.ForeignKey(
        'doctor.email', ondelete="CASCADE"), primary_key=True)


class Record(db.Model):
    __tablename__ = 'record'

    rec_id = db.Column(db.Integer, db.Identity(start=1, cycle=True))
    email = db.Column(db.String(60), db.ForeignKey(
        'publicservant.email', ondelete="CASCADE"), primary_key=True)
    cname = db.Column(db.String(50), db.ForeignKey(
        'country.cname', ondelete="CASCADE"), primary_key=True)
    disease_code = db.Column(db.String(50), db.ForeignKey(
        'disease.disease_code', ondelete="CASCADE"), primary_key=True)
    total_deaths = db.Column(db.Integer)
    total_patients = db.Column(db.Integer)
    create_date = db.Column(db.DateTime(timezone=True),
                            server_default=func.now())


@app.route('/')
def index():
    return render_template('index.html')


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    surname = StringField("Surname", validators=[InputRequired()])
    phone = StringField('Phone', validators=[InputRequired()])
    salary = IntegerField('Salary', validators=[InputRequired()])
    country = StringField('Country', validators=[InputRequired()])
    degree = StringField('Degree')
    dept = StringField('Department')
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[Length(min=5)])
    repeat_password = PasswordField(
        "Repeat password", validators=[Length(min=5)])


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit() and form.password.data == form.repeat_password.data:
        db.session.execute("insert into users(email,name,surname,salary,phone,cname,password) values ('" + form.email.data + "','" + form.name.data + "','" +
                           form.surname.data + "'," + str(form.salary.data) + ",'" + form.phone.data + "','" + form.country.data + "','" + generate_password_hash(form.password.data)+"');")
        db.session.commit()
        if form.degree.data == None:
            ps = PublicServant(email=form.email.data,
                               department=form.dept.data)
            db.session.add(ps)
        else:
            doctor = Doctor(email=form.email.data, degree=form.degree.data)
            db.session.add(doctor)
        user = Users.query.filter_by(email=form.email.data).first()
        login_user(user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('register.html', form=form)


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[Email()])
    password = PasswordField("Password", validators=[Length(min=5)])


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()

        if check_password_hash(user.password, form.password.data):
            login_user(user)

            return redirect(url_for("index"))

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    response = make_response(redirect(url_for("index")))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache" # HTTP 1.0.
    response.headers["Expires"] = "0"
    return response


@app.route("/mypage", methods=['GET'])
@login_required
def mypage():
    if current_user.is_doctor:
        doctor = Doctor.query.filter_by(email=current_user.email).first()
        return render_template("mypage.html", degree=doctor.degree)
    else:
        ps = PublicServant.query.filter_by(email=current_user.email).first()
        return render_template("mypage.html", department=ps.department)


@app.route("/edit", methods=['POST'])
def edit():
    user = Users.query.filter_by(email=current_user.email).first()
    if request.form['name'] != user.name:
        user.name = request.form['name']
    if request.form['surname'] != user.surname:
        user.surname = request.form['surname']
    if request.form['country'] != user.cname:
        user.cname = request.form['country']
    if request.form['phone'] != user.phone:
        user.phone = request.form['phone']
    if request.form['salary'] != user.salary:
        user.salary = request.form['salary']
    if not current_user.is_doctor:
        ps = PublicServant.query.filter_by(email=current_user.email).first()
        if request.form['department'] != ps.department:
            ps.department = request.form['department']
    else:
        doctor = Doctor.query.filter_by(email=current_user.email).first()
        if doctor.degree != request.form['degree']:
            doctor.degree = request.form['degree']
    db.session.commit()
    return redirect(url_for('mypage'))


class mycontr_res():
    def __init__(self, dt, dis):
        self.dtype = dt
        self.diseases = dis


def mycontr_response():
    res = []
    for dis in db.session.query(Disease.id).filter_by(creator=current_user.email).distinct():
        dt = DiseaseType.query.filter_by(id=dis[0]).first()
        dlist = []
        for dises in Disease.query.filter_by(creator=current_user.email, id=dis[0]):
            dlist.append((dises, Discover.query.filter_by(
                disease_code=dises.disease_code).first()))
        res.append(mycontr_res(dt, dlist))
    return res


@app.route("/mycontributions", methods=['GET'])
def mycontrs():
    disease_types = DiseaseType.query.all()
    return render_template('mycontrs.html', dtypes=disease_types, res=mycontr_response())


@app.route("/dtype", methods=['POST'])
def dtype():
    dis_type = DiseaseType(
        name=request.form['name'], description=request.form['description'])
    db.session.add(dis_type)
    db.session.commit()
    disease_types = DiseaseType.query.all()
    return redirect(url_for('mycontrs'))


@app.route("/disease", methods=['POST'])
def disease():
    disease = Disease(disease_code=request.form['dis_code'], disease_name=request.form['dis_name'],
                      pathogen=request.form['dis_path'], description=request.form['description'], id=DiseaseType.query.filter_by(name=request.form['dtype']).first().id, creator=current_user.email)
    db.session.add(disease)
    db.session.commit()
    discover = Discover(cname=request.form['dis_country'],
                        disease_code=request.form['dis_code'], first_enc_date=request.form['dis_year'])
    db.session.add(discover)
    db.session.commit()
    return redirect(url_for('mycontrs'))


@app.route("/diseaseedit", methods=['POST'])
def diseaseedit():
    if request.method == 'POST':
        disease = Disease.query.filter_by(dis_id=request.form['id']).first()
        if request.form['name'] != disease.disease_name:
            disease.disease_name = request.form['name']
        if request.form['code'] != disease.disease_code:
            disease.disease_code = request.form['code']
        if request.form['pathogen'] != disease.pathogen:
            disease.pathogen = request.form['pathogen']
        if request.form['description'] != disease.description:
            disease.description = request.form['description']
        db.session.commit()
        discover = Discover.query.filter_by(
            disease_code=disease.disease_code).first()
        if request.form['date'] != discover.first_enc_date:
            discover.first_enc_date = request.form['date']
        db.session.commit()
    return redirect(url_for('mycontrs'))


@app.route("/diseasedelete/<int:id>", methods=['post'])
def diseasedelete(id):
    disease = Disease.query.filter_by(dis_id=id).first()
    db.session.delete(disease)
    db.session.commit()
    return redirect(url_for('mycontrs'))


@app.route("/myrecords", methods=['get'])
def myrecords():
    records = Record.query.filter_by(email=current_user.email).all()
    disease_codes = db.session.query(Disease.disease_code).all()
    countries = db.session.query(Country.cname).all()
    return render_template('myrecords.html', records=records, disease_codes=disease_codes, countries=countries)


@app.route("/recordadd", methods=['post'])
def recordadd():
    record = Record(email=current_user.email, cname=request.form['cname'], disease_code=request.form[
                    'dcode'], total_deaths=request.form['deaths'], total_patients=request.form['patients'])
    db.session.add(record)
    db.session.commit()
    return redirect(url_for('myrecords'))


@app.route("/recordedit", methods=['POST'])
def recordedit():
    record = Record.query.filter_by(rec_id=request.form['id']).first()
    if request.form['cname'] == '':
        print()
    elif request.form['cname'] != record.cname:
        record.cname = request.form['cname']
    if request.form['dcode'] == '':
        print()
    elif request.form['dcode'] != record.disease_code:
        record.disease_code = request.form['dcode']
    if request.form['deaths'] != record.total_deaths:
        record.total_deaths = request.form['deaths']
    if request.form['patients'] != record.total_patients:
        record.total_patients = request.form['patients']
    db.session.commit()
    return redirect(url_for('myrecords'))


@app.route("/recorddelete/<int:id>", methods=['post'])
def recorddelete(id):
    record = Record.query.filter_by(rec_id=id).first()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('myrecords'))


@app.route("/records", methods=['get'])
def records():
    sort = request.args.get('sort')
    res = []
    if  sort == None or sort == '0':
        for record in Record.query.order_by(desc(Record.create_date)).all():
            res.append((record, Users.query.filter_by(
                email=record.email).first()))
    if sort == '1':
        for record in Record.query.order_by(desc(Record.disease_code)).all():
            res.append((record, Users.query.filter_by(
                email=record.email).first()))
    if sort == '2':
        for record in Record.query.order_by(desc(Record.total_deaths)).all():
            res.append((record, Users.query.filter_by(
                email=record.email).first()))
    if sort == '3':
        for record in Record.query.order_by(desc(Record.total_patients)).all():
            res.append((record, Users.query.filter_by(
                email=record.email).first()))
    return render_template('records.html', res=res, sort=sort)

@app.route("/doctors", methods=['get'])
def doctors():
    doctors = []
    for doctor in Doctor.query.all():
        doctors.append((doctor, Users.query.filter_by(email=doctor.email).first()))
    return render_template('doctors.html', doctors=doctors)

@app.route("/publicservants", methods=['get'])
def publicservants():
    doctors = []
    for doctor in PublicServant.query.all():
        doctors.append((doctor, Users.query.filter_by(email=doctor.email).first()))
    return render_template('publicservants.html', doctors=doctors)

if __name__ == '__main__':
    countries= ['Kazakhstan', 'USA', 'UK', 'Russia', 'China', 'France', 'Australia', 'Morocco', 'Bolivia']
    for country in countries:
        db.session(Country(country, 0))
        db.session.commit()
    app.run(debug=True)
