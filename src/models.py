from flask_login import UserMixin

from src import login_manager, db, bcrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    favorites = db.relationship('Item', backref='user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    @property
    def favorite_count(self):
        return len(self.favorites)

    def __repr__(self):
        return f'{self.username}'


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    main_price = db.Column(db.Integer(), nullable=False)
    discount_price = db.Column(db.Integer(), nullable=True)
    description = db.Column(db.String(length=1024), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    image_path = db.Column(db.String(length=255), nullable=False)
    category_id = db.Column(db.Integer(), db.ForeignKey('category.id'), nullable=False)

    def __repr__(self):
        return f'Item: {self.name}'


class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    items = db.relationship('Item', backref='category', lazy=True)

    def __repr__(self):
        return self.name

    @property
    def item_count(self):
        return len(self.items)


class ContactDetails(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    subject = db.Column(db.String(length=50), nullable=False)
    message = db.Column(db.String(length=255), nullable=False)
