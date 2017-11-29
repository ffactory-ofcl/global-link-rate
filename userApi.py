from databaseConnection import executeSql


def executeApiAction(functionName, arguments):
    # TODO rate limiting and user profiles
    return (globals()[functionName](arguments))


def gainXp(arguments):
    username = arguments[0]
    reason = arguments[1]
    amont = arguments[2]
    currentXP = executeSql("SELECT xp FROM `users` WHERE username = '{}'",
                           username)[0]['xp']
    newXP = currentXP + amont
    #print(currentXP[0]['xp'])
    if executeSql("UPDATE users SET xp='{}' WHERE username='{}'",
                  (newXP, username)) == ():
        return True
    else:
        return False
