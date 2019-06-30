from werkzeug.security import safe_str_cmp # Just compare the String
from user import User

users = [
		# 'id': 1,
		# 'username': 'rex',
		# 'password': '1234'
		User(1, 'rex', '1234')
]

username_mapping = {
	# 'rex': {
	# 	'id': 1,
	# 	'username': 'rex',
	# 	'password': "1234"
	# }
	u.username: u for u in users
}

userid_mapping = {
	u.id: u for u in users
}

def authenticate(username, password):
	user = username_mapping.get(username, None)
	if user and safe_str_cmp(user.password, password):
		return user

def identity(payload):
	"""
	Function in JWT
	payload['identity'] will extract the id from the user
	"""
	user_id = payload['identity']
	return userid_mapping.get(user_id, None)