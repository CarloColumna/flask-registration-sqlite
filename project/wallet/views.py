# project/wallet/views.py

#import

from flask import render_template, Blueprint, redirect, url_for, flash
from project.decorators import roles_required
from flask_login import login_required, current_user
from .forms import WalletRegisterForm
from project.models import Wallet, Coin
from project import db

# config
wallet_blueprint = Blueprint('wallet', __name__,)


"""
    Creates the form object to receive the entered wallet details and queries
    the db for the coin type to be presented to the user.
    Creates a wallet record for each successful submission.
"""
@wallet_blueprint.route('/registerwallet', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def registerwallet():

    form = WalletRegisterForm()
    form.wallet_coinType.choices = [(row.id, row.coin_name) for row in Coin.query.all()]

    if form.validate_on_submit():
        wallet = Wallet(wallet_address=form.wallet_address.data, wallet_location=form.wallet_location.data, 
        	wallet_status=form.wallet_status.data, coin_id=form.wallet_coinType.data, user_id=current_user.id, pay_id=1)	#payment id not finished
        db.session.add(wallet)
        db.session.commit()

        flash('Wallet successfully registered', 'success')
        return redirect(url_for('wallet.registerwallet'))                           

    return render_template('wallet/registerwallet.html', form=form)