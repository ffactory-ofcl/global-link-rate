import api

# start flask-login -----------------------------------------------------------


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
    usernameValidCode = api.check.UsernameAndPasswordValidity(
        username, request.form['password'])
    user.is_authenticated = usernameValidCode
    return user


def login():
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
