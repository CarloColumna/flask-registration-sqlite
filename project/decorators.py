# project/decorators.py


from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

""" Checks and confirm if a user has confirmed their accounts before 
they are gicen access """
def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.active is False:
            flash('Please confirm your account!', 'warning')
            return redirect(url_for('user.unconfirmed'))
        return func(*args, **kwargs)

    return decorated_function

# Checks if a user has one of the accepted role before given access
def roles_accepted(*accepted_roles):

	def wrapper(fn):
		@wraps(fn)
		def decorated_view(*args, **kwargs):
			for userrole in current_user.roles:
				for acceptedrole in accepted_roles:

					if userrole.name == acceptedrole:
						return fn(*args, **kwargs)

			flash('You don\'t have admin permission')
			return redirect(url_for('user.dashboard'))

		return decorated_view

	return wrapper

# Checks that the user has all the roles required before given access
def roles_required(*required_roles):

	def wrapper(fn):
		@wraps(fn)
		def decorated_view(*args, **kwargs):
			""" Checking if the number of required roles is greater than the roles of the current user
			if so, the current user will not satisfy the requirement """
			if len(required_roles) > len(current_user.roles):	
				flash('You don\'t have admin permission')		
				return redirect(url_for('user.dashboard'))

			"""
			Checking if the number of required roles is less than the roles of the current user
			If so, the outer loop is set to the lesser in number which in this case is the required roles
			"""

			elif len(required_roles) < len(current_user.roles):	
				all_required_roles = True 						
				for requiredrole in required_roles:				

					# Setting the loop counter to False
					role_counter = False						
					for userrole in current_user.roles:			
						# If one of the current user roles equaled that of the required role, 
						# the inner loop counter is set to True
						if userrole.name == requiredrole:		
							role_counter = True

					# For each complete iteration of the inner loop, the outer loop counter 
					# is set based from the inner loop counter
					if not role_counter:							
						all_required_roles = False

				# Checks the outer loop counter to determine if the current user satisfies all the required roles
				if all_required_roles:				
					return fn(*args, **kwargs)
				else:
					flash('You don\'t have admin permission to access the page', 'page')
					return redirect(url_for('user.dashboard'))

			# Runs if the number of required roles is equal to the number of the current user roles
			else:
				all_required_roles = True
				
				for userrole in current_user.roles:
				
					role_counter = False
					for requiredrole in required_roles:

						if userrole.name == requiredrole:
							role_counter = True

					if not role_counter:
						all_required_roles = False

				if all_required_roles:
					return fn(*args, **kwargs)
				else:
					flash('You don\'t have admin permission to access the page', 'page')
					return redirect(url_for('user.dashboard'))

		return decorated_view

	return wrapper