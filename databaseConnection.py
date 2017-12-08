from pymongo import MongoClient
from bson import ObjectId
from parseConfig import parse
import urllib  #, parseConfig
#import pymysql.cursors

connectedToDb = False
client = None
db = None

# db.users.update({
# '_id': ObjectId('5a255d493cfc4a3c6cd6b372')
# }, {
# '$set': {
# 'username': 'tetre'
# }
# })
#for entry in db.users.find({'_id': ObjectId('5a255d493cfc4a3c6cd6b372')}):
#    print(entry)
#print(db.users.find({'_id': {'oid': '5a255d493cfc4a3c6cd6b372'}}))
# client.close()


# hier weiter REEEEE
# https://docs.python.org/3.4/library/configparser.html https://docs.python.org/3.4/library/configparser.html https://docs.python.org/3.4/library/configparser.html
def ConnectionToDb():
    global connectedToDb

    if connectedToDb == False:
        connectToDb()


def connectToDb():
    global client
    global db
    global connectedToDb

    username = str(parse()['mlab']['username'])
    password = urllib.parse.quote_plus(parse()['mlab']['password'])
    client = MongoClient(parse()['mlab']['clientUrl'].format(
        username, password))
    db = client.get_database()

    connectedToDb = True


def executeMDb(database, dbAction, mongoDbInput, rowCount=1, sortStr=None):
    errorCode = 0  #0: undef | 1: success | 2: no valid action | 3: empty input string
    dbReturn = None
    global db
    ConnectionToDb()
    #print(database)
    #print(dbAction)
    #print(str(mongoDbInput))
    if mongoDbInput == None:  #or _input == ''
        errorCode = 3
    else:
        saneStr = mongoDbInput  #sanitizeInput(mongoDbInput)

        if dbAction == 'insert':
            db[database].insert(saneStr)
        elif dbAction == 'update':
            db[database].update(saneStr[0], saneStr[1])
        elif dbAction == 'find':
            if rowCount == 'all':
                if sortStr != None:
                    #print(str(sortStr))
                    dbReturn = db[database].find(saneStr).sort(
                        sortStr[0], sortStr[1])
                else:
                    dbReturn = db[database].find(saneStr)
            else:
                dbReturn = db[database].find(saneStr).limit(rowCount)
        else:
            errorCode = 2

        errorCode = 1
    if dbReturn != None:
        return {'errorCode': errorCode, 'dbReturn': dbReturn}
    else:
        return {'errorCode': errorCode}
    #print(sqlStrSanitized)
    #with connection.cursor() as cursor:
    #    cursor.execute(sqlStrSanitized)
    #connection.commit()
    #cursor.close()
    #    https://stackoverflow.com/questions/30585213/do-i-need-to-sanitize-user-input-before-inserting-in-mongodb-mongodbnode-js-co

    #if rowCount == 'all':
    #    return cursor.fetchall()
    #else:
    #    return cursor.fetchmany(rowCount)


def sanitizeInput(mongoDbStr):
    #global connection
    return mongoDbStr.replace('$', '\\$')


def createDatabase():
    errorCode = None
    try:
        executeSql(
            """CREATE DATABASE IF NOT EXISTS `global link rate` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `global link rate`;

-- Exportiere Struktur von Tabelle global link rate.inputs
CREATE TABLE IF NOT EXISTS `inputs` (
  `index` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL DEFAULT '0',
  `link` varchar(2000) NOT NULL DEFAULT '0',
  `rating` float NOT NULL DEFAULT 0,
  `tags` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=417 DEFAULT CHARSET=latin2;

-- Exportiere Struktur von Tabelle global link rate.ratings
CREATE TABLE IF NOT EXISTS `ratings` (
  `index` int(16) NOT NULL AUTO_INCREMENT,
  `link` varchar(2000) NOT NULL DEFAULT '0',
  `rating` float NOT NULL DEFAULT 0,
  `allLinkRating` int(32) DEFAULT 0,
  `allLinkRatingCount` int(32) DEFAULT 0,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=latin1;

-- Exportiere Struktur von Tabelle global link rate.users
CREATE TABLE IF NOT EXISTS `users` (
  `username` varchar(20) NOT NULL,
  `password` varchar(50) NOT NULL,
  `role` varchar(50) NOT NULL DEFAULT 'user',
  `xp` int(10) unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
""")
    except:
        errorCode = 0
    errorCode = 1
    return errorCode


#createDatabase()

#print(
#    executeMDb('users', 'find', {
#        '_id': ObjectId('5a255d493cfc4a3c6cd6b372')
#    }))

#for entry in executeMDb('users', 'find', {
#        '_id': ObjectId('5a255d493cfc4a3c6cd6b372')
#})['dbReturn']:
#    print(entry['username'])

#print(executeMDb('ratings', 'find', {}, 'all', {'allLinkRating': '-1'}))
# connectToDb()
# print(db['ratings'].find({
# 'link': 'http://youtube.com'
# }).sort('allLinkRating', -1)[0]['allLinkRating'])
