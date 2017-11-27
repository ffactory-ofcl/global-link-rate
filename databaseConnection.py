import pymysql.cursors

connectedToDb = False
connection = None


def ConnectionToDb():
    global connectedToDb
    if connectedToDb == False:
        connectToDb()


def connectToDb():
    global connection
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='global link rate',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    global connectedToDb
    connectedToDb = True


def executeSql(sqlStr, _input='', rowCount=5):
    if _input == None:  #or _input == ''
        return ()
    ConnectionToDb()

    if isinstance(_input, tuple):
        _input = ','.join(map(str, _input))
        #print(_input)
    saneInput = sanitizeInput(_input)
    sqlStrSanitized = sqlStr.format(*tuple(saneInput.split(",")))
    #print(sqlStrSanitized)
    with connection.cursor() as cursor:
        cursor.execute(sqlStrSanitized)
    connection.commit()
    cursor.close()
    if rowCount == 'all':
        return cursor.fetchall()
    else:
        return cursor.fetchmany(rowCount)


#


def sanitizeInput(sqlStr):
    global connection
    return connection.escape_string(sqlStr)


# print(
# executeSql(
# "SELECT %s FROM `users` WHERE `username`=%s",
# ['id', 'ffactory'],

#print(executeSql("SELECT `id` FROM `users` WHERE `username`='{}'", 'ffactory'))
#tost = "SELECT {} FROM `users` WHERE `username`='{}'"
#tost.format(*('id'))
