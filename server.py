"""Python Flask WebApp Auth0 integration example
"""
import json
import constants
import manageapi
from functools import wraps
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask import request
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)
if AUTH0_AUDIENCE is '':
    AUTH0_AUDIENCE = AUTH0_BASE_URL + '/userinfo'

app = Flask(__name__, static_url_path='/public', static_folder='./public')
app.secret_key = constants.SECRET_KEY
app.debug = True


@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response


oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated


# Controllers API
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/callback')
def callback_handling():

    error = request.args.get('error')
    error_desc = request.args.get('error_description')
	
    if error == None and error_desc == None: 
        auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        userinfo = resp.json()

        session[constants.JWT_PAYLOAD] = userinfo
        session[constants.PROFILE_KEY] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
			
        return redirect('/dashboard')
    else:
	    # In case of error message, clear auth0 session, display error page
        session[constants.ERR_MESG] = {
		    'err_mesg': error,
			'err_desc': error_desc
        }
		#Redirect to unauthorised page
        params = {'returnTo': url_for('unauthorised', _external=True), 'client_id': AUTH0_CLIENT_ID}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
	
	   


@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)


@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session[constants.PROFILE_KEY],
                           userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD], indent=4))

@app.route('/appruledisplay')
@requires_auth
def appruledisplay():
    client_rule_map = manageapi.get_client_rule_map()
    return render_template('appruledisplay.html',
                           userinfo=session[constants.PROFILE_KEY],
                           client_rule_info=client_rule_map)

@app.route('/unauthorised')
def unauthorised():
    error_mesg = session[constants.ERR_MESG]
    session.clear()
    return render_template('unauthorised.html',
                           error=error_mesg)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=env.get('PORT', 3000))
