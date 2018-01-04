from flask import Flask, request, jsonify
from flask import json
import base64

app = Flask(__name__)

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
    print obj

    for key in obj:
        obj[key] = base64.b64decode(obj[key])

    print obj
    return jsonify(obj)

if __name__ == '__main__':
    app.run()
