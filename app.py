from flask import Flask, render_template, request, url_for, redirect
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from main import testing,quantumTime
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "OMGTaohanLin"

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):

    __tablename__ = 'user'

    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    acctype = db.Column(db.Integer, nullable=False)
    admin = db.Column(db.Integer, nullable=False)
    def get_id(self):

        return self.username

class Block(db.Model):
    __tablename__ = 'blocks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student = db.Column(db.String)
    teacher = db.Column(db.String)
    subject = db.Column(db.Integer)
    period = db.Column(db.Integer)
    room = db.Column(db.Integer)

class Choice(db.Model):
    __tablename__ = 'choices'

    username = db.Column(db.String, primary_key=True)
    preferences = db.Column(db.String)

class Created(db.Model):
    __tablename__ = 'schedulecreated'

    username = db.Column(db.String, primary_key=True)
    created = db.Column(db.Boolean, nullable=False)
    
db.init_app(app)
with app.app_context():
    db.create_all()

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)


classes = open("main/classes.txt", "r")
classnames = []
for line in classes:
    classnames.append(line.strip())




@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = User(username=request.form.get("username"),
                     password=request.form.get("password"))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("sign_up.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form.get("username")).first()
        if user.password == request.form.get("password"):
            db.session.add(user)
            db.session.commit()

            login_user(user)
            return redirect(url_for("home"))
    return render_template("login.html")


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    else:
        return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    created = Created.query.first().created
    # created = False
    if current_user.username == "s2":
        created = True
    if not created:
        if current_user.acctype == 0:
            ch = Choice.query.filter_by(username=current_user.username).first().preferences.split(";")
            print(ch)
            if len(ch) > 1:
                first = eval(ch[0])
                second = eval(ch[1])
                return render_template('index.html', c = classnames, f = first, s = second)
            blank = ["" for _ in range(len(classnames))]
            return render_template('index.html', c = classnames, f = blank, s = blank)
        elif current_user.acctype == 1:
            return render_template('teacherpage.html')
        else:
            users = User.query.filter_by(admin=current_user.username).all()
            stds = []
            tchs = []
            for u in users:
                if u.acctype == 0:
                    stds.append(u)
                elif u.acctype == 1:
                    tchs.append(u)

            return render_template('admindashboard.html', s = stds, t = tchs)
    else:
        if current_user.acctype == 0:
            schedule = Block.query.filter_by(student=current_user.username).order_by(Block.period).all()
            return render_template('studentschedule.html', c = classnames, s = schedule)
        elif current_user.acctype == 1:
            schedule = Block.query.filter_by(teacher=current_user.username).order_by(Block.period).all()
            teacherperiods = {1:[],2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
            for item in schedule:
                teacherperiods[item[4]].append((item[1], item[5]))
            return render_template('teacherschedule.html', c = classnames, t =teacherperiods )
        else:
            users = User.query.filter_by(admin=current_user.username).all()
            stds = []
            tchs = []
            for u in users:
                if u.acctype == 0:
                    stds.append(u)
                elif u.acctype == 1:
                    tchs.append(u)

            return render_template('admindashboard.html', s = stds, t = tchs)


@app.route('/logout')
def logout():
    if current_user.is_authenticated:

        """Logout the current user."""
        # db.session.add(current_user)
        # db.session.commit()
        logout_user()
    return redirect(url_for('login'))


@login_required
@app.route('/submit', methods=['POST'])
def submit():
    first_choices = []
    second_choices = []
    for i in range(1, 8):
        first_choices.append(int(request.form[f'class{i}_first_choice']))
        second_choices.append(int(request.form[f'class{i}_second_choice']))
    ch = Choice.query.filter_by(username=current_user.username).first()
    ch.preferences=str(first_choices)+";"+str(second_choices)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/generate', methods=['POST'])
def generate():
    Block.query.delete()
    allchoices = db.session.query(User, Choice).join(User, User.username==Choice.username).filter_by(admin=current_user.username).order_by(User.username).all()
    biglist = []
    for pref in allchoices:
        s = pref[1].preferences
        if not s:
            s = "([],[])"
        else:
            s = "(" + s.replace(";", ",") + ")"
        biglist.append(eval(s))
    entriesfile = open("main/test_student_entries.txt", "w")
    entriesfile.write(str(biglist))
    entriesfile.close()

    quantumTime.main()  
    testing.main()


    anotherbiglist = eval(open("main/schedules.txt").read())
    for choice, si in zip(allchoices, anotherbiglist):
        u = choice[1].username
        print(len(si))
        for item in si:
            db.session.add(Block(student=u, teacher=item[3], subject=item[0], period=item[1], room=item[2]))
    db.session.commit()

    cr = Created.query.first()
    cr.created = True
    db.session.add(cr)
    db.session.commit()

    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)