from flask import Flask, request, jsonify
from flask import json
import base64
import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from keras.models import Sequential
from keras.layers import Dense

app = Flask(__name__)
boDebug = True
mongo_client = None
mongo_db = None

def connectMongoDB(addr, usr, psw, dbname):
    global mongo_client, mongo_db
    try:
        if usr != "" and psw != "":
            mongo_client = MongoClient("mongodb://" + usr + ":" + psw + "@" + addr + "/?authSource=admin")
        else:
            mongo_client = MongoClient("mongodb://" + addr + "/")

        if boDebug:
            print "mongoDB client: ", mongo_client

        mongo_db = mongo_client[dbname]
        if boDebug:
            print "mongoDB db: ", mongo_db
    except Exception,e:
        print "connect MongoDB error: %s"%e
        return False
    else:
        return True

def disconnectMongoDB():
    global mongo_client, mongo_db
    if boDebug:
        print "disconnect MongoDB"
    if mongo_client is not None:
        mongo_client.close()
        mongo_db = None
        mongo_client = None

def clickAndTrackerValidate(clicktracker, tracker):
    model = Sequential()
    return True

def fingerprintSuccessCache(fingerprint):
    try:
        coll = mongo_db['fingerprint']
        coll.create_index([('fp', 1)], unique=True)

        coll.insert_one({'fp': fingerprint, 'last_modified': datetime.datetime.utcnow()})

    except DuplicateKeyError:
        print "duplicate document of fingerprint [%s]" % fingerprint

    except Exception, e:
        print 'insert fingerprint [%s] error:[%s]' % (fingerprint, e)


def fingerprintValidate(fingerprint):
    try:
        coll = mongo_db['fingerprint']
        cursor = coll.find({'fp': fingerprint})
        if cursor.count() > 0:
            return True

        return False
    except Exception, e:
        print 'valide fingerprint [%s] error:[%s]' % (fingerprint, e)
        return False

@app.route('/fp', methods=['POST'])
def fp():
    # print request
    # if request.is_json:
    #     print "request is json"
    # else:
    #     print "request is other"
    #
    # json = request.get_json()
    # print json
    obj = json.loads(request.data)
    if boDebug:
        print obj

    for key in obj:
        obj[key] = base64.b64decode(obj[key])
    if boDebug:
        print obj

    res = {u'f_result':u'fail', u't_result':u'fail'}

    #device fingerprint check in MongoDB
    if fingerprintValidate(obj[u'fingerprint']):
        res[u'f_result'] = u'success'

    #clicktracker and tracker check with Deep Learning
    if clickAndTrackerValidate(obj[u'clicktracker'], obj[u'tracker']):
        res[u't_result'] = u'success'

    #store the result to MongoDB
    if res[u'f_result'] == u'fail' and res[u't_result'] == u'success':
        fingerprintSuccessCache(obj[u'fingerprint'])

    return jsonify(res)

if __name__ == '__main__':
    if connectMongoDB('10.88.2.228', '', '', '3DTestDB'):
        app.run(host='0.0.0.0')

