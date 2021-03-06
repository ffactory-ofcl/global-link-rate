from flask import Flask, render_template, request, redirect, jsonify
import flask_login
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import linkApi, userApi, users, log, parseConfig

glrLinkApiPath = '/api/link/'
glrUserApiPath = '/api/user/<string:username>/'

app = Flask(__name__)
app.secret_key = parseConfig.parse()['flask'][
    'flaskSecretKey']  #secretkey from config  # todo: change for production
login_manager = LoginManager()
login_manager.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)


# start frontend --------------------------------------------------------------
@app.route('/')
def index():
    try:
        username = flask_login.current_user.id
    except:
        username = 'anonymous_user'
    #return 'hello'
    return render_template('indexTemplate.html', username=username)


@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


# end frontend ----------------------------------------------------------------


# start link api --------------------------------------------------------------
@app.route(glrLinkApiPath + 'rate', methods=['POST'])
@login_required
def addRating():
    try:
        username = flask_login.current_user.id
    except:
        username = 'anonymous_user'
    #return request.form['link']
    response = request.json
    link = response['link']
    rating = response['rating']

    apiResponse = linkApi.executeApiAction('addRating',
                                           (username, link, rating))
    errorCode = apiResponse['errorCode']

    log.writeLog(username, 'Add rating for {} ({}/10)'.format(link, rating),
                 errorCode)
    #else:
    #    log.writeLog(username, 'Calculating for {} failed.'.format(link),errorCode)
    return jsonify(apiResponse)  #'ffactory'


@app.route(glrLinkApiPath + 'calculate', methods=['POST'])
@login_required
def calculateLinkRating():
    try:
        username = flask_login.current_user.id
    except:
        username = 'anonymous_user'
    link = request.json['link']

    apiResponse = linkApi.executeApiAction('calculateLinkRating', (link, ''))
    errorCode = apiResponse['errorCode']

    log.writeLog(username, 'Calculate rating for {}'.format(link), errorCode)
    return jsonify(apiResponse)


@app.route(glrLinkApiPath + 'get', methods=['POST'])
@login_required
def getLinkRating():
    try:
        username = flask_login.current_user.id
    except:
        username = 'anonymous_user'
    link = request.json['link']

    apiResponse = linkApi.executeApiAction('getLinkRating', link)
    errorCode = apiResponse['errorCode']

    log.writeLog(username, 'Get rating for {}'.format(link), errorCode)
    return jsonify(apiResponse)


@app.route(glrLinkApiPath + 'toplinks')
def getTopLinkRatings():
    try:
        username = flask_login.current_user.id
    except:
        username = 'anonymous_user'

    apiResponse = linkApi.executeApiAction('getTopLinkRatings')
    errorCode = apiResponse['errorCode']

    log.writeLog(username, 'Get top links', errorCode)
    return jsonify(apiResponse)


# end link api ----------------------------------------------------------------

# start user api --------------------------------------------------------------


@app.route('/user/<string:username>')
def showProfile(username):
    currentUser = users.showProfile(username)
    return render_template('userprofile.html', user=currentUser)


@app.route(glrUserApiPath + 'gainXp/r=<reason>&a=<int:amount>')
@login_required
def gainXp(username, reason, amount):
    return jsonify(
        userApi.executeApiAction('gainXp', (username, reason, amount)))


# end user api ----------------------------------------------------------------

#@app.route(glrUserApiPath + 'gainxp/a=<int:amount>&r=<reason>')
#def idontunderstand(userid1, amount2, reason3):
#    return jsonify(api.executeApiAction('gainXp', (userid, amount, reason)))


# start flask-login -----------------------------------------------------------
class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if users.userExists(username) != 1:
        return
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    user = None
    username = request.form.get('username')
    password = request.form.get('password')

    if users.UsernameAndPasswordValidity(username, password) != 1:
        return

    user = User()
    user.id = username
    return user
    #user.is_authenticated = (usernameValidCode == 1)
    #flask_login.user(user)
    #log.writeLog(username, 'Log in.', 1)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        #return render_template('register.html')
        return render_template(
            'loginRegisterTemplate.html', formAction='register')
    username = request.form['username']
    password = request.form['password']
    errorCode = 0

    errorCode = users.registerUser(username, password)

    if errorCode == 1:
        user = User()
        user.id = username
        login_user(user)
        return render_template(
            'simpleResponseTemplate.html',
            response='Registered ' + flask_login.current_user.id,
            title='Registered'
        )  #'<p>Logged in as ' + flask_login.current_user.id + '</p>'
    elif errorCode == 2:
        return render_template(
            'simpleResponseTemplate.html',
            response=
            'An error occurred while trying to register. The username is already taken',
            title='Error while registering')
    else:
        return render_template(
            'simpleResponseTemplate.html',
            response='An error occurred while trying to register.',
            title='Error while registering')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template(
            'loginRegisterTemplate.html', formAction='login')
    # '''
    # <form action='login' method='POST'>
    # <input type='text' name='username' id='username' placeholder='username'/>
    # <input type='password' name='password' id='password' placeholder='password'/>
    # <input type='submit' name='submit'/>
    # </form>

    username = request.form['username']
    password = request.form['password']
    errorCode = users.UsernameAndPasswordValidity(username, password)
    usernameValidCode = (errorCode == 1)
    if usernameValidCode:
        user = User()
        user.id = username
        login_user(user)
        username = flask_login.current_user.id
        log.writeLog(username, 'Log in.', 1)
        return render_template(
            'simpleResponseTemplate.html',
            response='You were logged in as ' + flask_login.current_user.id,
            title='Logged in.'
        )  #'<p>Logged in as ' + flask_login.current_user.id + '</p>'
    log.writeLog(username, 'Log in.', 0)
    return render_template(
        'simpleResponseTemplate.html',
        response='An error occurred while trying to log in.',
        title='Error while logging in')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template(
        'simpleResponseTemplate.html',
        response='You have been logged out',
        title='Logged out.')  #Response('<p>Logged out</p>')


# end flask-login -------------------------------------------------------------


# start redirects -------------------------------------------------------------
@app.route('/control')
@app.route('/control/')
def redirectToIndex():
    return redirect('/')


#@app.route(glrLinkApiPath + '<path:link>')
def redirectToRate(link):
    return redirect(glrLinkApiPath + link + '/get')


# end redirects ---------------------------------------------------------------

# start contextprocessors -----------------------------------------------------
#@app.app_context_processor
#def returnUser():
#    return dict(user=currentuser)
