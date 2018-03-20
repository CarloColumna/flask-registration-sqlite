# project/coin/views.py

#import

from flask import render_template, Blueprint, redirect, url_for, flash, jsonify, request
from project.decorators import roles_required
from flask_login import login_required
from .forms import CoinRegisterForm
from project.models import Coin, Miningtype
from project import db
import json
from sqlalchemy.ext.declarative import DeclarativeMeta

# config
coin_blueprint = Blueprint('coin', __name__,)


# Route in creating a coin
@coin_blueprint.route('/registercoin', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def registercoin():
	form = CoinRegisterForm()
	form.mining_name.choices = [(row.id, row.mining_name) for row in Miningtype.query.all()]

	if form.validate_on_submit():
		coin = Coin(coin_name=form.coin_name.data, coin_symbol=form.coin_symbol.data, coin_website=form.coin_website.data, 
			coin_forum=form.coin_forum.data, coin_status=form.coin_status.data, miningtype_id=form.mining_name.data)
		db.session.add(coin)
		db.session.commit()

		flash('Coin successfully registered', 'success')
		return redirect(url_for('coin.registercoin'))

	return render_template('coin/registercoin.html', form=form)



# Route that checks the database if the coin already exist.
@coin_blueprint.route('/dbcoincheck', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def dbcoincheck():
	myvar = request.args["term"]
	query = db.session.query(Coin.coin_name).filter(Coin.coin_name.like('%' + str(myvar) + '%'))

	result = [coin[0] for coin in query.all()]
	return jsonify(result)

# Route that checks a web api for the coin's validity and information
@coin_blueprint.route('/webcoincheck', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def webcoincheck():
	coinNameInput = request.args["coin_name"]
	coinJson = request.args.get('https://api.coinmarketcap.com/v1/ticker/' + coinNameInput)
	query = db.session.query(Coin.coin_name).filter(Coin.coin_name.like('%' + str(coinNameInput) + '%'))

	for coin in query.all():
		if coin[0].lower() == coinNameInput.lower():
			return jsonify(" Coin has been registered.")
	return jsonify('')