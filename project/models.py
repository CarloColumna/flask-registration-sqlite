# project/models.py


from datetime import datetime
from project import db, bcrypt
from flask_login import UserMixin


# Define the data model

class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(255), nullable=True)
    active = db.Column(db.Boolean(), nullable=False)
    confirmed_at = db.Column(db.DateTime(), nullable=True)
    user_wallet = db.relationship('Wallet', backref='user', lazy= 'dynamic')
    user_referral = db.relationship('Referral', backref='user', lazy= 'dynamic')
    roles = db.relationship('Role', secondary='user_roles', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, password, username, active, confirmed_at=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.username = username
        self.active = active
        self.confirmed_at = confirmed_at

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<email {}'.format(self.email)

class Miningtype(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    mining_name = db.Column(db.String(10), nullable=False, unique=True)

class Coin(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    coin_name = db.Column(db.String(), nullable=False, unique=True)
    coin_symbol = db.Column(db.String(), nullable=True, unique=True)
    coin_status = db.Column(db.Boolean(), nullable=True)
    coin_website = db.Column(db.String(), nullable=True)
    coin_rank = db.Column(db.Integer(), nullable=True)
    coin_max_supply = db.Column(db.Integer(), nullable=True)
    coin_stake = db.Column(db.Integer(), nullable=True)
    coin_age = db.Column(db.Integer(), nullable=True)
    coin_price = db.Column(db.Integer(), nullable=True)
    #coin_block_explorer = db.Column(db.String(), nullable=True)
    coin_forum = db.Column(db.String(), nullable=True)
    soft_delete = db.Column(db.Boolean(), nullable=True)
    #mining_types = db.relationship('Miningtype', secondary=coin_miningtype, backref=db.backref('coins', lazy='dynamic'))
    miningtype_id = db.Column(db.Integer(), db.ForeignKey('miningtype.id'))
    coin_wallet = db.relationship('Wallet', backref = 'coin', lazy= 'dynamic')
    coin_faucet = db.relationship('Faucet', backref = 'coin', lazy= 'dynamic')
    coin_captcha = db.relationship('Captcha', backref = 'coin', lazy= 'dynamic')
    coin_game = db.relationship('Game', backref = 'coin', lazy= 'dynamic')

class Wallet(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    wallet_address = db.Column(db.String(), unique=True)
    wallet_location = db.Column(db.String(), nullable=False)
    wallet_status = db.Column(db.Boolean(), nullable=False)
    coin_id = db.Column(db.Integer(), db.ForeignKey('coin.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    pay_id = db.Column(db.Integer(), db.ForeignKey('payment.id'))

class Exchange(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    exchange_name = db.Column(db.String(100), unique=True)
    exchange_url = db.Column(db.String(), nullable=False, unique=True)

coin_exchange = db.Table('Coin_Exchange',
        db.Column('coin_id', db.Integer(), db.ForeignKey('coin.id')),
        db.Column('exchange_id', db.Integer(), db.ForeignKey('exchange.id')))

class Faucet(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    faucet_link = db.Column(db.String(), unique=True)
    faucet_status = db.Column(db.Boolean(), nullable=False)
    coin_id = db.Column(db.Integer(), db.ForeignKey('coin.id'))

class Captcha(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    captcha_name = db.Column(db.String(100), unique=True)
    captcha_link = db.Column(db.String(), nullable=False, unique=True)
    captcha_status = db.Column(db.Boolean(), nullable=False)
    coin_id = db.Column(db.Integer(), db.ForeignKey('coin.id'))

class Game(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    game_url = db.Column(db.String(), unique=True)
    game_status = db.Column(db.Boolean(), nullable=False)
    coin_id = db.Column(db.Integer(), db.ForeignKey('coin.id'))

class Payment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    pay_time = db.Column(db.DateTime(), nullable=True)
    payment_url = db.Column(db.String(), nullable=False)

class Referral(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    referral = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))




