# project/wallet/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo

from project.models import Wallet



""" A form class containing the required form fields in registering a wallet
    It validates the form input and also checks to prevent duplication.
"""
class WalletRegisterForm(FlaskForm):
    wallet_address = StringField('address', validators=[InputRequired(), Length(min=1, max=80)])
    wallet_location = StringField('location', validators=[InputRequired(), Length(min=1, max=100)])
    wallet_status = BooleanField('status')
    wallet_coinType = SelectField(u'coin', coerce=int)

    def validate(self):
        initial_validation = super(WalletRegisterForm, self).validate()
        if not initial_validation:
            return False
        wallet_address = Wallet.query.filter_by(wallet_address=self.wallet_address.data).first()
        if wallet_address:
            self.name.errors.append("Wallet already registered")
            return False
        return True