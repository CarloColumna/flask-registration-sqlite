# project/coins/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo

from project.models import Coin, Miningtype



# Form class in creating a new coin record
class CoinRegisterForm(FlaskForm):
    coin_name = StringField('name', validators=[InputRequired(), Length(min=1, max=80)])
    coin_symbol = StringField('symbol', validators=[InputRequired(), Length(min=1, max=6)])
    coin_website = StringField('website', validators=[InputRequired(), Length(min=1)])
    coin_forum = StringField('forum')
    coin_status = BooleanField('status')
    mining_name = SelectField(u'mining type', coerce=int)

    def validate(self):
        initial_validation = super(CoinRegisterForm, self).validate()
        if not initial_validation:
            return False
        coin_name = Coin.query.filter_by(coin_name=self.coin_name.data).first()
        if coin_name:
            self.name.errors.append("Coin already registered")
            return False
        return True