from flask import Flask, render_template, request, redirect, jsonify
import flask_login
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import api, check, users

glrLinkApiPath = '/api/link/'
app = Flask(__name__)
app.secret_key = 'tis is ma suppa sekkret string that aint tooo short'  # todo: change for production
login_manager = LoginManager()

if __name__ == "__main__":
    app.run(debug=True)

login_manager.init_app(app)


# start frontend --------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<string:username>')
def showProfile(username):
    currentUser = users.showProfile(username)
    return render_template('userprofile.html', user=currentUser)


# @app.route('/?path=<path:link>')
# def indexWithParam(link):
# return render_template('calculated.html', link=link)
@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


# end frontend ----------------------------------------------------------------


# start flask-login -----------------------------------------------------------
class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if api.check.IfUsernameIsInDatabase(username) != 1:
        return
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    user = None
    username = request.form.get('username')
    if not api.check.IfUsernameIsInDatabase(username):
        return

    user = User()
    user.id = username

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    usernameValidCode = check.UsernameAndPasswordValidity(
        username, request.form['password'])
    user.is_authenticated = usernameValidCode
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    # '''
    # <form action='login' method='POST'>
    # <input type='text' name='username' id='username' placeholder='username'/>
    # <input type='password' name='password' id='password' placeholder='password'/>
    # <input type='submit' name='submit'/>
    # </form>

    username = request.form['username']
    password = request.form['password']
    errorCode = check.UsernameAndPasswordValidity(username, password)
    usernameValidCode = (errorCode == 1)
    if usernameValidCode:
        user = User()
        user.id = username
        login_user(user)
        return render_template(
            'simpleResponse.html',
            response='You were logged in as ' + flask_login.current_user.id,
            title='Logged in.'
        )  #'<p>Logged in as ' + flask_login.current_user.id + '</p>'

    return 'Bad login'


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template(
        'simpleResponse.html', response='Logged out',
        title='Logged out.')  #Response('<p>Logged out</p>')


# end flask-login -------------------------------------------------------------


# start api -------------------------------------------------------------------
@app.route(glrLinkApiPath + '<path:link>/rate:<int:rating>', methods=['GET'])
@login_required
def addRating(link, rating):
    return jsonify(
        api.executeApiAction('addRating',
                             [link, flask_login.current_user.id, rating]))


@app.route(glrLinkApiPath + '<path:link>/calculate', methods=['GET'])
@login_required
def calculateLinkRating(link):
    return jsonify(api.executeApiAction('calculateRatings', tuple([link, ''])))


@app.route(glrLinkApiPath + '<path:link>/get', methods=['GET'])
@login_required
def getLinkRating(link):
    return jsonify(api.executeApiAction('getLinkRating', link))


# end api ---------------------------------------------------------------------


# start redirects -------------------------------------------------------------
@app.route('/control')
@app.route('/control/')
def redirectToIndex():
    return redirect('/')


@app.route(glrLinkApiPath + '<path:link>')
def redirectToRate(link):
    return redirect(glrLinkApiPath + link + '/get')


# end redirects ---------------------------------------------------------------

# start contextprocessors -----------------------------------------------------
#@app.app_context_processor
#def returnUser():
#    return dict(user=currentuser)
