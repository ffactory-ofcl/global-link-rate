#from flask import render_template
#from flask import render_template
#from userClass import User
from databaseConnection import executeMDb


def showProfile(username):
    return getUserinformation(username)


def getUserinformation(username):
    userinformation = getRawUserdataFromDb(username)
    #_userid = userinformation['id']
    _username = userinformation['username']
    _role = userinformation['role']
    _xp = userinformation['xp']
    return {'username': _username, 'role': _role, 'xp': _xp}  #_userid,


def userExists(username):
    errorCode = None  #0: unknown; 1:is in db; 2: isnt in db

    try:
        fetchedResults = executeMDb('users', 'find', {
            'username': username
        })['dbReturn'][0]
        #print('result: ' + str(fetchedResults))
        if not fetchedResults or fetchedResults == None or fetchedResults == '':
            errorCode = 2
        else:
            errorCode = 1
    except IndexError:
        errorCode = 2
    except:
        #print("Unexpected error:", str(sys.exc_info()[0]))
        errorCode = 0
    return errorCode
    #return executeSql("SELECT * FROM `users` WHERE `username`='{}'",
    #                  username) != ()


def getRawUserdataFromDb(username):
    return executeMDb('users', 'find', {'username': username})['dbReturn'][0]
    #return executeSql("SELECT * FROM `users` WHERE `username`='{}'",
    #                  username)[0]


def getUsernameFromId(userid):
    return executeMDb('users', 'find', {
        'id': userid
    })['dbReturn'][0]['username']
    #return executeSql("SELECT username FROM `users` WHERE `id`='{}'",
    #                  userid)[0]['username']


def getUseridFromUsername(username):
    return executeMDb('users', 'find', {
        'username': username
    })['dbReturn'][0]['userid']
    #return executeSql("SELECT id FROM `users` WHERE `username`='{}'",
    #                  username)[0]['id']


def registerUser(username, password):
    errorCode = 0
    if userExists(username) != 1:
        executeMDb('users', 'insert', {
            'username': username,
            'password': password,
            'role': 'user',
            'xp': 0
        })
        errorCode = 1
    else:
        errorCode = 2
    #executeSql("INSERT INTO `users` (`username`,`password`, `role`, `xp`) VALUES ('{}','{}','{}','{}')",(username, password, 'user', '0'))
    return errorCode


def UsernameAndPasswordValidity(username, password):
    #ConnectionToDb()
    errorCode = None  # 0: unknown; 1:username+pw correct; 2: no user with this name; 3: pw wrong
    fetchedResult = None
    #fetchedResults = executeSql("SELECT * FROM `users` WHERE `username`='{}'",username)
    try:
        fetchedResult = executeMDb('users', 'find', {
            'username': username
        })['dbReturn'][0]
    except IndexError:
        errorCode = 2
        return errorCode
    except:
        errorCode = 0
        return errorCode

    if fetchedResult['password'] == password:
        errorCode = 1
    else:
        errorCode = 3
    return errorCode


# class User(UserMixin):
# pass

#user = User()
#user.id2 = 'ud'
#print(userExists('ffactory2'))
#def gainXP(username):
#   pass
#print(UsernameAndPasswordValidity('ffactory', 'wiu3on'))
#print(registerUser('reee', 'peet'))
