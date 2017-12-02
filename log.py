from datetime import datetime
import os.path


def writeLog(user, message, errorCode=''):
    logPath = os.path.join('logs', 'users', user, user + '.log')
    logPathDir = os.path.dirname(logPath)
    errorCode = str(errorCode)

    if errorCode == '1':
        messageType = 'INF'
    else:
        messageType = 'ERR'
    time = str(datetime.now())[:len(str(datetime.now())) - 4]

    if errorCode == '':
        logMessage = '{} [{}] ({}) {}\n'.format(time, messageType,
                                                'unknown errorCode', message)
    else:
        logMessage = '{} [{}] ({}) {}\n'.format(time, messageType,
                                                'Code: ' + errorCode, message)

    if not (os.path.exists(logPathDir)):  # and os.path.isfile(logPath)
        os.makedirs(logPathDir)

    if os.path.exists(logPath):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'

    fhh = open(logPath, append_write)
    fhh.write(logMessage)
    fhh.close()


#writeLog('ffacto3ry', 'error', 'deee')
