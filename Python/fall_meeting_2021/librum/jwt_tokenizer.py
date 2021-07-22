#this script generates a JSON Web Token (JWT) that is then packaged with our API calls to the Zoom API
#further information on what a JWT is can be found at the link in the README

#this function returns a complete header to be included in a standard API call made with the requests package

import time
from authlib.jose import jwt

#Generate JWT
def generate_token(api_key, api_secret):

	header = {"alg": "HS256", "typ": "JWT"}
	payload = {"iss": api_key, "exp": int(time.time() + 86400)}
	encoded_jwt = str(jwt.encode(header,payload, api_secret), 'utf-8')
	#Insert JWT into https request
	headers = {
	    'authorization': "Bearer %s" % encoded_jwt,
	    'content-type': "application/json"
	    }

	return headers