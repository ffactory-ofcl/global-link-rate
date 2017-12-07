import urllib.request, urllib.error, sys
from databaseConnection import executeMDb

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

    try:
        fetchedResults = executeMDb('ratings', 'find', {
            'link': link
        })['dbReturn'][0]
        #print('result: ' + str(fetchedResults))
        if not fetchedResults or fetchedResults == None or fetchedResults == '':
            errorCode = 2
        else:
            errorCode = 1
    except IndexError:
        errorCode = 2
    except:
        print("Unexpected error:", str(sys.exc_info()[0]))
        errorCode = 0
    #fetchedResults = executeSql("SELECT * FROM `ratings` WHERE `link`='{}'",
    #                            link)

    return errorCode


def DbIsNotEmpty(table):
    result = executeMDb(table, 'find', {})['dbReturn'][0]
    return result != None and result != ''


#SELECT * from `{}`", table, 5) != ''


def CallerValidity(caller):
    return caller == 'executeApiAction'


def RatingValidity(rating):
    #errorCodes: 1 ok | 2 rating invalid | 3 invalid type
    try:
        rating = int(rating)
    except:
        return 0

    if type(rating) == int:
        if 0 <= rating <= 10:
            return 1
        else:
            return 2
    else:
        return 3
    return 0


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
    #fetchedResults = executeSql("SELECT * FROM `users` WHERE `username`='{}'",
    #                            username)
    fetchedResults = executeMDb('users', 'find', {
        'username': username
    })['dbReturn']
    if fetchedResults == () or fetchedResults == None:
        errorCode = 2
    else:
        for row in fetchedResults:
            if row['password'] == password:
                errorCode = 1
            else:
                errorCode = 3
    return errorCode


def IfUsernameIsInDatabase(username):
    #return executeSql("SELECT * FROM `users` WHERE `username`='{}'",
    #                  username) != (
    return None


#fetchedResults = executeMDb('inputs', 'find', {'link': 'http://youtube.com'},
#                            2)['dbReturn'][5]
#print(IfisInRatingsDb('http://youtube.com'))
