from flask import Flask, render_template, redirect, url_for, Response, request, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_required, current_user, login_user, logout_user
from flask_bcrypt import Bcrypt
from sqlalchemy import and_

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/'
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.sqlite3'
app.secret_key = "WOOoW, it's a super secret key you've ever seen!"

# === database-related ===
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False, unique=True)
    hashed_password = db.Column(db.Text, nullable=False)
    def __init__(self, name: str, username: str, hashed_password: str):
        self.name = name
        self.username = username
        self.hashed_password = hashed_password
    def get_id(self) -> str:
        return str(self.uid)

class Todo(db.Model):
    __tablename__ = 'todos'
    tid = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    def __init__(self, user_id: int, title: str, description: str):
        self.user_id = user_id
        self.title = title
        self.description = description

current_user: User
# === end of database-related ===

# === basic pages-related ===
@app.get('/')
def index() -> str:

    todos: list[Todo] = None
    if current_user.is_authenticated:
        todos = Todo.query.filter(Todo.user_id == current_user.uid).all()

    return render_template(
        'index.html',
        messages=get_flashed_messages(),
        user=current_user,
        todos=todos
    )

@app.get('/about')
def about() -> str:
    return render_template('about.html')
# === end of basic pages-related ===

# === login management-related ===
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

# returns the definition of "load a user"
@login_manager.user_loader
def load_user(uid: int) -> User:
    return db.session.get(User, str(uid))

@login_manager.unauthorized_handler
def unauthorized_callback() -> Response:
    flash("You're unauthorized!", 'warning')
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup() -> str | Response:
    if request.method == 'GET':
        return render_template('signup.html', messages=get_flashed_messages())

    # signup mechanism

    username = request.form.get('username')
    name = request.form.get('name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    # there are some empty inputs
    if not username or not name or not password or not confirm_password:
        flash('Fill all the required inputs!', 'warning')
        return redirect(url_for('signup'))

    # if the password and password confirmation are different
    if password != confirm_password:
        flash('The password and password confirmation have to be the same!', 'warning')
        return redirect(url_for('signup'))

    # if there is a same username in the database
    if User.query.filter(User.username == username).first():
        flash('Username already exists!', 'warning')
        return redirect(url_for('signup'))

    hashed_password = bcrypt.generate_password_hash(password)

    db.session.add(User(
        username=username,
        name=name,
        hashed_password=hashed_password
    ))
    db.session.commit()

    flash('Successfully added an account!', 'message')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login() -> str | Response:

    # the user must be logout first
    if current_user.is_authenticated:
        flash("You're already login!", 'warning')
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('login.html', messages=get_flashed_messages())

    # login mechanism

    username = request.form.get('username')
    password = request.form.get('password')

    targeted_user: User = User.query.filter(User.username == username).first()

    # check the password
    if targeted_user and bcrypt.check_password_hash(targeted_user.hashed_password, password):
        login_user(targeted_user)
        flash('Successfully login!', 'message')
    else:
        flash('Wrong username / password!', 'warning')
        return redirect(url_for('login'))

    return redirect(url_for('index'))

@app.get('/logout')
@login_required
def logout() -> Response:
    logout_user()
    flash('Successfully logout!', 'message')
    return redirect(url_for('index'))
# === end of login management-related ===

# === todos-related ===
@app.post('/add-todo')
@login_required
def add_todo() -> Response:

    title = request.form.get('title')
    description = request.form.get('description')

    db.session.add(Todo(
        user_id=current_user.uid,
        title=title,
        description=description
    ))
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/edit-todo/<string:tid>', methods=['GET', 'POST'])
@login_required
def edit_todo(tid: str) -> str | Response:
    if request.method == 'GET':
        # IMPORTANT !!!
        # make sure the user's id and todo's id match
        targeted_todo: Todo = Todo.query \
            .filter(and_(Todo.tid == tid, Todo.user_id == current_user.uid)) \
            .first()
        
        # todo is not found
        if not targeted_todo:
            flash('The todo is not found!', 'warning')
            return redirect(url_for('index'))

        return render_template(
            'edit-todo.html',
            tid=tid,
            old_title=targeted_todo.title,
            old_description=targeted_todo.description
        )
    
    # IMPORTANT !!!
    # make sure the user's id and todo's id match
    todo: Todo = Todo.query \
        .filter(and_(Todo.tid == tid, Todo.user_id == current_user.uid)) \
        .first()

    if todo:
        todo.title = request.form.get('new-title')
        todo.description = request.form.get('new-description')
        db.session.commit()
        flash('Successfully edited a todo!', 'message')
    else:
        flash('The todo is not found!', 'warning')

    return redirect(url_for('index'))

@app.post('/delete-todo/<string:tid>')
@login_required
def delete_todo(tid: str) -> Response:

    # IMPORTANT !!!
    # make sure the user's id and todo's id match
    todo: Todo = Todo.query \
        .filter(and_(Todo.tid == tid, Todo.user_id == current_user.uid)) \
        .first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash('Successfully deleted a todo!', 'message')
    else:
        flash('Todo was not found!', 'warning')

    return redirect(url_for('index'))
# === end of todos-related ===

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)