# montecryoto/main/views.py

#import
from flask import Flask, render_template, Blueprint



# config
main_blueprint = Blueprint('main', __name__,)


# Route for the homepage
@main_blueprint.route('/')
def home():
	return render_template('main/index.html')
