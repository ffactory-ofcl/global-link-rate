import urllib.request, urllib.error, databaseConnection

# def BeforeApi(link):
#errorCode = None
#
# isInDbCode = IfisInRatingsDb(link)
# if (UrlValidity(link) == 1) and (isInDbCode == 1):
# return 1
# else:


def IfisInRatingsDb(link):
    #ConnectionToDb()
    errorCode = None  #0: unknown; 1:is in db; 2: isnt in db
    fetchedResults = databaseConnection.executeSql(
        "SELECT * FROM `ratings` WHERE `link`='{}'", link)
    if not fetchedResults:
        errorCode = 2
    else:
        errorCode = 1
    return errorCode


def CallerValidity(caller):
    return caller == 'executeApiAction'


def RatingValidity(rating):
    if type(rating) == int and (0 <= rating <= 10):
        return True
    else:
        return False


def UrlValidity(link):
    errorCode = None  #1:ok | 2: connection error | 0: unknown
    try:
        urllib.request.urlopen(link)
        #response = urllib.urlopen(request)
        errorCode = 1
    except urllib.error.HTTPError:  # 404, 500,...
        errorCode = 2
    except urllib.error.URLError:
        errorCode = 2
    except:
        errorCode = 0
    return errorCode


def UsernameAndPasswordValidity(username, password):
    #ConnectionToDb()
    errorCode = None  # 0: unknown; 1:username+pw correct; 2: no user with this name; 3: pw wrong
    fetchedResults = databaseConnection.executeSql(
        "SELECT * FROM `users` WHERE `username`='{}'", username)
    if not fetchedResults:
        errorCode = 2
    else:
        for row in fetchedResults:
            if row['password'] == password:
                errorCode = 1
            else:
                errorCode = 3
    return errorCode


def IfUsernameIsInDatabase(username):
    return databaseConnection.executeSql(
        "SELECT * FROM `users` WHERE `username`='{}'", username) != ()


#print(UrlValidity('http://google.com'))
