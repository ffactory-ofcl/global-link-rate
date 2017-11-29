#from flask import render_template
#from flask import render_template
from userClass import User
from databaseConnection import executeSql


def showProfile(username):
    return getUserinformation(username)


def getUserinformation(username):
    userinformation = getRawUserdataFromDb(username)
    _userid = userinformation['id']
    _username = userinformation['username']
    _role = userinformation['role']
    _xp = userinformation['xp']
    return User(_userid, _username, _role, _xp)


def getRawUserdataFromDb(username):
    return executeSql("SELECT * FROM `users` WHERE `username`='{}'",
                      username)[0]


def getUsernameFromId(userid):
    return executeSql("SELECT username FROM `users` WHERE `id`='{}'",
                      userid)[0]['username']


def getUseridFromUsername(username):
    return executeSql("SELECT id FROM `users` WHERE `username`='{}'",
                      username)[0]['id']


# class User(UserMixin):
# pass

#user = User()
#user.id2 = 'ud'
#print(user.id2)
#def gainXP(username):
#   pass
